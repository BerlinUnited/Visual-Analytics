import { FileIcon, XIcon } from "@primer/octicons-react";
import { useEffect, useState } from "react";
import Entry from "./Entry";


import styles from './FileEditor.module.css';

function FileEditor({ activeEditorTabs, selectedTabId, setSelectedTabId, handleCloseTab }) {
    const [selectedTabData, setSelectedTabData] = useState(null);

    useEffect(() => {
        const data = activeEditorTabs.find((tab) => tab.id === selectedTabId);
        setSelectedTabData(data?.data || "");
    }, [activeEditorTabs, selectedTabId]);

    return (
        <div className={styles.fileeditor_main}>
            {activeEditorTabs.length !== 0 ? (
                <>
                    <div className={styles.tabs}>
                        {activeEditorTabs.map((tab) => (
                            <TabButton
                                key={tab.id}
                                tab={tab}
                                handleCloseTab={handleCloseTab}
                                isSelected={tab.id === selectedTabId}
                                onClick={() => setSelectedTabId(tab.id)}
                            />
                        ))}
                    </div>
                    <div className={styles.text_content}>
                        {selectedTabData}
                    </div>
                </>
            ) : (
                <Entry />
            )}
        </div>
    );
}

function TabButton({ tab, isSelected, onClick, handleCloseTab }) {
    const activeClass = isSelected ? styles.tab_button_selected : styles.tab_button;

    return (
        <div
            role="button"
            onClick={onClick}
            className={activeClass}
        >
            <div className="flex items-center gap-1.5">
                <span className="flex items-center">
                    <FileIcon size={12} />
                </span>
                <span>{tab.name}</span>
            </div>
            <button
                className={styles.tab_button_close}
                onClick={(e) => {
                    e.stopPropagation();
                    handleCloseTab(tab.id);
                }}
            >
                <XIcon size={12} />
            </button>
        </div>
    );
}

export default FileEditor;