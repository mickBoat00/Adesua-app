from datetime import datetime
from decimal import Decimal
from math import ceil

from celery import shared_task
from django.db import transaction

from apps.reviewers.tasks import send_course_email
from apps.students.models import CourseEnrollment

from .models import CoursesOnPromotion, Promotion, TrailCourse


@shared_task()
def promotion_prices(reduction_amount, obj_id):
    pass

    # with transaction.atomic():
    #     promotions = Promotion.courses_on_promotion.through.objects.filter(promotion_id=obj_id)
    #     reduction = reduction_amount / 100

    #     for promo in promotions:
    #         if promo.price_override == False:
    #             course_price = promo.course_id.price
    #             new_price = ceil(course_price - (course_price * Decimal(reduction)))
    #             promo.promo_price = Decimal(new_price)
    #             promo.save()


@shared_task()
def activate_user_promotion(promo_id):
    promotion = Promotion.objects.get(id=promo_id, is_schedule=True)
    discount_percentage = promotion.promo_percentage / 100
    discount_amount = promotion.promo_amount

    now = datetime.now().date()

    if promotion.promo_end < now:
        promotion.is_active = False
        promotion.is_schedule = False

    else:
        if promotion.promo_start <= now:
            if promotion.is_active != True:

                courses_on_promo = promotion.courses_on_promotion.through.objects.all()

                for course in courses_on_promo:
                    if course.price_override == False:
                        course_price = course.course_id.price

                        if discount_percentage > 0:
                            new_price = ceil(course_price - (course_price * Decimal(discount_percentage)))
                        elif discount_amount > 0:
                            new_price = course_price - discount_amount
                        else:
                            new_price = 0

                        course.promo_price = Decimal(new_price)
                        course.save()

                promotion.is_active = True

        else:
            promotion.is_active = False

    promotion.save()


"""
    PROMOTION ACTIVATION PSEUDOCODE


    get all promotions on schedule

    for each promotion:
        if end_date < now:
            set promotion is_active to false 
            # cos its done its work 

            
            course in that promo's promo_price should be set to null
            # those course will be activated by another promo if they are in that promo

            promo. is_schedule set to false
            # so its not queried again


        else:
            # means promotion.end_date is not yet up

            if promotion.start_date <= now:
                # activate it
                get all courses in that promotion

                get promotion reduction % or promotion reduction amount

                for each course in promotion:
                    get it orginal price

                    calculate each courses promo_price based on orginal price and promotion reduction

                    save course promo_price

            else:
                # means now is days/minutes into the start of the promo
                # do we have to do something ?
                # no

            promotion set to active
        
        save promo
            
"""


@shared_task()
def promotion_management():
    with transaction.atomic():
        promotions = Promotion.objects.filter(is_schedule=True)

        now = datetime.now().date()

        for promo in promotions:
            discount_percentage = promo.promo_percentage / 100
            discount_amount = promo.promo_amount

            if promo.promo_end < now:
                promo.is_active = False
                promo.is_schedule = False
            else:
                if promo.promo_start <= now:
                    if promo.is_active != True:

                        courses_on_promo = promo.courses_on_promotion.through.objects.all()

                        for course in courses_on_promo:
                            if course.price_override == False:
                                course_price = course.course_id.price

                                if discount_percentage > 0:
                                    new_price = ceil(course_price - (course_price * Decimal(discount_percentage)))
                                elif discount_amount > 0:
                                    new_price = course_price - discount_amount
                                else:
                                    new_price = 0

                                course.promo_price = Decimal(new_price)
                                course.save()

                        promo.is_active = True

                else:
                    promo.is_active = False

            promo.save()


"""

    TRAIL ACTIVATION PSEUDOCODE

    Get all trails on schedule

    for each trail :

        if trail.end_date < now:
            set on_trail for its courses to False 
            set trail to inactive
            set trail.is_schedule to false
        else:
            if trail start_date <= now:
                get all courses in that trail

                for each course:
                    set on_trail for its courses to True
                    save course

            set trail to active

        save trail

"""


@shared_task
def activate_free_trail():
    with transaction.atomic():
        trails = TrailCourse.objects.filter(is_scheduled=True)

        now = datetime.now().date()

        for trail in trails:
            courses_on_trail = trail.courses_on_trail.through.objects.all()

            if trail.end_date < now:
                print("task ends")
                for course in courses_on_trail:
                    course.on_trail = False
                    course.save()
                    print("end course", course)
                    print("ssaaa", course.course_id)

                    course = course.course.id

                    courseEnrollment = CourseEnrollment.objects.get(course=course, course_on_free_trail=True)

                    student = courseEnrollment.student.email

                    send_course_email.delay(
                        courseEnrollment.student.course_id.title,
                        courseEnrollment.student.email,
                        "trial_ended_email_message.txt",
                    )

                    # course = course.course_id

                    # course.enrollments.all()

                    """
                        Send an email to the person enrolled in a course
                        that the free trail has ended.

                        Prevent access to course lessons

                    """

                trail.is_active = False
                trail.is_scheduled = False

            else:
                print("task not ended")
                if trail.start_date <= now:
                    print("task here")

                    for course in courses_on_trail:
                        course.on_trail = True
                        course.save()

                    trail.is_active = True

                print("task here last")

            trail.save()
