from django import template

from school.views import teacher
from school.models import Results

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