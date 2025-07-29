from django.shortcuts import render

# Create your views here.
import os
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

FIREBASE_API_KEY = os.environ.get("FIREBASE_WEB_API_KEY")
FIREBASE_SIGN_IN_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
)


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect("login")

        # Step 1: Send credentials to Firebase REST API
        response = requests.post(
            FIREBASE_SIGN_IN_URL,
            params={"key": FIREBASE_API_KEY},
            json={
                "email": email,
                "password": password,
                "returnSecureToken": True,
            },
        )

        if response.status_code != 200:
            messages.error(request, "Invalid credentials.")
            return redirect("login")

        id_token = response.json().get("idToken")

        # Step 2: Use Django authenticate() and login()
        user = authenticate(request, id_token=id_token)
        if user:
            login(request, user)
            return redirect("dashboard")  # or another logged-in page
        else:
            messages.error(request, "Authentication failed.")
            return redirect("login")

    return render(request, "accounts/login.html")