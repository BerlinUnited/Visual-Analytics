import styles from './Timeline.module.css';
import { useRef, useState, useEffect } from 'react';

import Ruler from '@shared//components/Ruler/Ruler';
import Tracks from '@shared//components/Tracks/Tracks';

const Timeline = ({
    onTimeSelect,
}) => {
    const [timelineWidth, setTimelineWidth] = useState(null);

    const timeline_container_ref = useRef(null);
    useEffect(() => {
        if (timeline_container_ref.current) {
            const rect = timeline_container_ref.current.getBoundingClientRect();
            console.log("Timeline Width: ", rect.width); // Should now be non-zero
            setTimelineWidth(rect.width)
        }
    }, []);

    return (
        <div className={styles.timeline_container} ref={timeline_container_ref}>
            {timelineWidth && (<Ruler
                maxTime={700}
                timelineWidth={timelineWidth}
                onTimeSelect={onTimeSelect}
            />
            )}
            {timelineWidth && (<Tracks
                timelineWidth={timelineWidth}
            />
            )}
        </div>
    );
};

export default Timeline;