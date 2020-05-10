from django.core.mail import send_mail
from django import forms
from django.conf import settings

# from core.mail import send_mail_template


class ContactCourse(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea)

    def send_mail(self, course):
        subject = f'Dúvida sobre o curso {course}'
        message = self.cleaned_data['message']
        from_ = self.cleaned_data['email']
        to = [settings.CONTACT_MAIL]
        send_mail(subject, message, from_, to)

        # template_name = 'contact_email.html'
        # send_mail_template(subject, template_name, message, from_, [to])

        