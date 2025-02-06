import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from math import sqrt

def is_prime(numb):
    """Check if a number is prime."""
    if numb < 2:
        return False
    for i in range(2, int(sqrt(numb)) + 1):
        if numb % i == 0:
            return False
    return True

def is_perfect(numb):
    """Check if a number is perfect."""
    return numb > 0 and sum(i for i in range(1, numb) if numb % i == 0) == numb

def is_armstrong(numb):
    """Check if a number is an Armstrong number."""
    digits = [int(d) for d in str(numb)]
    power = len(digits)
    return sum(d ** power for d in digits) == numb

def get_fun_fact(number):
    """Fetch a fun fact about a number from Numbers API."""
    try:
        response = requests.get(f"http://numbersapi.com/{number}/math?json")
        if response.status_code == 200:
            return response.json().get("text", f"{number} because = {number}.")
    except requests.RequestException:
        return "Fun fact not available."
    return f"{number} because = {number}"

@method_decorator(csrf_exempt, name='dispatch')
class NumberClassificationAPI(View):
    """API View to classify numbers and return properties."""
    
    def get(self, request):
        number = request.GET.get("number")
        
        # Validate the input
        if not number or not number.isdigit():
            return JsonResponse({"number": number, "error": True}, status=400)
        
        number = int(number)
        
        # Determine number properties
        properties = []
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("odd" if number % 2 else "even")
        
        # Build the response
        response_data = {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": sum(int(digit) for digit in str(number)),
            "fun_fact": get_fun_fact(number)
        }
        
        return JsonResponse(response_data, status=200)
