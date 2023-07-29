import openai
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone

# open_ai_api_key = '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'
# open_ai_api_key = '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'
open_ai_api_key = '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'
openai.api_key = open_ai_api_key

def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages = [
                {'role': 'system', 'content': 'AI helping assistance'},
                {'role': 'user', 'content': message}
            ]
        )
        # print(response)
        answer = response.choices[0].message.content.strip()
        return answer
    
    except openai.error.OpenAIError as e:
        # Log the error or handle it in an appropriate way
        print("OpenAI API Error:", e)
        return "An error occurred while processing your request. Please try again later."


def chatgpt(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == "POST":
        message = request.POST.get('message') 
        response = ask_openai(message)
        chat = Chat (user = request.user, message = message, response = response, created_at = timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatgpt.html', {'chats': chats})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatgpt')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatgpt')
            except:
                error_msg = 'Error Creating Account'
                return render(request, 'register.html', {'error_msg': error_msg})
        else:
            error_msg = 'Password Does Not Match'
            return render(request, 'register.html', {'error_msg': error_msg})
    return render(request, 'register.html')