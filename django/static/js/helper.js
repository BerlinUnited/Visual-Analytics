const isObjectEmpty = (objectName) => {
  // generic function for checking if an javascript object is empty
  // we use it for checking for an empty annotation json
  return (
    objectName &&
    Object.keys(objectName).length === 0 &&
    objectName.constructor === Object
  );
};

const generateUUID4 = () => {
  // similar to what python would return
  return crypto.randomUUID().replace(/-/g, "").slice(0, 9).toUpperCase();
}

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

const scrollTimeline = () => {
  const activeElement = document.querySelector('.timeline-active');
  if (activeElement) {
    activeElement.scrollIntoView({
      behavior: 'smooth', // Smooth scrolling animation
      block: 'nearest',   // Keeps vertical alignment as is (you can adjust if needed)
      inline: 'center',   // Horizontally centers the element in the viewport
    });
  }
};

const arrow_navigation = () => {
  // Get the URLs for the previous and next frames
  const prevLink = document.querySelector('.prev-button');
  const nextLink = document.querySelector('.next-button');

  document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft' && prevLink && prevLink.href !== '#') {
      // Navigate to the previous frame when the left arrow key is pressed
      window.location.href = prevLink.href;
    } else if (event.key === 'ArrowRight' && nextLink && nextLink.href !== '#') {
      // Navigate to the next frame when the right arrow key is pressed
      window.location.href = nextLink.href;
    }
  });
}

const currentClassListener = () => {
  // TODO persist this across page loads
  // TODO add number shortcuts

  // Add an event listener to the radio button group
  document.querySelectorAll('input[name="number-list"]').forEach((radio) => {
    radio.addEventListener('input', (event) => {
      console.log("Selected value:", event.target.value);
      currentClass = event.target.value;
      console.log(currentClass)
    });
  });
}

const getCurrentClassColor = () => {
  console.log(currentClass)
  if (currentClass == 1) {
    return "rgba(0, 255, 0, 0.5)"
  }
  if (currentClass == 2) {
    return "rgba(255, 0, 0, 0.5)"
  }
  if (currentClass == 3) {
    return "rgba(0, 0, 255, 0.5)"
  }
  if (currentClass == 4) {
    return "rgba(255, 0, 255, 0.5)"
  }
}


const saveFunction = () => {
  // FIXME: this would change uuid everytime you click submit
  const stage = Konva.stages.find((s) => s.container().id === 'konva-container1');
  const new_bbox_list = []
  if (stage) {
    const drawingLayer = stage.findOne('.drawingLayer'); // Retrieve the layer
    const rects = drawingLayer.find('.bb'); // Find all Rect shapes
    console.log(rects)

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    rects.forEach((rect) => {
      console.log(rect.x(), rect.y());
      // dont allow too tiny bounding boxes
      if (Math.abs(rect.height()) * Math.abs(rect.width()) > 50) {
        bbox = {
          height: Math.abs(rect.height()) / 480,
          width: Math.abs(rect.width()) / 640,
          id: generateUUID4(),
          x: rect.x() / 640,
          y: rect.y() / 480,
          label: "ball", // FIXME 
        }
        new_bbox_list.push(bbox)
      }
    });
    state.top_image.annotation.bbox = new_bbox_list;

    fetch(state.api_url, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        image: state.top_image.id,
        annotations: state.top_image.annotation
      }),
    })
      .then(response => response.json())
      .then(data => {
        console.log("Success:", data);
      })
      .catch(error => {
        console.error("Error:", error);
      });
  }

  // FIXME: this would change uuid everytime you click submit
  const stage2 = Konva.stages.find((s) => s.container().id === 'konva-container2');
  const new_bbox_list2 = []
  if (stage2) {
    const drawingLayer = stage2.findOne('.drawingLayer'); // Retrieve the layer
    const rects = drawingLayer.find('.bb'); // Find all Rect shapes
    console.log(rects)

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    rects.forEach((rect) => {
      console.log("bla:", rect.x(), rect.y(), rect.width(), rect.height());
      // dont allow too tiny bounding boxes
      if (Math.abs(rect.height()) * Math.abs(rect.width()) > 50) {
        bbox = {
          height: Math.abs(rect.height()) / 480,
          width: Math.abs(rect.width()) / 640,
          id: generateUUID4(),
          x: rect.x() / 640,
          y: rect.y() / 480,
          label: "ball", // FIXME 
        }
        new_bbox_list2.push(bbox)
      }
    });
    state.bottom_image.annotation.bbox = new_bbox_list2;

    fetch(state.api_url, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        image: state.bottom_image.id,
        annotations: state.bottom_image.annotation
      }),
    })
      .then(response => response.json())
      .then(data => {
        console.log("Success:", data);
      })
      .catch(error => {
        console.error("Error:", error);
      });
  }
  console.log("Save function triggered!");
}

