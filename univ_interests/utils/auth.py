from functools import wraps

import jwt

from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED


def login_required(func):
    @wraps(func)
    def decorated(self, request):
        access_token = request.headers.get('Authorization', None)
        if access_token is None:
            return Response({'detail': 'Invalid Token'}, status=HTTP_401_UNAUTHORIZED)
        else:
            try:
                payload = jwt.decode(access_token, 'SECRET', 'HS256')
            except jwt.InvalidTokenError:
                return Response({'detail': 'Invalid Token'}, status=HTTP_401_UNAUTHORIZED)
        return func(self, request, user=payload)
    return decorated
