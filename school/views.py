from django.contrib.auth import login
from django.shortcuts import render,redirect,get_object_or_404
from. forms import *
from .models import *
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
      return render(request,'../templates/hod/hod.html')
# def register(request):
#     return render(request,'../templates/auth/register.html')

class UserCreateView(FormView):
    form_class = CustomUserForm
    template_name = '../templates/auth/register.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save()
        if user.user_type == "student":
            return redirect(f'/create-student/{user.id}')
        elif user.user_type == "principal":
            return redirect(f'/create-principal/{user.id}')
        
        elif user.user_type == "teacher":
            return redirect(f'/create-teacher/{user.id}')
        


    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context.update({
            'user_create': True,
            'student_create': False,
            'teacher_create': True
        })
        return context




class PrincipalView(FormView):
    form_class = PrincipalRegistrationForm
    template_name =  '../templates/auth/headregister.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.user_id = self.kwargs['_id']
        user = User.objects.get(id=self.kwargs['id'])
        principal = Principal.objects.create(user=user)
        principal.save()
        print(principal)
        return super().form_valid(form)
 

    def get_context_data(self, **kwargs):
        context = super(PrincipalView, self).get_context_data(**kwargs)
        context.update({
            'user_create': False,
            'student_create': True
        })
        return context

class TeacherView(FormView):
    form_class = TeacherRegisterForm
    template_name = '../templates/auth/teacherregister.html'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.user_id = self.kwargs['_id']
        user = User.objects.get(id=self.kwargs['id'])
        teacher = Teacher.objects.create(user=user)
        teacher.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TeacherView, self).get_context_data(**kwargs)
        context.update({
            'user_create': False,
            'student_create': True
        })
        return context



class StudentView(FormView):
    form_class = StudentRegisterForm
    template_name = '../templates/auth/studentregister.html'
  
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.user_id = self.kwargs['_id']
        user = User.objects.get(id=self.kwargs['id'])
        student = Student.objects.create(user=user)
        student.save()
        return super().form_valid(form)
        print(student.classes)
        return redirect("home")

    def get_context_data(self, **kwargs):
        context = super(StudentView, self).get_context_data(**kwargs)
        context.update({
            'user_create': False,
            'student_create': True
        })
        return context
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
    

    all_students = subject.students.all()
    
    # students = Student.objects.filter(subjects_id=subject)
    return render(request,"teacher/studentlist.html",{"subject":subject,"all_students":all_students,})

def addmarks(request,id):
    subject = Subjects.objects.filter(teacher=request.user.id)[0]
    student = get_object_or_404(Student,pk=id)
    marks = addResultsForm()
    if request.method == 'POST':
        form = addResultsForm(request.POST)
        if form.is_valid():
            marks = form.save(commit=False)
            marks.student = student
            marks.subject = subject
            marks.save()
        return HttpResponseRedirect(request.path_info) 
    else:
        form = addResultsForm()  
    return render(request,"teacher/marks.html",{"form":form})  



    


