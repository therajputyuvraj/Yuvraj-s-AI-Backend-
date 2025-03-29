from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import ollama

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        prompt = data.get("message", "")
        history = data.get("history", [])

        # Ensure last response is not duplicated
        if history and history[-1]["role"] == "assistant":
            history = history[:-1]

        response = ollama.chat(model="mistral", messages=history + [{"role": "user", "content": prompt}])

        # Extract response content
        reply_message = str(response["message"].content) if hasattr(response["message"], "content") else str(response["message"])

        updated_history = history + [{"role": "user", "content": prompt}, {"role": "assistant", "content": reply_message}]

        return JsonResponse({
            "reply": reply_message,
            "history": updated_history
        })
    
    return JsonResponse({"error": "Invalid request"}, status=400)
