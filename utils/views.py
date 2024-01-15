from django.shortcuts import render, redirect
from django.views import View
import json
from validate_email import validate_email
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import ContactUs,SubscribedUsers

User = get_user_model()

class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is invalid'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry email is already registered'})
        return JsonResponse({'email_valid':True})
    
def TermsConds(request):
    return render(request,'utils/terms_conds.html')

class ContactUsForm(View):
    def get(self,request):
        return render(request,"utils/contact_us.html")
    
    def post(self,request):
        email = request.POST['email']
        name = request.POST['name']
        mobile_no = request.POST['mobile_no']
        mobile_no_full = request.POST['mobile_no_full']
        message = request.POST['message']
        if request.user.is_authenticated:
            by_lgu = True
        else:
            by_lgu = False
        context = {
            "FieldValues":request.POST
        }
        if not validate_email(email):
            messages.error(request,"Email is invalid")
            return render(request,"utils/contact_us.html",context)
        if len(mobile_no)>10:
            messages.error(request,"Mobile Number is invalid")
            return render(request,"utils/contact_us.html",context)
        contact = ContactUs.objects.create(
            name= name,
            email = email,
            phone_no = mobile_no_full,
            message = message,
            by_login_user = by_lgu,
        )
        contact.save()
        messages.success(request,"We will get in touch soon.")
        return render(request,"utils/contact_us.html")
    
class SubscribePage(View):
    def post(self,request):
        email = request.POST['email']
        if request.user.is_authenticated:
            by_lgu = True
        else:
            by_lgu = False
        if not validate_email(email):
            messages.error(request,"Email is invalid")
            return redirect("main-home")
        if SubscribedUsers.objects.filter(email=email).exists():
            messages.error(request,"Email is already Subscribed")
            return redirect("main-home")
        s = SubscribedUsers.objects.create(
            email = email,
            by_login_user = by_lgu,
        )
        s.save()
        messages.success(request,"You Subscribed to the Newsletter.")
        return redirect("main-home")