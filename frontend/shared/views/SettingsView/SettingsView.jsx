import { useState, useEffect } from 'react';
//import { saveToken, loadToken } from '@/store/tauri_store';
//import { saveLogRoot, loadLogRoot } from '@/store/tauri_store';

import styles from './SettingsView.module.css';

const SettingsView = () => {
  const [token, setToken] = useState('');
  const [log_root, setlogRoot] = useState('');

  /*
  useEffect(() => {
    async function loadSavedToken() {
      const savedToken = await loadToken();
      if (savedToken) {
        setToken(savedToken);
      }
    }
    async function loadSavedLogRoot() {
      const savedLogRoot = await loadLogRoot();
      if (savedLogRoot) {
        setlogRoot(savedLogRoot);
      }
    }
    loadSavedToken();
    loadSavedLogRoot();
  }, []);

  const handleSave = async () => {
    await saveToken(token);
    await saveLogRoot(log_root);
    alert('Token saved!');
  };*/

  return (
    <div className="view-content">
      <div className="panel-header">
        <h3>⚙️ Settings</h3>
      </div>
      <div className="panel-content">
        <div className={styles.info_card}>
          <lable>Api Token: </lable>
          <input
            type="password"
            value={token}
            onChange={(e) => setToken(e.target.value)}
            placeholder="Enter API token"
          />
          <button onClick={handleSave}>Save</button>
        </div>
        <div className={styles.info_card}>
          <lable>Log Folder: </lable>
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