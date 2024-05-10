from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from services.models import User
from services.serializers import UserSerializer
import jwt, datetime


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        phone = request.data['phone']
        password = request.data['password']

        user = User.objects.filter(phone=phone).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'userId': user.userId,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
            'iat': datetime.datetime.now(datetime.UTC),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        decode = jwt.decode(token, 'secret', algorithms=['HS256'])

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'message': 'You are logged in',
            'jwt': token,
        }

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')

        user = User.objects.filter(userId=payload['userId']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'You are logged out'
        }

        return response