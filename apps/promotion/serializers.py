from email.policy import default

from rest_framework import serializers

from apps.course.models import Course

from .models import CoursesOnPromotion, Promotion, TrialCourse, UserPromotion


class PromotionsSerializers(serializers.ModelSerializer):

    courses_on_promotion = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Course.objects.all(),
    )

    created_by = serializers.CharField(source="created_by.username", read_only=True)

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
        read_only_fields = [
            "is_active",
            "created_by",
        ]


class UserPromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPromotion
        fields = [
            "student",
            "promotion",
        ]


class CoursesOnTrailSerializer(serializers.ModelSerializer):
    courses_on_trail = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Course.objects.all(),
    )

    class Meta:
        model = TrialCourse
        fields = [
            "name",
            "description",
            "start_date",
            "end_date",
            "is_active",
            "is_scheduled",
            "courses_on_trail",
        ]
