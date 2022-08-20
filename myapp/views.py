from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from . import forms, models


@login_required
def feed(request):
    reviews = models.Review.objects.all()
    tickets = models.Ticket.objects.all()

    context = {
        "reviews": reviews,
        "tickets": tickets,
    }
    return render(request, "myapp/feed.html", context=context)


@login_required
def my_posts(request):
    return render(request, "myapp/my_posts.html")


@login_required
def subscriptions(request):
    return render(request, "myapp/subscriptions.html")


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
def change_review(request):
    return render(request, "myapp/change_review.html")


@login_required
def change_ticket(request):
    return render(request, "myapp/change_ticket.html")


@login_required
def ticket_review(request):
    return render(request, "myapp/ticket_review.html")
