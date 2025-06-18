import jwt
import datetime


def build_token():
    """
    Generates the authorization token
    :return: authorization token
    """
    payload = {
        'user_id': 1,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, secret, algorithm='HS256')


def decode_token(token):
    """
    Decodes the authorization token
    :param token:
    :return:
    """
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


# Change this secret to something unique for your group
secret = "quiz-app-secret-group-unique-key"