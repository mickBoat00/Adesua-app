from django.http import HttpResponse

from rest_framework.views import APIView

from apps.course.serializers import CourseSearchSerializer

from elasticsearch_dsl import Q

from .documents import CourseDocument

from rest_framework.pagination import LimitOffsetPagination



class SearchCourse(APIView, LimitOffsetPagination):
    course_serializer = CourseSearchSerializer
    search_document = CourseDocument

    def get(self, request, query):
        try:
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'title',
                    'description',
                ],
                fuzziness='auto'
            )

            search = self.search_document.search().query(q)
            response = search.execute()

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.course_serializer(results, many=True)

            return self.get_paginated_response(serializer.data)

        except Exception as e:
            return HttpResponse(e, status=500)
