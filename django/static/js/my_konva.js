const getBoundingBoxTransformer = () => {
    // create new transformer
    var tr = new Konva.Transformer();
    tr.rotateEnabled(false);
    tr.flipEnabled(false);
    tr.anchorStroke("green");
    tr.anchorFill('white');
    tr.keepRatio(false);
    tr.ignoreStroke(true);
    tr.borderStrokeWidth(0);
    tr.enabledAnchors([
        "top-left",
        "top-right",
        "bottom-left",
        "bottom-right",
    ]);
    tr.anchorCornerRadius(10);
  
    return tr;
  };

function draw_db_annotations(){
    current_annotations.map((db_box, i) => {
        console.log("db_box", db_box)
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
        });
        console.log("rect", rect)

        drawingLayer.add(rect);
        rect.on('transformend', () => {
            // Get updated dimensions
            const newWidth = rect.width() * rect.scaleX();
            const newHeight = rect.height() * rect.scaleY();
        
            // Reset scale to 1 after applying
            rect.width(newWidth);
            rect.height(newHeight);
            rect.scaleX(1);
            rect.scaleY(1);
        });
    });

    tr = getBoundingBoxTransformer()
    drawingLayer.add(tr);
    stage.on("click tap", (e) => {
        // If we click on the image clear the transformer and update the layer
        if (e.target === konvaImage) {
            tr.nodes([]);
            drawingLayer.batchDraw();
            return;
        }
        // Add the selected element to the transformer and update the layer
        tr.nodes([e.target]);
        drawingLayer.batchDraw();
        // update the rest of the UI when object is clicked
        handle_select(e.target);
    });
}

function setUpKonvaCanvas(){
    ({targetWidth, targetHeight} = get_canvas_dims());

    stage = new Konva.Stage({
        container: 'konva',
        width: targetWidth,
        height: targetHeight,
    });
    const layer = new Konva.Layer({ name: 'imageLayer' });
    stage.add(layer);

    imageObj = new Image();
    imageObj.src = bottom_image_url;

    imageObj.onload = function() {        
        // Create Konva image
        konvaImage = new Konva.Image({
            image: imageObj,
            width: targetWidth,
            height: targetHeight,
        });
        
        layer.add(konvaImage);
        layer.draw();
    };
    drawingLayer = new Konva.Layer({ name: 'drawingLayer' });
    stage.add(drawingLayer);
    
    draw_db_annotations();
}

function switchImage() {
    is_bottom_main = !is_bottom_main;
    if(is_bottom_main){
        current_annotations = bottom_annotations;
    }else{
        current_annotations = top_annotations;
    }
    console.log("is_bottom_main", is_bottom_main)
    const secondaryImageContainer = document.getElementById("secondaryImage");
    const secondaryImage = secondaryImageContainer.querySelector('img');
    
    const old_url = imageObj.src;
    const newUrl = secondaryImage.src;
    imageObj = new Image();
    imageObj.onload = function() {
      // Update the image property of your Konva.Image node
      konvaImage.image(imageObj);
      
      // Redraw the layer
      konvaImage.getLayer().batchDraw();
    };
    imageObj.src = newUrl;
    secondaryImage.src = old_url;
    
    //
    tr.detach();
    drawingLayer.destroyChildren();
    draw_db_annotations();
}

function handle_select(target){
    console.log("clicked on ", target)
    let element = document.getElementById("classSelect");
    element.value = target.attrs.class;
    selectedShape = target;
}

window.addEventListener('keydown', (e) => {
    const my_csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Check if 'v' is pressed and we have a selected node
    if (e.key === 'v' && selectedShape) {
        // Do something with the selected node
        console.log('Pressed V with selected node:', selectedShape);
        console.log(my_csrfToken)
        // Example action: change the fill color
        selectedShape.fill(getRandomColor());
        drawingLayer.batchDraw();
        console.log("annotation id", selectedShape.attrs.id)
        fetch(`${BASE_URL}/api/annotations/${selectedShape.attrs.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": my_csrfToken,
            },
            
            body: JSON.stringify({
                validated: true,
            }),
            credentials: 'include'  // Important for session auth
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Update successful:', data);
        })
        .catch(error => {
            console.error('Error making PATCH request:', error);
        });
    }
});
  
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}