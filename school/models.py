from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.files import ImageField
from django.db.models import Count, F, Value,Avg
from django.db.models.query_utils import subclasses
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
# from django.views.generic.detail import T
# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_principal = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.username

class Principal(models.Model):
    profile_photo = models.ImageField(upload_to='Profiles/')
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    staff_number = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    # @property
    # def profile_pic_url(self):
    #     if self.profile_pic and hasattr(self.profile_pic, 'url'):
    #         return self.profile_pic.url
    #     else:
    #         return "/media/default.png"
        
    def save_principal(self):
        self.save()

    def update_principal(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            if fields.intersection(deferred_fields):
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)

    def delete_principal(self):
        self.delete()

    def create_principal_profile(sender, **kwargs):
        if kwargs['created']:
            principal_profile = Principal.objects.create(
                user=kwargs['instance'])

    # post_save.connect(create_principal_profile, sender=User)

terms = (
        ("Term one Jan- April"," Term one Jan- April"),
        ("Term two May- August", "Term two May- August"),
        ("Term three September- December", "Term three September- December"),
    )

class AcademicYear(models.Model):
    year =  models.CharField(max_length=2000)
    term = models.CharField(choices=terms,max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.year, self.term)

    class Meta:
        unique_together=("year", "term")

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

    class Meta:
        unique_together=("name", "year")

    def saveclasses(self):
        self.save()

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    profile_photo = models.ImageField(upload_to='Profiles/',blank=True,null=True)
    staff_number = models.CharField(max_length=2000,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def save_teacher(self):
        self.save()

    def update_teacher(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            if fields.intersection(deferred_fields):
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)

    def delete_teacher(self):
        self.delete()

    def create_teacher_profile(sender, **kwargs):
        if kwargs['created']:
            teacher_profile = Teacher.objects.create(
                user=kwargs['instance'])

    # post_save.connect(create_teacher_profile, sender=User)

    @classmethod
    def search_student(cls,staff_number):
        return cls.objects.filter(staff_number=staff_number).user

subject_names = (
    ("English", "English"),
    ("Mathematics","Mathematics"),
    ("Kiswahili", "Kiswahili"),
    ("Chemistry","Chemistry"),
    ("Physics", "Physics"),
    ("Biology","Biology"),
    ("Geography", "Geography"),
    ("History", "History"),
    ("C.R.E", "C.R.E"),
    ("Agriculture", "Agriculture"),
    ("Business Studies", "Business Studies"),
    )
class Subjects(models.Model):
    name = models.CharField(choices=subject_names,max_length=2000)
    classes = models.ForeignKey(Classes,related_name="subjects",on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.name,self.classes)

    class Meta:
        unique_together=("name", "classes")

    def savesubjects(self):
        self.save()

    @classmethod
    def get_class_subjects(cls,student_class):
        return cls.objects.filter(classes=student_class)

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

    def save_student(self):
        self.save()

    def update_student(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            if fields.intersection(deferred_fields):
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)

    def delete_student(self):
        self.delete()

    def create_student_profile(sender, **kwargs):
        if kwargs['created']:
            student_profile = Student.objects.create(
                user=kwargs['instance'])

    # post_save.connect(create_student_profile, sender=User)

    @classmethod
    def search_student(cls,reg_number):
        return cls.objects.filter(reg_number=reg_number).user
        
class Results(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    exam1 = models.FloatField(blank=True,null=True,validators=[MaxValueValidator(30),MinValueValidator(0)])
    exam2 = models.FloatField(blank=True,null=True,validators=[MaxValueValidator(30),MinValueValidator(0)])
    endterm = models.FloatField(blank=True,null=True,validators=[MaxValueValidator(70),MinValueValidator(0)])
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "{} ={}".format(self.subjects,(self.exam1 + self.exam2)/2 + self.endterm)
    class Meta:
        unique_together=("student", "subjects")
        
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