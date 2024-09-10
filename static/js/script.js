// Validação de formulário no cliente
document.addEventListener('DOMContentLoaded', function () {
    var forms = document.getElementsByClassName('needs-validation');
    Array.prototype.forEach.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}, false);

// Validação específica para o campo de código de barras
document.getElementById('barcode').addEventListener('input', function (event) {
    var barcode = event.target.value;
    if (isNaN(barcode)) {
        event.target.setCustomValidity('O código de barras deve ser um número.');
        event.target.reportValidity();
    } else {
        event.target.setCustomValidity('');
    }
});

// Função para exibir mensagens de alerta dinâmicas
function showAlert(message, type) {
    var alertPlaceholder = document.getElementById('alert-placeholder');
    var alertHTML = `<div class="alert alert-${type} alert-dismissible fade show" role="alert" aria-live="assertive" aria-atomic="true">
                        ${message}
                        <button type="button" class="close" data-dismiss="alert" aria-label="Fechar">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>`;
    alertPlaceholder.innerHTML = alertHTML;

    // Alerta desaparece após 5 segundos
    setTimeout(function () {
        $('.alert').alert('close');
    }, 5000);
}

// Função para mostrar o spinner de carregamento
function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

// Feedback visual para formulários
document.querySelectorAll('.form-control').forEach(function(input) {
    input.addEventListener('input', function() {
        if (input.checkValidity()) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
        }
    });
});