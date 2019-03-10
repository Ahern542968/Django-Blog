from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

User = get_user_model()


class UserAuthBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """
        always return True, so we can control is_active by if email is active
        """
        return True
