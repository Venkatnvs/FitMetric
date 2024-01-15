import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Nutrition,NutritionItems
from django.shortcuts import get_object_or_404

def get_nutrition_data(request):
    if request.method == 'GET':
        food_input = request.GET.get('food_input', '')
        url = f'https://api.edamam.com/api/food-database/parser?app_id=b121f9b0&app_key=571a65bed82fb6f3f0dd6a4ddbc47723&ingr={food_input}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data:
                return JsonResponse(data,safe=False)
            return JsonResponse({'error': 'Not Food data Found'}, status=500)
        else:
            return JsonResponse({'error': 'Failed to fetch nutrition data'}, status=500)
        

@csrf_exempt
def save_nutrition_data(request):
    if request.method == 'POST':
        try:
            nutrition_data = json.loads(request.body)

            nutrition, _ = Nutrition.objects.get_or_create(
                user=request.user,
                is_completed=False,
            )

            NutritionItems.objects.create(
                order=nutrition,
                quantity=1,
                name=nutrition_data['label'],
                img_url=nutrition_data['image'],
                energy=nutrition_data['energy'],
                protein=nutrition_data['protein'],
                fat=nutrition_data['fat'],
                carbohydrates=nutrition_data['carbohydrates'],
            )

            return JsonResponse({'message': 'Nutrition data saved successfully.'}, status=200)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Invalid JSON format: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Failed to save nutrition data: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
@csrf_exempt
def delete_nutrition_data(request, item_id):
    if request.method == 'DELETE':
        try:
            item = get_object_or_404(NutritionItems, pk=item_id)
            if request.user == item.order.user:
                item.delete()
                return JsonResponse({'message': 'Nutrition data deleted successfully.'}, status=200)
            else:
                return JsonResponse({'error': 'Permission denied. You are not the owner of this nutrition data.'}, status=403)

        except NutritionItems.DoesNotExist:
            return JsonResponse({'error': 'Nutrition data not found.'}, status=404)

        except Exception as e:
            return JsonResponse({'error': f'Failed to delete nutrition data: {str(e)}'}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)