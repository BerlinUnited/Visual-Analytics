import { forwardRef, useEffect } from 'react';
import { Stage, Layer, Rect, Text } from 'react-konva';
import styles from './VideoPlayer.module.css';

const VideoPlayer = forwardRef(({
    videoSrc,
    annotations,
    dimensions,
    currentFrame,
    onMetadataLoaded,
    onTimeUpdate,
    onPlay,
    onPause
}, ref) => {

    useEffect(() => {
        const video = ref.current;
        if (!video) return;

        // --- Event Listeners ---
        // These listeners report events up to the parent component.
        video.addEventListener('loadedmetadata', onMetadataLoaded);
        video.addEventListener('timeupdate', onTimeUpdate);
        video.addEventListener('play', onPlay);
        video.addEventListener('pause', onPause);

        return () => {
            video.removeEventListener('loadedmetadata', onMetadataLoaded);
            video.removeEventListener('timeupdate', onTimeUpdate);
            video.removeEventListener('play', onPlay);
            video.removeEventListener('pause', onPause);
        };
    }, [ref, videoSrc, onMetadataLoaded, onTimeUpdate, onPlay, onPause]);

    const renderAnnotation = (annotation) => {
        if (annotation.type === 'rect') {
            return <Rect key={annotation.id} {...annotation} />;
        }
        return null;
    };

    return (
        <div className={styles.blub}>
            <div className={styles.player_container}>
                <video ref={ref} src={videoSrc} className={styles.video_element} />
                <div className={styles.konva_overlay}>
                    <Stage width={dimensions.width} height={dimensions.height}>
                        <Layer>
                            {annotations.map(renderAnnotation)}
                            <Text
                                text={`Frame: ${currentFrame}`} x={10} y={10} fontSize={16} fill="#00ff00"
                                fontFamily='monospace' shadowColor="black" shadowBlur={5} shadowOffsetX={1} shadowOffsetY={1}
                            />
                        </Layer>
                    </Stage>
                </div>
            </div>
        </div>
    );
});

export default VideoPlayer;