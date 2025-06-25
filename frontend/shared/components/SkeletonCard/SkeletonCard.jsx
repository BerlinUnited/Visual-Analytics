
import styles from './SkeletonCard.module.css';


const SkeletonCard = () => {
    return (
        <div className={styles.card_wrapper}>
            <div className={styles.card_header}>
                <div className={styles.imagePlaceholder}></div>
            </div>
            <div className={styles.card_content}>
                <p className={styles.card_title}>
                    Event
                </p>
            </div>
            <div className={styles.card_footer}>
                <progress className={styles.card_progressbar} value="40" max="100">40%</progress>
            </div>
        </div>
    );
};

export default SkeletonCard;