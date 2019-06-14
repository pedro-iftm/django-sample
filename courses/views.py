from django.shortcuts import render, get_object_or_404
from courses.models import Course
from .forms import ContactCourse


def courses(request):
    TEMPLATE_COURSES = 'courses.html'

    courses = Course.objects.all()
    context = {'courses': courses}
    
    return render(request, TEMPLATE_COURSES, context)


def details(request, slug):
    TEMPLATE_DETAILS = 'details.html'

    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            print(form.cleaned_data['name'])
            #PAREI AQ
            # como esvaziar o form dps de clicar em enviar
            # o que fazer com esse isvalid?
    else:
        form = ContactCourse()
    

    course = get_object_or_404(Course, slug=slug)
    context = {
        'course': course,
        'form': form
    }

    return render(request, TEMPLATE_DETAILS, context)