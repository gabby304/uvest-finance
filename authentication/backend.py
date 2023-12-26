from typing import Any
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest 

class EmailBackend(ModelBackend):
    
    def authenticate(self, request: HttpRequest, username: str=None, password: str=None, **kwargs: Any) -> AbstractBaseUser:
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None 
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user 
        
    def get_user(self, user_id: int) -> AbstractBaseUser:
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None 
        else:
            return user if self.user_can_authenticate(user) else None 