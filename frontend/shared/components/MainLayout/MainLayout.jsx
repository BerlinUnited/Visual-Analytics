import { useRef } from 'react';
import Sidebar from '@shared/components/Sidebar/Sidebar';

import HomeView from '@shared/components/HomeView/HomeView';
import EventListView from '@shared/components/EventListView/EventListView.jsx';
import SettingsView from '@shared/components/SettingsView/SettingsView';
import GameListView from '@shared/components/GameListView/GameListView';
import LogListView from '@shared/components/LogListView/LogListView';
import VideoAnalysisView from '@shared/components/VideoAnalysisView/VideoAnalysisView';
import DebuggerView from '@shared/components/DebuggerView/DebuggerView';
import VideoPlayerCanvas from '@shared/components/VideoPlayerCanvas/VideoPlayerCanvas'

import { Routes, Route } from "react-router-dom";

const ResizableLayoutContent = ({ appVersion }) => {
  const containerRef = useRef(null);

  return (
    <div className="app-container" ref={containerRef}>
      <Sidebar
        appVersion={appVersion}
      />

      <div className="main-content">
        <Routes>
          <Route path="/" element={<HomeView />} />
          <Route element={<EventListView />} />
          <Route
            path="/events"
            element={
              <EventListView />
            }
          />
          <Route
            path="/events/:id"
            element={
              <GameListView />
            }
          />
          <Route
            path="/games/:id"
            element={
              <LogListView />
            }
          />
          <Route
            path="/video/:id"
            element={
              <VideoAnalysisView />
            }
          />
          <Route path="/settings" element={<SettingsView />} />
          <Route path="/debug" element={<DebuggerView />} />
          <Route path="/test" element={<VideoPlayerCanvas />} />

        </Routes>
      </div>
    </div>
  );
};

const ResizableLayout = ({ appVersion }) => {
  return (
    <ResizableLayoutContent appVersion={appVersion} />
  );
};

export default ResizableLayout;