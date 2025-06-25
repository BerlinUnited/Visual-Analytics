import { invoke } from '@tauri-apps/api/core'
import { useState } from 'react';
import { useRef, useEffect } from 'react';
const BackgroundCompiler = () => {
  const [repoUrl, setRepoUrl] = useState('');
  const [commitHash, setCommitHash] = useState('');
  const [targetDir, setTargetDir] = useState('D:/');
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Initialize with default directory
  
  useEffect(() => {
    async function init() {
      const defaultDir = "D:/";
      setTargetDir(defaultDir + "repositories");
    }
    init();
  }, []);
    
  
  const handleFetchAndBuild = async () => {
    setIsLoading(true);
    setStatus('Starting...');
    setError('');
    
    try {
      setStatus('Cloning repository...');
      const result = await invoke('git_operations', { 
        repoUrl, 
        commitHash,
        targetDir: targetDir || undefined, // Fallback to Rust's default if empty
      });
      
      setStatus(`Operation completed successfully! ${result}`);
    } catch (err) {
      setError(err);
      setStatus('Operation failed');
    } finally {
      setIsLoading(false);
    }
  };

  
  return (
    <div>
      <h2>Fetch and Build Repository</h2>
      <div>
        <label>
          Repository URL:
          <input 
            type="text" 
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/user/repo.git"
          />
        </label>
      </div>
      <div>
        <label>
          Commit Hash:
          <input 
            type="text" 
            value={commitHash}
            onChange={(e) => setCommitHash(e.target.value)}
            placeholder="a1b2c3d..."
          />
        </label>
      </div>
      <div>
        <label>
          Target Directory:
          <input 
            type="text" 
            value={targetDir}
            onChange={(e) => setTargetDir(e.target.value)}
            placeholder="Leave empty for default location"
          />
        </label>
      </div>
      <button 
        onClick={handleFetchAndBuild} 
        disabled={isLoading || !repoUrl || !commitHash}
      >
        {isLoading ? 'Processing...' : 'Fetch & Build'}
      </button>
      
      {status && <div className="status">{status}</div>}
      {error && <div className="error">{error}</div>}
    </div>
  );
}

export default BackgroundCompiler;