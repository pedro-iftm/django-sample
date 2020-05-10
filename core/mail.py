from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_mail_template(subject, template_name, context, recipient_list, fail_silently=False,
                       from_=settings.CONTACT_MAIL):
    message_html = render_to_string(template_name, context)
    message = striptags(message_html)

    email = EmailMultiAlternatives(subject=subject, body=message, from_email=from_,
                                   to=list(recipient_list))
    email.attach_alternative(message_html, 'text/html')
    email.send(fail_silently=fail_silently)
