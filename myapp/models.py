from django.db import models
from django.conf import settings


class Review(models.Model):
    title = models.CharField(max_length=128, verbose_name="titre")
    comment = models.CharField(max_length=6000, verbose_name="commentaire")
    original_poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Ticket(models.Model):
    title = models.CharField(max_length=128, verbose_name="titre")
    description = models.CharField(max_length=6000, verbose_name="description")
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='demandeur')
    image = models.ImageField(verbose_name="image")
    review = models.ForeignKey(Review, null=True, on_delete=models.SET_NULL, blank=True)
