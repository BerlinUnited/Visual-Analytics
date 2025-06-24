import { useNavigate } from "react-router-dom";

import styles from './EventCard.module.css';
import robocup_img from '@shared/assets/robocup.jpeg';

const EventCard = ({ event }) => {
    const navigate = useNavigate();

    return (
        <div className={styles.event_card}>
            <div className={styles.event_header} onClick={() => navigate(`/events/${event.id}`)}>
                <img src={robocup_img} alt="RoboCup Image" />
            </div>
            <div className={styles.event_content}>
                <p className={styles.event_title}>
                    Event: {event.name}
                </p>
            </div>
            <div className={styles.event_footer}>
                <progress className={styles.event_progressbar} value="40" max="100">40%</progress>
            </div>
        </div>
    );
};

export default EventCard;