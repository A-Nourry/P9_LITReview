from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="titre")
    description = models.CharField(max_length=6000, verbose_name="description")
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="demandeur"
    )
    image = models.ImageField(verbose_name="image")
    date_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (132, 216)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    title = models.CharField(max_length=128, verbose_name="titre")
    comment = models.TextField(verbose_name="commentaire")
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    original_poster = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, primary_key=True)
