from datetime import datetime
from decimal import Decimal
from math import ceil

from celery import shared_task
from django.db import transaction

from .models import CoursesOnPromotion, Promotion


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
