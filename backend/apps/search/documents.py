from django.contrib.auth import get_user_model
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from apps.course.models import Course

User = get_user_model()


@registry.register_document
class CourseDocument(Document):
    categories = fields.ObjectField(properties={
        'name': fields.TextField(),
    })

    instructor = fields.ObjectField(properties={
        'about_me': fields.TextField(),
    })

    class Index:
        name = 'courses'

    class Django:
        model = Course
        fields = [
            'id',
            'title',
            'description',
        ]