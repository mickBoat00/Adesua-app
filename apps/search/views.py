from django.http import HttpResponse

from rest_framework.views import APIView

from apps.course.serializers import CourseSearchSerializer

from elasticsearch_dsl import Q

from .documents import CourseDocument, CourseInstructorDocument

from rest_framework.pagination import PageNumberPagination


class SearchCourse(APIView, PageNumberPagination):
    course_serializer = CourseSearchSerializer
    search_document = CourseDocument

    def generate_q_expression(self, query):
        return Q(
            'multi_match',
            query=query,
            fields=[
                'curriculum.name',
                'year.value',
                'title',
                'instructor.username',
                'instructor.first_name',
                'instructor.last_name',
            ],
            fuzziness='auto'
        ) & Q(
            should=[
                Q("match", published_status=True),
                Q("match", status="Approved"),
            ], minimum_should_match=1
        )

    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)

            search = self.search_document.search().query(q)
            response = search.execute()

            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.course_serializer(results, many=True)

            return self.get_paginated_response(serializer.data)

        except Exception as e:
            return HttpResponse(e, status=500)
