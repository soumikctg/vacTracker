import base64
import secrets
import requests
from rest_framework import status

from services.aes_cipher import AESCipher
import jwt, datetime


def random_key(length=32):
    return base64.b64encode(secrets.token_bytes(length)).decode('utf-8')


def url():
    base_url = "http://localhost:8080/"
    # base_url = "https://5tk88679-8080.inc1.devtunnels.ms/"
    return base_url


def generate_jwt_token(userId):
    payload = {
        'userId': userId,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
        'iat': datetime.datetime.now(datetime.timezone.utc),
    }
    return jwt.encode(payload, 'secret', algorithm='HS256')


class EncryptionHelper:
    @staticmethod
    def encrypt_data(data, key):
        aes = AESCipher(key)
        encrypted_data = {}
        for field in ['password', 'phone', 'nid', 'address']:
            if data.get(field):
                encrypted_data[field] = aes.encrypt(data[field])
        return encrypted_data


class NodeAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def post_encryption_key(self, userId, key):
        node_api_url = f'{self.base_url}users/create-user-keys'
        node_api_data = {
            'uid': userId,
            'key': key
        }

        try:
            response = requests.post(node_api_url, json=node_api_data)
            response.raise_for_status()
            return {'message': 'Key saved successfully.'}, status.HTTP_201_CREATED
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

    def get_encryption_key(self, userId):
        """Fetch encryption key from the API."""
        node_api_url = f'{self.base_url}users/get-keys-by-uid/{userId}'

        try:
            response = requests.get(node_api_url)
            response.raise_for_status()
            res = response.json()
            return res['data']['key']
        except requests.exceptions.RequestException as e:
            raise ValueError(f'Error fetching encryption key: {e}')
