from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import CharField, Value
from django.db.models import Q

from . import forms, models

User = get_user_model()


@login_required
def feed(request):
    tickets = models.Ticket.objects.filter(
        Q(requester__in=request.user.follows.all())
        | Q(requester__exact=request.user.id)
    )
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    reviews = models.Review.objects.filter(
        Q(original_poster__in=request.user.follows.all())
        | Q(original_poster__exact=request.user.id)
        | Q(ticket__requester=request.user)
    )
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.date_created, reverse=True
    )

    context = {
        "posts": posts,
    }
    return render(request, "myapp/feed.html", context=context)


@login_required
def my_posts(request):
    reviews = models.Review.objects.filter(Q(original_poster__exact=request.user.id))
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    tickets = models.Ticket.objects.filter(requester__exact=request.user.id)
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.date_created, reverse=True
    )

    context = {
        "posts": posts,
    }
    return render(request, "myapp/my_posts.html", context=context)


@login_required
def subscriptions(request):
    followed = request.user.follows.all()
    followers = User.objects.filter(follows=request.user.id)
    follow_form = forms.FollowUsersForm()
    message = ""

    if request.method == "POST":
        if "unfollow_user" in request.POST:
            delete_form = forms.UnfollowsUserForm(request.POST)
            if delete_form.is_valid():
                request.user.follows.remove()
                return redirect("subscriptions")

        if follow_form.is_valid():
            follow_form.save(commit=False)
            following_user = User.objects.get(username="david")
            if following_user in User.objects.all():
                request.user.follows.add(following_user)
                request.user.save()
                return redirect("subscriptions")

        message = "Nom d'utilisateur invalide."

    context = {
        "form": follow_form,
        "followed": followed,
        "followers": followers,
        "message": message,
    }

    return render(request, "myapp/subscriptions.html", context=context)


@login_required
def create_review(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all([review_form.is_valid(), ticket_form.is_valid()]):
            ticket = ticket_form.save(commit=False)
            ticket.requester = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.original_poster = request.user
            review.ticket = ticket
            review.save()

            return redirect("feed")

    context = {
        "review_form": review_form,
        "ticket_form": ticket_form,
    }

    return render(request, "myapp/create_review.html", context=context)


@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.requester = request.user
            ticket.save()
            return redirect("feed")

    context = {"ticket_form": ticket_form}

    return render(request, "myapp/create_ticket.html", context=context)


@login_required
def change_review(request, review_id):
    review = get_object_or_404(models.Review, ticket_id=review_id)
    ticket = get_object_or_404(models.Ticket, id=review_id)
    edit_form = forms.EditReviewForm(instance=review)
    user = review.original_poster
    delete_form = forms.DeletePostForm()
    if request.method == "POST":
        if "edit_review" in request.POST:
            edit_form = forms.EditReviewForm(request.POST, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("feed")
        if "delete_post" in request.POST:
            delete_form = forms.DeletePostForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect("feed")
    context = {
        "edit_form": edit_form,
        "delete_form": delete_form,
        "ticket": ticket,
    }
    if request.user == user:
        return render(request, "myapp/change_review.html", context=context)
    else:
        return redirect("feed")


@login_required
def change_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    user = ticket.requester
    edit_form = forms.EditTicketForm(instance=ticket)
    delete_form = forms.DeletePostForm()
    if request.method == "POST":
        if "edit_ticket" in request.POST:
            edit_form = forms.EditTicketForm(
                request.POST, request.FILES, instance=ticket
            )
            if edit_form.is_valid():
                edit_form.save()
                return redirect("feed")
        if "delete_post" in request.POST:
            delete_form = forms.DeletePostForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect("feed")
    context = {
        "edit_form": edit_form,
        "delete_form": delete_form,
        "ticket": ticket,
    }
    if request.user == user:
        return render(request, "myapp/change_ticket.html", context=context)
    else:
        return redirect("feed")


@login_required
def ticket_review(request, ticket_id):
    review_form = forms.ReviewForm()
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == "POST":
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.original_poster = request.user
            review.ticket = ticket
            review.save()

            return redirect("feed")

    context = {
        "review_form": review_form,
        "ticket": ticket,
    }
    return render(request, "myapp/ticket_review.html", context=context)
