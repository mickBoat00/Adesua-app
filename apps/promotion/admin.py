from django.contrib import admin

from .models import (
    Coupon,
    CoursesOnPromotion,
    CoursesOnTrail,
    Promotion,
    PromoType,
    TrailCourse,
    UserPromotion,
)

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


class CoursesOnTrailAdmin(admin.StackedInline):
    model = TrailCourse.courses_on_trail.through
    extra = 2


class TrailCourseAdmin(admin.ModelAdmin):
    list_display = ["name", "start_date", "end_date", "is_active", "is_scheduled"]
    inlines = (CoursesOnTrailAdmin,)


admin.site.register(TrailCourse, TrailCourseAdmin)
admin.site.register(CoursesOnTrail)
