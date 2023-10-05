window.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.querySelector('.drop-zone');
    const convertBtn = document.querySelector('.convert-btn');
    const loader = document.getElementById('loader');
    const fileInput = document.getElementById('pdf_files');
    const selectedFileCount = document.getElementById('selected-file-count'); // Reference to the selected-file-count <span> element

    dropZone.addEventListener('dragover', handleDragOver);
    dropZone.addEventListener('dragleave', handleDragLeave);
    dropZone.addEventListener('drop', handleDrop);

    function handleDragOver(event) {
        event.preventDefault();
        dropZone.classList.add('active');
    }

    function handleDragLeave(event) {
        event.preventDefault();
        dropZone.classList.remove('active');
    }

    function handleDrop(event) {
        event.preventDefault();
        dropZone.classList.remove('active');
        fileInput.files = event.dataTransfer.files;
        handleFileInput();
    }

    function openFileInput() {
        fileInput.click();
    }

    fileInput.addEventListener('change', handleFileInput);

    function handleFileInput() {
        const files = fileInput.files;
        selectedFileCount.textContent = files.length > 0 ? `${files.length} file(s) selected` : '';
        dropZone.classList.toggle('file-selected', files.length > 0);
    }

    convertBtn.addEventListener('click', convertFiles);

    function convertFiles() {
        const formData = new FormData();
        const files = fileInput.files;

        if (files.length === 0) {
            alert('Please select at least one PDF file.');
            return;
        }

        for (const file of files) {
            formData.append('pdf_files', file);
        }

        convertBtn.disabled = true;
        loader.style.display = 'block';

        // Simulating conversion delay (remove this in your actual implementation)
        setTimeout(() => {
            convertBtn.disabled = false;
            loader.style.display = 'none';
            alert('Conversion successful!'); // Replace this with your desired action after conversion
        }, 3000);
    }
});
