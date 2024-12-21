// Mobile Menu Toggle
const menuToggle = document.getElementById('mobile-menu');
const navLinks = document.querySelector('.nav-links');

// Toggle the 'active' class to show/hide the menu
menuToggle.addEventListener('click', () => {
    // alert(navLinks.classList)
    navLinks.classList.toggle('active');
});


// Function to trigger the file input for image upload
function triggerFileUpload() {
    document.getElementById('image-upload').click();
}

// Event listener for file input change
document.getElementById('image-upload').addEventListener('change', (event) => {
    const file = event.target.files[0];
    const originalImage = document.getElementById('original-image');
    
    // If a file is selected, display it in the image element
    console.log(file);
    
    if (file) {
        originalImage.src = URL.createObjectURL(file);
    }
});

// Ensure the file input has a file selected before form submission
document.getElementById('upload-form').addEventListener('submit', function(event) {
    const fileInput = document.getElementById('image-upload');
    if (!fileInput.files.length) {
        event.preventDefault();  // Prevent form submission if no file is selected
        alert("Please upload an image first.");
    }
});
