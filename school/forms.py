import typing_extensions 
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.db import transaction
from django.db.models import fields
from django.forms import widgets
from django.contrib.auth import get_user_model

User = get_user_model()
from bootstrap_datepicker_plus import DatePickerInput

from .models import *
from school.models import User

class PrincipalSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    middle_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=20, required=True)
   

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name','middle_name' ,'last_name',
                 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_principal = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.middle_name = self.cleaned_data.get('middle_name')
        user.save()
        principal = Principal.objects.create(user=user)
        principal.save()
        return user


class PrincipalUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'middle_name','last_name']


class PrincipalProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Principal
        fields = ['staff_number', 'profile_photo']



class TeacherSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    middle_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=20, required=True)
   

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name','middle_name' ,'last_name',
                 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.middle_name = self.cleaned_data.get('middle_name')
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.save()
        return user


class TeacherUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'middle_name','last_name']


class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['staff_number', 'profile_photo']



class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    middle_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=20, required=True)
   

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name','middle_name' ,'last_name',
                 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.middle_name = self.cleaned_data.get('middle_name')
        user.save()
        student = Student.objects.create(user=user)
        student.save()
        return user


class StudentUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'middle_name','last_name']


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['reg_number','kcpe_marks' ,'profile_photo','classes','subjects','hse']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = Subjects.objects.none()

        if 'classes' in self.data:
            try:
                classes_id = int(self.data.get('classes'))
                self.fields['subjects'].queryset = Subjects.objects.filter(classes_id=classes_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['subjects'].queryset = self.instance.classes.subject_set.order_by('name')




# class AdminUpdateForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email']

# class CustomUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('user_type','username', 'password1', 'password2',)


# class PrincipalRegistrationForm(forms.Form):
#     user_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
#     first_name = forms.CharField(max_length=100, required=True)
#     middle_name = forms.CharField(max_length=100, required=True)
#     last_name = forms.CharField(max_length=100, required=True)
#     profile_photo = forms.ImageField(required=False)
#     staff_number = forms.CharField(max_length=100, required=True)

#     class Meta:
#         model = Principal
#         fields = ('user_id', 'first_name', 'middle_name',
#                   'last_name', 'staff_number','profile_photo',)



# class TeacherRegisterForm(forms.Form):
#     user_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
#     first_name = forms.CharField(max_length=100, required=True)
#     middle_name = forms.CharField(max_length=100, required=True)
#     last_name = forms.CharField(max_length=100, required=True)
#     # staff_number = forms.CharField(max_length=100, required=True)
#     subjects = forms.ModelMultipleChoiceField(queryset=Subjects.objects.all(),widget=forms.CheckboxSelectMultiple)

#     profile_photo = forms.ImageField(required=False)

#     class Meta:
#         model = Teacher
#         fields = ('user_id', 'first_name', 'middle_name',
#                   'last_name', 'staff_number','profile_photo','subjects')



# class StudentRegisterForm(forms.Form):
#     user_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
#     first_name = forms.CharField(max_length=100, required=True)
#     middle_name = forms.CharField(max_length=100, required=True)
#     last_name = forms.CharField(max_length=100, required=True)
#     reg_number = forms.CharField(max_length=100, required=True)
#     profile_photo = forms.ImageField(required=False)
#     classes = forms.ModelChoiceField(queryset=Classes.objects.all(),required=True)
#     subjects = forms.ModelMultipleChoiceField(queryset=Subjects.objects.all(),widget=forms.CheckboxSelectMultiple)
#     hse = forms.CharField(max_length=100, required=True)

#     class Meta:
#         model = Student
#         fields = ('user_id', 'first_name', 'middle_name',
#                   'last_name', 'reg_number', 'hse','profile_photo','subjects','classes')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['subjects'].queryset = Subjects.objects.none()

#         if 'classes' in self.data:
#             try:
#                 classes_id = int(self.data.get('classes'))
#                 self.fields['subjects'].queryset = Subjects.objects.filter(classes_id=classes_id).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty City queryset
#         # elif self.instance.pk:
#         #     self.fields['subjects'].queryset = self.instance.classes.subject_set.order_by('name')





class addSubjectForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = '__all__'



class addAcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = '__all__'


class addTeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ['profile_photo']


class addStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['profile_photo']


class addClassForm(forms.ModelForm):
    class Meta:
        model = Classes
        fields = "__all__"


class addResultsForm(forms.ModelForm):
    class Meta:
        model = Results
        fields = ['exam1','exam2','endterm']

class addFeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = ['amount_payable','amount_paid']


class addInformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ('title','desc','openingDate','closingDate')

        widgets = {
      'openingDate':(DatePickerInput(attrs={'placeholder':'YYYY-MM-DD', 'input_format' : '%Y-%m-%d'})),
      'closingDate':(DatePickerInput(attrs={'placeholder':'YYYY-MM-DD', 'input_format' : '%Y-%m-%d'})),
    }


# class createTimeTableForm(forms.ModelForm):
#     class Meta:
#         model = TimeTable
#         fields = ['classes']

# class createTimeTableItemsForm(forms.ModelForm):
#     class Meta:
#         model = TimeTableItems
#         fields = ('timetable','day_of_the_week','subject','starttime','duration')
        
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.fields['subject'].queryset = Subjects.objects.none()

#             if 'timetable' in self.data:
#                 try:
#                     timetable_id = int(self.data.get('timetable'))
#                     self.fields['subjects'].queryset = Subjects.objects.filter(classes_id=timetable_id.classes).order_by('name')
#                 except (ValueError, TypeError):
#                     pass 
        




##############################
# class addPrincipalCommentForm(forms.ModelForm):
#     class Meta:
#         model = Results
#         fields = ['p_comments']

# class addClassTCommentForm(forms.ModelForm):
#     class Meta:
#         model = Results
#         fields = ['t_comments']

# class addFeeForm(forms.ModelForm):
#     class Meta:
#         model = Fees
#         fields = "__all__"


# class HeadTeacherRegisterForm(UserCreationForm):
#     first_name = forms.CharField(max_length=100,required=True)
#     middle_name = forms.CharField(max_length=100,required=True)
#     last_name = forms.CharField(max_length=100,required=True)
#     staff_number = forms.CharField(max_length=100,required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User

#     @transaction.atomic
#     def data_save(self):
#         user = super().save(commit=False)
#         user.is_headteacher = True
#         user.is_staff = True
#         user.first_name = self.cleaned_data.get("first_name")
#         user.middle_name = self.cleaned_data.get("middle_name")
#         user.last_name = self.cleaned_data.get("last_name")
#         user.save()
#         headteacher = HeadTeacher.objects.create(user=user)
#         headteacher.staff_number = self.cleaned_data.get("staff_number")
#         headteacher.save()
#         return user



    # @transaction.atomic
    # def data_save(self):
    #     user = super().save(commit=False)
    #     user.is_teacher = True
    #     user.is_staff = True
    #     user.first_name = self.cleaned_data.get("first_name")
    #     user.middle_name = self.cleaned_data.get("middle_name")
    #     user.last_name = self.cleaned_data.get("last_name")
    #     user.save()
    #     teacher = Teacher.objects.create(user=user)
    #     teacher.staff_number = self.cleaned_data.get("staff_number")
    #     teacher.save()
    #     return user


    
# class StudentRegisterForm(UserCreationForm):
#     first_name = forms.CharField(max_length=100,required=True)
#     middle_name = forms.CharField(max_length=100,required=True)
#     last_name = forms.CharField(max_length=100,required=True)
#     reg_number = forms.CharField(max_length=100,required=True)
#     classes = forms.ModelChoiceField(queryset=Classes.objects.all().order_by('name'),required=True)
#     subjects = forms.ModelMultipleChoiceField(queryset=Subjects.get_class_subjects(classes),widget=forms.CheckboxSelectMultiple)
#     hse = forms.CharField(max_length=100,required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User

#     @transaction.atomic
#     def data_save(self):
#         user = super().save(commit=False)
#         user.is_student = True
#         user.first_name = self.cleaned_data.get("first_name")
#         user.middle_name = self.cleaned_data.get("middle_name")
#         user.last_name = self.cleaned_data.get("last_name")
#         user.save()
#         student = Student.objects.create(user=user)
#         student.reg_number = self.cleaned_data.get("reg_number")
#         student.classes = self.cleaned_data.get("classes")
#         student.subjects = self.cleaned_data.get("subjects")
#         student.hse = self.cleaned_data.get("hse")
#         student.save()
#         return user