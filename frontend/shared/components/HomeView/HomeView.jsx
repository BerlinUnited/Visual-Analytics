import { Link } from "react-router-dom";
import ui_preview from '@shared/assets/home_screen_image.png';
import large_vat from '@shared/assets/logo.svg';
import styles from './HomeView.module.css';

const HomeView = () => {

  return (
    <div className={styles.view_content}>
      <div className={styles.panel_content}>
        <div className={styles.info_card_logo}>
          <img src={large_vat} className={styles.logo_image} alt="large VAT Logo" />
        </div>

        <div className={styles.info_grid}>
          <div className={styles.description}>
            <h1 className={styles.h11}>Welcome to the Visual Analytics Toolbox</h1>
            <p className={styles.p1}>
              <strong>Visual Analytics Toolbox</strong> is an interactive tool for viewing, annotating, and debugging robot soccer matches.
              Inspired by advanced sports analysis platforms, it goes beyond simple video review by integrating synchronized log data from each robot.
            </p>

            <p className={styles.p1}>Use this tool to:</p>
            <ul className={styles.ul1}>
              <li>Watch game recordings with overlaid positional data</li>
              <li>Tag and comment on key situations where behavior could be improved</li>
              <li>Inspect what each robot perceived, decided, and executed during any moment</li>
              <li>Dive into the corresponding code paths for deeper debugging</li>
            </ul>

            <p className={styles.p1}>
              This powerful workflow bridges the gap between observation and understanding, helping you fine-tune both strategy and implementation with precision.
            </p>

            <p className={styles.p1}>
              Let’s uncover what the robots were thinking—and why.
            </p>
          </div>
          <div className={styles.image_wrapper}>
            <img src={ui_preview} className={styles.main_img} alt="ui preview image" />
          </div>
        </div>
        <div className={styles.info_card}>
          <h2>Get Started</h2>
          <p>
            Register now and set up your api token and start getting insights into your robot soccer team.
          </p>
          <Link to="/settings" className={styles.link}>
            Register here
          </Link>
        </div>
      </div>

    </div>
  );
};

export default HomeView;