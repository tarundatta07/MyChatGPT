import openai
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import auth

# open_ai_api_key = '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'
open_ai_api_key = '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'
openai.api_key = open_ai_api_key

def ask_openai(message):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response.choices[0].text.strip()
        return answer
    except openai.error.OpenAIError as e:
        # Log the error or handle it in an appropriate way
        print("OpenAI API Error:", e)
        return "An error occurred while processing your request. Please try again later."


def chatgpt(request):
    if request.method == "POST":
        message = request.POST.get('message') 
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatgpt.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)

def register(request):
    return render(request, 'register.html')