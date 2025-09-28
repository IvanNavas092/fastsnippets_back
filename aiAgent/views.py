import json
import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from google import genai

GEMINI_API_KEY = settings.GEMINI_API_KEY 

@ensure_csrf_cookie
def get_csrf(request):
    """Endpoint para obtener el token CSRF"""
    return JsonResponse({
        "detail": "CSRF cookie set", 
        "csrfToken": get_token(request)  # Devuelve el token en la respuesta
    })
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
                    contents=(
        "Eres un asistente experto en programación especializado en crear snippets "
        "en frameworks (Angular, React, Vue, Svelte). "
        "Responde únicamente preguntas sobre frameworks. "
        "Si te preguntan otra cosa, responde: "
        "'Lo siento, solo puedo responder preguntas sobre frameworks de programación.'\n\n"
        f"Usuario: {user_message}"
    ),
                
            )
            reply = response.text
            return JsonResponse({"reply": reply})
        except Exception  as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)


