import ast

from .serializers import SignUpSerializer, SignInSerializer, UniversitySearchSerializer
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN)
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import User, University
from .utils.auth import login_required


class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.create(validated_data=serializer.validated_data)
            return Response({'detail': 'success', 'user_data': user}, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def post(self, request):
        serializer = SignInSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'detail': serializer.errors},
                            status=HTTP_400_BAD_REQUEST)
        else:
            email = request.data.get('email')
            input_password = request.data.get('password')
            user = User.objects.get(email=email)
            token = serializer.login(user=user, input_password=input_password)

            if token:
                return Response({'detail': 'success', 'token': token},
                                status=HTTP_200_OK, headers={'Authorization': token})
            else:
                return Response({'detail': '아이디와 비밀번호를 확인해주세요'},
                                status=HTTP_403_FORBIDDEN)


class UniversityPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class UniversitySearchView(ListAPIView):
    serializer_class = UniversitySearchSerializer
    pagination_class = UniversityPagination

    @login_required
    def get_queryset(self, **kwargs):
        univ_name = self.request.query_params.get('name', None)
        country_code = self.request.query_params.get('country_code', None)

        query_param = {}
        if univ_name is not None:
            query_param['name__icontains'] = univ_name
        if country_code is not None:
            query_param['country__code__in'] = ast.literal_eval(country_code)

        queryset = University.objects.filter(**query_param).order_by('id')
        return queryset
