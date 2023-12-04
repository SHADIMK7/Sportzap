from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
<<<<<<< HEAD
            # If the username is not an email, try to get the user by username
            user = UserModel.objects.get(phone_no=username)
=======
            user = UserModel.objects.get(username=username)
>>>>>>> 96d3b44411a3984f002cd2ac26039bf3985f2e92

        if user.check_password(password):
            return user
        else:
            return None
