from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.filter(email=username).first()
        except UserModel.DoesNotExist:
            # If the username is not an email, try to get the user by username
            user = UserModel.objects.filter(phone_no=username).first()

            if user.check_password(password):
                return user
            else:
                return None
