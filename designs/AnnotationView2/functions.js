const mainImage = document.getElementById("mainImage");
const secondaryImageContainer = document.getElementById("secondaryImage");
const secondaryImage = secondaryImageContainer.querySelector('img');
const timeline = document.getElementById("timeline");
const numFrames = 100; // Total number of frames
let currentFrame = 1; // Initial frame

secondaryImageContainer.addEventListener('click', swapImages);

function swapImages() {
    const mainImageSrc = mainImage.src;
    mainImage.src = secondaryImage.src;
    secondaryImage.src = mainImageSrc;
}

function loadFrame(frameNumber) {
    // Replace these with your actual image loading logic based on frame number
    const baseUrlBottom = "https://logs.berlin-united.com/2025-03-12-GO25/2025-03-15_17-15-00_BerlinUnited_vs_Hulks_half2/extracted/4_35_Nao0022_250315-1825/log_bottom_jpg/";
    const baseUrlTop = "https://logs.berlin-united.com/2025-03-12-GO25/2025-03-15_17-15-00_BerlinUnited_vs_Hulks_half2/extracted/4_35_Nao0022_250315-1825/log_top_jpg/";
    //const frameNumberPadded = String(frameNumber).padStart(7, '0'); // Pad with leading zeros

    mainImage.src = `${baseUrlBottom}0008295.png`;
    secondaryImage.src = `${baseUrlTop}0008295.png`;

    const activeButtons = document.querySelectorAll('.frame_button.active');
    activeButtons.forEach(button => button.classList.remove('active'));
    const currentButton = document.getElementById(`frame-${frameNumber}`);
    if (currentButton) {
        currentButton.classList.add('active');
        timelineContainer.scrollLeft = currentButton.offsetLeft - (timelineContainer.offsetWidth / 2) + (currentButton.offsetWidth / 2);
    }

    currentFrame = frameNumber;
}

// Create timeline buttons
for (let i = 1; i <= numFrames; i++) {
    const button = document.createElement('button');
    button.classList.add('frame_button');
    button.textContent = "";
    button.id = `frame-${i}`;
    button.addEventListener('click', () => loadFrame(i));
    timeline.appendChild(button);

    if (i === 1) {
        button.classList.add('active');
    }
}