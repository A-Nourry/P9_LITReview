from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="titre")
    description = models.CharField(max_length=6000, verbose_name="description")
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="demandeur"
    )
    image = models.ImageField(verbose_name="image")
    date_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    title = models.CharField(max_length=128, verbose_name="titre")
    comment = models.CharField(max_length=6000, verbose_name="commentaire")
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    original_poster = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, primary_key=True)
