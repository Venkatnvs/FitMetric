from django.shortcuts import render
from django.views import View

def Home(request):
    return render(request,'games/index.html')

class ColorGames(View):
    def get(self,request):
        return render(request,'games/color_game.html')