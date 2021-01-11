from django.db import models
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User, AbstractUser
from django.utils.timezone import now

# Table with all foods
class Main_food(models.Model):
    CATEGORY = (
        ('drink', 'drink'),
        ('food', 'food'),
    )

    name        = models.CharField(max_length=50)
    brand       = models.CharField(max_length=50, null=True, blank=True)
    category    = models.CharField(max_length=40, null=True, choices=CATEGORY)
    weight      = models.PositiveIntegerField(default=100, validators=[MaxValueValidator(1000)], blank=True)
    calories    = models.PositiveIntegerField(validators=[MaxValueValidator(5000)], null=True)
    total_fat   = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    carbs       = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    fiber       = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    protein     = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    salt        = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    creator     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_food', null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name}, {self.brand}"

    def serialize(self):
        return {
            'id': self.id,
            'name':self.name,
            'brand': self.brand,
            'category': self.category,
            'weight': self.weight,
            'calories': self.calories,
            'total_fat': self.total_fat,
            'carbs': self.carbs,
            'fiber': self.fiber,
            'protein': self.protein,
            'salt': self.salt,
            'creator': self.creator.id if self.creator != None else None
        }

# Table profile
class Profile_user(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email       = models.EmailField(max_length=150, null=True, blank=True)
    first_name  = models.CharField(max_length=50, null=True, blank=True)
    last_name   = models.CharField(max_length=50, null=True, blank=True)
    weight      = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    height      = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    age         = models.PositiveIntegerField(null=True, blank=True)
    weight_goal = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(200)], null=True, blank=True)

    favourite_foods  = models.ManyToManyField(Main_food, blank=True, related_name="users_fav_food")

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.weight}kg"

    def serialize(self):
        return {
            'user': self.user.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'weight': self.weight,
            'height': self.height,
            'age': self.age,
            'weight_goal': self.weight_goal,
            'list-foods': [food.id for food in self.favourite_foods.all()]
        }

# Table with what each user ate
class Daily_food(models.Model):
    CATEGORY = (
        ('drink', 'drink'),
        ('food', 'food'),
    )

    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name="consumed_food")
    food            = models.ForeignKey(Main_food, null=True, on_delete=models.SET_NULL)
    category        = models.CharField(max_length=40, choices=CATEGORY)
    weight          = models.PositiveIntegerField(validators=[MaxValueValidator(10000)])
    date_consumed   = models.DateField(default=now)

    def __str__(self):
        return f"{self.user.profile.first_name}, {self.weight}g of {self.food}"

# Table with recipes
class Recipes(models.Model):
    TYPE = (
        ('bulk', 'bulk'),
        ('reduce weight', 'reduce weight'),
        ('healthy dessert', 'healthy dessert'),
    )
    name        = models.CharField(max_length=50)
    summary     = models.TextField()
    url_field   = models.URLField(max_length=400)
    category    = models.CharField(max_length=20, choices=TYPE)
    image       = models.ImageField(upload_to="gallery")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Recipes"
    
    def serialize(self):
        return {
            'name': self.name,
            'summary': self.summary,
            'url_field': self.url_field,
            'category': self.category,
            'image': self.image.url
        }


class Messages(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='messages_app')
    message = models.TextField(max_length=300)

    class Meta:
        verbose_name_plural = "Messages"

# When user is created, create profile to that user
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile_user.objects.create(user=instance, email=instance.email)

post_save.connect(create_profile, sender=User)