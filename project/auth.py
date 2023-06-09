from apps.user.models import CustomUser


class UserAuthentication(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
      

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
