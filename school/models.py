from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.files import ImageField
from django.db.models import Count, F, Value,Avg
# from django.views.generic.detail import T
# Create your models here.

class User(AbstractUser):
    is_headteacher = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    

class HeadTeacher(models.Model):
    profile_photo = models.ImageField(upload_to='Profiles/')
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    staff_number = models.CharField(max_length=2000,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username 


class AcademicYear(models.Model):
    year =  models.CharField(max_length=2000)
    term = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} {}".format(self.year, self.term)

    def saveacademicyear(self):
        self.save()

classes =(
    ("Form One", "Form One"),
    ("Form Two", "Form Two"),
    ("Form Three", "Form Three"),
    ("Form Four ","Form Four"),
)

class Classes(models.Model):
    name = models.CharField(choices=classes,max_length=1000)
    year = models.ForeignKey(AcademicYear,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}--{}".format(self.name,self.year)
        
    
    def saveclasses(self):
        self.save()


class Subjects(models.Model):
    name = models.CharField(max_length=2000)
    classes = models.ManyToManyField(Classes,related_name="subjects")
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    def savesubjects(self):
        self.save()

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    subjects = models.ManyToManyField(Subjects,related_name="teacher")
    profile_photo = models.ImageField(upload_to='Profiles/',blank=True,null=True)
    staff_number = models.CharField(max_length=2000,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    def saveteacher(self):
        self.save()

    @classmethod
    def search_student(cls,staff_number):
        return cls.objects.filter(staff_number=staff_number).user


class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    profile_photo = models.ImageField(upload_to='Profiles/',blank=True,null=True)
    classes = models.ForeignKey(Classes,on_delete=models.CASCADE,related_name="students")
    subjects = models.ManyToManyField(Subjects,related_name="students")
    reg_number = models.CharField(max_length=2000,unique=True)
    hse = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username

    def savestudent(self):
        self.save()

    @classmethod
    def search_student(cls,reg_number):
        return cls.objects.filter(reg_number=reg_number).user

class Results(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    exam1 = models.FloatField(blank=True,null=True)
    exam2 = models.FloatField(blank=True,null=True)
    endterm = models.FloatField(blank=True,null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} ={}".format(self.subjects,(self.exam1 + self.exam2)/2 + self.endterm)



class report(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    all_subjects = models.ManyToManyField(Results)
    date_created = models.DateTimeField(auto_now_add=True)

    def mean(self):
        # marks = 0
        # for mark in self.all_subjects:
        #     marks += mark

        # return marks/self.get_number_of_elements()
        # return self.objects.all().aggregate(Avg('all_subjects'))
        #return self.all_subjects.add()
        pass
    def __str__(self):
        return str(self.mean())

         

class Fees(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    amount_payable = models.FloatField()
    amount_paid  = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
 

    def get_balance(self):
        return str(self.amount_payable - self.amount_paid)

    def __str__(self):
        return self.get_balance()

    def savesfees(self):
        self.save()


