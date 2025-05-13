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
  
            alert("Logged in!");
  
            // Delay redirect slightly to ensure storage completes
            setTimeout(() => {
              window.location.href = "/";
            }, 100);
          } else {
            showError("Login failed. Invalid credentials.");
          }
        })
        .catch(error => {
          console.error("Login error:", error);
          showError("An error occurred while logging in.");
        });
  
      function showError(message) {
        const errorDiv = document.getElementById("login-error");
        if (errorDiv) {
          errorDiv.style.display = "block";
          errorDiv.textContent = message;
        }
      }
    });
  });
  