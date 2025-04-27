let isDrawing = false;
let rect = null
let currentClass = null;

function setUpCanvas(is_top, container_id){
    
    if(is_top){
        image_url = state.top_image.url
    }else{
        image_url = state.bottom_image.url
    }
    
    const stage = new Konva.Stage({
        container: container_id,
        width: 640,
        height: 480,
    });
    const layer = new Konva.Layer();
    stage.add(layer);
    
    const imageObj = new Image();
    imageObj.src = image_url;

    imageObj.onload = function() {        
        // Create Konva image
        const konvaImage = new Konva.Image({
            image: imageObj,
            width: 640,
            height: 480,
        });
        
        layer.add(konvaImage);
        layer.draw();
        draw_annotation(stage, is_top)
    };
}

function draw_annotation(stage, is_top){
    console.log("drawing on top image: ", is_top)
    if(is_top){
        image_id = state.top_image.id
        annotation_list = state.top_image.annotation
    }else{
        image_id = state.bottom_image.id
        annotation_list = state.bottom_image.annotation
    }
    const drawingLayer = new Konva.Layer({ name: 'drawingLayer' });
    stage.add(drawingLayer);

    // load annotations if they exist
    if(!isObjectEmpty(annotation_list)){
        annotation_list.bbox.map((db_box, i) => {
            //console.log(db_box)
            var rect = new Konva.Rect({
                x: db_box.x * 640,
                y: db_box.y * 480,
                width: db_box.width * 640,
                height: db_box.height * 480,
                fill: getCurrentClassColor(),
                stroke: "rgba(0, 255, 0, 1)",
                strokeWidth: 2,
                name: 'rect',
                strokeScaleEnabled: false,
                opacity: 0.5,
                draggable: true,
                name: 'bb',
            });
            console.log(rect)
            drawingLayer.add(rect);
            rect.on('dragend', () => {
                console.log('Updated position:', rect.x(), rect.y());
            });
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
    }

    // create new transformer
    var tr = getBoundingBoxTransformer()
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

    function mousedownhandler(){
        const pos = stage.getRelativePointerPosition();
        const shape = stage.getIntersection(pos);
        if (shape instanceof Konva.Image) {
            isDrawing = true;
            rect = new Konva.Rect({
                x: stage.getPointerPosition().x,
                y: stage.getPointerPosition().y,
                width: 0,
                height: 0,
                fill: getCurrentClassColor(),
                stroke: "rgba(0, 255, 0, 1)",
                strokeWidth: 2,
                strokeScaleEnabled: false,
                opacity: 0.5,
                draggable: true,
                name: 'bb',
            });
            drawingLayer.add(rect).batchDraw();
        }
        else{
            console.log("clicked on", shape)
            if(shape instanceof Konva.Rect){
                console.log("clicked on rect", shape.x(), shape.y())
            }
        }
        //TODO somehow check if you click on a rectangle and have this selected to be able to refer to that
    }
    function mousemovehandler(){
        if(isDrawing){
            const newWidth = stage.getPointerPosition().x - rect.x();
            const newHeight = stage.getPointerPosition().y - rect.y();
            rect.width(newWidth).height(newHeight);
            drawingLayer.batchDraw();
        }
       
    }
    
    function mouseuphandler(){
        isDrawing = false;
        
    }

    window.addEventListener('keydown', (e) => {
        if (e.key === 'Delete' || e.key === 'Del') {
          const selectedRect = tr.nodes()[0]; // Get the selected rectangle
          if (selectedRect) {
            selectedRect.destroy(); // Remove the rectangle
            tr.nodes([]); // Clear the transformer
            drawingLayer.draw(); // Redraw the layer
          }
        }
      });

    stage.on("mousedown", mousedownhandler);
    stage.on("mousemove", mousemovehandler);
    stage.on("mouseup", mouseuphandler);
}

const save_button = document.getElementById("save_button");
save_button.addEventListener("click", saveFunction);

// Attach the save function to Ctrl+S (or Cmd+S on macOS)
document.addEventListener("keydown", function (event) {
    // Check if Ctrl (or Cmd on macOS) and S are pressed
    if ((event.ctrlKey || event.metaKey) && event.key === "s") {
        event.preventDefault(); // Prevent the default browser save dialog
        saveFunction(); // Trigger the save function
    }
});