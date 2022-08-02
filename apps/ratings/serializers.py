from rest_framework import serializers

from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    # rater = serializers.SerializerMethodField()
    # course = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = [
            "course",
            "rating",
            "comment",
        ]

    def get_rater(self, obj):
        return obj.rater.user.username

    def get_agent(self, obj):
        return obj.title
