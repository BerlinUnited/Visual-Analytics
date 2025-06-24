import { useNavigate } from "react-router-dom";
import styles from './GameCard.module.css';
import robocup_img from '@shared/assets/robocup.jpeg';

const GameCard = ({ game }) => {
    const navigate = useNavigate();

    return (
        <div className={styles.event_card}>
            <div className={styles.event_header}>
                <img src={robocup_img} alt="RoboCup Image" />
                <h2>{game.team1} vs {game.team2}</h2>
                <h3>{game.half}</h3>
            </div>
            <div className={styles.event_content}>
                <div className={styles.my_button} onClick={() => navigate(`/games/${game.id}`)}>View Log Data</div>
                <div className={styles.my_button} onClick={() => navigate(`/video/${game.id}`)}>View Video Data</div>
            </div>
            <div className={styles.event_footer}>
                <progress className={styles.event_progressbar} value="40" max="100">40%</progress>
            </div>
        </div>
    );
};

export default GameCard;