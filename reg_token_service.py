from itsdangerous import URLSafeTimedSerializer
from properties import *

'''
    Service to generate and validate authorization tokens
'''


def generate_reg_token(email):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email


def _example():
    token = generate_reg_token("szlaci83@gmail.com")
    print("Token: " + token)
    email = confirm_token(token)
    print("Email: " + email)


if __name__ == "__main__":
    _example()
