from django import template

from school.views import allstudents, teacher
from school.models import Results,Student

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
  
    for mark in marks:
        my_marks.append(mark.mean_marks)
    all_marks = sum(my_marks)
    if len(my_marks) != 0:
        return int(all_marks/(len(my_marks)*100) * 100)
    else:
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