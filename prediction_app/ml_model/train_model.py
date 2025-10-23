import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_titanic_model():
    # Cargar datos
    train_data = pd.read_csv('prediction_app/ml_model/train.csv')
    
    # Preprocesamiento
    train_data['Age'].fillna(train_data['Age'].median(), inplace=True)
    train_data['Sex'] = train_data['Sex'].map({'male': 1, 'female': 0})
    
    # One-hot encoding para Embarked
    embarked_dummies = pd.get_dummies(train_data['Embarked'], prefix='Embarked')
    train_data = pd.concat([train_data, embarked_dummies], axis=1)
    
    # Seleccionar características - USAR SOLO VALORES NUMÉRICOS
    features = ['Pclass', 'Sex', 'Age', 'Embarked_C', 'Embarked_Q', 'Embarked_S']
    X = train_data[features].values  # Convertir a numpy array sin nombres
    y = train_data['Survived'].values
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Escalar características
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entrenar modelo
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # Evaluar modelo
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Precisión del modelo: {accuracy:.4f}")
    print("\nReporte de clasificación:")
    print(classification_report(y_test, y_pred))
    
    # Guardar modelo y scaler
    model_dir = 'prediction_app/ml_model'
    os.makedirs(model_dir, exist_ok=True)
    
    joblib.dump(model, os.path.join(model_dir, 'logistic_regression_model.pkl'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    
    # Guardar el orden de las características para referencia
    feature_order = {
        'features': features,
        'feature_order': ['Pclass', 'Sex', 'Age', 'Embarked_C', 'Embarked_Q', 'Embarked_S']
    }
    joblib.dump(feature_order, os.path.join(model_dir, 'feature_order.pkl'))
    
    print(f"Modelo guardado en {model_dir}/")
    print("Orden de características:", features)

if __name__ == '__main__':
    train_titanic_model()