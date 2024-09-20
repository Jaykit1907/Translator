const video = document.getElementById('camera');
const canvas = document.getElementById('canvas');
const fileInput = document.getElementById('file-input');
const captureBtn = document.getElementById('capture-btn');
const takePhotoBtn = document.getElementById('take-photo-btn');
const cropBtn = document.getElementById('crop-btn');
const translateBtn = document.getElementById('translate-btn');
const croppedImage = document.getElementById('cropped-image');
const translatedText = document.getElementById('translated-text');
const loadingSpinner = document.getElementById('loading-spinner');
const cropContainer = document.querySelector('.crop-container'); // Crop container element
let cropper, stream;

// Turn off the camera and hide the video element
function stopCamera() {
    if (stream) {
        let tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
    }
    video.style.display = 'none';
    takePhotoBtn.style.display = 'none';
    captureBtn.style.display = 'inline';
}

// Access the camera only when the user clicks the "Capture from Camera" button
captureBtn.addEventListener('click', () => {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((mediaStream) => {
            stream = mediaStream;
            video.srcObject = stream;
            video.style.display = 'block';
            takePhotoBtn.style.display = 'inline';
            captureBtn.style.display = 'none'; // Hide the "Capture from Camera" button while the camera is active
        })
        .catch((err) => {
            console.log("Error accessing camera: ", err);
        });
});

// Capture image from the camera
takePhotoBtn.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
    displayImage(canvas.toDataURL('image/png'));

    // Turn off the camera after taking the photo
    stopCamera();
});

// Handle image upload from file input
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
            displayImage(event.target.result);
        }
        reader.readAsDataURL(file);
    }

    // If the camera is active, stop it when an image is selected from the device
    stopCamera();
});

// Function to display the image for cropping
function displayImage(imageSrc) {
    const image = document.getElementById('image');
    image.src = imageSrc;
    image.style.display = 'block';

    // Show the crop container in case it was hidden
    cropContainer.style.display = 'block';

    // Clear previous cropper instance
    if (cropper) {
        cropper.destroy();
    }

    // Initialize new cropper instance
    cropper = new Cropper(image, {
        aspectRatio: NaN, // Allow free cropping
        viewMode: 1
    });
}

// Handle cropping
cropBtn.addEventListener('click', () => {
    const croppedCanvas = cropper.getCroppedCanvas();
    const croppedDataURL = croppedCanvas.toDataURL('image/png');
    croppedImage.src = croppedDataURL;
    croppedImage.style.display = 'block';

    // Hide the crop container after cropping the image
    cropContainer.style.display = 'none';

    // Enable the translate button after cropping
    translateBtn.disabled = false;
});

// Handle translation
translateBtn.addEventListener('click', () => {
    const language = document.getElementById('language').value;
    const language1= document.getElementById('language1').value;
    const croppedDataURL = croppedImage.src;

    // Show loading spinner
    loadingSpinner.style.display = 'block';
    translatedText.innerText = ''; // Clear previous translated text

    // Send cropped image to the backend
    fetch('/translate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ image: croppedDataURL, language: language , language1: language1})
    })
    .then(response => response.json())
    .then(data => {
        translatedText.innerText = data.translated_text;

        // Hide loading spinner after receiving translation
        loadingSpinner.style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        loadingSpinner.style.display = 'none'; // Hide spinner in case of an error
    });
});

// CSRF Token Helper (for Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}






//for online and offline check

function updateOnlineStatus() {
    const offlineMessage = document.getElementById('offlineMessage');
    if (navigator.onLine) {
      offlineMessage.style.display = 'none';
    } else {
      offlineMessage.style.display = 'block';
    }
  }

  // Initial check
  updateOnlineStatus();


  // Listen for online/offline events
  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);