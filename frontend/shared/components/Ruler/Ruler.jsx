import { useState, useRef, useCallback, useEffect, useMemo } from 'react';
import { Stage, Layer, Line, Text, Rect } from 'react-konva';

const calculateZoom = (width, maxTime, padding) => {
    const availableWidth = width - (padding * 2);
    const totalTimeWidth = maxTime * 50; // Base pixels per second * total seconds
    // Prevent division by zero and handle cases where width isn't ready
    if (!width || !maxTime || totalTimeWidth <= 0 || availableWidth <= 0) {
        return 1; // Return a default zoom
    }
    return availableWidth / totalTimeWidth;
};

const Ruler6 = ({
  maxTime,
  timelineWidth,
  onTimeSelect, // Note: onTimeSelect is not used in the provided code, but kept for API consistency
}) => {
  const timelineStageRef = useRef(null);
  const timelineHeight = 100;
  const timelineY = 55;

  const timelinePadding = 50;
  const scrollbarHeight = 10;
  const scrollbarY = timelineHeight - scrollbarHeight - 10;

  const [zoom, setZoom] = useState(() => calculateZoom(timelineWidth, maxTime, timelinePadding));
  const [offset, setOffset] = useState(0);

  // Refs to hold the latest state values for event handlers
  const zoomRef = useRef(zoom);
  const offsetRef = useRef(offset);
  const dragStartRef = useRef({ x: 0, offset: 0 });
  const isDraggingScrollbarRef = useRef(false);

  // Keep refs updated with the latest state
  useEffect(() => {
    zoomRef.current = zoom;
  }, [zoom]);

  useEffect(() => {
    offsetRef.current = offset;
  }, [offset]);


  useEffect(() => {
    const availableWidth = timelineWidth - (timelinePadding * 2);
    // Assuming a base pixels per second, e.g., 50. This can be adjusted.
    const totalTimeWidth = maxTime * 50;
    if (totalTimeWidth) {
      setZoom(availableWidth / totalTimeWidth);
    }
  }, [timelineWidth, maxTime]);

  // Convert time (in seconds) to x position
  const timeToX = useCallback((timeInSeconds) => {
    // Read from state for rendering
    const pixelsPerSecond = 50 * zoom;
    return timeInSeconds * pixelsPerSecond - offset + timelinePadding;
  }, [zoom, offset]);

  // Convert x position to time (in seconds)
  const xToTime = useCallback((x) => {
    // Use REFS for calculations in event handlers to get the latest value
    const pixelsPerSecond = 50 * zoomRef.current;
    return (x + offsetRef.current - timelinePadding) / pixelsPerSecond;
  }, []); // No dependencies needed as it uses refs

  // Calculate scrollbar properties
  const getScrollbarProperties = useCallback(() => {
    const totalWidth = maxTime * 50 * zoom + (timelinePadding * 2);
    const visibleRatio = timelineWidth / totalWidth;
    const scrollbarThumbWidth = Math.max(20, timelineWidth * visibleRatio);
    const scrollableWidth = timelineWidth - scrollbarThumbWidth;
    const maxOffset = Math.max(0, totalWidth - timelineWidth);
    const scrollbarThumbX = maxOffset > 0 ? (offset / maxOffset) * scrollableWidth : 0;
    const isScrollbarNeeded = totalWidth > timelineWidth;

    return {
      thumbWidth: scrollbarThumbWidth,
      thumbX: scrollbarThumbX,
      maxOffset,
      scrollableWidth,
      isScrollbarNeeded,
    };
  }, [maxTime, zoom, timelineWidth, offset]);

  // Clamp offset to valid range
  const clampOffset = useCallback((newOffset) => {
    const { maxOffset } = getScrollbarProperties();
    return Math.max(0, Math.min(maxOffset, newOffset));
  }, [getScrollbarProperties]);


  const handleTimelineClick = useCallback((e) => {
    const stage = e.target.getStage();
    if (!stage) return;
    const pointer = stage.getPointerPosition();

    const clickedTime = xToTime(pointer.x);
    const clampedTime = Math.max(0, Math.min(maxTime, clickedTime));

    //console.log(`Clicked at time: ${clampedTime.toFixed(2)}s`);
    // Pass the selected time to the parent component if the callback is provided
    if (onTimeSelect) {
        onTimeSelect(clampedTime);
    }
  }, [maxTime, xToTime, onTimeSelect]);


  const handleWheel = useCallback((e) => {
    e.evt.preventDefault();
    const stage = e.target.getStage();
    if (!stage) return;

    const pointer = stage.getPointerPosition();

    if (e.evt.ctrlKey || e.evt.metaKey) {
      // Zooming
      const scaleBy = 1.1;
      const oldZoom = zoomRef.current;
      const newZoom = e.evt.deltaY > 0 ? oldZoom / scaleBy : oldZoom * scaleBy;
      
      // Define your zoom limits
      const minZoom = 0.1; 
      const maxZoom = 10;
      const clampedZoom = Math.max(minZoom, Math.min(maxZoom, newZoom));
      
      const mouseTime = xToTime(pointer.x);
      
      // Recalculate offset to keep the time under the mouse pointer constant
      const newOffset = (mouseTime * 50 * clampedZoom) - (pointer.x - timelinePadding);
      
      setZoom(clampedZoom);
      setOffset(clampOffset(newOffset));

    } else {
      // Panning
      const { maxOffset } = getScrollbarProperties();
      if (maxOffset <= 0) return; // No need to pan if everything is visible

      const newOffset = offsetRef.current + e.evt.deltaX;
      setOffset(clampOffset(newOffset));
    }
  }, [clampOffset, getScrollbarProperties, xToTime]);

  const handleMouseDown = useCallback((e) => {
    const pointer = e.target.getStage().getPointerPosition();
    const { thumbX, thumbWidth, isScrollbarNeeded } = getScrollbarProperties();
    
    if (isScrollbarNeeded && pointer.y >= scrollbarY && pointer.y <= scrollbarY + scrollbarHeight) {
      if (pointer.x >= thumbX && pointer.x <= thumbX + thumbWidth) {
        isDraggingScrollbarRef.current = true;
        dragStartRef.current = { x: pointer.x, offset: offsetRef.current };
      }
    }
  }, [getScrollbarProperties, scrollbarY, scrollbarHeight]);


  const handleMouseMove = useCallback((e) => {
    if (!isDraggingScrollbarRef.current) return;

    const pointer = e.target.getStage().getPointerPosition();
    const { scrollableWidth, maxOffset } = getScrollbarProperties();

    const deltaX = pointer.x - dragStartRef.current.x;
    const offsetDelta = (deltaX / scrollableWidth) * maxOffset;
    
    const newOffset = dragStartRef.current.offset + offsetDelta;
    setOffset(clampOffset(newOffset));
  }, [clampOffset, getScrollbarProperties]);

  const handleMouseUpOrLeave = useCallback(() => {
    isDraggingScrollbarRef.current = false;
  }, []);


  const { ticks, labels } = useMemo(() => {
    const newTicks = [];
    const newLabels = [];
    const pixelsPerSecond = 50 * zoom;

    let majorTickInterval = 10;
    let minorTickInterval = 1;

    // Adjust tick intervals based on zoom level
    if (pixelsPerSecond < 2) {
      majorTickInterval = 120; minorTickInterval = 10;
    } else if (pixelsPerSecond < 5) {
      majorTickInterval = 60; minorTickInterval = 10;
    } else if (pixelsPerSecond < 15) {
      majorTickInterval = 10; minorTickInterval = 1;
    } else if (pixelsPerSecond < 50) {
      majorTickInterval = 5; minorTickInterval = 0.5;
    } else {
      majorTickInterval = 1; minorTickInterval = 0.1;
    }

    const startTime = Math.max(0, xToTime(timelinePadding));
    const endTime = Math.min(maxTime, xToTime(timelineWidth - timelinePadding));
    //console.log("endTime", endTime, "timelineWidth", timelineWidth, "xToTime", xToTime(timelineWidth))
    //console.log("offsetRef.current", offsetRef.current)

    const loopStart = Math.floor(startTime / minorTickInterval) * minorTickInterval;

    for (let time = loopStart; time <= endTime + 0.7; time += minorTickInterval) {
      if (time < 0) continue;

      const x = timeToX(time);
      const isMajorTick = Math.abs(time % majorTickInterval) < 0.001 || time === 0;
      const tickHeight = isMajorTick ? 20 : 10;

      newTicks.push(
        <Line key={`tick-${time}`} points={[x, timelineY, x, timelineY - tickHeight]} stroke="#fff" strokeWidth={1} />
      );

      if (isMajorTick) {
        newLabels.push(
          <Text key={`label-${time}`} x={x} y={timelineY - 35} text={`${Math.round(time)}s`} fontSize={12} fontFamily="Arial" fill="#fff" offsetX={10} align="center" />
        );
      }
    }
    return { ticks: newTicks, labels: newLabels };
  }, [zoom, maxTime, timeToX, xToTime]);


  const { thumbWidth, thumbX, isScrollbarNeeded } = getScrollbarProperties();

  return (
    <Stage
      width={timelineWidth}
      height={timelineHeight}
      onWheel={handleWheel}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUpOrLeave}
      onMouseLeave={handleMouseUpOrLeave}
      onClick={handleTimelineClick}
      ref={timelineStageRef}
      style={{ cursor: isDraggingScrollbarRef.current ? 'grabbing' : 'default' }}
    >
      <Layer>
        <Rect x={0} y={0} width={timelineWidth} height={timelineHeight} fill="#252526" />
        <Line points={[timelinePadding, timelineY, timelineWidth - timelinePadding, timelineY]} stroke="#fff" strokeWidth={2} />
        {ticks}
        {labels}

        {isScrollbarNeeded && (
          <>
            <Rect x={0} y={scrollbarY} width={timelineWidth} height={scrollbarHeight} fill="#444" cornerRadius={scrollbarHeight / 2} />
            <Rect 
              x={thumbX} 
              y={scrollbarY} 
              width={thumbWidth} 
              height={scrollbarHeight} 
              fill="#888" 
              cornerRadius={scrollbarHeight / 2} 
            />
          </>
        )}
      </Layer>
    </Stage>
  );
};

export default Ruler6;