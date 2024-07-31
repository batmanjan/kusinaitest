# yourappname/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

class PhoneOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, phone_number=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            if username:
                user = UserModel.objects.get(username=username)
            elif phone_number:
                user = UserModel.objects.get(phone_number=phone_number)
            else:
                return None

            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
