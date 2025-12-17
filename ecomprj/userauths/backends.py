from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to login with email or username.
    Supports case-insensitive email lookup.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None

        try:
            # Try to fetch the user by email first (case-insensitive)
            user = User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            try:
                # If not found by email, try by username (case-sensitive)
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Run the default password hasher once to reduce timing attack
                User().set_password(password)
                return None

        # Check the password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
