import uuid

from royal.users.models import BaseUser

def get_jwt_scrt_key(user:BaseUser) -> str:
    return str(user.jwt_key)

def auth_jwt_response_payload_handler(token, user=None, request=None, issued_at=None):
    if user:
        return{
            "token": token,
            "user": {
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            "issued_at": issued_at
        }

    return {"token": token}

def auth_logout(user:BaseUser) -> BaseUser:
    user.jwt_key = uuid.uuid4()
    user.full_clean()
    user.save(update_fields=["jwt_key"])

    return user