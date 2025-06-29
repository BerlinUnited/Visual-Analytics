import React, { useState, useEffect, useRef } from 'react';
import { Stage, Layer, Image as KonvaImage } from 'react-konva';
import styles from './VideoPlayerCanvas.module.css';

const VideoPlayerCanvas = () => {
    // State for video playback and dimensions
    const [isPlaying, setIsPlaying] = useState(false);
    const [videoDimensions, setVideoDimensions] = useState({ width: 0, height: 0 });
    const [videoUrl] = useState("https://www.w3schools.com/html/mov_bbb.mp4"); // Example video URL

    // Refs for the HTML video element and Konva components
    const videoRef = useRef(null);
    const layerRef = useRef(null); // Ref for the Konva Layer to trigger redraws
    const videoImageRef = useRef(null); // Ref for the Konva Image that displays the video frame

    // Function to draw the current video frame onto the Konva canvas
    // This callback is called by requestVideoFrameCallback
    const drawVideoFrame = (now, metadata) => {
        const videoElement = videoRef.current;
        const layer = layerRef.current;
        const videoImage = videoImageRef.current;

        if (videoElement && layer && videoImage) {
            // Set the image source for Konva.Image to the video element
            videoImage.image(videoElement);
            // Redraw the layer to update the video frame
            layer.draw();

            // If video is still playing, request the next frame callback
            if (!videoElement.paused && !videoElement.ended) {
                videoElement.requestVideoFrameCallback(drawVideoFrame);
            }
        }
    };

    // Effect to handle video element events and Konva setup
    useEffect(() => {
        const videoElement = videoRef.current;
        if (!videoElement) return;

        // --- Event Listeners for HTML Video Element ---

        // When video metadata is loaded, set its dimensions for the canvas
        const handleLoadedMetadata = () => {
            setVideoDimensions({
                width: videoElement.videoWidth,
                height: videoElement.videoHeight,
            });
            // Draw the first frame once metadata is loaded
            // This makes sure the video is visible on canvas before playing
            if (layerRef.current && videoImageRef.current) {
                videoImageRef.current.image(videoElement);
                layerRef.current.draw();
            }
        };

        // When video starts playing
        const handlePlay = () => {
            setIsPlaying(true);
            // Start the requestVideoFrameCallback loop when video plays
            // Check if requestVideoFrameCallback is supported
            if ('requestVideoFrameCallback' in HTMLVideoElement.prototype) {
                videoElement.requestVideoFrameCallback(drawVideoFrame);
            } else {
                // Fallback for browsers that don't support requestVideoFrameCallback
                // Use a less precise animation loop
                console.warn("requestVideoFrameCallback not supported. Using setInterval fallback for video updates.");
                const intervalId = setInterval(() => {
                    if (!videoElement.paused && !videoElement.ended) {
                        if (layerRef.current && videoImageRef.current) {
                            videoImageRef.current.image(videoElement);
                            layerRef.current.draw();
                        }
                    } else {
                        clearInterval(intervalId);
                    }
                }, 1000 / 30); // Aim for 30 FPS, adjust as needed
            }
        };

        // When video pauses
        const handlePause = () => {
            setIsPlaying(false);
        };

        // When video ends
        const handleEnded = () => {
            setIsPlaying(false);
        };

        videoElement.addEventListener('loadedmetadata', handleLoadedMetadata);
        videoElement.addEventListener('play', handlePlay);
        videoElement.addEventListener('pause', handlePause);
        videoElement.addEventListener('ended', handleEnded);

        // Cleanup function for event listeners
        return () => {
            videoElement.removeEventListener('loadedmetadata', handleLoadedMetadata);
            videoElement.removeEventListener('play', handlePlay);
            videoElement.removeEventListener('pause', handlePause);
            videoElement.removeEventListener('ended', handleEnded);
        };
    }, [videoUrl]); // Rerun effect if videoUrl changes

    // Handler for Play/Pause button
    const togglePlayPause = () => {
        const videoElement = videoRef.current;
        if (videoElement) {
            if (isPlaying) {
                videoElement.pause();
            } else {
                videoElement.play();
            }
        }
    };

    // Determine stage size based on video dimensions, with a fallback
    const stageWidth = videoDimensions.width || 640;
    const stageHeight = videoDimensions.height || 360;

    return (
        <div className={styles.wrapper}>
            <h1 className={styles.h1}>Video Annotation Tool</h1>

            <div className={styles.div2}>
                {/* Hidden HTML Video Element - Konva uses this as its source */}
                <video
                    ref={videoRef}
                    src={videoUrl}
                    preload="auto"
                    className={styles.video} // Keep the video element hidden
                />

                {/* Konva Stage and Layer to display video and annotations */}
                {/* The stage size is set based on the video's actual dimensions once loaded */}
                <Stage
                    width={stageWidth}
                    height={stageHeight}
                    className={styles.stage} // Make Konva stage responsive
                >
                    <Layer ref={layerRef}>
                        {/* Konva Image for displaying the video frame */}
                        <KonvaImage
                            ref={videoImageRef}
                            x={0}
                            y={0}
                            width={stageWidth}
                            height={stageHeight}
                        // The 'image' property will be set dynamically in drawVideoFrame
                        />
                        {/* Future annotations will be added here */}
                    </Layer>
                </Stage>
            </div>

            {/* Play/Pause Controls */}
            <button
                onClick={togglePlayPause}
                className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-md shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-75 transition-colors duration-200"
            >
                {isPlaying ? 'Pause' : 'Play'}
            </button>

            <p className={styles.text}>Video URL: {videoUrl}</p>
        </div>
    );
};

export default VideoPlayerCanvas;