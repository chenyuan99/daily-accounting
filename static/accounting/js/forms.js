// Form handling and loading states
document.addEventListener('DOMContentLoaded', function() {
    // Handle all forms with the form-loading-button class
    document.querySelectorAll('form.form-loading-button').forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });

    // Initialize datepicker on all elements with datepicker class
    document.querySelectorAll('.datepicker').forEach(elem => {
        flatpickr(elem, {
            enableTime: true,
            dateFormat: "Y-m-d H:i",
            defaultDate: new Date()
        });
    });

    // Initialize currency inputs
    document.querySelectorAll('.currency-input').forEach(input => {
        input.addEventListener('input', formatCurrencyInput);
    });
});

function handleFormSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const submitButton = form.querySelector('button[type="submit"]');
    const originalButtonText = submitButton.innerHTML;

    // Show loading state
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';

    // Clear previous error messages
    form.querySelectorAll('.invalid-feedback').forEach(elem => elem.remove());
    form.querySelectorAll('.is-invalid').forEach(elem => elem.classList.remove('is-invalid'));

    // Submit form data
    fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Show success message using toast
            showToast('Success', data.message, 'success');
            
            // Redirect if specified
            if (data.redirect) {
                setTimeout(() => {
                    window.location.href = data.redirect;
                }, 1500);
            }
        } else {
            // Handle validation errors
            Object.entries(data.errors).forEach(([field, errors]) => {
                const input = form.querySelector(`[name="${field}"]`);
                if (input) {
                    input.classList.add('is-invalid');
                    const feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    feedback.textContent = errors.join(' ');
                    input.parentNode.appendChild(feedback);
                }
            });
            
            // Show error message using toast
            showToast('Error', 'Please correct the errors in the form', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Error', 'An unexpected error occurred', 'error');
    })
    .finally(() => {
        // Reset button state
        submitButton.disabled = false;
        submitButton.innerHTML = originalButtonText;
    });
}

function formatCurrencyInput(event) {
    let input = event.target;
    let value = input.value.replace(/[^\d.]/g, '');
    
    // Ensure only two decimal places
    let parts = value.split('.');
    if (parts.length > 1) {
        parts[1] = parts[1].slice(0, 2);
        value = parts.join('.');
    }
    
    input.value = value;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showToast(title, message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="toast-header">
            <strong class="me-auto">${title}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    const toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        const container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
    }
    
    document.querySelector('.toast-container').appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', () => {
        toast.remove();
    });
}
