const fileInput = document.getElementById('files');
const previewContainer = document.getElementById('preview');
let selectedFiles = [];

document.addEventListener('DOMContentLoaded', () => {

    fileInput.addEventListener('change', () => {
        selectedFiles = Array.from(fileInput.files);
        renderPreviews();
    });
});

function renderPreviews() {
previewContainer.innerHTML = '';
selectedFiles.forEach((file, index) => {
    const reader = new FileReader();

    reader.onload = function (e) {
    const previewDiv = document.createElement('div');
    previewDiv.classList.add('image-preview');

    const img = document.createElement('img');
    img.src = e.target.result;

    const removeBtn = document.createElement('button');
    removeBtn.classList.add('remove-button');
    removeBtn.onclick = function () {
        selectedFiles.splice(index, 1);
        updateInputFiles();
        renderPreviews(); // Odśwież podgląd po usunięciu
    };

    previewDiv.appendChild(img);
    previewDiv.appendChild(removeBtn);
    previewContainer.appendChild(previewDiv);
    };

    reader.readAsDataURL(file);
});
}

function updateInputFiles() {
    const dataTransfer = new DataTransfer();
    selectedFiles.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;
}

function clearPreviews(){
    previewContainer.innerHTML = '';
}

