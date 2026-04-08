from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class PhoneBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):

        phone = kwargs.get("telephone") or username

        try:
            user = User.objects.get(telephone=phone)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None