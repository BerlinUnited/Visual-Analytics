import { useRef, useState, useEffect, useCallback } from 'react';
import { useParams } from "react-router-dom";
import { useQueries } from '@tanstack/react-query';

import VideoPlayer from '@shared/components/VideoPlayer/VideoPlayer';
import VideoControls from '@shared/components/VideoControls/VideoControls';
import Timeline from '@shared/components/Timeline/Timeline';
import ImageView from '@shared/components/ImageView/ImageView';
import DataExplorer from '@shared/components/DataExplorer/DataExplorer';
import styles from './VideoAnalysisView.module.css';


const MOCK_ANNOTATIONS = {
    // Frames 30-89: A red box
    ...Object.fromEntries(Array.from({ length: 60 }, (_, i) => [i + 30, [{
        id: 'box1', type: 'rect', x: 50, y: 60, width: 150, height: 100,
        stroke: '#ff4d4d', strokeWidth: 4, fill: 'rgba(255, 77, 77, 0.2)'
    }]])),
    // Frames 90-150: The red box moves to the right
    ...Object.fromEntries(Array.from({ length: 61 }, (_, i) => [i + 90, [{
        id: 'box1', type: 'rect', x: 50 + (i * 3), y: 60, width: 150, height: 100,
        stroke: '#ff4d4d', strokeWidth: 4, fill: 'rgba(255, 77, 77, 0.2)'
    }]])),
    // Frames 160-220: A blue circle appears
    ...Object.fromEntries(Array.from({ length: 61 }, (_, i) => [i + 160, [
        {
            id: 'box1', type: 'rect', x: 230, y: 60, width: 150, height: 100,
            stroke: '#ff4d4d', strokeWidth: 4, fill: 'rgba(255, 77, 77, 0.2)'
        },
        {
            id: 'box2', type: 'rect', x: 350, y: 150, width: 120, height: 120,
            stroke: '#4d4dff', strokeWidth: 4, fill: 'rgba(77, 77, 255, 0.2)', cornerRadius: 10
        }
    ]]))
};
const FPS = 30;


const fetch_logs = async (game_id) => {
    const token = await electronAPI.get_value("apiToken");
    const response = await fetch(`https://vat.berlin-united.com/api/logs?game=${game_id}`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

const fetch_videos = async (game_id) => {
    const token = await electronAPI.get_value("apiToken");
    const response = await fetch(`https://vat.berlin-united.com/api/video?game=${game_id}`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

const VideoAnalysisView = () => {
    const { id } = useParams();

    const results = useQueries({
        queries: [
            { queryKey: ['logs'], queryFn: () => fetch_logs(id), staleTime: 5 * 60 * 1000, },
            { queryKey: ['videos'], queryFn: () => fetch_videos(id), staleTime: 5 * 60 * 1000, },
        ],
    });

    const [logs, videos] = results;

    // --- State Management ---
    const [videoSrc, setVideoSrc] = useState(null);
    const [allAnnotations, setAllAnnotations] = useState({}); // Cache for all fetched annotations
    const [currentFrameAnnotations, setCurrentFrameAnnotations] = useState([]);
    const [selectedTime, setSelectedTime] = useState(0);
    // Playback state
    const [isPlaying, setIsPlaying] = useState(false);
    const [duration, setDuration] = useState(0);
    const [currentTime, setCurrentTime] = useState(0);
    const [currentFrame, setCurrentFrame] = useState(0);

    // Player dimensions
    const [dimensions, setDimensions] = useState({ width: 640, height: 360 });

    // state for image/video view change
    const [currentView, setCurrentView] = useState('video'); // 'video' or 'image'
    const [imageData, setImageData] = useState(null); // Will store the fetched image

    const videoRef = useRef(null);
    const drawCanvasRef = useRef(null);


    // --- Data Fetching Logic ---
    // In a real app, this effect would fetch data in chunks based on currentTime.
    // For this example, we'll "fetch" all mock data at once.
    useEffect(() => {
        // Simulating an API call that returns all annotation data
        const fetchAnnotations = () => {
            console.log("Fetching and caching all annotation data...");
            setAllAnnotations(MOCK_ANNOTATIONS);
        };

        fetchAnnotations();
    }, []);

    const load_video = async (local_url) => {
        try {
            // Convert the file path to a usable URL
            //const url = convertFileSrc(filePath);
            console.log("local_url", encodeURI(local_url))
            videoRef.current.currentTime = 0;
            setCurrentTime(0);
            setCurrentFrame(0);
            setIsPlaying(false);
            setVideoSrc(local_url);
            videoRef.current.pause()
        } catch (error) {
            console.error('Error loading video:', error);
        }
    }

    // --- Callbacks passed to children ---
    const handleTimeSelect = (time) => {
        console.log(`Time selected: ${time.toFixed(2)}s`);
        setSelectedTime(time);
        if (videoRef.current) {
            videoRef.current.currentTime = time;
            setCurrentTime(time); // Update state immediately for responsive UI
        }
    };

    // Action handlers for controls
    const handlePlayPause = useCallback(() => {
        if (videoRef.current) {
            isPlaying ? videoRef.current.pause() : videoRef.current.play();
        }
    }, [isPlaying]);

    const handleSeek = useCallback((event) => {
        const newTime = Number(event.target.value);
        if (videoRef.current) {
            videoRef.current.currentTime = newTime;
            setCurrentTime(newTime); // Update state immediately for responsive UI
        }
    }, []);

    // Event handlers from the video player
    const handleMetadataLoaded = useCallback(() => {
        if (videoRef.current) {
            setDimensions({ width: videoRef.current.videoWidth, height: videoRef.current.videoHeight });
            setDuration(videoRef.current.duration);
        }
    }, []);

    const handleTimeUpdate = useCallback(() => {
        if (videoRef.current) {
            const time = videoRef.current.currentTime;
            const frame = Math.floor(time * FPS);
            setCurrentTime(time);
            setCurrentFrame(frame);
            // This is where the parent looks up the correct annotation for the frame
            setCurrentFrameAnnotations(allAnnotations[frame] || []);
        }
    }, [allAnnotations]);

    const handlePlay = useCallback(() => setIsPlaying(true), []);
    const handlePause = useCallback(() => setIsPlaying(false), []);

    const handleFetchImage = (imageData) => {
        setImageData(imageData);
        setCurrentView('image');
    };

    const captureAndSaveFrame = async () => {
        if (!videoRef.current || !drawCanvasRef.current) {
            console.error("Component refs are not ready.");
            return;
        }

        const video = videoRef.current;
        const canvas = drawCanvasRef.current;
        const context = canvas.getContext('2d');

        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        const dataURL = canvas.toDataURL('image/png');
        // --- Tauri File Saving Logic ---

        try {
            // 1. Convert the Base64 dataURL to a binary format (Uint8Array)
            const base64 = dataURL.split(',')[1];
            const binaryString = window.atob(base64);
            const len = binaryString.length;
            const bytes = new Uint8Array(len);
            for (let i = 0; i < len; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }

            // 2. Get the path to the OS's temporary directory
            const temp_dir = await tempDir();

            // 3. Create a full file path
            const filePath = await join(temp_dir, `capture-${Date.now()}.png`);

            // 4. Write the file to the path
            await writeFile(filePath, bytes);

            // 5. Log the path to the console
            console.log('✅ Image saved successfully to:', filePath);

        } catch (error) {
            console.error('Failed to save the image:', error);
        }
    };

    if (logs.isLoading || videos.isLoading) {
        return <div>Loading...</div>;
    }

    if (logs.isError || videos.isError) {
        return <div>Error fetching logs: {logs.error.message}</div>;
    }

    return (
        <div className={styles.videoanalysis_wrapper}>
            <DataExplorer
                logs={logs.data}
                videos={videos.data}
                onclick_handler={load_video}
                videoRef={videoRef}
                currentTime={currentTime}
                onShowImageView={handleFetchImage}
                onClose={() => setCurrentView('video')}
            />

            <div className={styles.media_view}>
                {currentView === 'video' ? (
                    <>
                        <VideoPlayer
                            ref={videoRef}
                            videoSrc={videoSrc}
                            annotations={currentFrameAnnotations}
                            dimensions={dimensions}
                            currentFrame={currentFrame}
                            onMetadataLoaded={handleMetadataLoaded}
                            onTimeUpdate={handleTimeUpdate}
                            onPlay={handlePlay}
                            onPause={handlePause}
                        />
                        <VideoControls
                            isPlaying={isPlaying}
                            currentTime={currentTime}
                            duration={duration}
                            onPlayPause={handlePlayPause}
                            onSeek={handleSeek}
                        />
                    </>
                ) : (
                    <ImageView
                        imageData={imageData}
                    />
                )}

            </div>
            <div className={styles.timeline}>
                <Timeline
                    onTimeSelect={handleTimeSelect}
                />
            </div>
        </div>
    );
};

export default VideoAnalysisView;