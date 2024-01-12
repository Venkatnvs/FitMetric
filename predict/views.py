from django.shortcuts import render
from django.views import View
import pickle
import os
from django.conf import settings
import pandas as pd
import numpy as np
import joblib

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
    

class DiabetesPredict(View):
    model_path = os.path.join(settings.BASE_DIR, "ml_models", "diabetes.pkl")

    def get(self,request):
        return render(request,"predict/diabetes_p.html")
    
    def post(self,request):
        preg = request.POST['pregnancies']
        glucose = request.POST['glucose']
        bp = request.POST['bloodpressure']
        st = request.POST['skinthickness']
        insulin = request.POST['insulin']
        bmi = request.POST['bmi']
        dpf = request.POST['dpf']
        age = request.POST['age']

        with open(self.model_path, 'rb') as f:
            diabetes = pickle.load(f)

        data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
        prediction = diabetes.predict(data)[0]

        if prediction==1:
            guess = "You has a high risk of Diabetes"
        elif prediction==0:
            guess = "You has a low risk of Diabetes"
        context = {
            "result":guess,
        }
        return render(request,'predict/mental_health.html',context)

class HeartPrediction(View):
    model_path = os.path.join(settings.BASE_DIR, "ml_models", "heart_disease.joblib")

    def get(self,request):
        return render(request,"predict/heart_p.html")
    
    def post(self,request):
        age = request.POST['age']
        sex = request.POST['sex']
        cp = request.POST['cp']
        trestbps = request.POST['trestbps']
        chol = request.POST['chol']
        fbs = request.POST['fbs']
        restecg = request.POST['restecg']
        thalach = request.POST['thalach']
        exang = request.POST['exang']
        oldpeak = request.POST['oldpeak']
        slope = request.POST['slope']
        ca = request.POST['ca']
        thal = request.POST['thal']

        model = joblib.load(self.model_path)

        data = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
        prediction = model.predict(data)[0]

        if prediction == 1:
            guess = "You have a high risk of Heart Disease"
        else:
            guess = "You have a low risk of Heart Disease"

        context = {
            'result':guess,
        }
        return render(request,'predict/heart_p.html',context)
    
class BreastCancerPredict(View):
    model_path = os.path.join(settings.BASE_DIR, "ml_models", "breast_cancer.joblib")

    def get(self,request):
        return render(request,"predict/breast_cancer_p.html")
    
    def post(self,request):
        clump_thickness = request.POST['clump_thickness']
        uniform_cell_size = request.POST['uniform_cell_size']
        uniform_cell_shape = request.POST['uniform_cell_shape']
        marginal_adhesion = request.POST['marginal_adhesion']
        single_epithelial_size = request.POST['single_epithelial_size']
        bare_nuclei = request.POST['bare_nuclei']
        bland_chromatin = request.POST['bland_chromatin']
        normal_nucleoli = request.POST['normal_nucleoli']
        mitoses = request.POST['mitoses']

        model = joblib.load(self.model_path)

        data = pd.DataFrame([[clump_thickness, uniform_cell_size, uniform_cell_shape, marginal_adhesion, single_epithelial_size, bare_nuclei, bland_chromatin, normal_nucleoli, mitoses]])
        prediction = model.predict(data)[0]

        if prediction == 4:
            guess = "You have a high risk of Breast Cancer"
        else:
            guess = "You have a low risk of Breast Cancer"

        context = {
            'result':guess,
        }
        return render(request,'predict/breast_cancer_p.html',context)
    
class LiverPredict(View):
    model_path = os.path.join(settings.BASE_DIR, "ml_models", "liver.joblib")

    def get(self,request):
        return render(request,"predict/liver_p.html")
    
    def post(self,request):
        age = request.POST['age']
        sex = request.POST['sex']
        total_bilirubin = request.POST['Total_Bilirubin']
        direct_bilirubin = request.POST['Direct_Bilirubin']
        alkaline_phosphotase = request.POST['Alkaline_Phosphotase']
        alamine_aminotransferase = request.POST['Alamine_Aminotransferase']
        aspartate_aminotransferase = request.POST['Aspartate_Aminotransferase']
        total_proteins = request.POST['Total_Protiens']
        albumin = request.POST['Albumin']
        albumin_and_globulin_ratio = request.POST['Albumin_and_Globulin_Ratio']

        model = joblib.load(self.model_path)
        data = pd.DataFrame([[age, sex, total_bilirubin, direct_bilirubin, alkaline_phosphotase, alamine_aminotransferase, aspartate_aminotransferase, total_proteins, albumin, albumin_and_globulin_ratio]])
        prediction = model.predict(data)[0]

        if prediction == 1:
            guess = "You has a high risk of Liver Disease, please consult your doctor immediately"
        else:
            guess = "You has a low risk of Kidney Disease"
        context = {
            'result':guess,
        }
        return render(request,'predict/liver_p.html',context)
    
class KidneyPredict(View):
    model_path = os.path.join(settings.BASE_DIR, "ml_models", "kidney_model.pkl")

    def get(self,request):
        return render(request,"predict/kidney_p.html")
    
    def post(self,request):
        age = float(request.POST['age'])
        blood_pressure = float(request.POST['blood_pressure'])
        specific_gravity = float(request.POST['specific_gravity'])
        albumin = float(request.POST['albumin'])
        sugar = float(request.POST['sugar'])
        red_blood_cells = float(request.POST['red_blood_cells'])
        pus_cell = float(request.POST['pus_cell'])
        pus_cell_clumps = float(request.POST['pus_cell_clumps'])
        bacteria = float(request.POST['bacteria'])
        blood_glucose_random = float(request.POST['blood_glucose_random'])
        blood_urea = float(request.POST['blood_urea'])
        serum_creatinine = float(request.POST['serum_creatinine'])
        sodium = float(request.POST['sodium'])
        potassium = float(request.POST['potassium'])
        haemoglobin = float(request.POST['haemoglobin'])
        packed_cell_volume = float(request.POST['packed_cell_volume'])
        white_blood_cell_count = float(request.POST['white_blood_cell_count'])
        red_blood_cell_count = float(request.POST['red_blood_cell_count'])
        hypertension = float(request.POST['hypertension'])
        diabetes_mellitus = float(request.POST['diabetes_mellitus'])
        coronary_artery_disease = float(request.POST['coronary_artery_disease'])
        appetite = float(request.POST['appetite'])
        peda_edema = float(request.POST['peda_edema'])
        aanemia = float(request.POST['aanemia'])

        model = joblib.load(self.model_path)
        data = pd.DataFrame([[age, blood_pressure, specific_gravity, albumin, sugar, red_blood_cells, pus_cell,
                                pus_cell_clumps, bacteria, blood_glucose_random, blood_urea, serum_creatinine,
                                sodium, potassium, haemoglobin, packed_cell_volume, white_blood_cell_count,
                                red_blood_cell_count, hypertension, diabetes_mellitus, coronary_artery_disease,
                                appetite, peda_edema, aanemia]])
        prediction = model.predict(data)[0]

        if prediction==1:
            guess = "You has a high risk of Kidney Disease, please consult your doctor immediately"
        else:
            guess = "You has a low risk of Kidney Disease"
        context = {
            'result':guess,
        }
        return render(request,'predict/kidney_p.html',context)