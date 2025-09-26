import json
import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from google import genai

GEMINI_API_KEY = settings.GEMINI_API_KEY 

@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})

def index(request):
    return HttpResponse("Hello, world. You're at the aiAgent index.")

def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('user_message')
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        if not user_message:
            return JsonResponse({"error": "Please enter a message."}, status=400)

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_message
            )
            reply = response.text
            return JsonResponse({"reply": reply})
        except Exception  as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


