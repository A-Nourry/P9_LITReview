"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import (
    LogoutView,
)
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import myapp.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", authentication.views.LoginPageView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", authentication.views.signup_page, name="signup"),
    path("feed/", myapp.views.feed, name="feed"),
    path("my_posts/", myapp.views.my_posts, name="my-posts"),
    path("subscriptions/", myapp.views.subscriptions, name="subscriptions"),
    path("create_review/", myapp.views.create_review, name="create-review"),
    path("create_ticket/", myapp.views.create_ticket, name="create-ticket"),
    path(
        "review/<int:review_id>/edit", myapp.views.change_review, name="change-review"
    ),
    path(
        "ticket/<int:ticket_id>/edit", myapp.views.change_ticket, name="change-ticket"
    ),
    path(
        "ticket/<int:ticket_id>/review", myapp.views.ticket_review, name="ticket-review"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
