from django.contrib.auth import login
from django.shortcuts import redirect, render
from. forms import *
from .models import *
from django.views.generic import CreateView

# Create your views here.

def home(request):
      return render(request,'../templates/home.html')
def register(request):
    return render(request,'../templates/auth/register.html')

class registerteacher(CreateView):
    model = User
    form_class = TeacherRegisterForm
    template_name = '../templates/auth/teacherregister.html'
    


class registerstudent(CreateView):
    model = User
    form_class = StudentRegisterForm
    template_name = '../templates/auth/studentregister.html'

  

class registerheadteacher(CreateView):
    model = User
    form_class = HeadTeacherRegisterForm
    template_name = '../templates/auth/headregister.html'

   

