from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    model = CustomUser
    fields = UserCreationForm.Meta.fields + ('user_id',)


class CustomUserChangeForm(UserChangeForm):
    model = CustomUser
    fields = UserChangeForm.Meta.fields

