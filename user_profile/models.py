from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from Post.models import Material
from django.dispatch import receiver
from django.db.models.signals import  post_save

User = get_user_model()

class Profile(TimeStampedModel):
    GENDER_MALE = "Male"
    GENDER_FEMALE = "Female"
    OTHER = "Other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (OTHER, "Other"),
    )
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    points = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(1000)
    ])
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    user_avatar = models.ImageField(upload_to="avatar/", blank=True)
    about = models.TextField(max_length=120, blank=True)

    materials_claimed = models.ManyToManyField(Material, related_name='profiles', blank=True)
    interests = models.ManyToManyField("Interests", related_name = "profiles", blank=True)
    #EDUCATION
    education_institute = models.CharField(max_length=128, blank=True, default="")
    education_degree = models.CharField(max_length=64, blank=True, default="")
    education_specialization = models.CharField(max_length=64, blank=True, default="")
    education_fromdate = models.DateTimeField(blank=True, null=True)
    education_todate = models.DateTimeField(blank=True, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

class Interests(models.Model):
    interest = models.CharField(max_length=255, blank=False)
    


