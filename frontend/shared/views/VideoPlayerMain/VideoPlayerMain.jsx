import { useRef } from 'react';
import { writeFile } from '@tauri-apps/plugin-fs';
import { join, tempDir } from '@tauri-apps/api/path';
import styles from './VideoPlayerMain.module.css';

const VideoPlayerMain = () => {
  // Create refs for the video, image, and a hidden canvas element
  const videoRef = useRef(null);
  const imageRef = useRef(null);
  const canvasRef = useRef(null);

  const playSelectedFile = (event) => {
    const file = event.target.files[0];
    if (file) {
      const fileURL = URL.createObjectURL(file);
      if (videoRef.current) {
        videoRef.current.src = fileURL;
      }
      // Clear any previous captured frame
      if (imageRef.current) {
        imageRef.current.src = '';
      }
    }
  };

  /**
   * Captures the current frame from the video and displays it in the image element.
   */
  const captureAndSaveFrame = async () => {
    if (!videoRef.current || !canvasRef.current || !imageRef.current) {
      console.error("Component refs are not ready.");
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataURL = canvas.toDataURL('image/png');
    imageRef.current.src = dataURL;

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


  return (
    <div className="view-content">
      <div className={styles.wrapper}>
        <div className={styles.video_wrapper}>
          <video
            ref={videoRef}
            controls
            width="640"
            autoPlay
            crossOrigin="anonymous" // Recommended for canvas operations
          />
        </div>
        <div className={styles.image_wrapper}>
          {/* Add the ref to your image tag */}
          <img ref={imageRef} className={styles.image} alt="Captured Frame" />
        </div>
      </div>

      {/* Input for selecting a video file */}
      <input
        type="file"
        accept="video/*"
        onChange={playSelectedFile}
      />

      {/* Button to trigger the frame capture */}
      <button onClick={captureAndSaveFrame} style={{ marginTop: '10px' }}>
        Capture Frame
      </button>

      {/* A hidden canvas element is used for drawing the frame */}
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
};

export default VideoPlayerMain;