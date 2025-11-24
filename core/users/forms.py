from django.forms import ModelForm, CharField, PasswordInput, BooleanField
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinLengthValidator

from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    password1 = CharField(
        label="Пароль",
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "new-password"}),
        validators=[MinLengthValidator(6)]
    )
    rules = BooleanField(
        label="Я согласен с правилами",
        # required=True,
        error_messages={'required': 'Вы должны согласиться с правилами'}
    )
    class Meta():
        model = CustomUser
        fields = ["first_name", "last_name", "patronymic", "username", "email", "password1", "password2", "rules"]