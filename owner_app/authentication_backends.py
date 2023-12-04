from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # If the username is not an email, try to get the user by username
            user = UserModel.objects.get(phone_no=username)

        if user.check_password(password):
            return user
        else:
            return None
