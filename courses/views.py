from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, Lesson, Material
from .forms import ContactCourse
from .decorators import enrollment_required


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


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    template = 'lessons.html'
    lessons = course.release_lessons()

    if request.user.is_staff:
        lessons = course.lessons.all()

    context = {'course': course,
               'lessons': lessons}

    return render(request, template, context)


@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)

    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Esta aula não está disponível')
        return redirect('/', slug=course.slug)

    template = 'lesson.html'
    context = {'course': course,
               'lesson': lesson}
    
    return render(request, template, context)


@login_required
@enrollment_required
def material(request, slug, lesson_pk, pk):
    course = request.course
    material = get_object_or_404(Material, pk=pk, lesson__course=course)
    lesson = material.lesson

    if not request.user.is_staff and not lesson.is_available():
        messages.error(request, 'Este material não está disponível')
        return redirect('/', slug=course.slug)

    if not material.is_embedded():
        return redirect(material.file.url)

    template = 'material.html'
    context = {'course': course,
               'lesson': lesson,
               'material': material}
    
    return render(request, template, context)
