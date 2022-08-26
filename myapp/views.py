from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from django.db.models import Q

from . import forms, models


@login_required
def feed(request):
    reviews = models.Review.objects.filter(
        Q(original_poster__in=request.user.follows.all())
        | Q(original_poster__exact=request.user.id)
    )
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    tickets = models.Ticket.objects.filter(
        Q(requester__in=request.user.follows.all())
        | Q(requester__exact=request.user.id)
    )
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

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
    users_followed = request.user.follows
    form = forms.FollowUsersForm(instance=request.user)
    if request.method == "POST":
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("subscriptions")

    context = {
        "form": form,
        "users": users_followed,
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
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeletePostForm()
    if request.method == "POST":
        if "edit_review" in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review)
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
    return render(request, "myapp/change_review.html", context=context)


@login_required
def change_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeletePostForm()
    if request.method == "POST":
        if "edit_ticket" in request.POST:
            edit_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
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
    return render(request, "myapp/change_ticket.html", context=context)


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
