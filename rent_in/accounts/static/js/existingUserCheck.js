document.addEventListener('DOMContentLoaded', function () {
  const usernameInput = document.getElementById('id_username');
  const emailInput = document.getElementById('id_email');
  const submitButton = document.querySelector('input[type="submit"]');

  function createMessageDiv(inputField) {
    const msg = document.createElement('div');
    msg.style.color = 'red';
    msg.style.marginTop = '5px';
    inputField.parentNode.appendChild(msg);
    return msg;
  }

  const usernameMsg = createMessageDiv(usernameInput);
  const emailMsg = createMessageDiv(emailInput);

  async function checkField(inputField, type, messageDiv) {
    const value = inputField.value.trim();
    if (!value) {
      messageDiv.textContent = '';
      submitButton.disabled = false;
      return;
    }

    try {
      const queryParam = type === 'username' ? `username=${encodeURIComponent(value)}` : `email=${encodeURIComponent(value)}`;
      const response = await fetch(`/ajax/check-user/?${queryParam}`);
      if (!response.ok) throw new Error('Network error');

      const data = await response.json();

      if (data.exists) {
        messageDiv.textContent = `${type === 'username' ? 'Phone number' : 'Email'} is already registered.`;
        submitButton.disabled = true;
      } else {
        messageDiv.textContent = '';
        submitButton.disabled = false;
      }
    } catch (err) {
      messageDiv.textContent = 'Could not validate. Try again later.';
      submitButton.disabled = false;
    }
  }

  usernameInput.addEventListener('input', () => checkField(usernameInput, 'username', usernameMsg));
  emailInput.addEventListener('input', () => checkField(emailInput, 'email', emailMsg));
});
