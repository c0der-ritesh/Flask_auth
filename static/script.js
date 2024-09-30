const pwShowHide = document.querySelectorAll(".showHidePw"),
      pwFields = document.querySelectorAll(".password");

pwShowHide.forEach((eyeIcon, index) => {
    // Add event listener to each eye icon
    eyeIcon.addEventListener("click", () => {
        // Toggle the type of the corresponding password field
        if (pwFields[index].type === "password") {
            pwFields[index].type = "text"; // Show password
            eyeIcon.classList.replace("uil-eye-slash", "uil-eye"); // Change icon to 'eye'
        } else {
            pwFields[index].type = "password"; // Hide password
            eyeIcon.classList.replace("uil-eye", "uil-eye-slash"); // Change icon back to 'eye-slash'
        }
    });
});

function msg() {
    alert('Are you sure? you want to submit');
}
