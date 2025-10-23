from django import forms

class TitanicForm(forms.Form):
    PCLASS_CHOICES = [
        ('', 'Selecciona tu clase'),
        ('1', 'Primera Clase'),
        ('2', 'Segunda Clase'),
        ('3', 'Tercera Clase')
    ]
    
    SEX_CHOICES = [
        ('', 'Selecciona tu sexo'),
        ('male', 'Hombre'),
        ('female', 'Mujer')
    ]
    
    EMBARKED_CHOICES = [
        ('', 'Selecciona puerto de embarque'),
        ('C', 'Cherbourg'),
        ('Q', 'Queenstown'),
        ('S', 'Southampton')
    ]
    
    pclass = forms.ChoiceField(
        choices=PCLASS_CHOICES,
        label='Clase del Pasajero',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    
    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        label='Sexo',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    
    age = forms.FloatField(
        label='Edad',
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu edad (0-100)',
            'required': 'required',
            'step': '0.1'
        })
    )
    
    embarked = forms.ChoiceField(
        choices=EMBARKED_CHOICES,
        label='Puerto de Embarque',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 0 or age > 100):
            raise forms.ValidationError('La edad debe estar entre 0 y 100 años.')
        return age