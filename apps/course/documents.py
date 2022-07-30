from django.contrib.auth import get_user_model
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Course

User = get_user_model()


@registry.register_document
class CourseDocument(Document):
    class Index:
        name = 'courses'

    class Django:
        model = Course
        fields = [
            'id',
            'title',
            'description',
        ]