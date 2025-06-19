document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    if (!form) return;
  
    form.addEventListener("submit", function (e) {
      e.preventDefault();
  
      const username = document.getElementById("id_username").value;
      const password = document.getElementById("id_password").value;
  
      fetch("/api/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password })
      })
        .then(res => {
          if (!res.ok) {
            throw new Error("Network response was not OK");
          }
          return res.json();
        })
        .then(data => {
          console.log("Login response:", data);
  
          if (data.access && data.refresh) {
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);
            showToast('You have successfully logged in !!!',5000);
  
            // Delay redirect slightly to ensure storage completes
            setTimeout(() => {
              window.location.href = getNextUrl();
            }, 3000);
          } else {
            showError("Login failed. Invalid credentials.");
          }
        })
        .catch(error => {
          console.error("Login error:", error);
          showError("You've enter incorrect phone or password.  Try again!!!");
        });
  
      function showError(message) {
        const errorDiv = document.getElementById("login-error");
        if (errorDiv) {
          errorDiv.style.display = "block";
          errorDiv.textContent = message;
        }
      }
    });
  function getNextUrl() {
  const params = new URLSearchParams(window.location.search);
  return params.get("next") || "/";
}
function showToast(message, duration = 3000) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.classList.remove('hidden');
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
    toast.classList.add('hidden');
  }, duration);
}


  });
  