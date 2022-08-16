from datetime import datetime
from decimal import Decimal
from math import ceil

from celery import shared_task
from django.db import transaction

from .models import CoursesOnPromotion, Promotion


@shared_task()
def promotion_prices(reduction_amount, obj_id):

    with transaction.atomic():
        promotions = Promotion.courses_on_promotion.through.objects.filter(promotion_id=obj_id)
        reduction = reduction_amount / 100

        for promo in promotions:
            if promo.price_override == False:
                course_price = promo.course_id.price
                new_price = ceil(course_price - (course_price * Decimal(reduction)))
                promo.promo_price = Decimal(new_price)
                promo.save()


@shared_task()
def promotion_management():
    with transaction.atomic():
        promotions = Promotion.objects.filter(is_schedule=True)

        now = datetime.now().date()

        for promo in promotions:
            if promo.is_schedule:
                if promo.promo_end < now:
                    promo.is_active = False
                    promo.is_schedule = False
                else:
                    if promo.promo_start <= now:
                        promo.is_active = True
                    else:
                        promo.is_active = False
                promo.save()
