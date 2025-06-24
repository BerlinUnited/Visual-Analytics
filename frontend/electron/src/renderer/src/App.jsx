
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState, useEffect } from 'react';
import VideoPlayer from '@shared/components/VideoPlayer';
import MainLayout from '@shared/components/MainLayout/MainLayout';

import '@shared/styles/App.css';
import '@shared/styles/global.css';

const queryClient = new QueryClient();

function App() {
  // TODO maybe we can get the versions here same as in rust
  const appVersion = "0.0.1"

  return (
    <div className="App">
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <MainLayout appVersion={appVersion} />
        </BrowserRouter>
      </QueryClientProvider>
    </div>
  );
}

export default App;