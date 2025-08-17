// Plant Disease Detection - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const imagePreview = document.getElementById('imagePreview');
    const previewImage = document.getElementById('previewImage');
    const uploadForm = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const loadingState = document.getElementById('loadingState');

    // File input change handler
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            
            if (file) {
                // Validate file type
                if (!isValidImageType(file)) {
                    showAlert('Invalid file type. Please select an image file.', 'error');
                    clearFileInput();
                    return;
                }

                // Validate file size (16MB limit)
                if (file.size > 16 * 1024 * 1024) {
                    showAlert('File too large. Please select an image smaller than 16MB.', 'error');
                    clearFileInput();
                    return;
                }

                // Show image preview
                showImagePreview(file);
                
                // Add visual feedback
                fileInput.classList.add('is-valid');
                fileInput.classList.remove('is-invalid');
            } else {
                hideImagePreview();
                fileInput.classList.remove('is-valid', 'is-invalid');
            }
        });
    }

    // Form submission handler
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            if (!validateForm()) {
                e.preventDefault();
                return;
            }

            // Show loading state
            showLoadingState();
        });
    }

    // Drag and drop functionality
    setupDragAndDrop();

    // Auto-dismiss alerts
    setupAutoDismissAlerts();
});

/**
 * Validate if file is a valid image type
 */
function isValidImageType(file) {
    const validTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif', 'image/bmp', 'image/webp'];
    return validTypes.includes(file.type);
}

/**
 * Show image preview
 */
function showImagePreview(file) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const previewImage = document.getElementById('previewImage');
        const imagePreview = document.getElementById('imagePreview');
        
        if (previewImage && imagePreview) {
            previewImage.src = e.target.result;
            imagePreview.style.display = 'block';
            
            // Add fade-in animation
            imagePreview.style.opacity = '0';
            setTimeout(() => {
                imagePreview.style.transition = 'opacity 0.3s ease';
                imagePreview.style.opacity = '1';
            }, 10);
        }
    };
    
    reader.readAsDataURL(file);
}

/**
 * Hide image preview
 */
function hideImagePreview() {
    const imagePreview = document.getElementById('imagePreview');
    if (imagePreview) {
        imagePreview.style.display = 'none';
    }
}

/**
 * Clear file input
 */
function clearFileInput() {
    const fileInput = document.getElementById('file');
    if (fileInput) {
        fileInput.value = '';
        hideImagePreview();
        fileInput.classList.remove('is-valid', 'is-invalid');
    }
}

/**
 * Validate form before submission
 */
function validateForm() {
    const fileInput = document.getElementById('file');
    
    if (!fileInput || !fileInput.files[0]) {
        showAlert('Please select an image file to analyze.', 'error');
        fileInput.classList.add('is-invalid');
        return false;
    }

    const file = fileInput.files[0];
    
    if (!isValidImageType(file)) {
        showAlert('Invalid file type. Please select an image file.', 'error');
        fileInput.classList.add('is-invalid');
        return false;
    }

    if (file.size > 16 * 1024 * 1024) {
        showAlert('File too large. Please select an image smaller than 16MB.', 'error');
        fileInput.classList.add('is-invalid');
        return false;
    }

    return true;
}

/**
 * Show loading state during form submission
 */
function showLoadingState() {
    const submitBtn = document.getElementById('submitBtn');
    const loadingState = document.getElementById('loadingState');
    
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Analyzing...';
    }
    
    if (loadingState) {
        loadingState.style.display = 'block';
    }
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert-custom');
    existingAlerts.forEach(alert => alert.remove());

    const alertDiv = document.createElement('div');
    const alertClass = type === 'error' ? 'alert-danger' : 'alert-success';
    const icon = type === 'error' ? 'exclamation-triangle' : 'check-circle';
    
    alertDiv.className = `alert ${alertClass} alert-dismissible fade show alert-custom`;
    alertDiv.innerHTML = `
        <i class="fas fa-${icon} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv && alertDiv.parentNode) {
                alertDiv.classList.remove('show');
                setTimeout(() => {
                    if (alertDiv && alertDiv.parentNode) {
                        alertDiv.remove();
                    }
                }, 300);
            }
        }, 5000);
    }
}

/**
 * Setup drag and drop functionality
 */
function setupDragAndDrop() {
    const fileInput = document.getElementById('file');
    const uploadArea = fileInput?.closest('.card-body');
    
    if (!uploadArea || !fileInput) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    uploadArea.addEventListener('drop', handleDrop, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        uploadArea.classList.add('border-success');
        uploadArea.style.backgroundColor = 'rgba(40, 167, 69, 0.1)';
    }

    function unhighlight() {
        uploadArea.classList.remove('border-success');
        uploadArea.style.backgroundColor = '';
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            fileInput.files = files;
            // Trigger change event
            const event = new Event('change', { bubbles: true });
            fileInput.dispatchEvent(event);
        }
    }
}

/**
 * Setup auto-dismiss for alerts
 */
function setupAutoDismissAlerts() {
    // Auto-dismiss existing alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-custom)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.classList.remove('show');
                setTimeout(() => {
                    if (alert && alert.parentNode) {
                        alert.remove();
                    }
                }, 300);
            }
        }, 5000);
    });
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Copy result to clipboard (future feature)
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Results copied to clipboard!', 'success');
    }).catch(() => {
        showAlert('Failed to copy to clipboard.', 'error');
    });
}
