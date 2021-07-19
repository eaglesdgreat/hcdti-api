
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from setup.settings import EMAIL_FROM
from django.core.mail import EmailMultiAlternatives


class Email:
    def welcome(self, email, staffname, password):
        subject, from_email, to = 'Welcome', EMAIL_FROM, email
        html_content = render_to_string(
            'email/welcome.html', {'staffname': staffname, 'email': email, 'password': password})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        pass

    def otp(self, email, otp, staffname):
        subject, from_email, to = 'OTP', EMAIL_FROM, email
        html_content = render_to_string(
            'email/otp.html', {'staffname': staffname, 'otp': otp})
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        pass
