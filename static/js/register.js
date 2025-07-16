document.addEventListener("DOMContentLoaded", function () {
  const roleSelect = document.querySelector('select[name="role"]');
  const doctorFields = document.getElementById("doctor_fields");

  function toggleDoctorFields() {
    if (roleSelect.value === "Doctor") {
      doctorFields.style.display = "block";
    } else {
      doctorFields.style.display = "none";
    }
  }

  // Initial check
  toggleDoctorFields();

  // Update on change
  roleSelect.addEventListener("change", toggleDoctorFields);
});
