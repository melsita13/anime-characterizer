async function predictCharacter() {
    const imageInput = document.getElementById('imageInput');
    const resultContainer = document.getElementById('resultContainer');
    const loadingSpinner = document.getElementById('loading');
    const errorDiv = document.getElementById('error');

    if (imageInput.files.length === 0) {
        errorDiv.style.display = 'block';
        errorDiv.innerText = 'Please select an image file.';
        resultContainer.style.display = 'none';
        return;
    }

    loadingSpinner.style.display = 'block';
    errorDiv.style.display = 'none';
    resultContainer.style.display = 'none';

    const formData = new FormData();
    formData.append('image', imageInput.files[0]);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();

        loadingSpinner.style.display = 'none';
        
        if (response.ok) {
            document.getElementById('characterName').innerText = result.character;
            document.getElementById('confidenceScore').innerText = (result.confidence * 100).toFixed(2);
            document.getElementById('animeName').innerText = result.anime || 'N/A';
            document.getElementById('characterDescription').innerText = result.description || 'N/A';
            
            const watchLinks = document.getElementById('watchLinks');
            watchLinks.innerText = result.where_to_watch ? result.where_to_watch.join(', ') : 'N/A';

            const relatedImagesDiv = document.getElementById('relatedImages');
            relatedImagesDiv.innerHTML = '';
            if (result.related_images && result.related_images.length > 0) {
                result.related_images.forEach(imageUrl => {
                    const img = document.createElement('img');
                    img.src = imageUrl;
                    relatedImagesDiv.appendChild(img);
                });
            } else {
                relatedImagesDiv.innerText = 'No related images available.';
            }

            resultContainer.style.display = 'block';
        } else {
            errorDiv.style.display = 'block';
            errorDiv.innerText = result.error || 'An unknown error occurred.';
        }

    } catch (e) {
        loadingSpinner.style.display = 'none';
        errorDiv.style.display = 'block';
        errorDiv.innerText = `An error occurred: ${e.message}`;
        console.error(e);
    }
}