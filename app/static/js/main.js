// Auto dismiss alerts
document.addEventListener('DOMContentLoaded', function() {
    // Alert otomatik kapanma
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-info)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });




});// Sayfa yüklenince
document.addEventListener('DOMContentLoaded', function() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    // Admin kontrolü
    if (user.kullanici_rol === 'admin' || user.rol === 'admin' || user.role === 'admin') {
        document.getElementById('adminMenuItem').style.display = 'block';
    }
});