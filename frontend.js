document.getElementById('uploadForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const imageInput = document.getElementById('imageInput');
  const file = imageInput.files[0];

  if (!file) {
    alert("Please upload an image.");
    return;
  }

  // Display loading message
  document.getElementById('predominantMaterial').innerText = "Identifying material...";
  document.getElementById('otherMaterials').innerText = "";
  document.getElementById('wavelength').innerText = "";

  // Create a FormData object to send the image to the server
  const formData = new FormData();
  formData.append("image", file);

  // Send image to backend (replace the URL with your backend endpoint)
  fetch('http://localhost:5000/api/identify-metal', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    // Handle the response and display results
    if (data.success) {
      document.getElementById('predominantMaterial').innerText = Predominant Material: ${data.predominantMetal};
      document.getElementById('otherMaterials').innerText = Other Major Materials: ${data.otherMaterials.join(', ')};
      document.getElementById('wavelength').innerText = Wavelength: ${data.wavelength} nm;
    } else {
      alert("Failed to identify materials. Please try again.");
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert("An error occurred. Please try again later.");
  });
});