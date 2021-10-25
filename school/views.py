from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect,get_object_or_404
from. forms import *
from .models import *
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
      return render(request,'../templates/hod/hod.html')

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


def student_registration(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            messages.success(
                request, first_name + ' ' + 'your account was created successfully!')
            return redirect('profile',request.id)
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
                return redirect('home')
            if user.is_teacher:
                return redirect('home')
            if user.is_student:
                return redirect('home')
        else:
            messages.error(request, 'Invalid Username and/or Password')

    context = {}
    return render(request, 'auth/login.html', context)


def logoutUser(request):
    current_user = request.user
    logout(request)
    messages.info(
        request, 'You have logged out. Log back in to book our services.')
    # if current_user.is_admin:
    #     return redirect('home')
    return redirect('login')


@login_required
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
                print(p_form.staff_number)
                print("saved")
                messages.success(request, f'Your account has been updated!')
                print("saved")
            return redirect('home')
        else:
            u_form = PrincipalUpdateForm(instance=request.user)
            p_form = PrincipalProfileUpdateForm(instance=request.user.profile)
            print("not saved")
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
                request.POST, request.FILES)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Your account has been updated!')
            return redirect('home')
        else:
            u_form = TeacherUpdateForm(instance=request.user)
            p_form = TeacherProfileUpdateForm(
                instance=request.user.teacher)

            context = {'u_form': u_form,
                    'p_form': p_form,
                    'current_user': current_user,
                    }
            return render(request, 'auth/teacherprofile.html', context)

            

            
# def register(request):
#     return render(request,'../templates/auth/register.html')

# class UserCreateView(FormView):
#     form_class = CustomUserForm
#     template_name = '../templates/auth/register.html'

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         user = form.save()
#         if user.user_type == "student":
#             return redirect(f'/create-student/{user.id}')
#         elif user.user_type == "principal":
#             return redirect(f'/create-principal/{user.id}')
        
#         elif user.user_type == "teacher":
#             return redirect(f'/create-teacher/{user.id}')
        


#     def get_context_data(self, **kwargs):
#         context = super(UserCreateView, self).get_context_data(**kwargs)
#         context.update({
#             'user_create': True,
#             'student_create': False,
#             'teacher_create': True
#         })
#         return context




# class PrincipalView(FormView):
#     form_class = PrincipalRegistrationForm
#     template_name =  '../templates/auth/headregister.html'

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         # form.user_id = self.kwargs['_id']
#         user = User.objects.get(id=self.kwargs['id'])
#         principal = Principal.objects.create(user=user)
#         principal.save()
#         print(principal)
#         return super().form_valid(form)
 

#     def get_context_data(self, **kwargs):
#         context = super(PrincipalView, self).get_context_data(**kwargs)
#         context.update({
#             'user_create': False,
#             'student_create': True
#         })
#         return context

# class TeacherView(FormView):
#     form_class = TeacherRegisterForm
#     template_name = '../templates/auth/teacherregister.html'

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         # form.user_id = self.kwargs['_id']
#         user = User.objects.get(id=self.kwargs['id'])
#         teacher = Teacher.objects.create(user=user)
#         teacher.save()
#         return super().form_valid(form)

#     def get_context_data(self, **kwargs):
#         context = super(TeacherView, self).get_context_data(**kwargs)
#         context.update({
#             'user_create': False,
#             'student_create': True
#         })
#         return context



# class StudentView(FormView):
#     form_class = StudentRegisterForm
#     template_name = '../templates/auth/studentregister.html'
  
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         # form.user_id = self.kwargs['_id']
#         user = User.objects.get(id=self.kwargs['id'])
#         student = Student.objects.create(user=user)
#         student.save()
#         return super().form_valid(form)
#         return redirect("home")

#     def get_context_data(self, **kwargs):
#         context = super(StudentView, self).get_context_data(**kwargs)
#         context.update({
#             'user_create': False,
#             'student_create': True
#         })
#         return context
def load_subjects(request):
    class_id = request.GET.get('classes_id')
    subjects = Subjects.objects.filter(classes_id=class_id)
    return render(request,'../templates/loadsubjects.html',{"subjects":subjects})

# class registerteacher(CreateView):
#     model = User
#     form_class = TeacherRegisterForm
#     template_name = '../templates/auth/teacherregister.html'
    
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('/')
 

# class registerstudent(CreateView):
#     model = User
#     form_class = StudentRegisterForm
#     template_name = '../templates/auth/studentregister.html'

    
#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('/')

# class registerheadteacher(CreateView):
#     model = User
#     form_class = HeadTeacherRegisterForm
#     template_name = '../templates/auth/headregister.html'

   

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('/')


def allstudents(request):
    all_classes = Classes.objects.all()
    all_students = Student.objects.filter(classes__name="Form One").all()
    
    return render(request,"students.html",{"all_classes":all_classes,"all_students":all_students})


def addTeacher(request):
    all_teachers = Teacher.objects.all()
    form = TeacherRegisterForm()
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.save()
        return HttpResponseRedirect(request.path_info) 
    else:
        form = TeacherRegisterForm()

    return render(request,"addteacher.html",{"form":form})




def addStudent(request):
    all_students = Student.objects.all()
    form = StudentRegisterForm()
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.save()
        return HttpResponseRedirect(request.path_info) 
    else:
        form = StudentRegisterForm()

    return render(request,"addstudent.html",{"form":form,"all_students":all_students})


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

    return render(request,"addsubject.html",{"form":form,"all_subjects":all_subjects})

def classes(request):
    all_classes = Classes.objects.all()    
    return render(request,"classes.html",{"all_classes":all_classes})

def subject(request,id):
    subject = get_object_or_404(Subjects, pk=id)
    return render(request,"subject.html",{"subject":subject})

def addresults(request):
    # subjects = Subjects.objects.filter(teacher.id=request.id)
    teacher = Teacher.objects.get(user_id=request.user)
    subjects = Subjects.objects.filter(teacher=request.user.id)
    form = addResultsForm()
    return render(request,"results.html",{"teacher":teacher,"subjects":subjects,"form":form})


def teacher(request):
    teacher = Teacher.objects.get(user_id=request.user)
    subjects = Subjects.objects.filter(teacher=request.user.id)
    return render(request,"teacher/teacher.html",)

def Students(request,id):
    subject = get_object_or_404(Subjects,pk=id)
    student_id = request.session.get('student_id')
    
    all_students = subject.students.all()
    marks = Results.objects.filter(subjects_id=id,student_id=student_id)

   
    request.session['current_class_id'] = id
    exam1 = Results.get_results(id)
    # students = Student.objects.filter(subjects_id=subject)
    context = {"subject":subject,
                "all_students":all_students,
                "exam1": exam1,
                "marks":marks}

    return render(request,"teacher/studentlist.html",context)

def addmarks(request,id):
    student = get_object_or_404(Student,pk=id)
    subjectid = request.session.get('current_class_id')
    subject = get_object_or_404(Subjects,pk=subjectid)
    student_id = request.session["student_id"] = id
    marks = addResultsForm()
    if request.method == 'POST':
        form = addResultsForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.subjects = subject
            marks.save()
        return HttpResponseRedirect(request.path_info) 
    else:
        form = addResultsForm()  
    return render(request,"teacher/marks.html",{"form":form,"subject":subject})







    


