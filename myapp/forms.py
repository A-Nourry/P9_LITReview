from django import forms
from django.contrib.auth import get_user_model

from . import models


class ReviewForm(forms.ModelForm):
    CHOICES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    rating = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect(attrs={"class": "form-check"})
    )

    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = models.Review
        fields = ["title", "rating", "comment"]


class EditReviewForm(forms.ModelForm):
    CHOICES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]

    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    rating = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect(attrs={"class": "form-check"})
    )

    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = models.Review
        fields = ["title", "rating", "comment"]


class TicketForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class EditTicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
            }
        )
    )

    class Meta:
        model = models.Ticket
        fields = ["title", "description", "image"]


class FollowUsersForm(forms.ModelForm):
    follows = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nom d'utilisateur",
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ["follows"]


class UnfollowUserForm(forms.ModelForm):
    unfollow_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeletePostForm(forms.Form):
    delete_post = forms.BooleanField(widget=forms.HiddenInput, initial=True)
