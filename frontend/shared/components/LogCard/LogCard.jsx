import styles from './LogCard.module.css';
import robocup_img from '@shared/assets/robocup.jpeg';

const LogCard = ({ log }) => {

    return (
        <div className={styles.event_card}>
            <div className={styles.event_header}>
                <img src={robocup_img} alt="RoboCup Image" />
            </div>
            <div className={styles.event_content}>
                <p class="event_title">
                    Player number: {log.player_number}
                    <br />
                    Head number: {log.head_number}
                </p>

            </div>
            <div className={styles.event_footer}>
                <progress className={styles.event_progressbar} value="33" max="100">40%</progress>
            </div>
        </div>
    );
};

export default LogCard;