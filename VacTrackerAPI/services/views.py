from django.db import connection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from services.models import User, UserVaccineDetails
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

        response.set_cookie(key='jwt', value=token)

        response.data = {
            'message': 'You are logged in',
            'jwt': token,
            'userType': user.userType,
        }

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


class UserVaccineView(APIView):
    def get(self, request):

        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')

        user_id = payload['userId']
        if not user_id:
            return Response({"message": "UnAuthenticated"}, status=status.HTTP_400_BAD_REQUEST)

        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT Vaccine_given_date, Vaccine_id_id FROM services_uservaccinedetails WHERE User_id_id = %s',
                [user_id]
            )

            vac = cursor.fetchall()

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

        for val in vac:
            vaccine_id = val[1]
            if vaccine_id in vaccine_mapping:
                index = vaccine_mapping[vaccine_id]
                vac_date_list[index] = val[0]
        data = {
            'vacDateList': vac_date_list
        }
        return Response(data)


class VacInfoWithoutLoginView(APIView):
    def post(self, request):
        userid = request.data['userId']
        user = get_object_or_404(User, userId=userid)
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT Vaccine_given_date, Vaccine_id_id FROM services_uservaccinedetails WHERE User_id_id = %s',
                [userid]
            )
            vac = cursor.fetchall()

        vac_date_list = ["Not Given"] * 15
        for val in vac:
            if (val[1] == "BCG1"):
                vac_date_list[0] = val[0]
            elif (val[1] == "BCG2"):
                vac_date_list[1] = val[0]
            elif (val[1] == "PENTA1"):
                vac_date_list[2] = val[0]
            elif (val[1] == "PENTA2"):
                vac_date_list[3] = val[0]
            elif (val[1] == "PENTA3"):
                vac_date_list[4] = val[0]
            elif (val[1] == "OPV1"):
                vac_date_list[5] = val[0]
            elif (val[1] == "OPV2"):
                vac_date_list[6] = val[0]
            elif (val[1] == "OPV3"):
                vac_date_list[7] = val[0]
            elif (val[1] == "PCV1"):
                vac_date_list[8] = val[0]
            elif (val[1] == "PCV2"):
                vac_date_list[9] = val[0]
            elif (val[1] == "PCV3"):
                vac_date_list[10] = val[0]
            elif (val[1] == "IPV1"):
                vac_date_list[11] = val[0]
            elif (val[1] == "IPV2"):
                vac_date_list[12] = val[0]
            elif (val[1] == "MR1"):
                vac_date_list[13] = val[0]
            elif (val[1] == "MR2"):
                vac_date_list[14] = val[0]

        response = Response()
        response.data = {
            'userId': user.userId,
            'userName': user.name,
            'vacDateList': vac_date_list
        }

        return response


class VaccinatorView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')
        try:
            vaccinatorid = payload['userId']
            vaccinator = get_object_or_404(User, userId=vaccinatorid)
            if vaccinator.userType == 'vaccinator':
                userid = request.data['userId']
                user = get_object_or_404(User, userId=userid)
                with connection.cursor() as cursor:
                    cursor.execute('SELECT Vaccine_id_id FROM services_uservaccinedetails WHERE User_id_id = %s',
                                   [userid])
                    vac = cursor.fetchall()
                    boolean_list1 = [False] * 15
                    for val in vac:
                        if (val[0] == "BCG1"):
                            boolean_list1[0] = True
                        elif (val[0] == "BCG2"):
                            boolean_list1[1] = True
                        elif (val[0] == "PENTA1"):
                            boolean_list1[2] = True
                        elif (val[0] == "PENTA2"):
                            boolean_list1[3] = True
                        elif (val[0] == "PENTA3"):
                            boolean_list1[4] = True
                        elif (val[0] == "OPV1"):
                            boolean_list1[5] = True
                        elif (val[0] == "OPV2"):
                            boolean_list1[6] = True
                        elif (val[0] == "OPV3"):
                            boolean_list1[7] = True
                        elif (val[0] == "PCV1"):
                            boolean_list1[8] = True
                        elif (val[0] == "PCV2"):
                            boolean_list1[9] = True
                        elif (val[0] == "PCV3"):
                            boolean_list1[10] = True
                        elif (val[0] == "IPV1"):
                            boolean_list1[11] = True
                        elif (val[0] == "IPV2"):
                            boolean_list1[12] = True
                        elif (val[0] == "MR1"):
                            boolean_list1[13] = True
                        elif (val[0] == "MR2"):
                            boolean_list1[14] = True

                    response = Response()
                    response.data = {
                        'userName': user.name,
                        'userId': user.userId,
                        'phone': user.phone,
                        'boolean_list': boolean_list1
                    }
                    return response

            else:
                raise AuthenticationFailed('Unauthenticated')

        except Exception as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VacUpdateView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        if token is None:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Invalid token')
        try:
            vaccinatorid = payload['userId']
            vaccinator = get_object_or_404(User, userId=vaccinatorid)
            if vaccinator.userType == 'vaccinator':
                selected_checkboxes = request.data['checkboxes']
                userid = request.data['userId']

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

                for val in selected_checkboxes:
                    if val in vaccine_mapping:
                        vaccineid = vaccine_mapping[val]
                        user_vaccine_details = UserVaccineDetails.objects.filter(User_id_id=userid,
                                                                                 Vaccine_id_id=vaccineid)
                        if not user_vaccine_details.exists():
                            new_record = UserVaccineDetails(Vaccinator_id=vaccinatorid, User_id_id=userid, Vaccine_id_id=vaccineid)
                            new_record.save()

                return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
            else:
                raise AuthenticationFailed('Unauthenticated')

        except Exception as e:
            print("Error:", e)
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
