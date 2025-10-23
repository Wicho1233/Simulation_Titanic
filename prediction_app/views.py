import joblib
import numpy as np
import pandas as pd
from django.shortcuts import render
from .forms import TitanicForm

def load_model():
    """
    Cargar el modelo entrenado, scaler y orden de características
    """
    try:
        model = joblib.load('prediction_app/ml_model/logistic_regression_model.pkl')
        scaler = joblib.load('prediction_app/ml_model/scaler.pkl')
        feature_order = joblib.load('prediction_app/ml_model/feature_order.pkl')
        print(" Modelo cargado correctamente")
        return model, scaler, feature_order
    except Exception as e:
        print(f"Error cargando modelo: {e}")
        return None, None, None

def preprocess_input(pclass, sex, age, embarked):
    """
    Preprocesar la entrada y convertir a numpy array sin nombres
    Orden: ['Pclass', 'Sex', 'Age', 'Embarked_C', 'Embarked_Q', 'Embarked_S']
    """
    
    # Crear array en el orden correcto
    input_data = [
        int(pclass),                    # Pclass
        1 if sex == 'male' else 0,      # Sex (male=1, female=0)
        float(age),                     # Age
        1 if embarked == 'C' else 0,    # Embarked_C
        1 if embarked == 'Q' else 0,    # Embarked_Q
        1 if embarked == 'S' else 0     # Embarked_S
    ]
    
    print(f"Datos preprocesados: {input_data}")
    return np.array([input_data])

def index(request):
    """
    Vista principal para el formulario de predicción
    """
    if request.method == 'POST':
        print("Formulario recibido via POST")
        form = TitanicForm(request.POST)
        
        if form.is_valid():
            print("Formulario válido")
            
            # Obtener datos limpios del formulario
            pclass = form.cleaned_data['pclass']
            sex = form.cleaned_data['sex']
            age = form.cleaned_data['age']
            embarked = form.cleaned_data['embarked']
            
            print(f" Datos del usuario: Clase={pclass}, Sexo={sex}, Edad={age}, Embarque={embarked}")
            
            # Cargar modelo y recursos
            model, scaler, feature_order = load_model()
            
            if model and scaler:
                try:
                    # Preprocesar entrada como numpy array
                    input_array = preprocess_input(pclass, sex, age, embarked)
                    
                    # Escalar los datos
                    input_scaled = scaler.transform(input_array)
                    print("Datos escalados correctamente")
                    
                    # Realizar predicción
                    prediction = model.predict(input_scaled)[0]
                    probability = model.predict_proba(input_scaled)[0]
                    
                    print(f"Predicción: {prediction}, Probabilidades: {probability}")
                    
                    # Interpretar resultados
                    survived = bool(prediction)
                    survival_prob = probability[1] * 100  # Probabilidad de sobrevivir
                    death_prob = probability[0] * 100     # Probabilidad de no sobrevivir
                    
                    # Obtener etiquetas legibles para mostrar
                    pclass_label = dict(form.fields['pclass'].choices).get(pclass)
                    sex_label = dict(form.fields['sex'].choices).get(sex)
                    embarked_label = dict(form.fields['embarked'].choices).get(embarked)
                    
                    print(f" Etiquetas: Clase={pclass_label}, Sexo={sex_label}, Embarque={embarked_label}")
                    
                    # Preparar contexto para el template
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
                    
                    print("Enviando resultado al template")
                    return render(request, 'prediction_app/result.html', context)
                    
                except Exception as e:
                    error_message = f"Error en la predicción: {str(e)}"
                    print(f"Error en predicción: {e}")
                    
                    return render(request, 'prediction_app/index.html', {
                        'form': form,
                        'error_message': error_message
                    })
            else:
                error_message = "Modelo no disponible. Por favor, contacte al administrador."
                print(" Modelo no disponible")
                
                return render(request, 'prediction_app/index.html', {
                    'form': form,
                    'error_message': error_message
                })
        else:
            print("Formulario inválido")
            return render(request, 'prediction_app/index.html', {
                'form': form,
                'error_message': 'Por favor, corrige los errores en el formulario.'
            })
    
    else:
        # GET request - mostrar formulario vacío
        print("Mostrando formulario vacío (GET)")
        form = TitanicForm()
    
    return render(request, 'prediction_app/index.html', {'form': form})

def ejemplo_sobrevive(request):
    """
    Vista que precarga datos de ejemplo que SÍ sobreviven
    Mujer, Primera Clase, 28 años, Cherbourg
    """
    print("Cargando ejemplo que SÍ sobrevive")
    
    # Datos que generalmente sobreviven
    initial_data = {
        'pclass': '1',
        'sex': 'female', 
        'age': 28,
        'embarked': 'C'
    }
    
    form = TitanicForm(initial=initial_data)
    
    # Cargar modelo y recursos
    model, scaler, feature_order = load_model()
    
    if model and scaler:
        try:
            # Preprocesar entrada como numpy array
            input_array = preprocess_input('1', 'female', 28, 'C')
            
            # Escalar los datos
            input_scaled = scaler.transform(input_array)
            print("Datos de ejemplo escalados correctamente")
            
            # Realizar predicción
            prediction = model.predict(input_scaled)[0]
            probability = model.predict_proba(input_scaled)[0]
            
            print(f" Predicción ejemplo: {prediction}, Probabilidades: {probability}")
            
            # Interpretar resultados
            survived = bool(prediction)
            survival_prob = probability[1] * 100
            death_prob = probability[0] * 100
            
            # Preparar contexto para el template
            context = {
                'survived': survived,
                'survival_prob': round(survival_prob, 2),
                'death_prob': round(death_prob, 2),
                'age': 28,
                'pclass': 'Primera Clase',
                'sex': 'Mujer',
                'embarked': 'Cherbourg',
                'es_ejemplo': True
            }
            
            print("Enviando resultado de ejemplo al template")
            return render(request, 'prediction_app/result.html', context)
            
        except Exception as e:
            error_message = f"Error en la predicción del ejemplo: {str(e)}"
            print(f"Error en predicción de ejemplo: {e}")
            
            # Si hay error, mostrar el formulario precargado
            return render(request, 'prediction_app/index.html', {
                'form': form,
                'error_message': error_message
            })
    
    # Si el modelo no está disponible
    error_message = 'Modelo no disponible. No se puede realizar la predicción.'
    print(" Modelo no disponible para ejemplo")
    
    return render(request, 'prediction_app/index.html', {
        'form': form,
        'error_message': error_message
    })

def ejemplo_no_sobrevive(request):
    """
    Vista que precarga datos de ejemplo que NO sobreviven
    Hombre, Tercera Clase, 35 años, Southampton
    """
    print("Cargando ejemplo que NO sobrevive")
    
    # Datos que generalmente NO sobreviven
    initial_data = {
        'pclass': '3',
        'sex': 'male', 
        'age': 35,
        'embarked': 'S'
    }
    
    form = TitanicForm(initial=initial_data)
    
    # Cargar modelo y recursos
    model, scaler, feature_order = load_model()
    
    if model and scaler:
        try:
            # Preprocesar entrada como numpy array
            input_array = preprocess_input('3', 'male', 35, 'S')
            
            # Escalar los datos
            input_scaled = scaler.transform(input_array)
            print("Datos de ejemplo (no sobrevive) escalados correctamente")
            
            # Realizar predicción
            prediction = model.predict(input_scaled)[0]
            probability = model.predict_proba(input_scaled)[0]
            
            print(f" Predicción ejemplo (no): {prediction}, Probabilidades: {probability}")
            
            # Interpretar resultados
            survived = bool(prediction)
            survival_prob = probability[1] * 100
            death_prob = probability[0] * 100
            
            # Preparar contexto para el template
            context = {
                'survived': survived,
                'survival_prob': round(survival_prob, 2),
                'death_prob': round(death_prob, 2),
                'age': 35,
                'pclass': 'Tercera Clase',
                'sex': 'Hombre',
                'embarked': 'Southampton',
                'es_ejemplo': True
            }
            
            print("Enviando resultado de ejemplo (no) al template")
            return render(request, 'prediction_app/result.html', context)
            
        except Exception as e:
            error_message = f"Error en la predicción del ejemplo: {str(e)}"
            print(f" Error en predicción de ejemplo (no): {e}")
            
            # Si hay error, mostrar el formulario precargado
            return render(request, 'prediction_app/index.html', {
                'form': form,
                'error_message': error_message
            })
    
    # Si el modelo no está disponible
    error_message = 'Modelo no disponible. No se puede realizar la predicción.'
    print(" Modelo no disponible para ejemplo (no)")
    
    return render(request, 'prediction_app/index.html', {
        'form': form,
        'error_message': error_message
    })

def estadisticas(request):
    """
    Vista opcional para mostrar estadísticas del Titanic
    """
    print("📊 Mostrando estadísticas")
    
    estadisticas_data = {
        'supervivencia_general': '38%',
        'mujeres_sobrevivieron': '74%',
        'hombres_sobrevivieron': '19%',
        'primera_clase_sobrevivio': '63%',
        'segunda_clase_sobrevivio': '47%',
        'tercera_clase_sobrevivio': '24%',
        'niños_sobrevivieron': '52%'
    }
    
    return render(request, 'prediction_app/estadisticas.html', {
        'estadisticas': estadisticas_data
    })