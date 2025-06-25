//import { convert_video_path } from '@/utils/log_utils.js'
//import { useTokenData, fetchWithToken, fetchWithTokenFrontend } from '@/hooks/useTokenData';
//import { convertFileSrc } from '@tauri-apps/api/core';
import styles from './DataExplorer.module.css';
import { useRef, useState, useEffect } from 'react';
import path from 'path';
import { QueryClient } from '@tanstack/react-query';
import { useQuery } from '@tanstack/react-query';
//import { loadToken } from '@/store/tauri_store';

//import BackgroundCompiler from '@/components/BackgroundCompiler/BackgroundCompiler'



const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1,
    },
  },
})

async function fetchWithToken2(url) {

  const response = await fetch(url, {
    headers: {
      'Authorization': `Token f71cdba178c23200963605d088470e5d39179150`
    }
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

const DataExplorer = ({
  game,
  logs,
  videos,
  onclick_handler,
  videoRef,
  currentTime,
  onShowImageView,
  onClose
}) => {

  //TODO: this needs to have an online method and a offline method
  /*
  const [selectedLogId, setSelectedLogId] = useState(null);
  
  // Only make the API call when a log is selected
  const { data: imageData, isLoading, error } = useTokenData(
      selectedLogId ? `http://127.0.0.1:8000/api/image-sync/?log=${selectedLogId}` : null
  );*/

  const get_current_frame = async (log, camera) => {
    console.log("trying to get current frame")
    const log_id = log.id
    if (videoRef.current) {
      videoRef.current.pause();
      console.log('Stopped at:', currentTime, " for log id ", log_id);
    }
    try {
      const data = await queryClient.fetchQuery({ queryKey: [log_id], queryFn: async () => fetchWithToken2(`http://localhost:8000/api/image-sync/?log=${log_id}&time=${currentTime}&camera=${camera}`) })
      console.log("random url: ", data)
      const url = convertFileSrc("E:/logs/" + data.url);
      console.log("E:/logs/" + data.url)
      onShowImageView(url);
    } catch (error) {
      console.log(error)
    }
  }

  /*
  // Effect to handle the API response
  useEffect(() => {
      if (imageData && imageData.url && selectedLogId) {
          console.log(imageData)
          onShowImageView(imageData.url);
          // Reset the selected log ID after handling the response
          setSelectedLogId(null);
      }
  }, [imageData, selectedLogId, onShowImageView]);
  */
  //FIXME: make root path  (E:/logs) are settings
  return (
    <div className={styles.data_explorer}>
      <div class={styles.header}>
        <h1>Team 1 vs. Team 2 - Second Half</h1>
      </div>
      <div class={styles.video_recordings}>
        <h2 >Video Recordings</h2>
        <ul>
          {videos.map((video) => (
            <li key={video.id} className={styles.data_row} onClick={() => onclick_handler("http://localhost:3001/video/" + encodeURIComponent(video.video_path))}>
              <svg fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <span>{video.video_path}</span>
            </li>
          ))}
        </ul>
      </div>
      <section class={styles.log_table_wrapper}>
        <h2>Player Logs</h2>
        <table>
          <thead>
            <tr>
              <th scope="col">Player</th>
              <th scope="col">Head #</th>
              <th scope="col">Git Commit</th>
              <th scope="col">Bottom</th>
              <th scope="col">Top</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log) => (
              <tr key={log.id} className={styles.data_row}>
                <td> {log.player_number} </td>
                <td>{log.head_number}</td>
                <td>{log.git_commit}</td>
                <td className={styles.clickme} onClick={() => get_current_frame(log, "TOP")}>Show</td>
                <td className={styles.clickme} onClick={() => get_current_frame(log, "BOTTOM")}>Show</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <p>
        <button onClick={onClose}>
          Return to Video
        </button>
      </p>
    </div>
  );
};

export default DataExplorer;