import { useState, useCallback, useEffect } from 'react';

export const useResizable = ({
  sidebarWidth,
  setSidebarWidth,
  topHeight,
  setTopHeight,
  containerRef
}) => {
  const [isDraggingVertical, setIsDraggingVertical] = useState(false);
  const [isDraggingHorizontal, setIsDraggingHorizontal] = useState(false);

  const handleVerticalMouseDown = useCallback((e) => {
    setIsDraggingVertical(true);
    e.preventDefault();
  }, []);

  const handleHorizontalMouseDown = useCallback((e) => {
    setIsDraggingHorizontal(true);
    e.preventDefault();
  }, []);

  const handleMouseMove = useCallback((e) => {
    if (isDraggingVertical && containerRef.current) {
      const containerRect = containerRef.current.getBoundingClientRect();
      const newWidth = e.clientX - containerRect.left;
      if (newWidth > 150 && newWidth < containerRect.width - 300) {
        setSidebarWidth(newWidth);
      }
    }
    
    if (isDraggingHorizontal && containerRef.current) {
      const containerRect = containerRef.current.getBoundingClientRect();
      const newHeight = e.clientY - containerRect.top;
      if (newHeight > 100 && newHeight < containerRect.height - 100) {
        setTopHeight(newHeight);
      }
    }
  }, [isDraggingVertical, isDraggingHorizontal, setSidebarWidth, setTopHeight]);

  const handleMouseUp = useCallback(() => {
    setIsDraggingVertical(false);
    setIsDraggingHorizontal(false);
  }, []);

  useEffect(() => {
    if (isDraggingVertical || isDraggingHorizontal) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = isDraggingVertical ? 'col-resize' : 'row-resize';
      document.body.style.userSelect = 'none';
      
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
        document.body.style.cursor = 'default';
        document.body.style.userSelect = 'auto';
      };
    }
  }, [isDraggingVertical, isDraggingHorizontal, handleMouseMove, handleMouseUp]);

  return {
    isDraggingVertical,
    isDraggingHorizontal,
    handleVerticalMouseDown,
    handleHorizontalMouseDown
  };
};