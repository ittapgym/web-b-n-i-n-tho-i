const { app, BrowserWindow } = require('electron');
const path = require('path');

app.commandLine.appendSwitch('disable-gpu-shader-disk-cache');
app.setPath('userData', path.join(app.getPath('appData'), 'PeachAdmin'));

function createWindow() {
  const win = new BrowserWindow({
    width: 1500,
    height: 700,
    minWidth: 1350,
    minHeight: 600,
    maxWidth: 1500, // Khống chế kéo ngang tối đa là 1500
    maxHeight: 800, // Khống chế kéo dọc tối đa là 800
    frame: false,
    transparent: true,
    backgroundColor: '#00000000',
    titleBarStyle: 'hidden',
    resizable: true,
    webPreferences: {
      nodeIntegration: true, 
      contextIsolation: false
    }
  });

  win.loadFile('index.html');

  win.webContents.session.webRequest.onHeadersReceived((details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        'Content-Security-Policy': [
          "default-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://via.placeholder.com https://store.storeimages.cdn-apple.com https://fonts.googleapis.com https://fonts.gstatic.com; connect-src 'self' http://127.0.0.1:8000; img-src 'self' data: https: http://127.0.0.1:8000; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' data: https://fonts.gstatic.com"
        ]
      }
    });
  });

  win.setMenuBarVisibility(false);

  // Window Controls IPC — Workaround for transparent + unmaximize bug on Windows
  const { ipcMain } = require('electron');
  let savedBounds = null;

  ipcMain.on('window-close', () => win.close());
  ipcMain.on('window-minimize', () => win.minimize());
  ipcMain.on('window-maximize', () => {
    if (win.isMaximized()) {
      win.unmaximize();
    } else {
      win.setMaximumSize(10000, 10000); // Gỡ giới hạn 1500 trước khi Maximize
      win.maximize();
    }
  });

  const updateState = () => {
    const isMax = win.isMaximized();
    win.webContents.send('window-state-maximized', isMax);
    win.webContents.executeJavaScript(`
      if (${isMax}) {
        document.body.classList.add('is-maximized');
      } else {
        document.body.classList.remove('is-maximized');
      }
    `);
  };

  win.on('will-maximize', () => {
    win.setMaximumSize(10000, 10000); // Cho phép mở rộng hết cỡ khi phóng to
  });

  win.on('maximize', updateState);
  
  win.on('unmaximize', () => {
    win.setMaximumSize(1500, 800); // Khóa lại kéo ngang 1500 và dọc 800 khi thu nhỏ
    updateState();
  });

  win.on('resize', updateState);
  
  // Kiểm tra trạng thái lúc vừa load xong
  win.webContents.on('did-finish-load', updateState);
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
