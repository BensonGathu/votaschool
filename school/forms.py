from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.db import transaction

from .models import *
from school.models import User


class HeadTeacherForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,required=True)
    middle_name = forms.CharField(max_length=100,required=True)
    last_name = forms.CharField(max_length=100,required=True)
    staff_number = forms.CharField(max_length=100,required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def data_save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name")
        user.middle_name = self.cleaned_data.get("middle_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.save()
        headteacher = HeadTeacher.objects.create(user=user)
        headteacher.staff_number = self.cleaned_data.get("staff_number")
        headteacher.save()
        return user

class TeacherForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,required=True)
    middle_name = forms.CharField(max_length=100,required=True)
    last_name = forms.CharField(max_length=100,required=True)
    staff_number = forms.CharField(max_length=100,required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def data_save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name")
        user.middle_name = self.cleaned_data.get("middle_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.staff_number = self.cleaned_data.get("staff_number")
        teacher.save()
        return user



class StudentForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,required=True)
    middle_name = forms.CharField(max_length=100,required=True)
    last_name = forms.CharField(max_length=100,required=True)
    reg_number = forms.CharField(max_length=100,required=True)
    classes = forms.ModelChoiceField(queryset=Classes.objects.all().order_by('id'),required=True)
    subjects = forms.ModelChoiceField(queryset=Subjects.objects.all().order_by('name'),required=True)
    hse = forms.CharField(max_length=100,required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def data_save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name")
        user.middle_name = self.cleaned_data.get("middle_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.save()
        student = Student.objects.create(user=user)
        student.reg_number = self.cleaned_data.get("reg_number")
        student.classes = self.cleaned_data.get("classes")
        student.subjects = self.cleaned_data.get("subjects")
        student.hse = self.cleaned_data.get("hse")
        student.save()
        return user