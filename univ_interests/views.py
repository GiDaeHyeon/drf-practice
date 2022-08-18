import ast

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    SignUpSerializer,
    SignInSerializer,
    UniversitySearchSerializer,
    UniversityPreferenceSerializer
)
from .models import User, University, UniversityPreference
from .utils.auth import login_required


class SignUpView(APIView):
    def put(self, request, **kwargs):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.create(validated_data=serializer.validated_data)
            return Response({'detail': 'success', 'user_data': user}, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def get(self, request, **kwargs):
        serializer = SignInSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'detail': serializer.errors},
                            status=HTTP_400_BAD_REQUEST)
        else:
            email = request.data.get('email')
            input_password = request.data.get('password')

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'detail': '아이디와 비밀번호를 확인해주세요.'},
                                status=HTTP_400_BAD_REQUEST)

            token = serializer.login(user=user, input_password=input_password)

            if token:
                return Response({'detail': 'success', 'token': token},
                                status=HTTP_200_OK, headers={'Authorization': token})
            else:
                return Response({'detail': '아이디와 비밀번호를 확인해주세요.'},
                                status=HTTP_400_BAD_REQUEST)


class UniversitySearchView(ListAPIView):

    class UniversityPagination(PageNumberPagination):
        page_size_query_param = 'page_size'
        page_query_param = 'page'

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


class UniversityPreferenceCreateView(APIView):
    @login_required
    def put(self, request, **kwargs):
        user_id = kwargs.get('user').get('user_id')
        user = User.objects.get(id=user_id)
        serializer = UniversityPreferenceSerializer(data=request.data)

        if serializer.is_valid():
            preference_list = UniversityPreference.objects.filter(user=user)

            if len(preference_list) >= 20:
                return Response({'detail': '선호대학은 20개를 초과할 수 없습니다.'},
                                status=HTTP_400_BAD_REQUEST)

            preference = serializer.create(user=user)

            if preference:
                return Response(preference, status=HTTP_201_CREATED)
            else:
                return Response({"detail": "Integrity Error"}, status=HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UniversityPreferenceDeleteView(APIView):
    @login_required
    def delete(self, request, **kwargs):
        user_id = kwargs.get('user').get('user_id')
        user = User.objects.get(id=user_id)
        serializer = UniversityPreferenceSerializer(data=request.data)

        if serializer.is_valid():
            is_updated = serializer.update(user=user)
            if is_updated:
                return Response({'detail': 'success'}, status=HTTP_200_OK)
            else:
                return Response({'detail': 'Not Exist'}, status=HTTP_400_BAD_REQUEST)


class UniversityRankingView(APIView):
    @login_required
    def get(self, request, **kwargs):
        query = """
            SELECT
              u.name AS name,
              u.id AS id,
              COUNT(DISTINCT u.country_id) + COUNT(up.university_id) AS score
            FROM
              university_preference AS up
              JOIN university AS u ON u.id = up.university_id
            GROUP BY
              u.name, u.id
            ORDER BY
              3 DESC, 2 ASC
            LIMIT 10;
        """
        queryset = UniversityPreference.objects.raw(query)
        results = [{'id': q.id, 'name': q.name, 'score': q.score} for q in queryset]
        return Response({'detail': 'success', 'results': results}, status=HTTP_200_OK)
