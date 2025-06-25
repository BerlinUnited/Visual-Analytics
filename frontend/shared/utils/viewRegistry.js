import HomeView from '@/views/HomeView';
import EventListView from '@/views/EventListView/EventListView.jsx';
import SearchView from '@/views/SearchView';
import SourceControlView from '@/views/SourceControlView';
import VideoAnalysisView from '@/views/VideoAnalysisView/VideoAnalysisView';
import VideoPlayerMain from '@/views/VideoPlayerMain/VideoPlayerMain';
import VideoPlayerMain2 from '@/views/VideoPlayerMain2';
import VideoPlayerMain3 from '@/views/VideoPlayerMain3';
import SettingsView from '@/views/SettingsView';

export const viewRegistry = { 
  home: {
    component: HomeView,
    title: 'Home',
    hasTimeline: false,
    showInSidebar: true,
  },
  'events': {
    component: EventListView,
    title: 'Events',
    hasTimeline: false,
    showInSidebar: true,
  },
  'games': {
    component: SearchView,
    title: 'Games',
    hasTimeline: false,
    showInSidebar: true,
  },
  'source-control': {
    component: SourceControlView,
    title: 'Source Control',
    hasTimeline: false,
    showInSidebar: true,
  },
  'videoplayer': {
    component: VideoPlayerMain,
    title: 'Video Player',
    hasTimeline: true, // This view has a timeline
    showInSidebar: true,
  },
  'VideoAnalysisView': {
    component: VideoAnalysisView,
    title: 'VideoAnalysisView',
    hasTimeline: false, // This view has a timeline
    showInSidebar: true,
  },
  
  'videoplayer2': {
    component: VideoPlayerMain2,
    title: 'Video Player2',
    hasTimeline: false, // This view has a timeline
    showInSidebar: true,
  },
  'videoplayer3': {
    component: VideoPlayerMain3,
    title: 'Video Player3',
    hasTimeline: false, // This view has a timeline
    showInSidebar: true,
  },
  settings: {
    component: SettingsView,
    title: 'Settings',
    hasTimeline: false,
    showInSidebar: true,
  }
};

export const getViewConfig = (viewId) => {
  return viewRegistry[viewId] || viewRegistry.home;
};
