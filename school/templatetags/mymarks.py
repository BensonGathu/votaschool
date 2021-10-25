from django import template

from school.views import teacher
from school.models import Results

register = template.Library()


@register.simple_tag
def student_marks(subject_id,student_id):
    
    return Results.objects.filter(student=student_id,subjects=subject_id)