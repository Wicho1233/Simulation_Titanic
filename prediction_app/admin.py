from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'pclass', 'sex', 'age', 'survived', 'probability', 'created_at']
    list_filter = ['survived', 'pclass', 'sex']