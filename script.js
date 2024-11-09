let downloadButton = document.querySelector('.download-button');
let overlay = document.querySelector('.overlay');
let downloadWindow = document.querySelector('.download-help-window');
let closeButton = document.querySelector('.close-window-button');

function openDownloadWindow() {
    overlay.style.display = 'block';
    downloadWindow.style.display = 'block';
}

function closeDownloadWindow() {
    overlay.style.display = 'none';
    downloadWindow.style.display = 'none';
}

downloadButton.addEventListener('click', openDownloadWindow);
closeButton.addEventListener('click', closeDownloadWindow);