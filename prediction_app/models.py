from django.db import models

# Por ahora no necesitamos modelos, pero dejamos el archivo
class Prediction(models.Model):
    pclass = models.IntegerField()
    sex = models.CharField(max_length=10)
    age = models.FloatField()
    embarked = models.CharField(max_length=1)
    survived = models.BooleanField()
    probability = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Predicción {self.id} - Sobrevivió: {self.survived}"