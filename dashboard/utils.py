import requests
from django.http import JsonResponse

def get_nutrition_data(request):
    if request.method == 'GET':
        food_input = request.GET.get('food_input', '')
        url = f'https://api.edamam.com/api/food-database/parser?app_id=b121f9b0&app_key=571a65bed82fb6f3f0dd6a4ddbc47723&ingr={food_input}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            data = data['parsed']
            if data:
                return JsonResponse(data,safe=False)
            return JsonResponse({'error': 'Not Food data Found'}, status=500)
        else:
            return JsonResponse({'error': 'Failed to fetch nutrition data'}, status=500)