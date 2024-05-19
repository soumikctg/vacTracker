from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from services.helper_functions import EncryptionHelper, NodeAPIClient, random_key, url, generate_jwt_token
from services.models import User, UserVaccineDetails
from services.serializers import UserSerializer
import jwt
from services.aes_cipher import AESCipher


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        data = request.data.copy()
        userId = data.get('userId')
        password = data.get('password')
        phone = data.get('phone')
        nid = data.get('nid')
        address = data.get('address')

        randomKey = random_key()
        base_url = url()

        # Encrypt the data
        encrypted_data = EncryptionHelper.encrypt_data(data, randomKey)
        data.update(encrypted_data)

        # Validate and save the user data
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Handle the external API call to post the user key
        node_api_client = NodeAPIClient(base_url)
        response_data, response_status = node_api_client.post_encryption_key(userId, randomKey)

        return Response(response_data, status=response_status)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        userId = data.get('userId')
        password = data.get('password')

        if not userId or not password:
            raise AuthenticationFailed('Please provide both userId and password')

        user = User.objects.filter(userId=userId).first()

        if not user:
            raise AuthenticationFailed('User not found')

        base_url = url()
        node_api_client = NodeAPIClient(base_url)
        randomKey = node_api_client.get_encryption_key(userId)

        if not randomKey:
            raise AuthenticationFailed('Encryption key not found')

        aes = AESCipher(randomKey)
        decrypted_password = aes.decrypt(user.password)

        if password != decrypted_password:
            raise AuthenticationFailed('Incorrect password')

        token = generate_jwt_token(user.userId)

        response = Response({
            'message': 'You are logged in',
            'jwt': token,
            'userType': user.userType,
        })

        response.set_cookie(key='jwt', value=token)

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'You are logged out'
        }

        return response


class UserDataView(APIView):
    def get(self, request):
        base_url = url()
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')

        user = User.objects.filter(userId=payload['userId']).first()

        if not user:
            raise AuthenticationFailed('User not found')

        node_api_client = NodeAPIClient(base_url)
        try:
            randomKey = node_api_client.get_encryption_key(user.userId)
        except ValueError as e:
            raise AuthenticationFailed(str(e))

        aes = AESCipher(randomKey)

        serializer = UserSerializer(user)
        data = serializer.data.copy()

        # Decrypt fields if they exist
        for field in ['phone', 'nid', 'address']:
            if data.get(field):
                data[field] = aes.decrypt(data[field])

        return Response(data)


class UserVaccineView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')

        user_id = payload.get('userId')
        if not user_id:
            return Response({"message": "Unauthenticated"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch vaccine details using Django ORM
        vaccine_details = UserVaccineDetails.objects.filter(User_id_id=user_id).values('Vaccine_given_date', 'Vaccine_id_id')

        # Mapping for vaccine types
        vaccine_mapping = {
            "BCG1": 0,
            "BCG2": 1,
            "PENTA1": 2,
            "PENTA2": 3,
            "PENTA3": 4,
            "OPV1": 5,
            "OPV2": 6,
            "OPV3": 7,
            "PCV1": 8,
            "PCV2": 9,
            "PCV3": 10,
            "IPV1": 11,
            "IPV2": 12,
            "MR1": 13,
            "MR2": 14,
        }

        vac_date_list = ["Not Given"] * 15

        for detail in vaccine_details:
            vaccine_id = detail["Vaccine_id_id"]
            if vaccine_id in vaccine_mapping:
                index = vaccine_mapping[vaccine_id]
                vac_date_list[index] = detail['Vaccine_given_date']

        data = {
            'vacDateList': vac_date_list
        }
        return Response(data)


class VacInfoWithoutLoginView(APIView):
    def post(self, request):
        user_id = request.data.get('userId')
        if not user_id:
            return Response({"error": "User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, userId=user_id)

        vaccine_details = UserVaccineDetails.objects.filter(User_id_id=user_id).values('Vaccine_given_date', 'Vaccine_id')

        # Mapping for vaccine types
        vaccine_mapping = {
            "BCG1": 0,
            "BCG2": 1,
            "PENTA1": 2,
            "PENTA2": 3,
            "PENTA3": 4,
            "OPV1": 5,
            "OPV2": 6,
            "OPV3": 7,
            "PCV1": 8,
            "PCV2": 9,
            "PCV3": 10,
            "IPV1": 11,
            "IPV2": 12,
            "MR1": 13,
            "MR2": 14,
        }

        vac_date_list = ["Not Given"] * 15

        for detail in vaccine_details:
            vaccine_id = detail['Vaccine_id']
            if vaccine_id in vaccine_mapping:
                index = vaccine_mapping[vaccine_id]
                vac_date_list[index] = detail['Vaccine_given_date']

        response_data = {
            'userId': user.userId,
            'userName': user.name,
            'vacDateList': vac_date_list
        }

        return Response(response_data)


class VaccinatorView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')

        vaccinator_id = payload.get('userId')
        vaccinator = get_object_or_404(User, userId=vaccinator_id)

        if vaccinator.userType != 'vaccinator':
            raise AuthenticationFailed('Unauthenticated')

        user_id = request.data.get('userId')
        user = get_object_or_404(User, userId=user_id)

        vaccine_details = UserVaccineDetails.objects.filter(User_id_id=user_id).values_list('Vaccine_id', flat=True)

        # Mapping for vaccine types
        vaccine_mapping = {
            "BCG1": 0,
            "BCG2": 1,
            "PENTA1": 2,
            "PENTA2": 3,
            "PENTA3": 4,
            "OPV1": 5,
            "OPV2": 6,
            "OPV3": 7,
            "PCV1": 8,
            "PCV2": 9,
            "PCV3": 10,
            "IPV1": 11,
            "IPV2": 12,
            "MR1": 13,
            "MR2": 14,
        }

        boolean_list = [False] * 15
        for vaccine_id in vaccine_details:
            if vaccine_id in vaccine_mapping:
                index = vaccine_mapping[vaccine_id]
                boolean_list[index] = True

        # Fetch encryption key
        base_url = url()
        node_api_client = NodeAPIClient(base_url)
        try:
            random_key = node_api_client.get_encryption_key(user.userId)
        except ValueError as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        aes = AESCipher(random_key)
        phone = user.phone
        if phone:
            phone = aes.decrypt(phone)

        response_data = {
            'userName': user.name,
            'userId': user.userId,
            'phone': phone,
            'boolean_list': boolean_list
        }

        return Response(response_data)


class VacUpdateView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        vaccinator_id = payload.get('userId')
        vaccinator = get_object_or_404(User, userId=vaccinator_id)

        if vaccinator.userType != 'vaccinator':
            raise AuthenticationFailed('Unauthorized access')

        selected_checkboxes = request.data.get('checkboxes')
        user_id = request.data.get('userId')

        if not selected_checkboxes or not user_id:
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

        vaccine_mapping = {
            "BCG1": "BCG1",
            "BCG2": "BCG2",
            "PENTA1": "PENTA1",
            "PENTA2": "PENTA2",
            "PENTA3": "PENTA3",
            "OPV1": "OPV1",
            "OPV2": "OPV2",
            "OPV3": "OPV3",
            "PCV1": "PCV1",
            "PCV2": "PCV2",
            "PCV3": "PCV3",
            "IPV1": "IPV1",
            "IPV2": "IPV2",
            "MR1": "MR1",
            "MR2": "MR2"
        }

        try:
            for val in selected_checkboxes:
                vaccine_id = vaccine_mapping.get(val)
                if vaccine_id:
                    user_vaccine_details, created = UserVaccineDetails.objects.get_or_create(
                        User_id_id=user_id,
                        Vaccine_id_id=vaccine_id,
                        defaults={'Vaccinator_id': vaccinator_id}
                    )
                    if not created:
                        # Optionally, you can handle cases where the record already exists
                        continue

            return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error:", e)
            return Response({"error": "An error occurred while saving data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)