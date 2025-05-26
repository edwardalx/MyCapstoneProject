document.addEventListener('DOMContentLoaded', function () {
  const propertySelect = document.getElementById('property');
  const unitSelect = document.getElementById('unit');
  const paymentForm = document.getElementById('paymentForm');

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

function getCSRFToken() {
  const name = 'csrftoken';
  const cookieValue = document.cookie
    .split('; ')
    .find(row => row.startsWith(name + '='));
  return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : '';
}

function payWithPaystack() {
  const email = document.getElementById('email').value;
  const phone = document.getElementById('phone').value;
  const amount = parseFloat(document.getElementById('amount').value) * 100; // Convert to pesewas
  const provider = document.getElementById('provider').value;
  const tenant_id = document.getElementById('tenant_id').value;
  const unit_id = document.getElementById('unit_id').value;

  fetch(window.initializePaymentUrl, {  // <--- YOUR NEW DRF VIEWSET ENDPOINT HERE
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify({
      email,
      phone,
      amount,
      provider,
      unit_id,
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.status && data.data && data.data.authorization_url) {
        // ✅ Redirect user to Paystack payment page
        window.location.href = data.data.authorization_url;
      } else {
        alert("Payment error: " + (data.error || data.message));
      }
    })
    .catch(error => {
      console.error("Payment error:", error);
      alert("Failed to initialize payment.");
    });
}
