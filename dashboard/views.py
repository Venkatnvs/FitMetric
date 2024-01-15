from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from .models import TdeeData
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Nutrition

def Home(request):
    titles = [
        'Mental health is just as important as physical health; prioritize self-care and seek support when needed.',
        'Consuming a variety of colorful fruits and vegetables provides a range of essential vitamins and minerals.',
        'Maintaining a healthy weight through diet and exercise is crucial for preventing obesity-related diseases.',
        'Moderate caffeine intake can enhance alertness, but excessive consumption may lead to negative health effects.',
        'Regular dental check-ups and oral hygiene practices are essential for overall health, preventing gum disease and infections.',
        'Bone density declines with age, making weight-bearing exercises crucial for maintaining bone health.',
        'The body circadian rhythm, influenced by sunlight, regulates sleep-wake cycles and overall well-being.',
        'Omega-3 fatty acids, found in fish and flaxseed, are beneficial for heart health and brain function.',
        'High levels of stress can negatively impact physical and mental health; practice stress-management techniques.',
        'Whole grains, rich in fiber, contribute to digestive health and can reduce the risk of chronic diseases.',
        'Regular stretching improves flexibility, reduces the risk of injury, and promotes better posture.',
        'Adequate sunlight exposure is essential for vitamin D synthesis, crucial for bone and immune health.',
        'Balancing different food groups ensures a diverse intake of nutrients for optimal health.',
        'Chronic inflammation is linked to various diseases; an anti-inflammatory diet can help reduce inflammation.',
        'Engaging in activities you enjoy boosts mental well-being and reduces the risk of depression.',
        'Maintaining proper posture supports spine health and reduces the risk of musculoskeletal issues.',
        'Chronic stress can contribute to weight gain; manage stress to support a healthy weight.',
        'Adequate water intake supports digestion, nutrient absorption, and overall bodily functions.',
        'Regular cardiovascular exercise enhances lung capacity and improves respiratory health.',
        'Mindful eating involves paying attention to food choices and savoring each bite, promoting healthier eating habits.',
        'Building and maintaining strong social connections is associated with a longer, healthier life.',
        'Maintaining a healthy gut microbiome through a balanced diet supports overall well-being.',
        'Moderation is key; balance indulgent treats with nutritious foods for a well-rounded diet.',
        'Regular health screenings, such as blood pressure and cholesterol checks, aid in early disease detection.',
        'Setting realistic and achievable fitness goals promotes motivation and long-term success.',
        'Mind-body practices like yoga and meditation can improve both physical and mental health.',
        'A good night sleep is essential for memory consolidation, emotional well-being, and overall health.',
        'Limiting alcohol consumption supports liver health and reduces the risk of alcohol-related diseases.',
        'Regular resistance training helps maintain muscle mass, strength, and overall functionality.',
        'Building healthy habits takes time; be patient and consistent for lasting improvements in well-being.',
        'Listening to your body hunger and fullness cues is crucial for maintaining a healthy weight.',
        'Social support is a powerful motivator; exercise with friends or join fitness classes for added encouragement.',
        'Practicing gratitude has positive effects on mental health and overall life satisfaction.',
        'Balancing work and leisure activities promotes a well-rounded and fulfilling life.',
    ]
    context = {
        'titles':titles
    }
    return render(request,'dashboard/index.html',context)

class TdeePage(LoginRequiredMixin,View):
    def get(self,request):
        context = {
            'recent_data':self.GetRecentData()
        }
        return render(request,'dashboard/tdee.html',context)
    
    def post(self,request):
        age = request.POST['age']
        gender = request.POST['gender']
        height = request.POST['height']
        weight = request.POST['weight']
        activityLevel = request.POST['activityLevel']
        context = {
            'FieldValues':request.POST,
            'recent_data':self.GetRecentData()
        }
        if int(age)<= 0 or int(height)<=0 or int(weight)<=0:
            messages.error(request,"Invalid input values. Age, height, and weight must be greater than 0.")
            return render(request,'dashboard/tdee.html',context)
        a = TdeeData.objects.create(
                user = request.user,
                age=age,
                gender=gender,
                height=height,
                weight=weight,
                activity_level=activityLevel
            )
        a.save()
        return redirect('main-tdee')
    
    def GetRecentData(self):
        return TdeeData.objects.filter(user=self.request.user).order_by('-created_at')[:4]

class NutritionPage(LoginRequiredMixin,View):
    def get(self,request):
        nutrition, _ = Nutrition.objects.get_or_create(
                user=request.user,
                is_completed=False,
        )
        context = {
            'data':nutrition,
        }
        return render(request,'dashboard/nutrition.html',context)

class MentalHealthPage(LoginRequiredMixin,View):
    def get(self,request):
        cat = int(request.GET.get('cat',0))
        if cat in [1,2,3]:
            return render(request,f'dashboard/mental_health_c{cat}.html')
        return render(request,"dashboard/mental_health_sel.html")