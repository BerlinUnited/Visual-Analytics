import { useParams } from "react-router-dom";
import { useQuery } from '@tanstack/react-query';

import GameCard from "@shared/components/GameCard/GameCard.jsx";
import SkeletonCard from '@shared/components/SkeletonCard/SkeletonCard';
import styles from './GameListView.module.css';

const fetch_games = async (id) => {
    const token = await electronAPI.get_value("apiToken");
    const response = await fetch(`https://vat.berlin-united.com/api/games?event=${id}`, {
        headers: {
            'Authorization': `Token ${token}`
        }
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
}

function GameListView() {
    // get the event id from the url
    const { id } = useParams();

    const games = useQuery({
        queryKey: ['games', id], queryFn: () => fetch_games(id),
        staleTime: 5 * 60 * 1000, // Cache data for 5 minutes
        cacheTime: 5 * 60 * 1000,
    });

    if (games.isError) {
        return <div>Error fetching logs: {games.error.message}</div>;
    }

    return (
        <div className={styles.bla}>
            <div className="panel-header">
                <h3>GameView</h3>
            </div>

            <div className={styles.projects_section}>
                <div className={`${styles.project_boxes} ${styles.jsGridView}`}>
                    {games.isLoading ? (
                        <>
                            <SkeletonCard />
                            <SkeletonCard />
                            <SkeletonCard />
                        </>
                    ) : games.data.length > 0 ? (
                        games.data
                            .sort((a, b) => {
                                // Example: sort by 'name' in ascending order
                                if (a.game_folder < b.game_folder) return -1;
                                if (a.game_folder > b.game_folder) return 1;
                                return 0;

                            }).map((game) => (
                                <GameCard
                                    game={game}
                                    key={game.id}
                                ></GameCard>
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
}

export default GameListView;