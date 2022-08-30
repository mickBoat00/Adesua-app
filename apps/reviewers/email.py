from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_course_approved_email(course_title, course_instructor, email_message):
    context = {
        "course_name": course_title,
        "course_instructor": course_instructor,
    }

    email_subject = "Course approved"
    # email_body = render_to_string("email_message.txt", context)
    email_body = render_to_string(email_message, context)

    email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [
            course_instructor,
        ],
    )
    return email.send(fail_silently=False)
