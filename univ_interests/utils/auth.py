from functools import wraps

import jwt
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from DRFPractice.settings import SECRET_KEY


def login_required(func):
    @wraps(func)
    def decorated(self, *args, **kwargs):
        request = self.request
        access_token = request.headers.get('Authorization', None)
        if access_token is None:
            return Response({'detail': 'InvalidToken'}, status=HTTP_401_UNAUTHORIZED)
        else:
            try:
                payload = jwt.decode(access_token, SECRET_KEY, 'HS256')
            except jwt.InvalidTokenError:
                return Response({'detail': 'InvalidToken'}, status=HTTP_401_UNAUTHORIZED)
        return func(self, *args, **kwargs, user=payload)
    return decorated
