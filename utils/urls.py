from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('validate-email', csrf_exempt(EmailValidation.as_view()), name='utils-validate-email'),
    path('terms-and-conditions', TermsConds, name='utils-terms-conds'),
    path('contact-us', ContactUsForm.as_view(), name='utils-contact-us'),
    path('subscribe', SubscribePage.as_view(), name='utils-subscribe'),
]