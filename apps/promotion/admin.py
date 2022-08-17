from django.contrib import admin

from .models import (
    Coupon,
    CoursesOnPromotion,
    Promotion,
    PromoType,
    TrailCourse,
    UserPromotion,
)
from .tasks import promotion_management, promotion_prices

admin.site.register(PromoType)

admin.site.register(CoursesOnPromotion)


class CoursesOnPromotionAdmin(admin.StackedInline):
    model = Promotion.courses_on_promotion.through
    extra = 4


class PromotionAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active", "promo_start", "promo_end"]
    inlines = (CoursesOnPromotionAdmin,)


admin.site.register(Promotion, PromotionAdmin)
admin.site.register(Coupon)
admin.site.register(UserPromotion)
admin.site.register(TrailCourse)
