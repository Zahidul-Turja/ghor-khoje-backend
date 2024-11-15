from django.http import JsonResponse
import requests
from random import randint


def get_random_quote(request):
    quote_number = randint(1, 1400)
    url = f"https://dummyjson.com/quotes/{quote_number}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        return JsonResponse(data)
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)
