import { useRef, useState, useEffect, useCallback } from 'react';

export default function VideoPlayer() {
    const videoFilename = "video3.mp4";
    const videoUrl = `http://localhost:3001/video/output.mp4`;

    const handleVideoEvents = (e) => {
        const video = e.target;
        console.log('Video event:', e.type, {
            videoWidth: video.videoWidth,
            videoHeight: video.videoHeight,
            currentTime: video.currentTime,
            duration: video.duration,
            readyState: video.readyState,
            networkState: video.networkState
        });
    };
    return (
        <video
            controls
            width="800"
            height="600"
            src={videoUrl}
            onLoadStart={handleVideoEvents}
            onLoadedMetadata={handleVideoEvents}
            onLoadedData={handleVideoEvents}
            onCanPlay={handleVideoEvents}
            onCanPlayThrough={handleVideoEvents}
            onPlay={handleVideoEvents}
            onError={(e) => console.error('Video error:', e)}
        >
            Your browser does not support the video tag.
        </video>
    );
}