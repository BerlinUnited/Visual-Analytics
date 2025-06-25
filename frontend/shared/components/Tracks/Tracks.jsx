import styles from './Tracks.module.css';
import { useRef, useState, useEffect } from 'react';
import { Stage, Layer, Line, Text, Rect } from 'react-konva';

const Tracks = ({
    timelineWidth
}) => {
    const tracksStageRef = useRef();

    // Tracks state
    const [tracks, setTracks] = useState([
        { id: 1, name: 'Track 1', events: [] },
        { id: 2, name: 'Track 2', events: [] }
    ]);
    const [trackElements, setTrackElements] = useState(null)
    

    const tracksHeight = 200;
    const isVerticalScrollbarNeeded = null;
    const verticalScrollbarWidth = 20;
    const thumbHeight = 20;
    const trackHeight = 40;
    const zoom = 1;
    const offset = 0;
    const timelinePadding = 50;

    useEffect(() => {
        setTracks([
            {
                id: 1,
                name: '',
                events: [
                    { id: 1, startTime: 0, endTime: 5, label: 'Intro Music', color: '#4CAF50' },
                    { id: 2, startTime: 15, endTime: 24, label: 'Main Audio', color: '#2196F3' },

                ]
            },
            {
                id: 2,
                name: '',
                events: [
                    { id: 4, startTime: 0, endTime: 8, label: 'Title Sequence', color: '#9C27B0' },
                ]
            },
            {
                id: 3,
                name: '',
                events: [
                    { id: 7, startTime: 25, endTime: 35, label: 'Fade In', color: '#FFEB3B' },
                ]
            }
        ]);
    }, []);

    // Convert time (in seconds) to x position (for tracks without padding)
    const timeToXTracks = (timeInSeconds) => {
        const pixelsPerSecond = 50 * zoom;
        return timeInSeconds * pixelsPerSecond - offset;
    };

    // Generate track events
    const generateTrackEvents = () => {
        const trackElements = [];

        tracks.forEach((track, trackIndex) => {
            const trackY = trackIndex * trackHeight;

            // Only render tracks that are visible
            if (trackY + trackHeight >= 0 && trackY <= tracksHeight) {
                // Track background
                trackElements.push(
                    <Rect
                        key={`track-bg-${track.id}`}
                        x={0 + timelinePadding}
                        y={trackY}
                        width={timelineWidth - 2*timelinePadding}
                        height={trackHeight}
                        fill={trackIndex % 2 === 0 ? '#252526' : '#222'}
                        stroke="#3e3e42"
                        strokeWidth={1}

                    />
                );



                // Track events
                track.events.forEach((event) => {
                    const eventStartX = timeToXTracks(event.startTime) + timelinePadding;
                    const eventEndX = timeToXTracks(event.endTime);
                    const eventY = trackY;
                    const eventHeight = trackHeight;
                    //console.log("event:", event.label, eventStartX,  event.startTime)

                    // Calculate visible portion of the event
                    const visibleStartX = Math.max(0, eventStartX);
                    const visibleEndX = Math.min(timelineWidth - (isVerticalScrollbarNeeded ? verticalScrollbarWidth : 0), eventEndX);
                    const visibleWidth = visibleEndX - visibleStartX;

                    // Only render events that have a visible portion
                    if (visibleWidth > 0 && eventEndX >= 0 && eventStartX <= timelineWidth) {
                        trackElements.push(
                            <Rect
                                key={`event-${event.id}`}
                                x={visibleStartX}
                                y={eventY}
                                width={visibleWidth}
                                height={eventHeight}
                                fill={event.color}
                                stroke="#333"
                                strokeWidth={1}
                                cornerRadius={3}
                                opacity={0.8}
                                draggable
                                dragBoundFunc={(pos) => ({
                                    x: Math.max(+ timelinePadding, Math.min(pos.x, timelineWidth - visibleWidth - timelinePadding)),
                                    y: trackY,
                                })}
                            />
                        );
                        /*
                        // Event label (only if there's enough space and event starts in visible area)
                        if (visibleWidth > 50 && eventStartX >= 0) {
                            trackElements.push(
                                <Text
                                    key={`event-label-${event.id}`}
                                    x={visibleStartX + 5}
                                    y={eventY + 5}
                                    text={event.label}
                                    fontSize={10}
                                    fontFamily="Arial"
                                    fill="#fff"
                                    width={visibleWidth - 10}
                                />
                            );
                        }*/
                    }
                });
            }
        });

        return trackElements;
    };

    useEffect(() => {
        const trackElements = generateTrackEvents();
        setTrackElements(trackElements)
    }, [tracks]);

    
    return (
        <Stage
            width={timelineWidth}
            height={tracksHeight}
            ref={tracksStageRef}
        >
            <Layer>
                <Rect x={0} y={0} width={timelineWidth} height={tracksHeight} />
                {trackElements}

                {isVerticalScrollbarNeeded && (
                    <>
                        <Rect x={timelineWidth - verticalScrollbarWidth} y={0} width={verticalScrollbarWidth} height={tracksHeight} fill="#e0e0e0" stroke="#ccc" strokeWidth={1} />
                        <Rect x={timelineWidth - verticalScrollbarWidth + 2} y={thumbY} width={verticalScrollbarWidth - 4} height={thumbHeight} fill="#888" stroke="#666" strokeWidth={1} cornerRadius={(verticalScrollbarWidth - 4) / 2} />
                    </>
                )}
            </Layer>
        </Stage>
    );
};

export default Tracks;