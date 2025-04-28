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
    const {targetWidth, targetHeight} = get_canvas_dims()
    current_annotations.map((db_box, i) => {
        console.log("db_box", db_box)
        var rect = new Konva.Rect({
            x: db_box.data.x * 640,
            y: db_box.data.y * 480,
            width: db_box.data.width * targetWidth,
            height: db_box.data.height * targetHeight,
            fill: db_box.color,
            stroke: "rgba(0, 255, 0, 1)",
            strokeWidth: 2,
            name: 'rect',
            strokeScaleEnabled: false,
            opacity: 0.5,
            draggable: true,
            name: 'bb',
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
        
            console.log('Updated dimensions:', newWidth, newHeight);
        });
    });

    tr = getBoundingBoxTransformer()
    drawingLayer.add(tr);
    stage.on("click tap", (e) => {
        // If we click on nothing clear the transformer and update the layer
        if (e.target === stage) {
            tr.nodes([]);
            drawingLayer.batchDraw();
            return;
        }
        // Add the selected element to the transformer and update the layer
        tr.nodes([e.target]);
        drawingLayer.batchDraw();
    });
}

function setUpKonvaCanvas(){
    const {targetWidth, targetHeight} = get_canvas_dims()

    //console.log(targetWidth, targetHeight)

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