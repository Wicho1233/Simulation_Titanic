import joblib
import numpy as np
from django.shortcuts import render
from .forms import TitanicForm

def load_model():
    """Cargar modelo, scaler y feature order"""
    try:
        model_path = 'prediction_app/ml_model/logistic_regression_model.pkl'
        scaler_path = 'prediction_app/ml_model/scaler.pkl'
        feature_path = 'prediction_app/ml_model/feature_order.pkl'
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        feature_order = joblib.load(feature_path)
        
        print("✅ Modelo cargado correctamente")
        return model, scaler, feature_order
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return None, None, None

def preprocess_input(pclass, sex, age, embarked):
    """Preprocesar entrada para el modelo"""
    input_data = [
        int(pclass),
        1 if sex == 'male' else 0,
        float(age),
        1 if embarked == 'C' else 0,
        1 if embarked == 'Q' else 0,
        1 if embarked == 'S' else 0
    ]
    return np.array([input_data])

def index(request):
    """Vista principal"""
    if request.method == 'POST':
        form = TitanicForm(request.POST)
        
        if form.is_valid():
            pclass = form.cleaned_data['pclass']
            sex = form.cleaned_data['sex']
            age = form.cleaned_data['age']
            embarked = form.cleaned_data['embarked']
            
            model, scaler, feature_order = load_model()
            
            if model and scaler:
                try:
                    input_array = preprocess_input(pclass, sex, age, embarked)
                    input_scaled = scaler.transform(input_array)
                    
                    prediction = model.predict(input_scaled)[0]
                    probability = model.predict_proba(input_scaled)[0]
                    
                    survived = bool(prediction)
                    survival_prob = probability[1] * 100
                    death_prob = probability[0] * 100
                    
                    pclass_label = dict(form.fields['pclass'].choices).get(pclass)
                    sex_label = dict(form.fields['sex'].choices).get(sex)
                    embarked_label = dict(form.fields['embarked'].choices).get(embarked)
                    
                    context = {
                        'survived': survived,
                        'survival_prob': round(survival_prob, 2),
                        'death_prob': round(death_prob, 2),
                        'age': age,
                        'pclass': pclass_label,
                        'sex': sex_label,
                        'embarked': embarked_label,
                        'es_ejemplo': False
                    }
                    
                    return render(request, 'prediction_app/result.html', context)
                    
                except Exception as e:
                    return render(request, 'prediction_app/index.html', {
                        'form': form,
                        'error_message': f'Error en predicción: {str(e)}'
                    })
            else:
                return render(request, 'prediction_app/index.html', {
                    'form': form,
                    'error_message': 'Modelo no disponible'
                })
        else:
            return render(request, 'prediction_app/index.html', {
                'form': form,
                'error_message': 'Por favor corrige los errores'
            })
    
    else:
        form = TitanicForm()
    
    return render(request, 'prediction_app/index.html', {'form': form})

def ejemplo_sobrevive(request):
    """Ejemplo que sobrevive"""
    initial_data = {'pclass': '1', 'sex': 'female', 'age': 28, 'embarked': 'C'}
    return process_ejemplo(request, initial_data, 'Mujer', 'Primera Clase', 'Cherbourg')

def ejemplo_no_sobrevive(request):
    """Ejemplo que no sobrevive"""
    initial_data = {'pclass': '3', 'sex': 'male', 'age': 35, 'embarked': 'S'}
    return process_ejemplo(request, initial_data, 'Hombre', 'Tercera Clase', 'Southampton')

def process_ejemplo(request, initial_data, sex_label, pclass_label, embarked_label):
    """Procesar ejemplo común"""
    model, scaler, feature_order = load_model()
    
    if model and scaler:
        try:
            input_array = preprocess_input(
                initial_data['pclass'], 
                initial_data['sex'], 
                initial_data['age'], 
                initial_data['embarked']
            )
            input_scaled = scaler.transform(input_array)
            
            prediction = model.predict(input_scaled)[0]
            probability = model.predict_proba(input_scaled)[0]
            
            context = {
                'survived': bool(prediction),
                'survival_prob': round(probability[1] * 100, 2),
                'death_prob': round(probability[0] * 100, 2),
                'age': initial_data['age'],
                'pclass': pclass_label,
                'sex': sex_label,
                'embarked': embarked_label,
                'es_ejemplo': True
            }
            
            return render(request, 'prediction_app/result.html', context)
            
        except Exception as e:
            form = TitanicForm(initial=initial_data)
            return render(request, 'prediction_app/index.html', {
                'form': form,
                'error_message': f'Error: {str(e)}'
            })
    
    form = TitanicForm(initial=initial_data)
    return render(request, 'prediction_app/index.html', {
        'form': form,
        'error_message': 'Modelo no disponible'
    })

def estadisticas(request):
    """Vista de estadísticas"""
    estadisticas_data = {
        'supervivencia_general': '38%',
        'mujeres_sobrevivieron': '74%',
        'hombres_sobrevivieron': '19%',
        'primera_clase_sobrevivio': '63%',
        'segunda_clase_sobrevivio': '47%',
        'tercera_clase_sobrevivio': '24%',
    }
    
    return render(request, 'prediction_app/estadisticas.html', {
        'estadisticas': estadisticas_data
    })