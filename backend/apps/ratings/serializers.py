from rest_framework import serializers

from .models import Rating


class RatingReadSerializer(serializers.ModelSerializer):
    course = serializers.CharField(source="course.title")
    rater = serializers.CharField(source="rater.username")

    class Meta:
        model = Rating
        fields = [
            "id",
            "course",
            "rater",
            "rating",
            "comment",
        ]

        read_only_fields = fields


class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            "rating",
            "comment",
        ]
