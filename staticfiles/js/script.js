// Validación básica del formulario
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const ageInput = form.querySelector('input[type="number"]');
            if (ageInput && !ageInput.value) {
                alert('Por favor ingresa tu edad');
                event.preventDefault();
            }
        });
    });
});