document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const imageInput = document.getElementById('imageInput');
    const file = imageInput.files[0];

    if (!file) {
        alert("Please upload an image.");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    fetch("http://127.0.0.1:5000/api/identify-metal", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const resultDiv = document.getElementById("result");
            resultDiv.innerHTML = "<h3>Detected Materials:</h3>";

            data.materials.forEach((material, index) => {
                resultDiv.innerHTML += `<p>Object ${index + 1}: RGB = ${material.rgb}, Wavelength = ${material.wavelength} nm</p>`;
            });
        } else {
            alert("Failed to identify materials.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred.");
    });
});
