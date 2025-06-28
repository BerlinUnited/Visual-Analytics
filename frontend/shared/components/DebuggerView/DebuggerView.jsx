import { useState } from "react";

import FileExplorer from "@shared/components/FileExplorer/FileExplorer";
import FileEditor from "@shared/components/FileEditor/FileEditor";
import styles from './DebuggerView.module.css';

const DebuggerView = () => {
    const [activeEditorTabs, setActiveEditorTabs] = useState([]);
    const [selectedTabId, setSelectedTabId] = useState(null);

    const handleCloseTab = (tabId) => {
        const updatedActiveEditorTabs = activeEditorTabs.filter((tab) => tab.id !== tabId);

        setActiveEditorTabs(updatedActiveEditorTabs);

        if (activeEditorTabs.length !== 1) {
            setSelectedTabId(updatedActiveEditorTabs.at(-1).id);
        } else {
            setSelectedTabId(null);
        }
    };

    const handleActiveEditorTabs = (tabId, tabName, tabData) => {
        const newTab = {
            id: tabId,
            name: tabName,
            data: tabData,
        };

        const isAlreadyOpened = activeEditorTabs.some((activeTab) => activeTab.id === tabId);

        if (!isAlreadyOpened) {
            setActiveEditorTabs([...activeEditorTabs, newTab]);
            setSelectedTabId(tabId);
        } else {
            setSelectedTabId(tabId);
        }
    };

    return (
        <div className={styles.view_content}>
            <FileExplorer
                handleActiveEditorTabs={handleActiveEditorTabs}
                activeEditorTabs={activeEditorTabs}
                setActiveEditorTabs={setActiveEditorTabs}
                setSelectedTabId={setSelectedTabId}
            />
            <FileEditor
                activeEditorTabs={activeEditorTabs}
                handleCloseTab={handleCloseTab}
                selectedTabId={selectedTabId}
                setSelectedTabId={setSelectedTabId}
            />
        </div>
    );
};

export default DebuggerView;