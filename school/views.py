from django.contrib.auth import login
from django.shortcuts import render,redirect,get_object_or_404
from. forms import *
from .models import *
from django.views.generic import CreateView
from django.http import HttpResponseRedirect

# Create your views here.

def home(request):
      return render(request,'../templates/hod/hod.html')
def register(request):
    return render(request,'../templates/auth/register.html')

class registerteacher(CreateView):
    model = User
    form_class = TeacherRegisterForm
    template_name = '../templates/auth/teacherregister.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


class registerstudent(CreateView):
    model = User
    form_class = StudentRegisterForm
    template_name = '../templates/auth/studentregister.html'

    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class registerheadteacher(CreateView):
    model = User
    form_class = HeadTeacherRegisterForm
    template_name = '../templates/auth/headregister.html'

   

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


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
    subjects = teacher.subjects.all()

    return render(request,"results.html",{"teacher":teacher,"subjects":subjects})

def addmarks(request,id):
    pass

