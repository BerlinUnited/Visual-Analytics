const { contextBridge, ipcRenderer } = require('electron');

// Expose a limited set of APIs to the renderer process
contextBridge.exposeInMainWorld('electronAPI', {
  // Function to request loading a video by filename
  getVideoByFilename: (filename) => ipcRenderer.invoke('get-predefined-video-path', filename),

});