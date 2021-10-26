from django import template

from school.views import teacher
from ..models import *

register = template.Library()




@register.simple_tag
def student_marks(a, b, *args, **kwargs):
    student_id = kwargs['student_id']
    subject_id = kwargs['subject_id']
    
    return Results.objects.filter(subjects_id=subject_id,student_id=student_id)