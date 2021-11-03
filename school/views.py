from django.contrib.auth import authenticate, login, logout
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT
from django.db.models.query import InstanceCheckMeta
from django.db.models.query_utils import PathInfo
from django.shortcuts import render,redirect,get_object_or_404
from. forms import *
from .models import *
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from.decorators import *

# Create your views here.
def home(request):
    return render(request,'../templates/home.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def hodhome(request):
    total_students = Student.objects.all().count()
    total_teachers = Teacher.objects.all().count()
    all_subjects = Subjects.objects.all()
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'all_subjects': all_subjects
        
    }
    return render(request,'../templates/hod/hod.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def teachhome(request):
    return render(request,'../templates/teacher/teacher.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def studhome(request):
    return render(request,'../templates/student/student.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def principal_registration(request):
    if request.method == 'POST':
        form = PrincipalSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(
                request, first_name + ' ' + 'your account was created successfully!')
            authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            return redirect('profile')
    else:
        form = PrincipalSignUpForm(request.POST)

    context = {
        'form': form
        
    }
    return render(request, 'auth/principalregistration.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def teacher_registration(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(
                request, first_name + ' ' + 'your account was created successfully!')
            new_teacher = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            return redirect('profile')
            
    else:
        form = TeacherSignUpForm(request.POST)

    context = {
        'form': form
    }
    return render(request, 'auth/teacherregistration.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def student_registration(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(
                request, first_name + ' ' + 'your account was created successfully!')
            
            login(request, user)
            return redirect('profile')
    else:
        form = StudentSignUpForm(request.POST)

    context = {
        'form': form
    }
    return render(request, 'auth/studentregistration.html', context)



# @unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in as' + ' ' + username)
            if user.is_principal:
                return redirect('hodhome')
            if user.is_teacher:
                return redirect('teachhome')
            if user.is_student:
                return redirect('studhome')
        else:
            messages.error(request, 'Invalid Username and/or Password')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    current_user = request.user
    logout(request)
    messages.info(
        request, 'You have logged out. Log back in to book our services.')
    # if current_user.is_admin:
    #     return redirect('home')
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    current_user = request.user
    if current_user.is_principal:
        if request.method == 'POST':
            u_form = PrincipalUpdateForm(
                request.POST, instance=request.user)
            p_form = PrincipalProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.principal)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
            return redirect('hodhome')
        else:
            u_form = PrincipalUpdateForm(instance=request.user)
            p_form = PrincipalProfileUpdateForm(instance=request.user.principal)
            
            context = {'u_form': u_form,
                    'p_form': p_form,
                    'current_user': current_user,
                    }
            return render(request, 'auth/principalprofile.html', context)

    if current_user.is_teacher:
        try:
            teacher = request.user.teacher
        except Teacher.DoesNotExist:
            teacher = Teacher(user=request.user)
        if request.method == 'POST':
            u_form = TeacherUpdateForm(request.POST )
            p_form = TeacherProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.teacher)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
            
            return redirect('teachhome')
        else:
            u_form = TeacherUpdateForm(instance=request.user)
            p_form = TeacherProfileUpdateForm(
                instance=request.user.teacher)

            context = {'u_form': u_form,
                    'p_form': p_form,
                    'current_user': current_user,
                    }
            return render(request, 'auth/teacherprofile.html', context)


    if current_user.is_student:
        if request.method == 'POST':
            u_form = StudentUpdateForm(
                request.POST, instance=request.user)
            p_form = StudentProfileUpdateForm(
                request.POST, request.FILES, instance=request.user.student)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
            
            return redirect('studhome')
        else:
            u_form = StudentUpdateForm(instance=request.user)
            p_form = StudentProfileUpdateForm(
                instance=request.user.student)

            context = {'u_form': u_form,
                    'p_form': p_form,
                    'current_user': current_user,
                    }
            return render(request, 'student/studentprofile.html', context)
  
            
@login_required(login_url='login')

def load_subjects(request):
    class_id = request.GET.get('classes_id')
    print(class_id)
    subjects = Subjects.objects.filter(classes_id=class_id)
    print(subjects)
    return render(request,'../templates/loadsubjects.html',{"subjects":subjects})



@login_required(login_url='login')
def allstudents(request):
    all_classes = Classes.objects.all()
    all_students = Student.objects.filter(classes__name="Form One").all()
    
    return render(request,"students.html",{"all_classes":all_classes,"all_students":all_students})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addSubject(request):
    all_subjects = Subjects.objects.all()
    form = addSubjectForm()
    if request.method == 'POST':
        form = addSubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.save()
        return HttpResponseRedirect(request.path_info) 
    else:
        form = addSubjectForm()

    return render(request,"hod/addsubject.html",{"form":form,"all_subjects":all_subjects})

@login_required(login_url='login')
def classes(request):
    all_classes = Classes.objects.all()
    context = {"all_classes":all_classes}    
    return render(request,"hod/allclasses.html",context)

@login_required(login_url='login')
def subject(request,id):
    subject = get_object_or_404(Subjects, pk=id)
    return render(request,"subject.html",{"subject":subject})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','teacher'])
def addresults(request):
    # subjects = Subjects.objects.filter(teacher.id=request.id)
    teacher = Teacher.objects.get(user_id=request.user)
    subjects = Subjects.objects.filter(teacher=request.user.id)
    form = addResultsForm()
    return render(request,"teacher/results.html",{"teacher":teacher,"subjects":subjects,"form":form})

@login_required(login_url='login')
def teacher(request):
    teacher = Teacher.objects.get(user_id=request.user)
    subjects = Subjects.objects.filter(teacher=request.user.id)
    return render(request,"teacher/teacher.html",)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def Students(request,id):
    subject = get_object_or_404(Subjects,pk=id)


    all_students = subject.students.all()
   
    request.session['current_class_id'] = id
    exam1 = Results.get_results(id)
    # students = Student.objects.filter(subjects_id=subject)
    context = {"subject":subject,
                "all_students":all_students,
                "exam1": exam1,
                }
    
    
    return render(request,"teacher/studentlist.html",context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def addmarks(request,id):
    student = get_object_or_404(Student,pk=id)
    subjectid = request.session.get('current_class_id')
    subject = get_object_or_404(Subjects,pk=subjectid)
    current_class = subject.classes
    marks = addResultsForm()

    if request.method == 'POST':
        form = addResultsForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.subjects = subject
            marks.classes = current_class
            marks.teacher = request.user.username
            marks.save()

            marks = Results.objects.filter(student_id=id,classes=current_class)
            my_marks = []
            for mark in marks:
                my_marks.append(mark.mean_marks)
            all_marks = sum(my_marks)

            student.total_marks = all_marks
            student.save()

        return HttpResponseRedirect(request.path_info) 
    else:
        form = addResultsForm()  
    return render(request,"teacher/marks.html",{"form":form,"subject":subject})

def student_positions(request,id):
    all_students = Student.objects.filter(classes=id).order_by("-total_marks")
    
    for i,student in enumerate(all_students):
        student.position = i+1 
        student.save()
        
    return redirect("allclasses") 



@login_required(login_url='login')
@allowed_users(allowed_roles=['teacher'])
def editmarks(request,id):
    student = get_object_or_404(Student,pk=id)
    subjectid = request.session.get('current_class_id')
    subject = get_object_or_404(Subjects,pk=subjectid)
    result = Results.objects.get(student=student,subjects__id=subjectid)
    
    current_class = subject.classes
    marks = addResultsForm()
    if request.method == 'POST':
        form = addResultsForm(request.POST, request.FILES, instance=result)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.subjects = subject
            marks.classes = current_class
            marks.save()


            marks = Results.objects.filter(student_id=id,classes=current_class)
            my_marks = []
            for mark in marks:
                my_marks.append(mark.mean_marks)
            all_marks = sum(my_marks)

            student.total_marks = all_marks
            student.save()
        return HttpResponseRedirect(request.path_info) 
    else:
        form = addResultsForm(instance=result)  
    
    return render(request,"teacher/marks.html",{"form":form,"subject":subject})


#students views
@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def studentInfo(request):
    current_student = Student.objects.get(user=request.user)
    if "selclasses" in request.GET and request.GET['selclasses']:
        classes = request.GET.get("selclasses")
    else:
        classes = current_student.classes
    subjects = current_student.subjects.all
    marks = Results.objects.filter(student_id=current_student,classes=classes)


    #Get previous classes add them into a list then push them to the frontend
    previous_results = Results.objects.filter(student_id = current_student)
    p_classes = []
    for pc in previous_results:
        if pc.classes not in p_classes:
            p_classes.append(pc.classes)
        
    #get total marks
 
    my_marks = []
    for mark in marks:
        my_marks.append(mark.mean_marks)
    all_marks = sum(my_marks)

    
    all_students = Student.objects.filter(classes=classes)
    studentNum = all_students.count()
    

    # #mean_marks 
    # mean = all_marks/(len(my_marks)*100) * 100
    #get total points

    my_points = []
    for mark in marks:
        my_points.append(mark.points)
    all_points = sum(my_points) / len(my_points)
  
    # all_student_marks = []
    # all_results = Results.objects.filter(classes=classes)
    # for results in all_results:
    #     all_student_marks.append(results.mean_marks)
    # print(len(all_student_marks))
    # print(all_student_marks)

    try:
        selectedClass = get_object_or_404(Classes,pk=classes)
    except:
        selectedClass = get_object_or_404(Classes,pk=classes.id)
    
    context = {
        "current_student":current_student,
        "classes":classes,
        "subjects":subjects,
        "marks": marks,
        "p_classes":p_classes,
        "all_marks":all_marks,
        "all_points":all_points,
        "selectedClass":selectedClass,
        "studentNum":studentNum
        
        }

    

    return render(request,"student/info.html",context)
        

@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def reportform(request):
    current_student = Student.objects.get(user=request.user)
    if "selclasses" in request.GET and request.GET['selclasses']:
        classes = request.GET.get("selclasses")
    else:
        classes = current_student.classes
    subjects = current_student.subjects.all
    marks = Results.objects.filter(student_id=current_student,classes=classes)


    #Get previous classes add them into a list then push them to the frontend
    previous_results = Results.objects.filter(student_id = current_student)
    p_classes = []
    for pc in previous_results:
        if pc.classes not in p_classes:
            p_classes.append(pc.classes)
        
    #get total marks
 
    my_marks = []
    for mark in marks:
        my_marks.append(mark.mean_marks)
    all_marks = sum(my_marks)

    
    all_students = Student.objects.filter(classes=classes)
    studentNum = all_students.count()
    

    # #mean_marks 
    # mean = all_marks/(len(my_marks)*100) * 100
    #get total points

    my_points = []
    for mark in marks:
        my_points.append(mark.points)
    all_points = sum(my_points) / len(my_points)
  
    # all_student_marks = []
    # all_results = Results.objects.filter(classes=classes)
    # for results in all_results:
    #     all_student_marks.append(results.mean_marks)
    # print(len(all_student_marks))
    # print(all_student_marks)

    try:
        selectedClass = get_object_or_404(Classes,pk=classes)
    except:
        selectedClass = get_object_or_404(Classes,pk=classes.id)
    
    context = {
        "current_student":current_student,
        "classes":classes,
        "subjects":subjects,
        "marks": marks,
        "p_classes":p_classes,
        "all_marks":all_marks,
        "all_points":all_points,
        "selectedClass":selectedClass,
        "studentNum":studentNum
        
        }

    

    return render(request,"student/report.html",context)
