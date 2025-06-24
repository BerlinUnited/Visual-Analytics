import { useRef } from 'react';
import Sidebar from '@shared/components/Sidebar/Sidebar';

import HomeView from '@shared/views/HomeView/HomeView';
import EventListView from '@shared/views/EventListView/EventListView.jsx';
import SettingsView from '@shared/views/SettingsView/SettingsView';
import GameListView from '@shared/views/GameListView/GameListView';
import LogListView from '@shared/views/LogListView/LogListView';
import VideoAnalysisView from '@shared/views/VideoAnalysisView/VideoAnalysisView';

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