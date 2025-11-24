from django.db import models
from django.core.validators import validate_image_file_extension, MinValueValidator, MaxValueValidator
from django.utils import timezone

from autoslug import AutoSlugField

from users.models import CustomUser


def product_image_path(instance, filename):
    return f'products/{filename}'


class Category(models.Model):
    title = models.CharField(
        "название",
        max_length=99,
        unique=True  # чтобы названия не повторялись
    )
    slug = AutoSlugField(
        "слаг",
        populate_from="title",
        unique=True,
        editable=True,      # можно редактировать вручную
        always_update=True, # автоматически обновляется при изменении title
        blank=True,
    )

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    image = models.ImageField(
        "картинка",
        upload_to=product_image_path,
        validators=[
            validate_image_file_extension,
        ]
    )
    title = models.CharField(
        "название",
        max_length=99,
    )
    model = models.CharField(
        "модель",
        max_length=99,
        blank=True,
    )
    year_of_production = models.PositiveIntegerField(
        "год производства",
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(timezone.now().year + 1)
        ],
        blank=True,
        null=True,
    )
    production_country = models.CharField(
        "страна производства",
        max_length=100,
        blank=True,
    )
    price = models.PositiveIntegerField(
        "цена",
        validators=[MinValueValidator(1)],
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="категория",
        related_name="products"
    )
    count_available = models.PositiveIntegerField(
        "количество в наличии",
        default=0,
    )
    created_at = models.DateTimeField(
        "дата создания",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    

class Basket(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="basket"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="товар",
        related_name="basket_items",
    )
    quantity = models.PositiveIntegerField(
        "количество товара в корзине",
        default=1,
        validators=[MinValueValidator(1)]
    )
    added_at = models.DateTimeField(
        "дата добавления",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "корзина"
        verbose_name_plural = "корзины"
        unique_together = ['user', 'product']
        ordering = ['-added_at']

    def __str__(self):
        return f"Корзина {self.user.username}: {self.product.title}, {self.quantity} шт. - {self.get_total_price()}"
    
    def get_total_price(self):
        return self.quantity * self.product.price