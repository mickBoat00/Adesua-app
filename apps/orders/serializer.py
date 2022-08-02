from rest_framework import serializers

from .models import OrderCourse


class OrderCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCourse
        fields = [
            "id",
            "course",
            "price",
        ]
