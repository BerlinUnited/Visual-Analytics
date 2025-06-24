import logo from '@shared/assets/logo_mini.svg';
import styles from './SidebarLogo.module.css';

const SidebarLogo = ({ appVersion }) => {
  return (
    <div className={styles.sidebar_header}>
      <img src={logo} className={styles.logo} alt="logo" />
      <p className={styles.version}>v{appVersion}</p>
    </div>
  );
};

export default SidebarLogo;