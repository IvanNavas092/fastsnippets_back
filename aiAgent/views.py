from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import openai
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie

openai.api_key = settings.OPENAI_API_KEY



@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})

def index(request):
    return HttpResponse("Hello, world. You're at the aiAgent index.")

def chat(request):
    if (request.method == 'POST'):
        user_message = request.POST.get('user_message')
        if not user_message:
            return HttpResponse("Please enter a message.")
        
        try:
            response = openai.chatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
            )
            reply = response.choices[0].message.content
            return JsonResponse({"reply": reply})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return HttpResponse("invalid request.")



