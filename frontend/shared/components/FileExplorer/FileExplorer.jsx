import { useEffect, useState } from "react";

import FileTree from "@shared/components/FileTree/FileTree";
import filesData from "./data";

import styles from './FileExplorer.module.css';

function FileExplorer({ handleActiveEditorTabs, setActiveEditorTabs, activeEditorTabs, setSelectedTabId }) {

    const [fileTree, setFileTree] = useState(filesData);

    useEffect(() => {
        if (!fileTree || (Array.isArray(fileTree) && fileTree.length === 0)) {
            const newFolder = {
                id: Date.now(),
                type: "folder",
                name: "welcome",
                children: [],
            };
            setFileTree(newFolder);
        }
    }, [fileTree]);

    return (
        <>
            <div className={styles.div1}>
                <div className="px-4 py-2 border-b border-b-vsdark-3">
                    <h3 className={styles.div2}>Explorer</h3>
                </div>
                <div className={styles.explorer3}>
                    <FileTree
                        fileTree={fileTree}
                        handleActiveEditorTabs={handleActiveEditorTabs}
                    />
                </div>
            </div>
        </>
    );
}

export default FileExplorer;