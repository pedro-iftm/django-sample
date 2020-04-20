from django.template import Library
from courses.models import Enrollment


register = Library()


@register.simple_tag
def load_my_courses(user):
    return Enrollment.objects.filter(user=user)
