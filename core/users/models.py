from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator


class CustomUser(AbstractUser):
    rules = models.BooleanField(
        "согласен с правилами",
        default=False,
        blank=False,
    )

    first_name = models.CharField(
        "имя",
        max_length=150,
        blank=False,
        validators=[
            RegexValidator(
                r"^[А-Яа-яЁё\s-]+$",
                message="Имя может содержать только русские буквы, пробелы и дефисы",
            ),
        ],
    )

    last_name = models.CharField(
        "фамилия",
        max_length=150,
        blank=False,
        validators=[
            RegexValidator(
                r"^[А-Яа-яЁё\s-]+$",
                message="Фамилия может содержать только русские буквы, пробелы и дефисы",
            ),
        ],
    )

    patronymic = models.CharField(
        "отчество",
        max_length=150,
        blank=True,
        validators=[
            RegexValidator(
                r"^[А-Яа-яЁё\s-]+$",
                message="Отчество может содержать только русские буквы, пробелы и дефисы",
            ),
        ],
    )
    username = models.CharField(
        "логин",
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                r"^[\w\d-]+$",
                message="Логин может содержать только русские буквы, пробелы и дефисы",
            ),
        ],
        error_messages={
            "unique": "Пользователь с таким логином уже существует.",
        },
    )

    email = models.EmailField(
        "электронная почта",
        unique=True,
        blank=False,
        error_messages={
            "unique": "Пользователь с такой почтой уже существует.",
        },
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.username

# securepassword123