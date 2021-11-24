from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.fields.files import ImageField
from django.db.models import Count, F, Value,Avg
from django.db.models.query_utils import subclasses
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save

# from school.templatetags.mymarks import mean_marks, position

# from school.templatetags.mymarks import mean_marks
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
        

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    profile_photo = models.ImageField(upload_to='Profiles/',blank=True,null=True)
    staff_number = models.CharField(max_length=2000)
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
    class_teacher = models.ForeignKey(Teacher,on_delete=models.SET("NoNe"),unique=True)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return "{}--{}".format(self.name,self.year)

    class Meta:
        unique_together=("name", "year")

 
    def saveclasses(self):
        self.save()


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
    kcpe_marks = models.IntegerField()
    classes = models.ForeignKey(Classes,on_delete=models.CASCADE,related_name="students",blank=True,null=True)
    subjects = models.ManyToManyField(Subjects,related_name="students")
    reg_number = models.CharField(max_length=2000)
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
    classes = models.ForeignKey(Classes,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name="student_results")
    subjects = models.ForeignKey(Subjects,on_delete=models.CASCADE,related_name="results")
    exam1 = models.FloatField(validators=[MaxValueValidator(30),MinValueValidator(0)],default=0)
    exam2 = models.FloatField(validators=[MaxValueValidator(30),MinValueValidator(0)],default=0)
    # comments = models.CharField(max_length=300)
    teacher = models.CharField(max_length=300)
    endterm = models.FloatField(validators=[MaxValueValidator(70),MinValueValidator(0)],default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        if self.exam1 != None and self.exam2 != None and self.endterm != None:
            return "{} = {}".format(self.subjects,(self.exam1 + self.exam2)/2 + self.endterm)
  
    class Meta:
        unique_together=("student", "subjects")
    @property
    def position(self):
        pass

    def update_results(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            if fields.intersection(deferred_fields):
                fields = fields.union(deferred_fields)
        super().refresh_from_db(using, fields, **kwargs)


    @property
    def mean_marks(self):
        return (self.exam1 + self.exam2)/2 + self.endterm
    
    
    
    @property
    def grade(self):
        gde = (self.exam1 + self.exam2)/2 + self.endterm
        if 80 <= gde <= 100:
            return "A"
        elif gde >= 75:
            return "A-"
        elif gde >= 70:
            return "B+"
        elif gde >= 65:
            return "B"
        elif gde >= 60:
            return "B-"
        elif gde >= 55:
            return "C+"
        elif gde >= 50:
            return "C"
        elif gde >= 45:
            return "C-"
        elif gde >= 40:
            return "D+"
        elif gde >= 35:
            return "D"
        elif gde >= 30:
            return "D-"
        elif  gde >= 0:
            return "E"


    @property
    def points(self):
        grade = self.grade
        if grade == "A":
            return 12
        elif grade == "A-":
            return 11
        elif grade == "B+":
            return 10
        elif grade == "B":
            return 9
        elif grade == "B-":
            return 8
        elif grade == "C+":
            return 7
        elif grade == "C":
            return 6
        elif grade == "C-":
            return 5
        elif grade == "D+":
            return 4
        elif grade == "D":
            return 3
        elif grade == "D-":
            return 2
        elif grade == "E":
            return 1

    @classmethod
    def get_results(cls,subject_id):
        return cls.objects.filter(subjects__pk=subject_id).all()
        
class report(models.Model):
    classes = models.ForeignKey(Classes,on_delete=models.CASCADE,related_name="class_report")
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name="student_report")
    all_subjects = models.ManyToManyField(Results)
    date_created = models.DateTimeField(auto_now_add=True)
    p_comments = models.CharField(max_length=100,null=True,blank=True)
    t_comments = models.CharField(max_length=100,null=True,blank=True)
    total_marks = models.FloatField(blank=True,null=True)
    position = models.IntegerField(blank=True,null=True)
    s_mean_marks = models.IntegerField(blank=True,null=True)
    all_points = models.FloatField(blank=True,null=True)


    @property
    def ov_grade(self):
        if self.all_points == 12 :
            return "A"
        elif self.all_points >= 11:
            return "A-"
        elif self.all_points >= 10:
            return "B+"
        elif self.all_points >= 9:
            return "B"
        elif self.all_points >= 8:
            return "B-"
        elif self.all_points >= 7:
            return "C+"
        elif self.all_points >= 6:
            return "C"
        elif self.all_points >= 5:
            return "C-"
        elif self.all_points >= 4:
            return "D+"
        elif self.all_points >= 3:
            return "D"
        elif self.all_points >= 2:
            return "D-"
        elif self.all_points >= 0:
            return "E"

    def mean(self):
        # marks = 0
        # for mark in self.all_subjects:
        #     marks += mark
        # return marks/self.get_number_of_elements()
        # return self.objects.all().aggregate(Avg('all_subjects'))
        #return self.all_subjects.add()
        pass
    class Meta:
        unique_together=("classes", "student")

    def __str__(self):
        return "{} - {}".format(self.student,self.classes)
    

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

class subjectInfo(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    position = models.IntegerField(blank=True,null=True)
    mean_marks = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return "{} {} {}".format(self.student,self.subject,self.position)

    def savesubjectinfo(self):
        self.save()

    class Meta:
        unique_together=("student","subject")


class Information(models.Model):
    title = models.CharField(max_length=200,blank=True,null=True)
    desc = models.CharField(max_length=200,blank=True,null=True)
    openingDate = models.DateField(blank=True,null=True)
    closingDate = models.DateField(blank=True,null=True)

    def __str__(self):
        return "{}".format(self.title)


class classRecord(models.Model):
    classes = models.ForeignKey(Classes,on_delete=models.SET("NoNe"))
    students = models.ManyToManyField(Student)
    class_teacher = models.CharField(max_length=200)

    def __str__(self):
        return "This is the {} class".format(self.classes)