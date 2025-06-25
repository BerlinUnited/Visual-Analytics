import styles from './VideoControls.module.css';

const VideoControls = ({ 
    isPlaying, 
    currentTime, 
    duration, 
    onPlayPause, 
    onSeek 
}) => {
    // Helper to format time in MM:SS
    const formatTime = (timeInSeconds) => {
        const minutes = Math.floor(timeInSeconds / 60);
        const seconds = Math.floor(timeInSeconds % 60);
        return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    };

    return (
        <div className={styles.custom_controls_container}>
            <button onClick={onPlayPause} className={styles.play_pause_btn} aria-label={isPlaying ? 'Pause' : 'Play'}>
                {isPlaying ? (
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"></path></svg>
                ) : (
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"></path></svg>
                )}
            </button>
            <span className={styles.time_display}>{formatTime(currentTime)}</span>
            <input
                type="range"
                min="0"
                max={duration || 0}
                step="0.01" // for smoother seeking
                value={currentTime}
                onInput={onSeek} // onInput is better than onChange for live seeking
                className={styles.seek_slider}
            />
            <span className={styles.time_display}>{formatTime(duration)}</span>
        </div>
    );
};

export default VideoControls;