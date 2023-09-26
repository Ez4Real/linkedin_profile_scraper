document.addEventListener("DOMContentLoaded", function () {
    const steps = document.querySelectorAll(".step-container[id^='step']");
    const backButton = document.getElementById("back-button");
    const nextButton = document.getElementById("next-button");
    const submitButton = document.getElementById("submit-button");

    // Function to navigate to the next step
    function goToStep(stepIndex) {
        steps.forEach(step => { step.style.display = "none"; }); 
        steps[stepIndex].style.display = "flex"; 
    }

    let currentStep = 0;

    updateButtonVisibility();

    backButton.addEventListener("click", function () {
        if (currentStep > 0) {
            goToStep(currentStep - 1);
            currentStep--;

            updateButtonVisibility();
        }
    });

    nextButton.addEventListener("click", function () {
        if (currentStep < steps.length - 1) {
            goToStep(currentStep + 1);
            currentStep++;

            updateButtonVisibility();
        }
    });

    function updateButtonVisibility() {
        if (currentStep === 0) {
            nextButton.style.display = formData.file ? "block" : "none";
        } else if (currentStep === 1) {
            nextButton.style.display = formData.allOptionsSelected ? "block" : "none";
        } else if (currentStep === 2) {
            nextButton.style.display = "none";
        }
        backButton.style.display = currentStep > 0 ? "block" : "none";
        submitButton.style.display = currentStep === 2 ? "block" : "none";
    }
});