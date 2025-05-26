document.addEventListener("DOMContentLoaded", function () {
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');
    const form = document.getElementById('register-form');

    if (!password1 || !password2 || !form) return;

    const passwordMessage = document.createElement('div');
    passwordMessage.style.color = 'red';
    password1.parentNode.appendChild(passwordMessage);

    const confirmMessage = document.createElement('div');
    confirmMessage.style.color = 'red';
    password2.parentNode.appendChild(confirmMessage);

    function validatePasswordStrength(pwd) {
      const minLength = 8;
      const hasUpper = /[A-Z]/.test(pwd);
      const hasLower = /[a-z]/.test(pwd);
      const hasNumber = /\d/.test(pwd);
      const hasSpecial = /[@$!%*?&]/.test(pwd);

      if (pwd.length < minLength) return "Password must be at least 8 characters long.";
      if (!hasUpper) return "Password must include at least one uppercase letter.";
      if (!hasLower) return "Password must include at least one lowercase letter.";
      if (!hasNumber) return "Password must include at least one number.";
      if (!hasSpecial) return "Password must include at least one special character (@$!%*?&).";

      return ""; // Valid
    }

    password1.addEventListener('input', () => {
      const msg = validatePasswordStrength(password1.value);
      passwordMessage.textContent = msg;
    });
     password1.addEventListener('blur', () => {
      const msg = validatePasswordStrength(password1.value);
      passwordMessage.textContent = msg;
    });

    password2.addEventListener('input', () => {
      confirmMessage.textContent = password2.value !== password1.value ? "Passwords do not match." : "";
    });

    form.addEventListener('submit', (e) => {
      const pwdError = validatePasswordStrength(password1.value);
      if (pwdError || password1.value !== password2.value) {
        e.preventDefault();
        passwordMessage.textContent = pwdError;
        confirmMessage.textContent = password1.value !== password2.value ? "Passwords do not match." : "";
      }
    });

    // Fade out success message after 5 seconds
    const successMessages = document.querySelectorAll('.success');
    if (successMessages.length > 0) {
      setTimeout(() => {
        successMessages.forEach(msg => {
          msg.style.transition = 'opacity 1s ease-out';
          msg.style.opacity = '0';
          setTimeout(() => msg.remove(), 1000);
        });
      }, 5000);
    }
  });
