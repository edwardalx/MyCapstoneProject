function selectPropertyFromElement(el) {
  const propertyId = el.dataset.id;
  const propertyName = el.dataset.name;
  const selectUnitUrl = selectUnitBaseUrl.replace('/0/', `/${propertyId}/`);

  console.log("Clicked property:", propertyId, propertyName);

  localStorage.setItem("selectedPropertyId", propertyId);
  localStorage.setItem("selectedPropertyName", propertyName);

  window.location.href = selectUnitUrl;
}

  // function selectPropertyFromElement(el) {
  //   const propertyId = el.dataset.id;
  //   const propertyName = el.dataset.name;
  //   const selectUnitUrl = selectUnitBaseUrl.replace('/0/', `/${propertyId}/`);

  //   console.log("Clicked property:", propertyId, propertyName);

  //   localStorage.setItem("selectedPropertyId", propertyId);
  //   localStorage.setItem("selectedPropertyName", propertyName);

  //   window.location.href = selectUnitUrl;
  // }