from adesua import celery
from adesua.celery import app
from celery.utils.log import get_task_logger

from .email import send_course_approved_email

logger = get_task_logger(__name__)


@app.task(name="send_course_email")
def send_course_email(course_title, course_instructor, email_message):
    logger.info("Sent Course approved email.")
    return send_course_approved_email(course_title, course_instructor, email_message)
