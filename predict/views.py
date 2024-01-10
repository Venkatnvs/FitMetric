from django.shortcuts import render
from django.views import View
import pickle
import os
from django.conf import settings
import pandas as pd

def Home(request):
    return render(request,"predict/index.html")

class MentalHealthPage(View):
    model_path = os.path.join(settings.BASE_DIR, "ml_models", "mental_health.pkl")

    def get(self,request):
        return render(request,"predict/mental_health.html")
    
    def post(self,request):
        q1 = float(request.POST['q1'])
        q2 = float(request.POST['q2'])
        q3 = float(request.POST['q3'])
        q4 = float(request.POST['q4'])
        q5 = float(request.POST['q5'])
        q6 = float(request.POST['q6'])
        q7 = float(request.POST['q7'])
        q8 = float(request.POST['q8'])
        q9 = float(request.POST['q9'])
        q10 = float(request.POST['q10'])

        with open(self.model_path, 'rb') as f:
            mental_health_model = pickle.load(f)
        
        input_variables = pd.DataFrame([[q1,q2,q3,q4,q5,q6,q7,q8,q9,q10]],
                                    columns=['q1','q2','q3','q4','q5','q6','q7','q8','q9','q10'],
                                    dtype=float,
                                    index=['input'])
        
        prediction = mental_health_model.predict(input_variables)[0]

        if prediction == 0: 
            guess = "Not Depressed"
        if prediction == 1: 
            guess = "Mildly Depressed"
        if prediction == 2: 
            guess = "Moderately Depressed"
        if prediction == 3: 
            guess = "Severely Depressed"
        if prediction == 4: 
            guess = "Critically Depressed"
        context = {
            "result":guess,
        }
        return render(request,"predict/mental_health.html",context)