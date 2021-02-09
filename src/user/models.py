from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import jwt

# class UserProfile(models.Model):
#     """Database model for users"""
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     # USERNAME_FIELD = 'user.name'
#     # REQUIRED_FIELDS = ['user.email']

class User(AbstractUser):
    username = models.CharField(max_length = 40, unique = True)
    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')