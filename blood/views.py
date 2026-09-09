
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from panel.models import News,Contact,BloodRequest,ReadyDonors
from django.db import IntegrityError

import traceback
def home(request):
    news = News.objects.first()
    context = {
        'news':news
    }
    return render(request,'home.html',context)
   

def news(request):
    data = News.objects.all()
    context = {
        'news':data
    }
    return render(request,'news.html',context)
  


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        contact = Contact(
            name=name,
            email=email,
            message=message
        )
        contact.save()
        
        # Add a success message
        messages.success(request, "Your message was sent successfully!")

    return render(request, 'contact.html')



def case(request):
    # Fetch unsolved and solved cases, ordered by newest first
    unsolved_cases = BloodRequest.objects.filter(is_solved=False).order_by('-created_at')
    solved_cases = BloodRequest.objects.filter(is_solved=True).order_by('-created_at')

    context = {
        'unsolved_cases': unsolved_cases,
        'solved_cases': solved_cases
    }

    return render(request, 'required.html', context)


def about(request):

    
    return render(request, 'about.html')


def donate(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address", "")  # Optional
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        weight = request.POST.get("weight")
        disease = request.POST.get("disease", "")  # Optional
        blood_group = request.POST.get("blood_group", "")  # Optional, default to empty string
        phone = request.POST.get("phone")
        email = request.POST.get("email", "")  # Optional, default to empty string
        donation_time = request.POST.get("donation_time", "Urgent")  # Default to "Urgent"

        # ✅ Validate Required Fields
        if not all([name, age, gender, weight, phone]):
            messages.error(request, "All fields except address, disease, blood group, email, and donation time are required.")
            return redirect("donate")

        # ✅ Convert Numeric Fields Safely
        try:
            age = int(age)
            weight = float(weight)
        except ValueError:
            messages.error(request, "Age and weight must be valid numbers.")
            return redirect("donate")

        # ✅ Try to Save Data
        try:
            ReadyDonors.objects.create(
                name=name, address=address, age=age, gender=gender, weight=weight,
                blood_group=blood_group, disease=disease, email=email,
                phone=phone, donation_time=donation_time
            )
            messages.success(request, "Thank you for registering as a donor!")
            return redirect("donate")
        except IntegrityError as e:
            print(" IntegrityError:", e)  # Debugging
            traceback.print_exc()
            messages.error(request, "An error occurred. Please check required fields.")
            return redirect("donate")

    return render(request, "donate.html") 
