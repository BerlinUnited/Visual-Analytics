import { useNavigate } from "react-router-dom";
import styles from './GameCard.module.css';
import robocup_img from '@shared/assets/robocup.jpeg';
import bembelbots from '@shared/assets/logos/3.png';
import berlin from '@shared/assets/logos/4.png';
import bhuman from '@shared/assets/logos/5.png';
import dutch from '@shared/assets/logos/8.png';
import naodevils from '@shared/assets/logos/12.png';
import htwk from '@shared/assets/logos/13.png';
import roboeireann from '@shared/assets/logos/17.png';
import runswift from '@shared/assets/logos/18.png';
import spqr from '@shared/assets/logos/19.png';
import nomadz from '@shared/assets/logos/33.png';
import naova from '@shared/assets/logos/45.png';
import r2 from '@shared/assets/logos/50.png';
import RedBackBots from '@shared/assets/logos/51.png';
import wistex from '@shared/assets/logos/54.png';


const GameCard = ({ game }) => {
    const navigate = useNavigate();

    // Define SVG dimensions and image sizes for responsiveness
    // ViewBox coordinates: 0,0 is top-left. Width and Height define the "canvas" size.
    // Images will be placed relative to this viewBox.
    const svgWidth = 300; // Logical width for the SVG canvas
    const svgHeight = 150; // Logical height for the SVG canvas
    const logoSize = 120; // Logical size for each logo

    // Calculate positions for logos and 'VS' text
    const team1LogoX = 20;
    const team1LogoY = (svgHeight - logoSize) / 2; // Vertically center
    const team2LogoX = svgWidth - logoSize - 20;
    const team2LogoY = (svgHeight - logoSize) / 2; // Vertically center
    const vsTextX = svgWidth / 2;
    const vsTextY = svgHeight / 2 + 10; // Adjust for vertical centering of text

    const teamLogos = {
        3: bembelbots,
        4: berlin,
        5: bhuman,
        8: bembelbots,
        12: bembelbots,
        13: bembelbots,
        17: bembelbots,
        18: bembelbots,
        19: bembelbots,
        33: bembelbots,
        45: bembelbots,
        50: bembelbots,
        51: bembelbots,
        54: bembelbots,
    };

    const team1Name = "B-Human";
    const team2Name = "B-Human";

    return (
        <div className={styles.event_card}>
            <div className={styles.event_header}>
                <svg
                    viewBox={`0 0 ${svgWidth} ${svgHeight}`}
                    className="w-full max-w-sm h-auto" // Responsive SVG
                    preserveAspectRatio="xMidYMid meet" // Maintain aspect ratio
                    aria-labelledby="match-title"
                    role="img"
                >
                    <title id="match-title">{`${team1Name} vs ${team2Name}`}</title>
                    {/* Team 1 Logo */}
                    <image
                        href={bhuman}
                        x={team1LogoX}
                        y={team1LogoY}
                        width={logoSize}
                        height={logoSize}
                        alt={`${team1Name} logo`}
                        // Add an onerror handler for robust image loading
                        onError={(e) => {
                            e.target.onerror = null; // Prevent infinite loop
                            e.target.href = 'https://placehold.co/100x100/CCCCCC/000000?text=Error'; // Fallback
                        }}
                    />

                    {/* Team 2 Logo */}
                    <image
                        href={bhuman}
                        x={team2LogoX}
                        y={team2LogoY}
                        width={logoSize}
                        height={logoSize}
                        alt={`${team2Name} logo`}
                        // Add an onerror handler for robust image loading
                        onError={(e) => {
                            e.target.onerror = null; // Prevent infinite loop
                            e.target.href = 'https://placehold.co/100x100/CCCCCC/000000?text=Error'; // Fallback
                        }}
                    />

                    {/* 'VS' Text Overlay */}
                    <text
                        x={vsTextX}
                        y={vsTextY}
                        textAnchor="middle" // Center horizontally
                        dominantBaseline="middle" // Center vertically
                        fontSize="48" // Larger font size for prominence
                        fontWeight="bold"
                        fill="#EF4444" // Tailwind red-500 equivalent
                        stroke="#FFFFFF" // White stroke for better visibility
                        strokeWidth="2"
                        className="font-inter opacity-90 drop-shadow-md" // Tailwind classes
                        aria-label="versus"
                    >
                        VS
                    </text>
                </svg>
                <h2>{game.team1} vs {game.team2}</h2>
                <h3>{game.half}</h3>
            </div>
            <div className={styles.event_content}>
                <div className={styles.my_button} onClick={() => navigate(`/games/${game.id}`)}>View Log Data</div>
                <div className={styles.my_button} onClick={() => navigate(`/video/${game.id}`)}>View Video Data</div>
            </div>
            <div className={styles.event_footer}>
                <progress className={styles.event_progressbar} value="40" max="100">40%</progress>
            </div>
        </div>
    );
};

export default GameCard;