document.addEventListener('DOMContentLoaded', function () {
    const unitCards = document.querySelectorAll('.unit-card');
    const paymentBtn = document.getElementById('proceedToPaymentBtn');
    let selectedUnitId = null;

    paymentBtn.style.display = 'none';

    unitCards.forEach(card => {
        const selectBtn = card.querySelector('.select-unit-btn');

        card.addEventListener('click', function (e) {
            if (e.target === selectBtn) return;

            if (!isAuthenticated) {
                showLoginModal();
                return;
            }

            selectUnit(card);
        });

        selectBtn.addEventListener('click', function (e) {
            e.stopPropagation();

            if (!isAuthenticated) {
                showLoginModal();
                return;
            }

            selectUnit(card);
        });
    });

    function selectUnit(card) {
        unitCards.forEach(c => {
            c.classList.remove('selected');
            const btn = c.querySelector('.select-unit-btn');
            btn.textContent = 'Select Unit';
            btn.classList.remove('selected');
        });

        card.classList.add('selected');
        const selectBtn = card.querySelector('.select-unit-btn');
        selectBtn.textContent = 'Selected!';
        selectBtn.classList.add('selected');
        selectedUnitId = card.dataset.unitId;

        paymentBtn.style.display = 'inline-block';
    }

    window.goToPayment = function () {
        if (!isAuthenticated) {
            showLoginModal();
            return;
        }

        if (!selectedUnitId) {
            alert('Please select a unit before proceeding to payment.');
            return;
        }

fetch(`${makePaymentUrl}?unit_id=${selectedUnitId}`, {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access')}`,
  },
})
  .then(response => {
    if (!response.ok) {
      throw new Error('Authentication failed or access denied.');
    }
    return response.text(); // response is HTML
  })
  .then(html => {
    // Replace the page content with the payment page
    document.open();
    document.write(html);
    document.close();
  })
  .catch(err => {
    alert("Could not load payment page: " + err.message);
  });

    };

    window.showLoginModal = function () {
        document.getElementById('loginModal').style.display = 'flex';
    };

    window.closeModal = function () {
        document.getElementById('loginModal').style.display = 'none';
    };
    
});
