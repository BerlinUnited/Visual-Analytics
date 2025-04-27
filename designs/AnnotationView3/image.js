function get_canvas_dims(){
    const leftContainer = document.querySelector('.big_image_wrapper');

    const containerWidth = leftContainer.clientWidth;
    const containerHeight = leftContainer.clientHeight;

    image_natural_width = 640;
    image_natural_height = 480;

    // Get image's natural aspect ratio
    const imageRatio = image_natural_width / image_natural_height;
    const containerRatio = containerWidth / containerHeight;

    let targetWidth = 0;
    let targetHeight = 0;

    // Determine scaling factor based on container aspect ratio
    if (imageRatio > containerRatio) {
        // Image is wider than container relative to height, scale based on width
        targetWidth = containerWidth;
        targetHeight = targetWidth / imageRatio;
    } else {
        // Image is taller than container relative to width (or ratios match), scale based on height
        targetHeight = containerHeight;
        targetWidth = targetHeight * imageRatio;
    }
    return {
        targetWidth: targetWidth,
        targetHeight: targetHeight,
    }
}


function scale_image(){
    const leftContainer = document.querySelector('.big_image_wrapper');
    const mainImage = document.getElementById('mainImage');

    // Function to scale the image
    const scaleImage = () => {
        // Ensure the image has loaded and natural dimensions are available
        if (!mainImage.naturalWidth || !mainImage.naturalHeight) {
            console.warn('Image natural dimensions not yet available.');
            return;
        }
        if (!leftContainer) {
                console.error('Left container not found.');
                return;
        }

        // Get container dimensions (content area, excluding padding)
        const containerWidth = leftContainer.clientWidth;
        const containerHeight = leftContainer.clientHeight;

        // Get image's natural aspect ratio
        const imageRatio = mainImage.naturalWidth / mainImage.naturalHeight;
        const containerRatio = containerWidth / containerHeight;

        let targetWidth = 0;
        let targetHeight = 0;

        // Determine scaling factor based on container aspect ratio
        if (imageRatio > containerRatio) {
            // Image is wider than container relative to height, scale based on width
            targetWidth = containerWidth;
            targetHeight = targetWidth / imageRatio;
        } else {
            // Image is taller than container relative to width (or ratios match), scale based on height
            targetHeight = containerHeight;
            targetWidth = targetHeight * imageRatio;
        }

        // Apply calculated dimensions to the image style
        mainImage.style.width = `${targetWidth}px`;
        mainImage.style.height = `${targetHeight}px`;

        // console.log(`Container: ${containerWidth}x${containerHeight}, Image scaled to: ${targetWidth.toFixed(2)}x${targetHeight.toFixed(2)}`);
    };

    // --- ResizeObserver Setup ---
    // Create an observer instance linked to the callback function
    const observer = new ResizeObserver(entries => {
            // We only observe one element, so entries[0] is the container
            // The callback might fire multiple times rapidly, consider debouncing for performance if needed
            scaleImage();
    });


    // --- Image Load Handling ---
    // Function to initialize scaling and observer *after* image loads
    const initializeScaling = () => {
        console.log('Image loaded, initializing scaling.');
        // Perform the initial scaling calculation
        scaleImage();
        // Start observing the container *after* the image is loaded and initially scaled
            if (leftContainer) {
            observer.observe(leftContainer);
            } else {
            console.error("Cannot observe null container.");
            }
    };

    // Check if the image is already loaded (e.g., from cache)
    if (mainImage.complete) {
        initializeScaling();
    } else {
        // If not loaded, wait for the onload event
        mainImage.onload = initializeScaling;
        // Optional: Handle image loading errors
        mainImage.onerror = () => {
            console.error("Failed to load the main image.");
            // Optionally hide the image or show a placeholder message
        };
    }
}