document.addEventListener('DOMContentLoaded', function () {
  const propertySelect = document.getElementById('property');
  const unitSelect = document.getElementById('unit');
  const paymentForm = document.getElementById('paymentForm');
  const reference = getQueryParam('reference') || getQueryParam('trxref');
  const token = localStorage.getItem("access");
if (reference && token) {
      fetch(`/api/payments/verify/${reference}/?reference=${reference}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(res => {
          if (!res.ok) {
            return res.json().then(data => {
              throw new Error(data.detail || 'Verification failed');
            });
          }
          return res.json();
        })
        .then(data => {
          alert("✅ Payment Verified: " + data.message);
        })
        .catch(err => {
          console.error('Verification error:', err);
          alert("❌ Payment verification failed: " + err.message);
        });
      }
  // Load units dynamically when property changes
  if (propertySelect && !propertySelect.disabled) {
    propertySelect.addEventListener('change', function () {
      const propertyId = this.value;

      if (!propertyId) {
        unitSelect.innerHTML = '<option value="">-- Select Room --</option>';
        unitSelect.disabled = true;
        paymentForm.style.display = 'none';
        return;
      }

      unitSelect.innerHTML = '<option value="">Loading...</option>';
      unitSelect.disabled = true;

      fetch(`/api/properties/${propertyId}/units/`)
        .then(res => res.json())
        .then(data => {
          unitSelect.innerHTML = '<option value="">-- Select Room --</option>';
          data.forEach(unit => {
            unitSelect.innerHTML += `
              <option value="${unit.id}" data-cost="${unit.cost}">
                Room ${unit.room_No} - GHS ${unit.cost}/month
              </option>`;
          });
          unitSelect.disabled = false;
        });
    });
  }

  // Show payment form when unit is selected
  if (unitSelect) {
    unitSelect.addEventListener('change', function () {
      const selected = this.selectedOptions[0];
      if (!selected || !selected.value) {
        paymentForm.style.display = 'none';
        return;
      }

      const cost = selected.getAttribute('data-cost');
      document.getElementById('amount').value = cost;
      document.getElementById('unit_id').value = selected.value;
      paymentForm.style.display = 'block';
    });
  }

  // ✅ Read prepopulated state safely from Django
  const unitIsPrepopulated = JSON.parse(document.getElementById('unit-data').textContent);
  if (unitIsPrepopulated) {
    paymentForm.style.display = 'block';
  }
});

// 🔐 Get CSRF token from cookies (for session auth)
function getCSRFToken() {
  const name = 'csrftoken';
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith(name + '='));
  return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : '';
}

// 💳 Initialize Paystack payment
function payWithPaystack() {
  const email = document.getElementById('email').value;
  const phone = document.getElementById('phone').value;
  const amount = parseFloat(document.getElementById('amount').value) * 100; // Convert to pesewas
  const provider = document.getElementById('provider').value;
  const unit_id = document.getElementById('unit_id').value;

  const accessToken = localStorage.getItem("access");  // 🔐 JWT token must be stored in localStorage

  if (!email || !phone || !amount || !provider || !unit_id) {
    alert("Please fill all required fields including selecting a payment provider.");
    return;
  }

  if (!accessToken) {
    alert("You're not logged in. Please log in first.");
    return;
  }

  fetch(window.initializePaymentUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${accessToken}`,  // 🔐 Important for DRF SimpleJWT
      'X-CSRFToken': getCSRFToken(),             // Optional if you're also using CSRF
    },
    body: JSON.stringify({
      email,
      phone,
      amount,
      provider,
      unit_id,
    })
  })
    .then(res => {
      if (!res.ok) {
        return res.json().then(data => {
          throw new Error(data.detail || "Unauthorized request");
        });
      }
      return res.json();
    })
    .then(data => {
      if (data.status && data.data && data.data.authorization_url) {
        window.location.href = data.data.authorization_url; // ✅ Redirect to Paystack
      } else {
        alert("Payment error: " + (data.error || data.message));
      }
    })
    .catch(error => {
      console.error("Payment error:", error);
      alert("Failed to initialize payment: " + error.message);
    });
    fetch('/api/payments/verify/4aa71043-4b41-42db-b6c4-8934e43303eb/', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access')}`
  }
});

}
