from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from Post.models import Material

User = get_user_model()

class Profile(TimeStampedModel):
    GENDER_MALE = "m"
    GENDER_FEMALE = "f"
    OTHER = "o"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (OTHER, "Other"),
    )
    user = models.OneToOneField(User, related_name='profiles', on_delete=models.CASCADE)
    points = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(1000)
    ])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user_avatar = models.ImageField(upload_to="avatar/", blank=True)
    about = models.TextField(max_length=120, blank=True)

    materials_claimed = models.ManyToManyField(Material, related_name='profiles')
    interests = models.ManyToManyField("Interests", related_name = "profiles")
    #EDUCATION
    education_institute = models.CharField(max_length=128, blank=True)
    education_degree = models.CharField(max_length=64, blank=True)
    education_specialization = models.CharField(max_length=64, blank=True)
    education_fromdate = models.DateTimeField(blank=True)
    education_todate = models.DateTimeField(blank=True)

class Interests(models.Model):
    interest = models.CharField(max_length=255, blank=False)
    


