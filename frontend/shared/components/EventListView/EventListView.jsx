
import { useQuery } from '@tanstack/react-query';
import EventCard from '@shared/components/EventCard/EventCard';
import SkeletonCard from '@shared/components/SkeletonCard/SkeletonCard';

import styles from './EventListView.module.css';


const fetch_events = async () => {
  const token = await electronAPI.get_value("apiToken");
  const response = await fetch(`https://vat.berlin-united.com/api/events/`, {
    headers: {
      'Authorization': `Token ${token}`
    }
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.json();
}

const EventListView = () => {

  const events = useQuery({
    queryKey: ['events'], queryFn: () => fetch_events(),
    staleTime: 5 * 60 * 1000, // Cache data for 5 minutes
    cacheTime: 5 * 60 * 1000,
  });

  if (events.isError) {
    return <div>Error fetching logs: {events.error.message}</div>;
  }

  return (
    <div className="view-content">
      <div className="panel-header">
        <h3>EventView</h3>
      </div>
      <div className={styles.projects_section}>
        <div className={`${styles.project_boxes} ${styles.jsGridView}`}>
          {events.isLoading ? (
            <SkeletonCard />
          ) : events.data.length > 0 ? (
            events.data.map((event) => (
              <EventCard
                event={event}
                key={event.name}
              ></EventCard>
            ))
          ) : (
            <div className={styles.emptyState}>
              No events found
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EventListView;