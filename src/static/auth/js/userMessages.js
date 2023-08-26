function hideMessages() {

    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(function(message) {
        message.style.background = '#FF0000';
    });

    const successMessages = document.querySelectorAll('.success-message');
    successMessages.forEach(function(message) {
        message.style.background = '#4BB543';
    });

    setTimeout(function() {
        const messages = document.querySelectorAll('.messages li');
        messages.forEach(function(message) {
            message.style.display = 'none';
        });
    }, 5000);
}

window.onload = function() {
    hideMessages();
}