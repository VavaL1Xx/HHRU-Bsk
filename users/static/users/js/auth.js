document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();
        
        xhr.open('POST', form.action, true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                const response = JSON.parse(xhr.responseText);
                if (response.success) {
                    window.location.href = '/users/login/';
                } else {
                    alert('Ошибка регистрации');
                }
            } else {
                alert('Ошибка сервера');
            }
        };

        xhr.send(formData);
    });
});