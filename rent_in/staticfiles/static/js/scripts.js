// // Basic example script to demonstrate dynamic behavior
// document.addEventListener('DOMContentLoaded', function() {
//     console.log('Blog page loaded');
// });

// document.addEventListener('DOMContentLoaded', function() {
//     console.log('Blog page loaded');
    
//     // Example: Toggle dark mode
//     const toggleButton = document.getElementById('toggle-dark-mode');
//     toggleButton.addEventListener('click', function() {
//         document.body.classList.toggle('dark-mode');
//     });
// });

document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded');

    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();  // Prevent default form submission
            console.log('Login form submitted');
            this.submit();  // Manually submit the form
        });
    }

    // Handle register form submission
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log('Register form submitted');
            this.submit();
        });
    }

    // Example: Toggle dark mode
    const toggleButton = document.getElementById('toggle-dark-mode');
    if (toggleButton) {
        toggleButton.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
        });
    }
});
