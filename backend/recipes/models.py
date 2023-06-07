from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Ингредиенты для рецепта."""
    name = models.CharField(
        blank=False,
        max_length=150,
        db_index=True,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=150,
        verbose_name='Единицы измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """Тэги для рецептов."""
    name = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text='Введите название тега',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Color (HEX code)',
        help_text='Цветовой HEX-код например, #49B64E'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text='Адрес для странице в браузере'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Название рецепта',
        help_text='Название рецепта'
    )
    image = models.ImageField(
        blank=True,
        upload_to='recipes/images/',
        help_text='Фото блюда',
        verbose_name='Фото'
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='QuantityIngredient',
        related_name='recipes',
        verbose_name='Список ингредиентов',
        help_text='Выберите ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег',
        help_text='Выберите тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах',
        validators=[MinValueValidator(
            1, 'Минимальное время приготовления - 1 минута')],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )


    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class QuantityIngredient(models.Model):
    """Количество ингредиентов в рецепте."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='quantity_ingredients',
        verbose_name='Ингридиент',
        help_text='Выберите ингредиенты'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='quantity_ingredients',
        verbose_name='Рецепт'
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(
            1, 'Минимальное количество ингридеентов - 1')],
        default=1,
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe'),
                name='unique_ingredients_recipe'
            ),
        )

    def __str__(self):
        return f'{self.ingredient}: {self.amount}'


class Favorite(models.Model):
    """Список избранного."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь',
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_for_favorite'
            ),
        )


class Cart(models.Model):
    """Список покупок (Продуктовая корзина)."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_for_carts'
            ),
        )