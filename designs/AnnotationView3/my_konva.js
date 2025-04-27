// global objects needed everywhere
let konvaImage;
let imageObj;

const top1 = "https://logs.berlin-united.com/2025-03-12-GO25/2025-03-15_17-15-00_BerlinUnited_vs_Hulks_half2/extracted/4_35_Nao0022_250315-1825/log_top_jpg/0008295.png"
const bottom1 = "https://logs.berlin-united.com/2025-03-12-GO25/2025-03-15_17-15-00_BerlinUnited_vs_Hulks_half2/extracted/4_35_Nao0022_250315-1825/log_bottom_jpg/0008295.png"

window.addEventListener('load', () => {
    const leftContainer = document.querySelector('.big_image_wrapper');
    const {targetWidth, targetHeight} = get_canvas_dims()
    const containerWidth = leftContainer.clientWidth;
    const containerHeight = leftContainer.clientHeight;
    console.log(targetWidth, targetHeight)

    var stage = new Konva.Stage({
        container: 'konva',
        width: targetWidth,
        height: targetHeight,
    });
    const layer = new Konva.Layer();
    stage.add(layer);

    imageObj = new Image();
    imageObj.src = bottom1;

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
});

function switchImage() {
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
}