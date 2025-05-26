document.addEventListener('DOMContentLoaded', function () {
    const selectButtons = document.querySelectorAll('.select-unit-btn');
    const paymentSection = document.getElementById('payment-section');
    const paymentBtn = document.getElementById('proceed-to-payment');

    selectButtons.forEach(button => {
        button.addEventListener('click', function () {
            const unitId = this.dataset.unitId;
            localStorage.setItem('selectedUnitId', unitId);

            document.querySelectorAll('.unit-card').forEach(card => {
                card.classList.remove('selected');
            });
            this.closest('.unit-card').classList.add('selected');
            this.textContent = 'Selected!';
            this.disabled = true;

            paymentSection.style.display = 'block';
        });
    });

    paymentBtn.addEventListener('click', function () {
        const unitId = localStorage.getItem('selectedUnitId');
        const propertyId = localStorage.getItem('selectedPropertyId');

        if (!unitId || !propertyId) {
            alert('Please select both a property and a unit before proceeding.');
            return;
        }

        // ✅ Use the dynamic URL with query params
        window.location.href = `${makePaymentUrl}?unit_id=${unitId}&property_id=${propertyId}`;
    });
});
