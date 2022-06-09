from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from PIL import Image


def image_upload(instance, filename):
    _ , extension = filename.split('.')
    return f"jobs/{instance.username}.{extension}"


class User(AbstractUser):
    picture = models.ImageField(null=True , blank=True, upload_to=image_upload)
    phone_number = models.CharField(max_length=18, validators=[MinLengthValidator(10)], null=True, blank=True)

    def save(self, *args, **kwargs):
        """ resize a big image """

        super().save(*args, **kwargs)

        # Resize a image
        if self.picture:
            img = Image.open(self.picture.path)
            if img.width > 800 or img.height > 800:
                img.thumbnail((800, 800))
                img.save(self.picture.path)

class UserCV(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cv')
    cv = models.FileField(upload_to='accounts/cvs/', null=True, blank=True)
    add_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)