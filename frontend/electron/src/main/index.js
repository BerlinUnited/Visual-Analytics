import { app, shell, BrowserWindow, ipcMain } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import express from 'express';
import fs from 'node:fs' // Add fs for checking file existence
import path from 'node:path'
import { Conf } from 'electron-conf/main'

// Initialize store
const conf = new Conf()

let server;
let serverPort = 3001;

function createLocalServer() {
  const app = express();

  // Enable CORS for your frontend
  app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Range');
    res.header('Access-Control-Expose-Headers', 'Accept-Ranges, Content-Encoding, Content-Length, Content-Range');
    next();
  });
  // Serve video files with range support (crucial for seeking)
  app.get('/video/:filename', (req, res) => {
    const filename = req.params.filename;
    const videoPath = path.join("E:/logs/", filename); // Adjust path
    console.log("videoPath", videoPath)
    if (!fs.existsSync(videoPath)) {
      console.log("video not found")
      return res.status(404).send('Video not found');
    }

    const stat = fs.statSync(videoPath);
    const fileSize = stat.size;
    const range = req.headers.range;

    if (range) {
      // Handle range requests for seeking
      const parts = range.replace(/bytes=/, "").split("-");
      const start = parseInt(parts[0], 10);
      const end = parts[1] ? parseInt(parts[1], 10) : fileSize - 1;
      const chunksize = (end - start) + 1;
      const file = fs.createReadStream(videoPath, { start, end });

      res.writeHead(206, {
        'Content-Range': `bytes ${start}-${end}/${fileSize}`,
        'Accept-Ranges': 'bytes',
        'Content-Length': chunksize,
        'Content-Type': 'video/mp4',
      });
      file.pipe(res);
    } else {
      // Full file
      res.writeHead(200, {
        'Content-Length': fileSize,
        'Content-Type': 'video/mp4',
      });
      fs.createReadStream(videoPath).pipe(res);
    }
  });

  server = app.listen(serverPort, '127.0.0.1', () => {
    console.log(`Local video server running on port ${serverPort}`);
  });
}

function getFolderTree(dirPath, indent = '') {
  // Check if the directory path exists
  if (!fs.existsSync(dirPath)) {
    console.error(`Error: Directory not found at ${dirPath}`);
    return null;
  }

  try {
    // Get basic information about the path (is it a file or directory?)
    const stats = fs.statSync(dirPath);

    // If it's a file, return an object representing the file
    if (stats.isFile()) {
      return {
        name: path.basename(dirPath),
        type: 'file',
        path: dirPath
      };
    }

    // If it's a directory, proceed to read its contents
    if (stats.isDirectory()) {
      const tree = {
        name: path.basename(dirPath),
        type: 'directory',
        path: dirPath,
        children: []
      };

      // Read the contents of the directory
      const items = fs.readdirSync(dirPath);

      // Iterate over each item in the directory
      for (const item of items) {
        const itemPath = path.join(dirPath, item);
        // Recursively call getFolderTree for each item
        const child = getFolderTree(itemPath, indent + '  ');
        if (child) {
          tree.children.push(child);
        }
      }
      return tree;
    }
  } catch (error) {
    console.error(`Error processing path ${dirPath}:`, error);
    return null;
  }
}

const folderTree = getFolderTree("D:/Repositories/naoth-2020");
if (folderTree) {
  // Convert the object to a pretty-printed JSON string for better readability
  console.log(JSON.stringify(folderTree, null, 2));
}

function createWindow() {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    resizable: true,
    width: 900,
    height: 670,
    show: false,
    frame: true,
    autoHideMenuBar: true,

    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      nodeIntegration: false,
      contextIsolation: true,
    }
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow.maximize()
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // HMR for renderer base on electron-vite cli.
  // Load the remote URL for development or the local html file for production.
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}


// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  // Set app user model id for windows
  electronApp.setAppUserModelId('com.electron')

  // Default open or close DevTools by F12 in development
  // and ignore CommandOrControl + R in production.
  // see https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  createLocalServer();

  createWindow()




  console.log(conf.get('apiToken'))
  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })

})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// Expose config methods to renderer
ipcMain.handle('get-config', async (event, key) => {
  return conf.get(key);
});

ipcMain.handle('save-config', async (event, key, value) => {
  conf.set(key, value)
  return { success: true };
});