from email.policy import default

from rest_framework import serializers

from apps.course.models import Course

from .models import CoursesOnPromotion, Promotion


class PromotionsSerializers(serializers.ModelSerializer):

    courses_on_promotion = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Course.objects.all(),
    )

    class Meta:
        model = Promotion
        fields = [
            "id",
            "name",
            "description",
            "promo_percentage",
            "promo_amount",
            "is_schedule",
            "is_active",
            "promo_start",
            "promo_end",
            "promo_type",
            "courses_on_promotion",
            "created_by",
        ]
        read_only_fields = ["is_active", "created_by"]
