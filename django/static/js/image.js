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

async function get_image_url(camera) {
    try {
        /* Fetches the image object from the API */
        const pathParts = window.location.pathname.split('/').filter(Boolean);
        const logId = pathParts[1];
        const frame_number = pathParts[3];
        
        const url = `${BASE_URL}/api/image/?camera=${camera}&log=${logId}&frame_number=${frame_number}`;
        
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
        }); 
        // FIXME how to handle dummy images correctly and make sure to not fetch annotations
        const data = await response.json();
        
        if (data.length == 0){
            console.log("data is too short")
            console.log(data)
            return {image_url: "/static/images/dummy_image.jpg"}; // Fallback image
        }
        console.log("Success:", data);
        return data[0];
        
    } catch (error) {
        console.error("Error:", error);
        // FIXME return a json with image_url as member
        return {image_url: "/static/images/dummy_image.jpg"}; // Fallback image
    }
}

async function get_annotations(image_id){
    try {
        /* Fetches the annotation objects from the API */
        const url = `${BASE_URL}/api/annotations/?image=${image_id}`;
        
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
        });
        
        const data = await response.json();
        console.log("Annotation Success:", data);
        // FIXME returning the list of rects
        data.map((db_box, i) => {
            console.log("cool db_box", db_box)
            var rect = new Konva.Rect({
                // coordinates
                x: db_box.data.x * targetWidth,
                y: db_box.data.y * targetHeight,
                width: db_box.data.width * targetWidth,
                height: db_box.data.height * targetHeight,
                // color
                fill: db_box.color,
                stroke: "rgba(0, 255, 0, 1)",
                strokeWidth: 2,
                name: 'rect',
                strokeScaleEnabled: false,
                opacity: 0.5,
                // for transformer
                draggable: true,
                // custom properties from the db annotation
                class: db_box.class_name,
                id: db_box.id,
                //FIXME add type here
            });
            
        });
        // TODO map data to list of rect elements
        return data;
        
    } catch (error) {
        console.error("Error:", error);
        return {}; // Fallback image
    }
}

function setup_secondary_image(){
    const secondaryImageContainer = document.getElementById("secondaryImage");
    const secondaryImage = secondaryImageContainer.querySelector('img');

    secondaryImageContainer.addEventListener('click', switchImage);
    secondaryImage.src = top_image_url;
}
