import { ChevronRightIcon, FileIcon } from "@primer/octicons-react";
import { useState, useEffect, useRef } from "react";

import styles from './FileTree.module.css';

function FileTree({ fileTree, handleActiveEditorTabs }) {
    const [isExpanded, setIsExpanded] = useState(false);
    const [showOptions, setShowOptions] = useState(false);

    const [isRenaming, setIsRenaming] = useState({
        showInput: false,
        name: "",
        newName: "",
        id: null,
    });
    const inputRef = useRef(null);


    useEffect(() => {
        if (isRenaming.showInput && inputRef.current) {
            inputRef.current.focus();
            inputRef.current.select();
        }
    }, [isRenaming.showInput]);


    if (fileTree.type === "folder") {
        return (
            <>
                <div
                    onMouseOver={() => setShowOptions(true)}
                    onMouseLeave={() => setShowOptions(false)}
                    className={styles.div3}
                >
                    <div className={styles.div1} onClick={() => setIsExpanded(!isExpanded)}>
                        <span className={`${isExpanded ? "rotate-90" : ""} flex items-center`}>
                            <ChevronRightIcon size={12} />
                        </span>
                        <span className={styles.span1}>
                            {fileTree.name}
                        </span>
                    </div>
                </div>

                {isExpanded && (
                    <div className={styles.pl2}>

                        {fileTree.children?.map((child) => (
                            <FileTree
                                key={child.id}
                                fileTree={child}
                                handleActiveEditorTabs={handleActiveEditorTabs}
                            />
                        ))}
                    </div>
                )}
            </>
        );
    }

    return (
        <div
            onClick={() => handleActiveEditorTabs(fileTree.id, fileTree.name, fileTree.data)}
            onMouseOver={() => setShowOptions(true)}
            onMouseLeave={() => setShowOptions(false)}
            className={styles.div2}
        >
            <div className={styles.div1}>
                <FileIcon size={12} />
                <span className={styles.span1}>
                    {fileTree.name}
                </span>
            </div>
        </div>
    );
}

function DropdownMenu({ isOpen, onClose, type, onItemClick, fileTreeId, fileTreeName }) {
    const dropdownRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                onClose();
            }
        };

        if (isOpen) {
            document.addEventListener("mousedown", handleClickOutside);
        }

        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [isOpen, onClose]);

    const handleClick = (action) => (e) => {
        e.stopPropagation();
        onItemClick(action, fileTreeId, fileTreeName);
        onClose();
    };

    if (!isOpen) return null;

    return (
        <div ref={dropdownRef} className="absolute -right-1 top-7 shadow-xl min-w-48 bg-vsdark-3 backdrop-blur-3xl z-10 rounded">
            {type === "folder" && (
                <div className="flex flex-col p-1.5 gap-1">
                    <button
                        onClick={handleClick("newFile")}
                        className="w-full text-left px-3 py-1 text-vsdark-5 hover:bg-vsdark-4/30 hover:text-vsdark-6 rounded text-xs"
                    >
                        New File...
                    </button>
                    <button
                        onClick={handleClick("newFolder")}
                        className="w-full text-left px-3 py-1 text-vsdark-5 hover:bg-vsdark-4/30 hover:text-vsdark-6 rounded text-xs"
                    >
                        New Folder...
                    </button>
                </div>
            )}

            {type === "folder" && <div className="border-t border-vsdark-4/30 mt-1" />}

            <div className="flex flex-col p-1.5 gap-1">
                <button
                    onClick={handleClick("rename")}
                    className="w-full text-left px-3 py-1 text-vsdark-5 hover:bg-vsdark-4/30 hover:text-vsdark-6 rounded text-xs"
                >
                    Rename...
                </button>
                <button
                    onClick={handleClick("delete")}
                    className="w-full text-left px-3 py-1 text-vsdark-5 hover:bg-vsdark-4/30 hover:text-vsdark-6 rounded text-xs"
                >
                    Delete {type === "folder" ? "Folder" : "File"}
                </button>
            </div>
        </div>
    );
}

export default FileTree;