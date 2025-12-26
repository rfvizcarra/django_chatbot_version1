from django.shortcuts import render, redirect
from django.http import JsonResponse
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from google_auth_oauthlib.flow import Flow

# from langchain_core.prompts import ChatPromptTemplate
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat, GmailToken
from django.utils import timezone

load_dotenv()

# llm = ChatOpenAI(
#    model="gpt-5-nano",
# )


def ask_openai(message):
    llm = ChatOpenAI(
        model="gpt-5-nano",
    )
    messages = [
        (
            "system",
            "You are a helpful assistant",
        ),
        ("human", message),
    ]
    response = llm.invoke(messages)
    print(response)
    answer = response.text
    return answer


# Create your views here.
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == "POST":
        message = request.POST.get("message")
        response = ask_openai(message)

        chat = Chat(
            user=request.user,
            message=message,
            response=response,
            created_at=timezone.now(),
        )
        chat.save()
        return JsonResponse({"message": message, "response": response})
    return render(request, "chatbot.html", {"chats": chats})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("chatbot")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect("chatbot")
            except:
                error_message = "Error creating account"
                return render(
                    request, "register.html", {"error_message": error_message}
                )
        else:
            error_message = "Passwords do not match"
            return render(request, "register.html", {"error_message": error_message})
    return render(request, "register.html")


def logout(request):
    auth.logout(request)
    return redirect("login")


# This must match what you put in Google Console EXACTLY
REDIRECT_URI = "http://127.0.0.1:8000/gmail/callback/"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]  # What permission we want


def connect_gmail(request):
    # 1. Create the flow using the JSON file we downloaded
    flow = Flow.from_client_secrets_file(
        "client_secrets.json", scopes=SCOPES, redirect_uri=REDIRECT_URI
    )

    # 2. Generate the URL the user needs to visit
    auth_url, state = flow.authorization_url(prompt="consent")

    # 3. Save 'state' in session to verify it's the same user coming back
    request.session["state"] = state

    # 4. Send the user to Google
    return redirect(auth_url)


def gmail_callback(request):
    # 1. Rebuild the flow
    state = request.session["state"]
    flow = Flow.from_client_secrets_file(
        "client_secrets.json", scopes=SCOPES, state=state, redirect_uri=REDIRECT_URI
    )

    # 2. Fetch the token using the code Google sent back in the URL
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    # 3. Get the credentials
    credentials = flow.credentials

    # 4. Save to Database (Update existing or Create new)
    GmailToken.objects.update_or_create(
        user=request.user,
        defaults={
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": " ".join(credentials.scopes),
        },
    )

    return redirect("chatbot")  # Send them back to your main page
