import { useState, useEffect } from 'react';
import styles from './SettingsView.module.css';

const SettingsView = () => {
  const [token, setToken] = useState('');
  const [log_root, setlogRoot] = useState('');

  useEffect(() => {
    async function loadSavedToken() {
      const savedToken = await electronAPI.get_value("apiToken");
      if (savedToken) {
        setToken(savedToken);
      }
    }
    async function loadSavedLogRoot() {
      const savedLogRoot = await electronAPI.get_value("logRoot");
      if (savedLogRoot) {
        setlogRoot(savedLogRoot);
      }
    }
    loadSavedToken();
    loadSavedLogRoot();
  }, []);

  const handleSave = async () => {
    await electronAPI.set_value("apiToken", token);
    await electronAPI.set_value("logRoot", log_root);
    alert('Token saved!');
  };

  return (
    <div className="view-content">
      <div className="panel-header">
        <h3>⚙️ Settings</h3>
      </div>
      <div className="panel-content">
        <div className={styles.info_card}>
          <label>Api Token: </label>
          <input
            type="password"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            placeholder="Enter API token"
          />
          <button onClick={handleSave}>Save</button>
        </div>
        <div className={styles.info_card}>
          <label>Log Folder: </label>
          <input
            type="text"
            value={log_root}
            onChange={(e) => setlogRoot(e.target.value)}
            placeholder="Enter Root of log folder"
          />
          <button onClick={handleSave}>Save</button>
        </div>
      </div>
    </div>
  );
};

export default SettingsView;