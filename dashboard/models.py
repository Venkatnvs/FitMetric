from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TdeeData(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    height = models.FloatField()
    weight = models.FloatField()
    activity_level = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.created_at}"

    def calculateTdee(self):
        if self.gender == "Male":
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        elif self.gender == "Female":
            bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)

        activity_multiplier = {
            'level1': 1.2,
            'level2': 1.375,
            'level3': 1.55,
            'level4': 1.725,
            'level5': 1.9,
            # 'level6': 2.0,
        }.get(self.activity_level, 1.0)

        tdee = bmr * activity_multiplier
        return tdee
    
    def calculateBMI(self):
        bmi = self.weight / ((self.height / 100) * (self.height / 100))
        return bmi
    
    def calculateMacronutrients(self):
        protein_percentage = 0.30
        fat_percentage = 0.30
        carbohydrate_percentage = 0.40
        calories = self.calculateTdee()
        protein_in_grams = (protein_percentage * calories) / 4.0
        fat_in_grams = (fat_percentage * calories) / 9.0
        carbohydrates_in_grams = (carbohydrate_percentage * calories) / 4.0

        macronutrients = {
            'protein': protein_in_grams,
            'fat': fat_in_grams,
            'carbohydrates': carbohydrates_in_grams,
        }
        return macronutrients
    
    @property
    def calories(self):
        return round(self.calculateTdee())
    
    @property
    def bmi(self):
        return round(self.calculateBMI(),1)
    
    @property
    def nutrients(self):
        macronutrients = self.calculateMacronutrients()
        rounded_macronutrients = {
            key: round(value, 2) for key, value in macronutrients.items()
        }
        return rounded_macronutrients
