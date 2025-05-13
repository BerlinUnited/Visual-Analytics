const getBoundingBoxTransformer = () => {
    // create new transformer
    var tr = new Konva.Transformer();
    tr.rotateEnabled(false);
    tr.flipEnabled(false);
    tr.anchorStroke("000");
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
            fill: db_box.validated == true ? "green" : db_box.color,
            stroke: "000",
            strokeWidth: 2,
            name: 'rect',
            strokeScaleEnabled: false,
            opacity: 0.5,
            // for transformer
            draggable: true,
            // custom properties from the db annotation
            class: db_box.class_name,
            id: db_box.id,
            validated: db_box.validated,
            color: db_box.color,
            //FIXME add type here
            // for boundary checks
            dragBoundFunc: function(pos) {
                const stageWidth = stage.width();
                const stageHeight = stage.height();
                const rectWidth = rect.width();
                const rectHeight = rect.height();
                
                // Calculate boundaries
                let x = Math.max(0, Math.min(pos.x, stageWidth - rectWidth));
                let y = Math.max(0, Math.min(pos.y, stageHeight - rectHeight));
                
                return {
                  x: x,
                  y: y
                };
            }
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
    let element = document.getElementById("classSelect");
    element.value = target.attrs.class;
    // selectedShape is a global object
    selectedShape = target;
}

window.addEventListener('keydown', (e) => {
    const my_csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    // Check if 'v' is pressed and we have a selected node
    if (e.key === 'v' && selectedShape) {
        // toggle the validated flag here
        selectedShape.attrs.validated = !selectedShape.attrs.validated

        // Do something with the selected node
        const fill_color = selectedShape.attrs.validated == true ? "green" : selectedShape.attrs.color;

        // Example action: change the fill color
        selectedShape.fill(fill_color);
        drawingLayer.batchDraw();

        fetch(`${BASE_URL}/api/annotations/${selectedShape.attrs.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": my_csrfToken,
            },
            
            body: JSON.stringify({
                validated: selectedShape.attrs.validated,
            }),
            credentials: 'include'  // Important for session auth
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log('Update successful:', data);
        })
        .catch(error => {
            console.error('Error making PATCH request:', error);
        });
    }
    if (e.key === 'Delete' && selectedShape){
        console.log("delete annotation")
        fetch(`${BASE_URL}/api/annotations/${selectedShape.attrs.id}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": my_csrfToken,
            },
            credentials: 'include'  // Important for session auth
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            //return response.json();
        })
        .then(() => {
            console.log('Delete successful:');
            
            tr.nodes([]); // remove the transformer from the selected object
            selectedShape.remove(); // Remove the shape from the layer
            drawingLayer.batchDraw(); // redraw the layer
        })
        .catch(error => {
            console.error('Error making DELETE request:', error);
        });
    }
    if (e.key === 's'&& selectedShape){
        fetch(`${BASE_URL}/api/annotations/${selectedShape.attrs.id}/`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": my_csrfToken,
            },
            
            body: JSON.stringify({
                data: {
                    x: selectedShape.attrs.x / targetWidth,
                    y: selectedShape.attrs.y / targetHeight,
                    width: selectedShape.attrs.width / targetWidth,
                    height: selectedShape.attrs.height / targetHeight,
                }
            }),
            credentials: 'include'  // Important for session auth
        })
        .then(response => {
            if (!response.ok) {
            throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            console.log('Update successful:', data);
        })
        .catch(error => {
            console.error('Error making PATCH request:', error);
        });
    }
});
