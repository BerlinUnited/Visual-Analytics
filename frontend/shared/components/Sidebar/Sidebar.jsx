import { NavLink } from "react-router-dom";
import SidebarLogo from '@shared/components/SidebarLogo/SidebarLogo'
import SidebarBottom from '@shared/components/SidebarBottom/SidebarBottom'
import styles from './Sidebar.module.css';

const Sidebar = ({ appVersion }) => {

  const getNavLinkClass = (styles) => {
    return ({ isActive }) =>
      isActive ? `${styles.sidebar_item} ${styles.active}` : styles.sidebar_item;
  };

  return (
    <div className={styles.sidebar}>
      <SidebarLogo appVersion={appVersion} />

      <div className={styles.sidebar_content}>
        <nav className={styles.sidebar_nav}>
          <NavLink to="/" className={getNavLinkClass(styles)}>Home</NavLink >
          <NavLink to="/events" className={getNavLinkClass(styles)}>Events</NavLink >
          <NavLink to="/test" className={getNavLinkClass(styles)}>Test</NavLink >
        </nav>
        <SidebarBottom />
      </div>
    </div>
  );
};

export default Sidebar;