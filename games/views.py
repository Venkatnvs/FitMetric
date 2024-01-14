from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required()
def Home(request):
    return render(request,'games/index.html')

class ColorGames(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'games/color_game.html')