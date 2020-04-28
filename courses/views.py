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
        enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso')
    else:
        messages.info(request, 'Você já está inscrito no curso')

    return redirect(f'/contas')

@login_required
def annoucements(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if not request.user.is_staff:
        enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

        if not enrollment.is_approved():
            messages.error(request, 'Sua inscrição está pendente')
            return redirect('/contas')

    template = 'announcements.html'
    context = {'course': course}

    return render(request, template, context)

@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso')
        return redirect('/contas')

    template = 'undo_enrollment.html'
    context = {'enrollment': enrollment,
               'course': course}

    return render(request, template, context)
