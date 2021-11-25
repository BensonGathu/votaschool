from django import template

from school.views import allstudents, teacher
from school.models import Results,Student,report,subjectInfo

register = template.Library()


@register.simple_tag
def student_marks(subject_id,student_id):
    
    return Results.objects.filter(student=student_id,subjects=subject_id)




student_list = {}
@register.simple_tag
def position(student_name, mean_marks):
    if student_name not in student_list.keys():
     
        student_list[student_name] = mean_marks
    
    return dict(sorted(student_list.values(), key=lambda item: item[1]))
    


@register.simple_tag
def ov_grade(all_points):
    if all_points == 12 :
        return "A"
    elif all_points >= 11:
        return "A-"
    elif all_points >= 10:
        return "B+"
    elif all_points >= 9:
        return "B"
    elif all_points >= 8:
        return "B-"
    elif all_points >= 7:
        return "C+"
    elif all_points >= 6:
        return "C"
    elif all_points >= 5:
        return "C-"
    elif all_points >= 4:
        return "D+"
    elif all_points >= 3:
        return "D"
    elif all_points >= 2:
        return "D-"
    elif all_points >= 0:
        return "E"

my_marks = []
@register.simple_tag
def mean_marks(current_student,classes):
    my_marks.clear()
    marks = Results.objects.filter(student_id=current_student,classes=classes)
    try:
        studentreport = report.objects.get(student=current_student,classes=classes)
    except:
        studentreport = report.objects.create(student=current_student,classes=classes)
    
    print(studentreport)
  
    for mark in marks:
        my_marks.append(mark.mean_marks)
    all_marks = sum(my_marks)
    if len(my_marks) != 0:
        studentreport.s_mean_marks = int(all_marks/(len(my_marks)*100) * 100)
        studentreport.save()
        return int(all_marks/(len(my_marks)*100) * 100)
    else:
        studentreport.s_mean_marks = 0
        studentreport.save()
        return 0
   
    
@register.simple_tag 
def subjectcomments(subject_grade):
    if subject_grade == "A" or subject_grade == "A-":
        return "Excellent"
    elif subject_grade == "B" or subject_grade == "B+":
        return "Very Good"
    elif subject_grade == "C+" or subject_grade == "B-":
        return "Good"
    elif subject_grade == "C" or subject_grade == "C-":
        return "Fair"
    elif subject_grade == "D" or subject_grade == "D+":
        return "Improve"
    elif subject_grade == "E" or subject_grade == "D-":
        return "Poor"


@register.simple_tag
def class_position(classes,stud_mean):
    all_students = Student.objects.filter(classes=classes)
    all_students.order_by(stud_mean)
    print(all_students)



@register.simple_tag
def all_students(classes):
    students = Student.objects.filter(classes=classes)
    return students


@register.simple_tag
def generate_subject_position(subject,student,meanmarks):

    try:
        studentsubjectInfo = subjectInfo.objects.get(subject=subject ,student=student)
    except:
        studentsubjectInfo = subjectInfo.objects.create(subject=subject ,student=student)
    
    studentsubjectInfo.mean_marks = meanmarks
    studentsubjectInfo.save()

@register.simple_tag
def get_subject_position(subject,student):
    try: 

        studentsubjectInfo = subjectInfo.objects.get(subject_id=subject ,student_id=student)
    except:
        return 0
        
    return studentsubjectInfo.position
   
    # for subjectinformation in studentsubjectInfo:
    #     print("Gathu")
    #     return subjectinformation.position

@register.simple_tag
def check_student_report(student,classes):
    try:
        if Results.objects.get(student_id=student,classes=classes):
            return True
    except:
        return False
