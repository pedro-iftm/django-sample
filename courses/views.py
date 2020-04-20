from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from courses.models import Course, Enrollment

from .forms import ContactCourse


def courses(request):
    TEMPLATE_COURSES = 'courses.html'

    courses = Course.objects.all()
    context = {'courses': courses}
    
    return render(request, TEMPLATE_COURSES, context)


def details(request, slug):
    TEMPLATE_DETAILS = 'details.html'

    context = {}
    course = get_object_or_404(Course, slug=slug)

    if request.method == 'POST':
        form = ContactCourse(request.POST)

        if form.is_valid():
            context['is_valid'] = True
            form.send_mail(course)

    form = ContactCourse()
    context.update({'course': course, 'form': form})

    return render(request, TEMPLATE_DETAILS, context)

@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        # enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')

    return redirect(f'/contas')
