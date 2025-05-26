//  function selectPropertyFromElement(el) {
//     const propertyId = el.dataset.id;
//     const propertyName = el.dataset.name;
//     localStorage.setItem("selectedPropertyId", propertyId);
//     localStorage.setItem("selectedPropertyName", propertyName);
//     window.location.href = "{% url 'select_unit' %}";
//   }
  function selectPropertyFromElement(el) {
    const propertyId = el.dataset.id;
    const propertyName = el.dataset.name;

    console.log("Clicked property:", propertyId, propertyName);

    localStorage.setItem("selectedPropertyId", propertyId);
    localStorage.setItem("selectedPropertyName", propertyName);

    window.location.href = selectUnitUrl;
  }