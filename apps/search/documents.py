from django.contrib.auth import get_user_model
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from apps.course.models import Course, Curriculum, Year
from apps.users.models import CourseInstructor

User = get_user_model()


@registry.register_document
class CourseInstructorDocument(Document):

    class Index:
        name = 'course_instructors'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = CourseInstructor
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]



@registry.register_document
class CourseDocument(Document):
    curriculum = fields.ObjectField(properties={
        'name': fields.TextField(),
    })

    year = fields.ObjectField(properties={
        'value': fields.TextField(),
    })

    instructor = fields.ObjectField(properties={
        'username': fields.TextField(),
        'first_name': fields.TextField(),
        'last_name': fields.TextField(),
    })

    class Index:
        name = 'courses'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Course
        fields = [
            'id',
            'title',
            'description',            
        ]


