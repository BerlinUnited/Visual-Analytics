
export function convert_video_path (video_path) {
    const lastUnderscoreIndex = video_path.lastIndexOf('_');
    const result = video_path.substring(lastUnderscoreIndex + 1);

    return result;
}

export function convert_log_path_to_name(log_path){
    //2025-03-12-GO25/2025-03-15_17-15-00_BerlinUnited_vs_Hulks_half2/game_logs/3_34_Nao0021_250315-1722/game.log
    const log_folder = log_path.split('/')[3];
    const parts = log_folder.split('_');
    
    playernumber = parts[0]
    head_number = parts[1]
    
    console.log(lastPart); // Output: "PiCam.mp4"
}   
//log.log_path
