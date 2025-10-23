// Titanic Predictor - JavaScript Completo
document.addEventListener('DOMContentLoaded', function() {
    console.log('Titanic Predictor - JavaScript cargado');
    
    // ===== VALIDACIÓN DE FORMULARIO =====
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Validación al enviar
        form.addEventListener('submit', function(event) {
            console.log('Validando formulario...');
            let isValid = true;
            const inputs = form.querySelectorAll('input, select');
            
            // Remover mensajes de error previos
            clearErrorMessages();
            
            // Validar cada campo
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                    showFieldError(input, getErrorMessage(input));
                    console.log(`Campo inválido: ${input.name}`);
                }
            });
            
            // Validación adicional para edad
            const ageInput = form.querySelector('input[type="number"]');
            if (ageInput && !validateAge(ageInput.value)) {
                isValid = false;
                showFieldError(ageInput, 'La edad debe estar entre 0 y 100 años');
                console.log('Edad inválida');
            }
            
            if (!isValid) {
                event.preventDefault();
                console.log('Formulario inválido, enviado bloqueado');
                showNotification('Por favor corrige los errores en el formulario', 'error');
            } else {
                console.log('Formulario válido, enviando...');
            }
        });
        
        // Validación en tiempo real
        form.addEventListener('input', function(event) {
            const target = event.target;
            if (target.tagName === 'INPUT' || target.tagName === 'SELECT') {
                clearFieldError(target);
                if (validateField(target)) {
                    showFieldSuccess(target);
                }
            }
        });
        
        // Cambio en selects
        form.addEventListener('change', function(event) {
            const target = event.target;
            if (target.tagName === 'SELECT') {
                clearFieldError(target);
                if (validateField(target)) {
                    showFieldSuccess(target);
                }
            }
        });
    });
    
    // ===== MEJORAS DE USABILIDAD =====
    enhanceSelectElements();
    setupAutoFocus();
    setupQuickFillButtons();
    
    // ===== MANEJO DE BOTONES ESPECIALES =====
    setupExampleButtons();
});

// ===== FUNCIONES DE VALIDACIÓN =====
function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const tagName = field.tagName.toLowerCase();
    
    if (tagName === 'select') {
        return value !== '';
    }
    
    switch (type) {
        case 'number':
            return validateNumber(field);
        case 'text':
            return value !== '';
        default:
            return value !== '';
    }
}

function validateNumber(field) {
    const value = parseFloat(field.value);
    const min = parseFloat(field.min) || 0;
    const max = parseFloat(field.max) || 100;
    
    if (field.value === '') {
        return false;
    }
    
    return !isNaN(value) && value >= min && value <= max;
}

function validateAge(age) {
    if (age === '') {
        return false;
    }
    
    const ageNum = parseFloat(age);
    return !isNaN(ageNum) && ageNum >= 0 && ageNum <= 100;
}

function getErrorMessage(field) {
    const type = field.type;
    const tagName = field.tagName.toLowerCase();
    
    if (tagName === 'select') {
        return 'Por favor selecciona una opción';
    }
    
    switch (type) {
        case 'number':
            const min = field.min || 0;
            const max = field.max || 100;
            return `Por favor ingresa una edad válida entre ${min} y ${max} años`;
        default:
            return 'Este campo es requerido';
    }
}

// ===== MANEJO DE ERRORES =====
function showFieldError(field, message) {
    // Remover éxito previo
    field.classList.remove('is-valid');
    
    // Agregar clases de error
    field.classList.add('is-invalid');
    
    // Remover mensaje de error existente
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
    
    // Crear elemento de error
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    // Insertar después del campo
    field.parentNode.appendChild(errorDiv);
}

function showFieldSuccess(field) {
    // Remover error previo
    field.classList.remove('is-invalid');
    clearFieldError(field);
    
    // Agregar clase de éxito
    field.classList.add('is-valid');
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

function clearErrorMessages() {
    const errorMessages = document.querySelectorAll('.invalid-feedback');
    errorMessages.forEach(msg => msg.remove());
    
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.classList.remove('is-invalid');
    });
}

// ===== MEJORAS DE USABILIDAD =====
function enhanceSelectElements() {
    const selects = document.querySelectorAll('select');
    
    selects.forEach(select => {
        // Agregar placeholder visual si no hay selección
        if (!select.value) {
            select.style.color = '#6c757d';
        }
        
        select.addEventListener('change', function() {
            if (this.value) {
                this.style.color = '#000';
            } else {
                this.style.color = '#6c757d';
            }
        });
    });
}

function setupAutoFocus() {
    const firstInput = document.querySelector('input, select');
    if (firstInput) {
        setTimeout(() => {
            firstInput.focus();
        }, 100);
    }
}

function setupQuickFillButtons() {
    // Buscar si existe un contenedor para botones rápidos
    const form = document.querySelector('form');
    if (!form) return;
    
    // Agregar botones rápidos si no existen
    if (!document.querySelector('.quick-fill-buttons')) {
        const ageContainer = form.querySelector('input[name="age"]')?.parentNode;
        if (ageContainer) {
            const quickButtons = document.createElement('div');
            quickButtons.className = 'quick-fill-buttons mt-2';
            quickButtons.innerHTML = `
                <small class="text-muted">Rápido: </small>
                <button type="button" class="btn btn-sm btn-outline-secondary" onclick="setAge(20)">20</button>
                <button type="button" class="btn btn-sm btn-outline-secondary" onclick="setAge(35)">35</button>
                <button type="button" class="btn btn-sm btn-outline-secondary" onclick="setAge(50)">50</button>
            `;
            ageContainer.appendChild(quickButtons);
        }
    }
}

function setupExampleButtons() {
    // Botón para cargar ejemplo que sobrevive
    const surviveExampleBtn = document.getElementById('survive-example');
    if (surviveExampleBtn) {
        surviveExampleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            loadSurviveExample();
        });
    }
    
    // Botón para cargar ejemplo que no sobrevive
    const notSurviveExampleBtn = document.getElementById('not-survive-example');
    if (notSurviveExampleBtn) {
        notSurviveExampleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            loadNotSurviveExample();
        });
    }
}

// ===== FUNCIONES DE EJEMPLOS =====
function loadSurviveExample() {
    console.log('Cargando ejemplo de supervivencia...');
    fillForm({
        pclass: '1',
        sex: 'female',
        age: '28',
        embarked: 'C'
    });
    showNotification('Ejemplo cargado: Mujer, Primera Clase, 28 años, Cherbourg - Alta probabilidad de supervivencia', 'info');
}

function loadNotSurviveExample() {
    console.log('Cargando ejemplo de no supervivencia...');
    fillForm({
        pclass: '3',
        sex: 'male',
        age: '35',
        embarked: 'S'
    });
    showNotification('Ejemplo cargado: Hombre, Tercera Clase, 35 años, Southampton - Alta probabilidad de no supervivencia', 'info');
}

function fillForm(data) {
    const form = document.querySelector('form');
    if (!form) return;
    
    // Llenar campos
    for (const [key, value] of Object.entries(data)) {
        const field = form.querySelector(`[name="${key}"]`);
        if (field) {
            field.value = value;
            
            // Disparar evento change para selects
            if (field.tagName === 'SELECT') {
                field.dispatchEvent(new Event('change'));
            }
            
            // Disparar evento input para inputs
            if (field.tagName === 'INPUT') {
                field.dispatchEvent(new Event('input'));
            }
            
            // Aplicar estilos de validación
            showFieldSuccess(field);
        }
    }
}

// ===== FUNCIONES UTILITARIAS =====
function setAge(age) {
    const ageInput = document.querySelector('input[name="age"]');
    if (ageInput) {
        ageInput.value = age;
        ageInput.dispatchEvent(new Event('input'));
        showFieldSuccess(ageInput);
    }
}

window.clearForm = function() {
    const form = document.querySelector('form');
    if (form) {
        form.reset();
        clearErrorMessages();
        
        // Resetear estilos de selects
        const selects = form.querySelectorAll('select');
        selects.forEach(select => {
            select.style.color = '#6c757d';
            select.classList.remove('is-valid', 'is-invalid');
        });
        
        // Resetear estilos de inputs
        const inputs = form.querySelectorAll('input');
        inputs.forEach(input => {
            input.classList.remove('is-valid', 'is-invalid');
        });
        
        showNotification('Formulario limpiado', 'info');
    }
};

window.submitForm = function() {
    const form = document.querySelector('form');
    if (form) {
        form.dispatchEvent(new Event('submit'));
    }
};

// ===== NOTIFICACIONES =====
function showNotification(message, type = 'info') {
    // Remover notificación previa si existe
    const existingNotification = document.querySelector('.custom-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Crear notificación
    const notification = document.createElement('div');
    notification.className = `custom-notification alert alert-${getAlertType(type)}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1050;
        min-width: 300px;
        max-width: 500px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    `;
    
    notification.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <span>${message}</span>
            <button type="button" class="btn-close" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remover después de 5 segundos
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function getAlertType(type) {
    const types = {
        'error': 'danger',
        'success': 'success',
        'warning': 'warning',
        'info': 'info'
    };
    return types[type] || 'info';
}

// ===== ATAJOS DE TECLADO =====
document.addEventListener('keydown', function(event) {
    // Ctrl + Enter para enviar formulario
    if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault();
        submitForm();
    }
    
    // Escape para limpiar formulario
    if (event.key === 'Escape') {
        event.preventDefault();
        clearForm();
    }
    
    // F1 para ejemplo que sobrevive
    if (event.key === 'F1') {
        event.preventDefault();
        loadSurviveExample();
    }
    
    // F2 para ejemplo que no sobrevive
    if (event.key === 'F2') {
        event.preventDefault();
        loadNotSurviveExample();
    }
});

// ===== INICIALIZACIÓN =====
// Verificar si hay parámetros en la URL para cargar ejemplos
function checkUrlParameters() {
    const urlParams = new URLSearchParams(window.location.search);
    const example = urlParams.get('example');
    
    if (example === 'survive') {
        setTimeout(loadSurviveExample, 100);
    } else if (example === 'notsurvive') {
        setTimeout(loadNotSurviveExample, 100);
    }
}

// Ejecutar al cargar la página
checkUrlParameters();

console.log('Titanic Predictor - JavaScript inicializado correctamente');