import { useParams, Link } from "react-router-dom";
//import { useTokenData } from '@shared/hooks/useTokenData';
import styles from './LogListView.module.css';
import LogCard from "@shared/components/LogCard/LogCard.jsx";


function LogListView() {
    // get the game id from the url
    const { id } = useParams();

    // get the list of logs for a game from the backend
    const { data, loading, error } = useTokenData(`https://vat.berlin-united.com/api/logs?game=${id}`);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    return (
        <div className="view-content">
            <div className="panel-header">
                <h3>LogView</h3>
            </div>
            <div className={styles.projects_section}>
                <div className={`${styles.project_boxes} ${styles.jsGridView}`}>
                    {data.map((log) => (
                        <Link to={`/logs/${log.id}`} key={log.id}>
                            <LogCard log={log} key={log.name}></LogCard>
                        </Link>
                    ))}

                </div>
            </div>
        </div>

    );
}

export default LogListView;