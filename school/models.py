from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(models.Model):
    is_headteacher = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class HeadTeacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    staff_number = models.CharField(max_length=2000,unique=True)
    

class AcademicYear(models.Model):
    year =  models.CharField(max_length=2000)
    term = models.CharField(max_length=2000)
    def __str__(self):
        return self.year

    def saveacademicyear(self):
        self.save()

classes =(
    ("form one", "form one"),
    ("form two", "form two"),
    ("form three", "form three"),
    ("form four", "form four")
)
class Classes(models.Model):
    names = forms.ChoiceField(choices = classes)
    year = models.ForeignKey(AcademicYear,on_delete=models.CASCADE)

    def __str__(self):
        return self.names

    
    def saveclasses(self):
        self.save()

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    staff_number = models.CharField(max_length=2000,unique=True)

    def __str__(self):
        return self.name

    def saveteacher(self):
        self.save()



class Subjects(models.Model):
    name = models.CharField(max_length=2000)
    teachers = models.OneToManyField(Teacher,blank=True,null=True)

    def __str__(self):
        return self.name

    def savesubjects(self):
        self.save()


class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    classes = models.OneToManyField(Classes)
    subjects = models.OneToManyField(Subjects)
    reg_number = models.CharField(max_length=2000)
    hse = models.CharField(max_length=2000)
    

    def __str__(self):
        return self.name

    def savestudent(self):
        self.save()

class Results(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    exam1 = models.FloatField(blank=True,null=True)
    exam2 = models.FloatField(blank=True,null=True)
    endterm = models.FloatField(blank=True,null=True)

    def percentage(self):
        return self.exam1 + self.exam2 + self.endterm 

    def __str__(self):
        self.percentage()


class report(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    all_subjects = models.ManyToManyField(Results)

    sub = len(all_subjects)

    def mean(self):
        marks = 0
        for mark in self.all_subjects:
            marks += mark

        return marks/self.sub
         

class Fees(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    amount_payable = models.FloatField()
    amount_paid  = models.FloatField()
    
    def __str__(self):
        return self.amount_paid

    def get_balance(self):
        return self.amount_payable - self.amount_paid

    def savesfees(self):
        self.save()


