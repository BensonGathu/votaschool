from re import S
from django import conf
from django.contrib.auth import authenticate, login, logout
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT
from django.db.models.query import InstanceCheckMeta
from django.db.models.query_utils import PathInfo
from django.shortcuts import render,redirect,get_object_or_404

# from school.templatetags.mymarks import all_students
#######
# from school.templatetags.mymarks import comments
from. forms import *
from .models import *
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from.decorators import *
from django.contrib.auth.models import Group

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
    try:
        classteacherof = Classes.objects.get(class_teacher = request.user.id)
    except:
        classteacherof = 0
    print(classteacherof)
    allstudents = Student.objects.filter(classes=classteacherof)
    # currentclass = get_object_or_404(Classes,pk=classteacherof)
    
    context = {
        "classteacherof":classteacherof,
        "allstudents": allstudents,
        # "currentclass":currentclass,
    }
    return render(request,'../templates/teacher/teacher.html',context)

def teacherComment(request,id):
    classes = Classes.objects.get(class_teacher = request.user.id)
    student = get_object_or_404(Student,pk=id)
    subjects = student.subjects.all
    marks = Results.objects.filter(student_id=student,classes=classes)

    my_marks = []
    for mark in marks:
        my_marks.append(mark.mean_marks)
    all_marks = sum(my_marks)
    
    my_points = []
    for mark in marks:
        my_points.append(mark.points)
    if len(my_points) != 0:
        all_points = sum(my_points) / len(my_points)
    else:
        all_points =1

    all_students = Student.objects.filter(classes=classes)
    studentNum = all_students.count()
   

    try:
        studentreport = report.objects.get(classes_id = classes ,student=student)
        
    except:
        studentreport = report.objects.create(classes_id = classes ,student=student)
    comm = request.GET.get("tcomments")

    studentreport.t_comments = comm
    studentreport.save()    
    context = {
        "marks":marks,
        "current_student":student,
        "classes":classes,
        "subjects":subjects,
        "marks": marks,
        "all_marks":all_marks,
        "all_points":all_points,
        "studentNum":studentNum
        
    }
   
    return render(request,"teacher/studentreport.html",context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['student'])
def studhome(request):
    currentstudent = request.user.id
    fee_info = Fees.objects.filter(student=currentstudent)
    context = {
        "fee_info":fee_info,
    }
    return render(request,'../templates/student/student.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def principal_registration(request):
    if request.method == 'POST':
        form = PrincipalSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="admin")
            group.user_set.add(user)
            first_name = form.cleaned_data.get('first_name')
            messages.success(
                request, first_name + ' ' + 'your account was created successfully!')
            # authenticate(username=form.cleaned_data['username'],
            #                         password=form.cleaned_data['password1'],
            #                         )
            # return redirect('profile')
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
            group = Group.objects.get(name="teacher")
            group.user_set.add(user)
            first_name = form.cleaned_data.get('first_name')
            messages.success(
                request, first_name + ' ' + 'your account was created successfully!')
            # new_teacher = authenticate(username=form.cleaned_data['username'],
            #                         password=form.cleaned_data['password1'],
            #                         )
            return redirect('admineditprofile', user.id)
            
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
            group = Group.objects.get(name="student")
            group.user_set.add(user)
            first_name = form.cleaned_data.get('first_name')
            messages.success(
                request, first_name + ' ' + 'your account was created successfully!')
            
            # login(request, user)

            return redirect('admineditprofile', user.id)
    else:
        form = StudentSignUpForm(request.POST)

    context = {
        'form': form
    }
    return render(request, 'auth/studentregistration.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def allteachers(request):
    all_teachers = Teacher.objects.all
    return render(request, 'hod/teachers.html',{'all_teachers': all_teachers})

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
        try:
            principal = request.user.principal
        except Principal.DoesNotExist:
            principal = Principal(user=request.user)

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
            u_form = TeacherUpdateForm(request.POST, instance=request.user)
            p_form = TeacherProfileUpdateForm(
                request.POST, request.FILES,instance=request.user.teacher)
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
@allowed_users(allowed_roles=['admin'])
def editprofile(request,id):
    current_user = User.objects.get(id=id)
    
    if current_user.is_teacher:
        teacher = get_object_or_404(Teacher,pk=current_user.id)
        if request.method == 'POST':
            u_form = TeacherUpdateForm(
                request.POST, instance=current_user)
            p_form = TeacherProfileUpdateForm(
                request.POST, request.FILES, instance=teacher)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
            
            return HttpResponseRedirect(request.path_info)   
        else:
            u_form = TeacherUpdateForm(instance=current_user)
            p_form = TeacherProfileUpdateForm(
                instance=teacher)

            context = {'u_form': u_form,
                    'p_form': p_form,
                    'current_user': current_user,
                    }
            return render(request, 'auth/teacherprofile.html', context)

    if current_user.is_student:
        student = get_object_or_404(Student,pk=current_user.id)
        if request.method == 'POST':
            u_form = StudentUpdateForm(
                request.POST, instance=current_user)
            p_form = StudentProfileUpdateForm(
                request.POST, request.FILES, instance=student)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
            
            return HttpResponseRedirect(request.path_info)   
        else:
            u_form = StudentUpdateForm(instance=current_user)
            p_form = StudentProfileUpdateForm(
                instance=student)

            context = {'u_form': u_form,
                    'p_form': p_form,
                    'current_user': current_user,
                    }
            return render(request, 'student/studentprofile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admineditprofile(request,id):
    current_user = User.objects.get(id=id)
    
    if current_user.is_teacher:
        teacher = get_object_or_404(Teacher,pk=current_user.id)
        if request.method == 'POST':
            u_form = TeacherUpdateForm(
                request.POST, instance=current_user)
            p_form = TeacherProfileUpdateForm(
                request.POST, request.FILES, instance=teacher)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
            
            return HttpResponseRedirect(request.path_info)   
        else:
            u_form = TeacherUpdateForm(instance=current_user)
            p_form = TeacherProfileUpdateForm(
                instance=teacher)

            context = {'u_form': u_form,
                    'p_form': p_form,
                    'current_user': current_user,
                    }
            return render(request, 'auth/editteacherprofile.html', context)

    if current_user.is_student:
        student = get_object_or_404(Student,pk=current_user.id)
        if request.method == 'POST':
            u_form = StudentUpdateForm(
                request.POST, instance=current_user)
            p_form = StudentProfileUpdateForm(
                request.POST, request.FILES, instance=student)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
            
            return HttpResponseRedirect(request.path_info)   
        else:
            u_form = StudentUpdateForm(instance=current_user)
            p_form = StudentProfileUpdateForm(
                instance=student)

            context = {'u_form': u_form,
                    'p_form': p_form,
                    'current_user': current_user,
                    }
            return render(request, 'auth/editstudentprofile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delprofile(request,id):
    user_to_del = User.objects.get(id=id)
    user_to_del.delete()
    # confirm = input("Are you sure you want to delete {} ('y/n')".format(user_to_del))
    # if confirm.lower() == "y":
    #     user_to_del.delete()
    # else:
    #     pass



@login_required(login_url='login')
def load_subjects(request):
    class_id = request.GET.get('classes_id')
    
    subjects = Subjects.objects.filter(classes_id=class_id)
    
    return render(request,'../templates/loadsubjects.html',{"subjects":subjects})



# @login_required(login_url='login')
# def allstudents(request,id):
#     all_students = Student.objects.filter(classes=id).all()
#     student = get_object_or_404(Student,pk=id)
#     if request.method == 'POST':
#         u_form = StudentUpdateForm(
#             request.POST, instance=student)
#         p_form = StudentProfileUpdateForm(
#             request.POST, request.FILES, instance=student)
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#             messages.success(request, f'Your account has been updated!')
        
#         return HttpResponseRedirect(request.path_info)   
#     else:
#         u_form = StudentUpdateForm(instance=student)
#         p_form = StudentProfileUpdateForm(
#             instance=student)

#         context = {'u_form': u_form,
#                 'p_form': p_form,
#                 "all_students":all_students
#                 }
#     request.session['class_id'] = id
    
#     return render(request,"hod/allstudents.html",context)

@login_required(login_url='login')
def allstudents(request,id):
    all_students = Student.objects.filter(classes=id).all()
    request.session['class_id'] = id
    
    return render(request,"hod/allstudents.html",{"all_students":all_students})

@login_required(login_url='login')
def allteachers(request):
    all_teachers = Teacher.objects.all()
    context = {
        "all_teachers":all_teachers
    }

    
    return render(request,"hod/allteachers.html",context)

@allowed_users(allowed_roles=['admin'])   
@login_required(login_url='login')
def principal_comment(request,id):
    classes =request.session.get('class_id')
    student = get_object_or_404(Student,pk=id)
    subjects = student.subjects.all
    marks = Results.objects.filter(student_id=student,classes=classes)

    my_marks = []
    for mark in marks:
        my_marks.append(mark.mean_marks)
    all_marks = sum(my_marks)
    
    my_points = []
    for mark in marks:
        my_points.append(mark.points)
    if len(my_points) != 0:
        all_points = sum(my_points) / len(my_points)
    else:
        all_points =1

    all_students = Student.objects.filter(classes=classes)
    studentNum = all_students.count()

    try:
        studentreport = report.objects.get(classes_id = classes ,student=student)
    except:
        studentreport = report.objects.create(classes_id = classes ,student=student)
    comm = request.GET.get("pcomments")

    studentreport.p_comments = comm
    studentreport.save()    
    context = {
        "marks":marks,
        "current_student":student,
        "classes":classes,
        "subjects":subjects,
        "marks": marks,
        "all_marks":all_marks,
        "all_points":all_points,
        "studentNum":studentNum
        
    }
   
    return render(request,"hod/studentreport.html",context)

# def generateStudentReports(request,id1,id2):
#     student_results = 
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
@allowed_users(allowed_roles=['admin'])
def addclasses(request):
    form = addClassForm()
    if request.method == 'POST':
        form = addClassForm(request.POST)
        if form.is_valid():
            classes = form.save(commit=False)
            classes.save()
        return HttpResponseRedirect(request.path_info) 
    else:
        form = addClassForm()

    return render(request,"hod/addclasses.html",{"form":form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addacademicyear(request):
    form = addAcademicYearForm()
    if request.method == 'POST':
        form = addAcademicYearForm(request.POST)
        if form.is_valid():
            classes = form.save(commit=False)
            classes.save()
        return HttpResponseRedirect(request.path_info) 
    else:
        form = addAcademicYearForm()

    return render(request,"hod/addacademicyear.html",{"form":form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','teacher'])
def classes(request):
    all_classes = Classes.objects.all()
    context = {"all_classes":all_classes}    
    return render(request,"hod/allclasses.html",context)


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
            ############### 
            smarks = Results.objects.get(student_id=id,classes=current_class)
            try:
                studentreport = report.objects.get(classes = current_class ,student=student)
            except:
                studentreport = report.objects.create(classes = current_class ,student=student)

            
            studentreport.all_subjects.add(smarks)
            studentreport.save()

            marks = Results.objects.filter(student_id=id,classes=current_class)
            my_marks = []
            for mark in marks:
                my_marks.append(mark.mean_marks)
            all_marks = sum(my_marks)

            s_report = report.objects.get(classes_id = current_class ,student=student)
            s_report.total_marks = all_marks
            s_report.save()

            # for student_marks in marks:
            #     print(student_marks)
        return redirect('/students/', subject) 
    else:
        form = addResultsForm()  
    return render(request,"teacher/marks.html",{"form":form,"subject":subject})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def student_positions(request,id):
    all_reports = report.objects.filter(classes=id).order_by("-total_marks")
    
    for i,reports in enumerate(all_reports):
        reports.position = i+1 
        reports.save()
        
    return redirect("allclasses")

@allowed_users(allowed_roles=['teacher'])
def student_subject_positions(request,id):
    all_info = subjectInfo.objects.filter(subject=id).order_by("-mean_marks")
    
    for i,info in enumerate(all_info):
        info.position = i+1 
        info.save()
        
    return redirect("students",id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def fees(request,id):
    student = get_object_or_404(Student,pk=id)
    fees = addFeesForm()

    if request.method == 'POST':
        form = addFeesForm(request.POST)
        if form.is_valid():
            fees = form.save(commit=False)
            fees.student = student
            fees.save()
            return HttpResponseRedirect(request.path_info) 
    else:
        form = addFeesForm()  
    return render(request,"hod/fees.html",{"form":form})




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
            s_report = report.objects.get(classes_id = current_class ,student=student)
            s_report.total_marks = all_marks
            s_report.save()
            ############### 
            smarks = Results.objects.get(student_id=id,classes=current_class)
            try:
                studentreport = report.objects.get(classes = current_class ,student=student)
            except:
                studentreport = report.objects.create(classes = current_class ,student=student)

            
            studentreport.all_subjects.add(smarks)
            studentreport.save()
            
        return redirect('students', subject.id) 
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
    studentNum = len(all_students)
    if studentNum <= 0:
        studentNum = 1
    

    # #mean_marks 
    # mean = all_marks/(len(my_marks)*100) * 100
    #get total points

    my_points = []
    for mark in marks:
        my_points.append(mark.points)
    if len(my_points) != 0:
        all_points = sum(my_points) / len(my_points)
    else:
        all_points=1
  
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
       
    try:
        p_report = report.objects.get(classes_id = selectedClass,student=current_student)
        c_report = report.objects.get(classes_id = classes ,student=current_student)
        p_report = report.objects.get(classes_id = selectedClass,student=current_student)
        c_report = report.objects.get(classes_id = classes.id ,student=current_student)
    except:
        c_report = 0
        p_report = 0

    
    context = {
        "current_student":current_student,
        "classes":classes,
        "subjects":subjects,
        "marks": marks,
        "p_classes":p_classes,
        "all_marks":all_marks,
        "all_points":all_points,
        "selectedClass":selectedClass,
        "studentNum":studentNum,
        "p_report":p_report,
        "c_report":c_report
        
        
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
        
  
    #get previous class report 

    try:
        p_report = report.objects.get(classes_id = p_classes[-2] ,student=current_student)
    except:
        p_report = 0
        

    try:
        c_report = report.objects.get(classes_id = classes ,student=current_student)
       
    except:
        c_report = 0
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
    if len(my_points) != 0:
        all_points = sum(my_points) / len(my_points)
    else:
        all_points =1
  
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
        # selectedClass = classes

    ######
    studentreport = report.objects.get(student_id=current_student,classes=classes)
    
    context = {
        "current_student":current_student,
        "classes":classes,
        "subjects":subjects,
        "marks": marks,
        "p_classes":p_classes,
        "all_marks":all_marks,
        "all_points":all_points,
        "selectedClass":selectedClass,
        "studentNum":studentNum,
        "studentreport":studentreport,
        "p_report":p_report,
        "c_report":c_report
        
        }

    

    return render(request,"student/report.html",context)


