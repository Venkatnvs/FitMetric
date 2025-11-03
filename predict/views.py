from django.shortcuts import render
from django.views import View
import pickle
import os
from django.conf import settings
import pandas as pd
import numpy as np
import joblib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

@login_required()
def Home(request):
    return render(request,"predict/index.html")

class DepressionLevelPage(LoginRequiredMixin,View):
    model_path = os.path.join(settings.BASE_DIR, "ml_models", "depression_level.pkl")

    def get(self,request):
        return render(request,"predict/depression_level_p.html")
    
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
        return render(request,"predict/depression_level_p.html",context)
    

class DiabetesPredict(LoginRequiredMixin,View):
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
        return render(request,'predict/diabetes_p.html',context)

class HeartPrediction(LoginRequiredMixin,View):
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
    
class BreastCancerPredict(LoginRequiredMixin,View):
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
    
class LiverPredict(LoginRequiredMixin,View):
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
    
class KidneyPredict(LoginRequiredMixin,View):
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
    

class DiseasesPredict(LoginRequiredMixin,View):
    model_path1 = os.path.join(settings.BASE_DIR, "ml_models", "diseases_dt.joblib")
    model_path2 = os.path.join(settings.BASE_DIR, "ml_models", "diseases_rf.joblib")
    model_path3 = os.path.join(settings.BASE_DIR, "ml_models", "diseases_knn.joblib")

    symptoms = [
        "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering",
        "chills", "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue", "muscle_wasting",
        "vomiting", "burning_micturition", "spotting_urination", "fatigue", "weight_gain",
        "anxiety", "cold_hands_and_feets", "mood_swings", "weight_loss", "restlessness", "lethargy",
        "patches_in_throat", "irregular_sugar_level", "cough", "high_fever", "sunken_eyes",
        "breathlessness", "sweating", "dehydration", "indigestion", "headache", "yellowish_skin",
        "dark_urine", "nausea", "loss_of_appetite", "pain_behind_the_eyes", "back_pain",
        "constipation", "abdominal_pain", "diarrhoea", "mild_fever", "yellow_urine",
        "yellowing_of_eyes", "acute_liver_failure", "fluid_overload", "swelling_of_stomach",
        "swelled_lymph_nodes", "malaise", "blurred_and_distorted_vision", "phlegm",
        "throat_irritation", "redness_of_eyes", "sinus_pressure", "runny_nose", "congestion",
        "chest_pain", "weakness_in_limbs", "fast_heart_rate", "pain_during_bowel_movements",
        "pain_in_anal_region", "bloody_stool", "irritation_in_anus", "neck_pain", "dizziness",
        "cramps", "bruising", "obesity", "swollen_legs", "swollen_blood_vessels",
        "puffy_face_and_eyes", "enlarged_thyroid", "brittle_nails", "swollen_extremities",
        "excessive_hunger", "extra_marital_contacts", "drying_and_tingling_lips", "slurred_speech",
        "knee_pain", "hip_joint_pain", "muscle_weakness", "stiff_neck", "swelling_joints",
        "movement_stiffness", "spinning_movements", "loss_of_balance", "unsteadiness",
        "weakness_of_one_body_side", "loss_of_smell", "bladder_discomfort", "foul_smell_of_urine",
        "continuous_feel_of_urine", "passage_of_gases", "internal_itching", "toxic_look_(typhos)",
        "depression", "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body",
        "belly_pain", "abnormal_menstruation", "dischromic_patches", "watering_from_eyes",
        "increased_appetite", "polyuria", "family_history", "mucoid_sputum", "rusty_sputum",
        "lack_of_concentration", "visual_disturbances", "receiving_blood_transfusion",
        "receiving_unsterile_injections", "coma", "stomach_bleeding", "distention_of_abdomen",
        "history_of_alcohol_consumption", "fluid_overload.1", "blood_in_sputum",
        "prominent_veins_on_calf", "palpitations", "painful_walking", "pus_filled_pimples",
        "blackheads", "scurring", "skin_peeling", "silver_like_dusting", "small_dents_in_nails",
        "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze"
    ]

    disease=['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis',
        'Drug Reaction', 'Peptic ulcer diseae', 'AIDS', 'Diabetes ',
        'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine',
        'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice',
        'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A',
        'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E',
        'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia',
        'Dimorphic hemmorhoids(piles)', 'Heart attack', 'Varicose veins',
        'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
        'Osteoarthristis', 'Arthritis',
        '(vertigo) Paroymsal  Positional Vertigo', 'Acne',
        'Urinary tract infection', 'Psoriasis', 'Impetigo']
    
    def getSymptomsLen(self):
        return len(self.symptoms)
    
    def get(self,request):
        context = {
            'symptoms':self.symptoms
        }
        return render(request,'predict/diseases_l.html',context)
    
    def post(self,request):
        symptoms_list = request.POST.getlist('symptoms[]')
        l2 = [0]*self.getSymptomsLen()
        for k in range(0,self.getSymptomsLen()):
            for z in symptoms_list:
                if(z==self.symptoms[k]):
                    l2[k]=1
        model1 = joblib.load(self.model_path1)
        model2 = joblib.load(self.model_path2)
        model3 = joblib.load(self.model_path3)
        data = pd.DataFrame([l2])
        pred1 = model1.predict(data)[0]
        pred2 = model2.predict(data)[0]
        pred3 = model3.predict(data)[0]
        pred = [self.disease[pred1],self.disease[pred2],self.disease[pred3]]
        guess = f'You have a risk of {max(pred)}'
        context = {
            'result':guess,
        }
        return render(request,'predict/diseases_l.html',context)
