document.addEventListener('DOMContentLoaded', function() {
    const unitCards = document.querySelectorAll('.unit-card');
    const paymentBtn = document.getElementById('proceedToPaymentBtn');
    let selectedUnitId = null;

    // Initialize the payment button as hidden
    paymentBtn.style.display = 'none';

    // Add click event to each unit card
    unitCards.forEach(card => {
        const selectBtn = card.querySelector('.select-unit-btn');
        
        // Click handler for the entire card
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking directly on the button
            if (e.target === selectBtn) return;
            
            selectUnit(card);
        });

        // Click handler for the select button
        selectBtn.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent card click from triggering
            selectUnit(card);
        });
    });

    function selectUnit(card) {
        // Deselect all units first
        unitCards.forEach(c => {
            c.classList.remove('selected');
            const btn = c.querySelector('.select-unit-btn');
            btn.textContent = 'Select Unit';
            btn.classList.remove('selected');
        });

        // Select the clicked unit
        card.classList.add('selected');
        const selectBtn = card.querySelector('.select-unit-btn');
        selectBtn.textContent = 'Selected!';
        selectBtn.classList.add('selected');
        selectedUnitId = card.dataset.unitId;

        // Show the payment button
        paymentBtn.style.display = 'inline-block';
    }

    // Payment button click handler
    window.goToPayment = function() {
        if (!selectedUnitId) {
            alert('Please select a unit before proceeding to payment.');
            return;
        }

        // Redirect to payment page with the selected unit ID
        window.location.href = `${makePaymentUrl}?unit_id=${selectedUnitId}`;
    };
});