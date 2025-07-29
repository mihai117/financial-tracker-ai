from django.contrib.auth.backends import BaseBackend  #django base class for authentication logic
from django.contrib.auth import get_user_model # when called returns the User class Django is using
from firebase_admin import auth as firebase_auth #renamed auth from firebase_admin for clarity
from firebase_admin.exceptions import FirebaseError

User = get_user_model()

class FirebaseAuthBackend(BaseBackend):     # subclass for the firebase authentication in the base class

    def authenticate(self, request, id_token=None):
        if not id_token:
            return None

        try:
            decoded = firebase_auth.verify_id_token(id_token)
        except (ValueError, FirebaseError):
            return None

        uid = decoded.get('uid')
        email = decoded.get('email')

        user, _ = User.objects.get_or_create(
            username=uid,
            defaults={'email': email or ''}
        )

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)  # function retrieves user from the data base using user ID as primary key
        except User.DoesNotExist:
            return None