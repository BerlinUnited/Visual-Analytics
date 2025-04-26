const mainImage = document.getElementById("mainImage");
const secondaryImageContainer = document.getElementById("secondaryImage");
const secondaryImage = secondaryImageContainer.querySelector('img');
secondaryImageContainer.addEventListener('click', swapImages);

function swapImages() {
    const mainImageSrc = mainImage.src;
    mainImage.src = secondaryImage.src;
    secondaryImage.src = mainImageSrc;
}
