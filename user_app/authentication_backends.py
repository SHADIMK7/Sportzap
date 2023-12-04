from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            # Check if the given username is an email address
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # If the username is not an email, try to get the user by username
            user = UserModel.objects.get(Phone_no=username)

        # Check the password against the user's password
        if user.check_password(password):
            return user
        else:
            return None
