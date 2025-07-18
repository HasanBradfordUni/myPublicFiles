import os
import sys
import json
import time
import shutil
import logging
import threading
import subprocess
from datetime import datetime
from pathlib import Path

"""The following imports are not from natively installed Python libraries,
see requirements.txt for which libraries to install."""

# PyQt6 imports (replacing Tkinter)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QRadioButton, QCheckBox, QGroupBox,
    QTreeWidget, QTreeWidgetItem, QScrollArea, QSpinBox, QTextEdit,
    QFileDialog, QMessageBox, QSplitter, QFrame, QButtonGroup, QDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QIcon

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ===============================
# APPLICATION PATH MANAGEMENT
# ===============================

# Get the directory where the script is running
APP_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# ===============================
# CONFIGURATION AND DEFAULT VALUES
# ===============================

DEFAULT_CONFIG = {
    'source_directory': '',
    'file_action': 'move',  # 'move' or 'copy'
    'destination_directory': '', # for choosing the destination directory
    'monitoring': {
        'enabled': False,
        'type': 'scheduled',  # 'realtime' or 'scheduled'
        'interval': 3600      # seconds, for scheduled monitoring
    },
    'sorting_rules': {
        'extensions': {
            'pdf': 'Documents/PDFs',
            'docx': 'Documents/Word',
            'xlsx': 'Documents/Excel',
            'jpg': 'Images/Photos',
            'png': 'Images/Photos',
            'mp3': 'Media/Audio',
            'mp4': 'Media/Video'
        },
        'patterns': {
            'invoice': 'Documents/Invoices',
            'receipt': 'Documents/Receipts'
        },
        'other': 'Unsorted'
    }
}

# ===============================
# CUSTOM LOGGER IMPLEMENTATION
# ===============================

class EnhancedLogger:
    """Enhanced logger that combines Python logging with custom log management"""
    
    def __init__(self, log_file="file_organizer.log"):
        self.log_file = log_file
        
        # Create log directory if it doesn't exist
        log_dir = APP_DIR / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Set up Python's standard logger
        self.logger = logging.getLogger("ManchesterUnitedFileOrganizer")
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers to avoid duplicates
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create file handler for standard logging with UTF-8 encoding
        file_handler = logging.FileHandler(log_dir / self.log_file, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)
        
        # Add console handler for debugging
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(console_handler)
        
        # Full path to the log file for custom operations
        self.log_path = log_dir / self.log_file
        
    def info(self, message):
        """Log an info message"""
        self.logger.info(message)
        self._add_to_logs(f"INFO: {message}")
    
    def error(self, message, exc_info=False):
        """Log an error message"""
        self.logger.error(message, exc_info=exc_info)
        self._add_to_error_logs(f"ERROR: {message}")
    
    def warning(self, message):
        """Log a warning message"""
        self.logger.warning(message)
        self._add_to_logs(f"WARNING: {message}")
    
    def debug(self, message):
        """Log a debug message"""
        self.logger.debug(message)
    
    def _add_to_logs(self, message):
        """Add custom formatted output logs"""
        with open(self.log_path, 'a', encoding='utf-8') as logger:
            logger.write("Output:\n")
            message = message.replace("  ", "\n")
            logger.write(message + "\n")
    
    def _add_to_error_logs(self, error_message):
        """Add custom formatted error logs"""
        with open(self.log_path, 'a', encoding='utf-8') as logger:
            logger.write("Error:\n")
            error_message = error_message.replace("  ", "\n")
            logger.write(error_message + "\n")
    
    def _add_to_input_logs(self, input_prompt, input_statement):
        """Add custom formatted input logs"""
        with open(self.log_path, 'a', encoding='utf-8') as logger:
            logger.write("User Input:\n")
            logger.write(input_prompt + " " + input_statement + "\n")
    
    def search_logs(self, search_term, log_type="all"):
        """Search logs for a specific term"""
        try:
            with open(self.log_path, 'r', encoding='utf-8') as logger:
                lines = logger.readlines()
                
            results = []
            line_type = None
            
            for line_num, line in enumerate(lines):
                if line.startswith("Output:"):
                    line_type = "output"
                elif line.startswith("Error:"):
                    line_type = "error"  
                elif line.startswith("User Input:"):
                    line_type = "input"
                    
                # Filter by log type if specified
                if log_type != "all" and line_type != log_type:
                    continue
                    
                if search_term.lower() in line.lower():
                    results.append(f"Line {line_num}: {line.strip()}")
                    
            return results
        except Exception as e:
            self.error(f"Error searching logs: {str(e)}")
            return [f"Error searching logs: {str(e)}"]
    
    def get_recent_logs(self, count=50, log_type="all"):
        """Get the most recent logs"""
        try:
            with open(self.log_path, 'r', encoding='utf-8') as logger:
                lines = logger.readlines()
                
            results = []
            line_type = None
            
            # Process in reverse to get the most recent logs first
            for line_num, line in enumerate(reversed(lines)):
                if line_num >= count:
                    break
                    
                if line.startswith("Output:"):
                    line_type = "output"
                elif line.startswith("Error:"):
                    line_type = "error"  
                elif line.startswith("User Input:"):
                    line_type = "input"
                    
                # Filter by log type if specified
                if log_type != "all" and line_type != log_type:
                    continue
                    
                results.append(line.strip())
                
            return results
        except FileNotFoundError:
            self.info("Log file does not exist yet.")
            return ["No logs found - log file does not exist yet."]
        except Exception as e:
            self.error(f"Error reading logs: {str(e)}")
            return [f"Error reading logs: {str(e)}"]

# Initialize the logger
logger = EnhancedLogger()

# ===============================
# FILE SORTER CLASS
# ===============================

class FileSorter:
    def __init__(self, config):
        self.config = config
        self.source_dir = Path(config.get('source_directory', ''))
        self.destination_dir = Path(config.get('destination_directory', ''))
        
        # Fix: If destination directory is empty or not set, explicitly use the source directory
        if not self.destination_dir or str(self.destination_dir).strip() == '':
            self.destination_dir = self.source_dir
            
        # Log the directories being used
        logger.info(f"Source directory: {self.source_dir}")
        logger.info(f"Destination directory: {self.destination_dir}")
        
        self.rules = config.get('sorting_rules', {})
        self.action = config.get('file_action', 'move')  # 'move' or 'copy'
        
    def sort_files(self):
        """Sort all files in the source directory according to rules."""
        if not self.source_dir.exists():
            logger.error(f"Source directory does not exist: {self.source_dir}")
            return False
            
        # Double-check that destination directory is properly set
        # If destination is empty, use source directory
        if not self.destination_dir or str(self.destination_dir).strip() == '':
            self.destination_dir = self.source_dir
            print(self.destination_dir)
            logger.info(f"Empty destination directory. Using source directory instead: {self.destination_dir}")
            
        if str(self.destination_dir).strip() == ".":
            self.destination_dir = self.source_dir
        logger.info(f"Starting file sorting from {self.source_dir} to {self.destination_dir}")
        file_count = 0
        
        try:
            for item in self.source_dir.iterdir():
                if item.is_file():
                    if self._process_file(item):
                        file_count += 1
                        
            logger.info(f"Sorting complete. Processed {file_count} files.")
            return True
        except Exception as e:
            logger.error(f"Error during sorting: {str(e)}", exc_info=True)
            return False
    
    def _process_file(self, file_path):
        """Process a single file according to sorting rules."""
        try:
            # Get file extension (without the dot)
            extension = file_path.suffix.lower()[1:] if file_path.suffix else "no_extension"
            
            # Check extension-based rules
            if extension in self.rules.get('extensions', {}):
                # Create an absolute path for the target folder
                target_folder_path = self.rules['extensions'][extension]
                target_folder = self.destination_dir / target_folder_path
                return self._move_or_copy_file(file_path, target_folder)
            
            # Check pattern-based rules (e.g., filename contains certain text)
            for pattern, folder in self.rules.get('patterns', {}).items():
                if pattern.lower() in file_path.name.lower():
                    # Create an absolute path for the target folder
                    target_folder = self.destination_dir / folder
                    return self._move_or_copy_file(file_path, target_folder)
            
            # Handle uncategorized files
            if 'other' in self.rules:
                # Create an absolute path for the target folder
                target_folder = self.destination_dir / self.rules['other']
                return self._move_or_copy_file(file_path, target_folder)
            
            return False
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return False
    
    def _move_or_copy_file(self, file_path, target_folder):
        """Move or copy file to target folder based on configuration."""
        try:
            # Convert relative path to absolute by joining with destination_dir
            target_folder = self.destination_dir / target_folder
            print(self.destination_dir)
            logger.info(f"Target folder is {target_folder} and destination directory is {self.destination_dir}")
            
            # Create target folder if it doesn't exist
            target_folder.mkdir(parents=True, exist_ok=True)
            
            # Handle duplicate files
            target_file = target_folder / file_path.name
            if target_file.exists():
                # Rename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
                target_file = target_folder / new_name
            
            # Log the actual paths being used for debugging
            logger.debug(f"Source: {file_path} (absolute: {file_path.absolute()})")
            logger.debug(f"Target: {target_file} (absolute: {target_file.absolute()})")
            
            # Move or copy based on configuration
            if self.action == 'move':
                shutil.move(str(file_path), str(target_file))
                logger.info(f"Moved: {file_path.name} to {target_file}")
            else:  # copy
                shutil.copy2(str(file_path), str(target_file))
                logger.info(f"Copied: {file_path.name} to {target_file}")
            
            return True
        except Exception as e:
            logger.error(f"Error moving/copying {file_path.name}: {str(e)}")
            return False

# ===============================
# CONFIG MANAGER CLASS
# ===============================

class ConfigManager:
    def __init__(self, config_path='config.json'):
        self.config_path = APP_DIR / config_path
        self.config = self._load_config()
        
    def _load_config(self):
        """Load configuration from file or create default if none exists."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
                return config
            else:
                # Create default config
                self.save_config(DEFAULT_CONFIG)
                logger.info(f"Created default configuration at {self.config_path}")
                return DEFAULT_CONFIG
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            logger.info("Using default configuration")
            return DEFAULT_CONFIG
    
    def save_config(self, config):
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            logger.info(f"Configuration saved to {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving configuration: {str(e)}")
            return False
    
    def get_config(self):
        """Return current configuration."""
        return self.config
    
    def update_config(self, new_config):
        """Update and save new configuration."""
        return self.save_config(new_config)

# ===============================
# FILE WATCHER CLASS
# ===============================

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, file_sorter):
        self.file_sorter = file_sorter
        self.cooldown = 2  # seconds to wait after file creation before processing
        self.pending_files = {}
        self.timer_thread = None
        
    def on_created(self, event):
        if event.is_directory:
            return
        
        logger.info(f"File created: {event.src_path}")
        self.pending_files[event.src_path] = time.time()
        
        # Start the timer thread if it's not already running
        if self.timer_thread is None or not self.timer_thread.is_alive():
            self.timer_thread = threading.Thread(target=self._process_pending_files)
            self.timer_thread.daemon = True
            self.timer_thread.start()
    
    def _process_pending_files(self):
        """Process files after a cooldown period to ensure they're fully written."""
        while self.pending_files:
            current_time = time.time()
            files_to_process = []
            
            # Find files that meet the cooldown requirement
            for file_path, timestamp in list(self.pending_files.items()):
                if current_time - timestamp >= self.cooldown:
                    files_to_process.append(file_path)
                    self.pending_files.pop(file_path)
            
            # Process the ready files
            if files_to_process:
                logger.info(f"Processing {len(files_to_process)} files after cooldown")
                self.file_sorter.sort_files()  # Will process all files in source dir
            
            # Sleep a bit before next check
            time.sleep(1)

class FileWatcher:
    def __init__(self, config, file_sorter):
        self.config = config
        self.file_sorter = file_sorter
        self.observer = None
        self.scheduler_thread = None
        self.running = False
        
    def start(self):
        """Start watching the directory based on the configured method."""
        if not self.config.get('monitoring', {}).get('enabled', False):
            logger.info("File monitoring is disabled.")
            return False
        
        if self.running:
            logger.warning("File watcher is already running.")
            return True
        
        monitor_type = self.config.get('monitoring', {}).get('type', 'scheduled')
        
        try:
            if monitor_type == 'realtime':
                return self._start_realtime_monitoring()
            else:  # scheduled
                return self._start_scheduled_monitoring()
        except Exception as e:
            logger.error(f"Error starting file watcher: {str(e)}")
            return False
    
    def _start_realtime_monitoring(self):
        """Start real-time file monitoring using watchdog."""
        try:
            source_dir = self.config.get('source_directory')
            if not source_dir:
                logger.error("Source directory is not specified.")
                return False
            
            self.observer = Observer()
            event_handler = FileEventHandler(self.file_sorter)
            self.observer.schedule(event_handler, source_dir, recursive=False)
            self.observer.start()
            
            logger.info(f"Started real-time monitoring for {source_dir}")
            self.running = True
            return True
        except Exception as e:
            logger.error(f"Failed to start real-time monitoring: {str(e)}")
            return False
    
    def _start_scheduled_monitoring(self):
        """Start periodic scheduled monitoring."""
        try:
            interval = self.config.get('monitoring', {}).get('interval', 3600)  # seconds
            
            def run_scheduler():
                logger.info(f"Started scheduled monitoring with {interval} seconds interval")
                while self.running:
                    self.file_sorter.sort_files()
                    time.sleep(interval)
            
            self.running = True
            self.scheduler_thread = threading.Thread(target=run_scheduler)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
            
            return True
        except Exception as e:
            logger.error(f"Failed to start scheduled monitoring: {str(e)}")
            self.running = False
            return False
    
    def stop(self):
        """Stop the file watcher."""
        self.running = False
        
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None
        
        # The scheduler thread will exit on next loop when self.running is False
        logger.info("File watcher stopped.")

# ===============================
# WORKER THREAD FOR UI RESPONSIVENESS
# ===============================

class SorterThread(QThread):
    """Worker thread to run file sorting without blocking UI"""
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    
    def __init__(self, file_sorter):
        super().__init__()
        self.file_sorter = file_sorter
        
    def run(self):
        try:
            success = self.file_sorter.sort_files()
            self.finished.emit(success)
        except Exception as e:
            logger.error(f"Error during sorting operation: {str(e)}", exc_info=True)
            self.error.emit(str(e))

# ===============================
# MAIN APPLICATION GUI - PYQT6 VERSION
# ===============================

class FileOrganizerApp(QMainWindow):
    def __init__(self, config_manager, file_sorter, file_watcher):
        super().__init__()
        self.config_manager = config_manager
        self.file_sorter = file_sorter
        self.file_watcher = file_watcher
        self.config = config_manager.get_config()
        self.sorter_thread = None
        
        # Setup the main window
        self.setWindowTitle("The Manchester United File Organiser System")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)
        
        # Set application style and theme colors - red and yellow for Manchester United
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #FFFFFF;
                color: #000000;
            }
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                background-color: #FFFFFF;
            }
            QTabBar::tab {
                background-color: #E8E8E8;
                color: #000000;
                padding: 8px 16px;
                font-weight: bold;
                font-family: Arial;
            }
            QTabBar::tab:selected {
                background-color: #C70101;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #FFD800;
                color: #000000;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
                font-family: Arial;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #FFC200;
            }
            QPushButton:pressed {
                background-color: #C70101;
                color: #FFFFFF;
            }
            QPushButton#accentButton {
                background-color: #C70101;
                color: #FFFFFF;
            }
            QPushButton#accentButton:hover {
                background-color: #A00000;
            }
            QLabel {
                font-family: Arial;
                color: #000000;
            }
            QGroupBox {
                font-family: Arial;
                font-weight: bold;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QTreeWidget {
                font-family: Arial;
                border: 1px solid #CCCCCC;
            }
            QTreeWidget::item:selected {
                background-color: #C70101;
                color: #FFFFFF;
            }
            QLineEdit, QTextEdit, QSpinBox {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 4px;
                font-family: Arial;
            }
            QRadioButton, QCheckBox {
                font-family: Arial;
            }
            QStatusBar {
                background-color: #F0F0F0;
                color: #000000;
                font-family: Arial;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Create main tabs
        self.main_tab = QWidget()
        self.rules_tab = QWidget()
        self.monitor_tab = QWidget()
        self.logs_tab = QWidget()
        self.about_tab = QWidget()
        
        # Add tabs to tab widget
        self.tabs.addTab(self.main_tab, "Main")
        self.tabs.addTab(self.rules_tab, "Sorting Rules")
        self.tabs.addTab(self.monitor_tab, "Monitoring")
        self.tabs.addTab(self.logs_tab, "Logs")
        self.tabs.addTab(self.about_tab, "About")
        
        # Build each tab's UI
        self._build_main_tab()
        self._build_rules_tab()
        self._build_monitor_tab()
        self._build_logs_tab()
        self._build_about_tab()
        
        # Status bar at the bottom
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
        # Load configuration into UI
        self._load_config_to_ui()
        
        logger.info("Application UI initialized")
    
    def _build_main_tab(self):
        """Build the main tab UI."""
        layout = QVBoxLayout(self.main_tab)
        
        # Source directory section
        source_group = QGroupBox("Source Directory")
        source_layout = QHBoxLayout(source_group)
        
        self.source_dir_edit = QLineEdit()
        source_layout.addWidget(self.source_dir_edit)
        
        browse_src_btn = QPushButton("Browse")
        browse_src_btn.clicked.connect(lambda: self._browse_directory("source"))
        source_layout.addWidget(browse_src_btn)
        
        layout.addWidget(source_group)
        
        # Destination directory section
        dest_group = QGroupBox("Destination Directory (leave empty to use source directory)")
        dest_layout = QHBoxLayout(dest_group)
        
        self.dest_dir_edit = QLineEdit()
        dest_layout.addWidget(self.dest_dir_edit)
        
        browse_dest_btn = QPushButton("Browse")
        browse_dest_btn.clicked.connect(lambda: self._browse_directory("destination"))
        dest_layout.addWidget(browse_dest_btn)

        layout.addWidget(dest_group)
        
        # Action frame
        action_group = QGroupBox("File Action")
        action_layout = QHBoxLayout(action_group)
        
        self.move_radio = QRadioButton("Move Files")
        self.move_radio.setChecked(True)
        self.copy_radio = QRadioButton("Copy Files")
        
        action_layout.addWidget(self.move_radio)
        action_layout.addWidget(self.copy_radio)
        action_layout.addStretch(1)
        
        layout.addWidget(action_group)
        
        # Operation buttons
        button_layout = QHBoxLayout()
        
        run_btn = QPushButton("Run Now")
        run_btn.setObjectName("accentButton")
        run_btn.clicked.connect(self._run_sorting)
        button_layout.addWidget(run_btn)
        
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self._save_config)
        button_layout.addWidget(save_btn)
        
        button_layout.addStretch(1)
        layout.addLayout(button_layout)
        
        # Activity log
        log_group = QGroupBox("Recent Activity")
        log_layout = QVBoxLayout(log_group)
        
        self.activity_log = QTextEdit()
        self.activity_log.setReadOnly(True)
        log_layout.addWidget(self.activity_log)
        
        refresh_log_btn = QPushButton("Refresh Logs")
        refresh_log_btn.clicked.connect(self._refresh_activity_logs)
        log_refresh_layout = QHBoxLayout()
        log_refresh_layout.addStretch(1)
        log_refresh_layout.addWidget(refresh_log_btn)
        log_layout.addLayout(log_refresh_layout)
        
        layout.addWidget(log_group, 1)  # 1 = stretch factor to take available space
    
    def _build_rules_tab(self):
        """Build the rules tab UI."""
        layout = QVBoxLayout(self.rules_tab)
        
        # Extension rules section
        ext_group = QGroupBox("File Extension Rules")
        ext_layout = QVBoxLayout(ext_group)
        
        # Tree widget for extension rules
        self.ext_tree = QTreeWidget()
        self.ext_tree.setHeaderLabels(["Extension", "Target Folder"])
        self.ext_tree.setColumnWidth(0, 100)
        ext_layout.addWidget(self.ext_tree)
        
        # Buttons for extension rules
        ext_btn_layout = QHBoxLayout()
        
        add_ext_btn = QPushButton("Add Rule")
        add_ext_btn.clicked.connect(self._add_extension_rule)
        ext_btn_layout.addWidget(add_ext_btn)
        
        edit_ext_btn = QPushButton("Edit Rule")
        edit_ext_btn.clicked.connect(self._edit_extension_rule)
        ext_btn_layout.addWidget(edit_ext_btn)
        
        remove_ext_btn = QPushButton("Remove Rule")
        remove_ext_btn.clicked.connect(self._remove_extension_rule)
        ext_btn_layout.addWidget(remove_ext_btn)
        
        ext_btn_layout.addStretch(1)
        ext_layout.addLayout(ext_btn_layout)
        
        layout.addWidget(ext_group)
        
        # Pattern rules section
        pattern_group = QGroupBox("Filename Pattern Rules")
        pattern_layout = QVBoxLayout(pattern_group)
        
        # Tree widget for pattern rules
        self.pattern_tree = QTreeWidget()
        self.pattern_tree.setHeaderLabels(["Pattern", "Target Folder"])
        self.pattern_tree.setColumnWidth(0, 100)
        pattern_layout.addWidget(self.pattern_tree)
        
        # Buttons for pattern rules
        pattern_btn_layout = QHBoxLayout()
        
        add_pattern_btn = QPushButton("Add Pattern")
        add_pattern_btn.clicked.connect(self._add_pattern_rule)
        pattern_btn_layout.addWidget(add_pattern_btn)
        
        edit_pattern_btn = QPushButton("Edit Pattern")
        edit_pattern_btn.clicked.connect(self._edit_pattern_rule)
        pattern_btn_layout.addWidget(edit_pattern_btn)
        
        remove_pattern_btn = QPushButton("Remove Pattern")
        remove_pattern_btn.clicked.connect(self._remove_pattern_rule)
        pattern_btn_layout.addWidget(remove_pattern_btn)
        
        pattern_btn_layout.addStretch(1)
        pattern_layout.addLayout(pattern_btn_layout)
        
        layout.addWidget(pattern_group)
        
        # Other files section
        other_group = QGroupBox("Uncategorized Files")
        other_layout = QHBoxLayout(other_group)
        
        other_layout.addWidget(QLabel("Folder for uncategorized files:"))
        
        self.other_folder_edit = QLineEdit("Unsorted")
        other_layout.addWidget(self.other_folder_edit, 1)
        
        layout.addWidget(other_group)
    
    def _build_monitor_tab(self):
        """Build the monitoring tab UI."""
        layout = QVBoxLayout(self.monitor_tab)
        
        # Monitoring options
        monitor_group = QGroupBox("File Monitoring Settings")
        monitor_layout = QVBoxLayout(monitor_group)
        
        # Enable monitoring checkbox
        self.monitoring_enabled_check = QCheckBox("Enable automatic monitoring")
        monitor_layout.addWidget(self.monitoring_enabled_check)
        
        # Monitor type
        monitor_type_layout = QVBoxLayout()
        monitor_type_layout.addWidget(QLabel("Monitoring Type:"))
        
        self.scheduled_radio = QRadioButton("Scheduled (periodic checks)")
        self.scheduled_radio.setChecked(True)
        self.realtime_radio = QRadioButton("Real-time (immediate processing)")
        
        monitor_type_layout.addWidget(self.scheduled_radio)
        monitor_type_layout.addWidget(self.realtime_radio)
        
        monitor_layout.addLayout(monitor_type_layout)
        layout.addWidget(monitor_group)
        
        # Interval settings
        interval_group = QGroupBox("Schedule Settings")
        interval_layout = QHBoxLayout(interval_group)
        
        interval_layout.addWidget(QLabel("Check interval (seconds):"))
        
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(60, 86400)  # 1 minute to 24 hours
        self.interval_spin.setValue(3600)
        self.interval_spin.setSingleStep(60)
        interval_layout.addWidget(self.interval_spin)
        
        # Preset intervals
        interval_layout.addWidget(QLabel("Presets:"))
        
        preset_5min = QPushButton("5 min")
        preset_5min.clicked.connect(lambda: self.interval_spin.setValue(300))
        interval_layout.addWidget(preset_5min)
        
        preset_30min = QPushButton("30 min")
        preset_30min.clicked.connect(lambda: self.interval_spin.setValue(1800))
        interval_layout.addWidget(preset_30min)
        
        preset_1hr = QPushButton("1 hour")
        preset_1hr.clicked.connect(lambda: self.interval_spin.setValue(3600))
        interval_layout.addWidget(preset_1hr)
        
        preset_6hr = QPushButton("6 hours")
        preset_6hr.clicked.connect(lambda: self.interval_spin.setValue(21600))
        interval_layout.addWidget(preset_6hr)
        
        preset_12hr = QPushButton("12 hours")
        preset_12hr.clicked.connect(lambda: self.interval_spin.setValue(43200))
        interval_layout.addWidget(preset_12hr)
        
        interval_layout.addStretch(1)
        layout.addWidget(interval_group)
        
        # Monitoring control buttons
        control_layout = QHBoxLayout()
        
        self.start_monitor_btn = QPushButton("Start Monitoring")
        self.start_monitor_btn.clicked.connect(self._start_monitoring)
        control_layout.addWidget(self.start_monitor_btn)
        
        self.stop_monitor_btn = QPushButton("Stop Monitoring")
        self.stop_monitor_btn.clicked.connect(self._stop_monitoring)
        self.stop_monitor_btn.setEnabled(False)
        control_layout.addWidget(self.stop_monitor_btn)
        
        control_layout.addStretch(1)
        layout.addLayout(control_layout)
        
        # Monitor status
        status_group = QGroupBox("Monitoring Status")
        status_layout = QVBoxLayout(status_group)
        
        self.monitor_status_label = QLabel("Monitoring is currently disabled")
        self.monitor_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Arial", 10)
        font.setBold(True)
        self.monitor_status_label.setFont(font)
        status_layout.addWidget(self.monitor_status_label)
        
        layout.addWidget(status_group)
        layout.addStretch(1)
    
    def _build_logs_tab(self):
        """Build the logs tab UI."""
        layout = QVBoxLayout(self.logs_tab)
        
        # Search section
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search logs:"))
        
        self.search_edit = QLineEdit()
        search_layout.addWidget(self.search_edit, 1)
        
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self._search_logs)
        search_layout.addWidget(search_btn)
        
        layout.addLayout(search_layout)
        
        # Log filter options
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter by:"))
        
        self.filter_all_radio = QRadioButton("All")
        self.filter_all_radio.setChecked(True)
        filter_layout.addWidget(self.filter_all_radio)
        
        self.filter_info_radio = QRadioButton("Information")
        filter_layout.addWidget(self.filter_info_radio)
        
        self.filter_error_radio = QRadioButton("Errors")
        filter_layout.addWidget(self.filter_error_radio)
        
        self.filter_input_radio = QRadioButton("User Input")
        filter_layout.addWidget(self.filter_input_radio)
        
        # Add radio buttons to group for mutual exclusivity
        self.filter_group = QButtonGroup()
        self.filter_group.addButton(self.filter_all_radio)
        self.filter_group.addButton(self.filter_info_radio)
        self.filter_group.addButton(self.filter_error_radio)
        self.filter_group.addButton(self.filter_input_radio)
        
        filter_layout.addStretch(1)
        layout.addLayout(filter_layout)
        
        # Log viewer
        log_group = QGroupBox("Log Messages")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group, 1)
        
        # Control buttons
        log_btn_layout = QHBoxLayout()
        
        refresh_log_btn = QPushButton("Refresh Logs")
        refresh_log_btn.clicked.connect(self._refresh_logs)
        log_btn_layout.addWidget(refresh_log_btn)
        
        clear_log_btn = QPushButton("Clear Display")
        clear_log_btn.clicked.connect(self._clear_log_display)
        log_btn_layout.addWidget(clear_log_btn)
        
        log_btn_layout.addStretch(1)
        
        open_log_btn = QPushButton("Open Log File")
        open_log_btn.clicked.connect(self._open_log_file)
        log_btn_layout.addWidget(open_log_btn)
        
        layout.addLayout(log_btn_layout)
    
    def _build_about_tab(self):
        """Build the about tab UI."""
        layout = QVBoxLayout(self.about_tab)
        
        # Logo area (if you have a logo)
        # logo_label = QLabel()
        # logo_pixmap = QPixmap("path/to/logo.png")
        # logo_label.setPixmap(logo_pixmap)
        # logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # layout.addWidget(logo_label)
        
        # App title
        title_label = QLabel("The Manchester United File Organiser System")
        title_font = QFont("Arial", 16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Version
        version_label = QLabel("Version 1.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # Description
        description = """
        The Manchester United File Organiser System is a utility to automatically sort files into folders 
        based on file types and naming patterns.
        
        Features:
        • Organize files by extension or filename patterns
        • Move or copy files to categorized folders
        • Real-time or scheduled monitoring
        • Detailed logging and activity tracking
        
        This application was built using Python and PyQt6.
        """
        
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)
        
        # Credits
        credits_label = QLabel("Developed by: Akhtar Hasan Software Solutions\n© 2025")
        credits_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(credits_label)
        
        # App directory info
        app_dir_label = QLabel(f"Application Directory:\n{APP_DIR}")
        app_dir_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_dir_font = QFont("Arial", 8)
        app_dir_label.setFont(app_dir_font)
        layout.addWidget(app_dir_label)
        
        layout.addStretch(1)
    
    def _load_config_to_ui(self):
        """Load configuration into the UI elements."""
        # Source directory
        self.source_dir_edit.setText(self.config.get('source_directory', ''))

        # Destination directory
        self.dest_dir_edit.setText(self.config.get('destination_directory', ''))
        
        # File action
        if self.config.get('file_action') == 'copy':
            self.copy_radio.setChecked(True)
        else:
            self.move_radio.setChecked(True)
        
        # Monitoring settings
        monitoring = self.config.get('monitoring', {})
        self.monitoring_enabled_check.setChecked(monitoring.get('enabled', False))
        
        if monitoring.get('type') == 'realtime':
            self.realtime_radio.setChecked(True)
        else:
            self.scheduled_radio.setChecked(True)
        
        self.interval_spin.setValue(monitoring.get('interval', 3600))
        
        # Other folder
        self.other_folder_edit.setText(self.config.get('sorting_rules', {}).get('other', 'Unsorted'))
        
        # Extension rules
        self.ext_tree.clear()
        for ext, folder in self.config.get('sorting_rules', {}).get('extensions', {}).items():
            item = QTreeWidgetItem([ext, folder])
            self.ext_tree.addTopLevelItem(item)
        
        # Pattern rules
        self.pattern_tree.clear()
        for pattern, folder in self.config.get('sorting_rules', {}).get('patterns', {}).items():
            item = QTreeWidgetItem([pattern, folder])
            self.pattern_tree.addTopLevelItem(item)
        
        # Update monitoring status
        self._update_monitoring_status()
        
        # Display logs
        self._refresh_logs()
        self._refresh_activity_logs()
    
    def _browse_directory(self, directory_type="source"):
        """Open directory browser dialog."""
        if directory_type == "source":
            current_dir = self.source_dir_edit.text()
            directory = QFileDialog.getExistingDirectory(self, "Select Source Directory", current_dir)
            if directory:
                self.source_dir_edit.setText(directory)
        else:  # destination
            current_dir = self.dest_dir_edit.text()
            directory = QFileDialog.getExistingDirectory(self, "Select Destination Directory", current_dir)
            if directory:
                self.dest_dir_edit.setText(directory)
    
    def _create_input_dialog(self, title, label1, label2, value1="", value2=""):
        """Create a reusable input dialog for rules."""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(400, 150)
        
        layout = QVBoxLayout(dialog)
        
        form_layout = QVBoxLayout()
        
        label1_widget = QLabel(label1)
        input1 = QLineEdit(value1)
        form_layout.addWidget(label1_widget)
        form_layout.addWidget(input1)
        
        label2_widget = QLabel(label2)
        input2 = QLineEdit(value2)
        form_layout.addWidget(label2_widget)
        form_layout.addWidget(input2)
        
        layout.addLayout(form_layout)
        
        buttons = QHBoxLayout()
        ok_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        
        buttons.addStretch(1)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        
        layout.addLayout(buttons)
        
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        return dialog, input1, input2
    
    def _add_extension_rule(self):
        """Add a new extension rule."""
        dialog, ext_input, folder_input = self._create_input_dialog(
            "Add Extension Rule",
            "File Extension:",
            "Target Folder:"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            ext = ext_input.text().strip()
            folder = folder_input.text().strip()
            
            if not ext or not folder:
                QMessageBox.critical(self, "Error", "Both fields are required.")
                return
            
            item = QTreeWidgetItem([ext, folder])
            self.ext_tree.addTopLevelItem(item)
    
    def _edit_extension_rule(self):
        """Edit selected extension rule."""
        selected_items = self.ext_tree.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Info", "Please select a rule to edit.")
            return
        
        item = selected_items[0]
        ext = item.text(0)
        folder = item.text(1)
        
        dialog, ext_input, folder_input = self._create_input_dialog(
            "Edit Extension Rule",
            "File Extension:",
            "Target Folder:",
            ext,
            folder
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_ext = ext_input.text().strip()
            new_folder = folder_input.text().strip()
            
            if not new_ext or not new_folder:
                QMessageBox.critical(self, "Error", "Both fields are required.")
                return
            
            item.setText(0, new_ext)
            item.setText(1, new_folder)
    
    def _remove_extension_rule(self):
        """Remove selected extension rule."""
        selected_items = self.ext_tree.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Info", "Please select a rule to remove.")
            return
        
        item = selected_items[0]
        index = self.ext_tree.indexOfTopLevelItem(item)
        self.ext_tree.takeTopLevelItem(index)
    
    def _add_pattern_rule(self):
        """Add a new pattern rule."""
        dialog, pattern_input, folder_input = self._create_input_dialog(
            "Add Pattern Rule",
            "Filename Pattern:",
            "Target Folder:"
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            pattern = pattern_input.text().strip()
            folder = folder_input.text().strip()
            
            if not pattern or not folder:
                QMessageBox.critical(self, "Error", "Both fields are required.")
                return
            
            item = QTreeWidgetItem([pattern, folder])
            self.pattern_tree.addTopLevelItem(item)
    
    def _edit_pattern_rule(self):
        """Edit selected pattern rule."""
        selected_items = self.pattern_tree.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Info", "Please select a pattern to edit.")
            return
        
        item = selected_items[0]
        pattern = item.text(0)
        folder = item.text(1)
        
        dialog, pattern_input, folder_input = self._create_input_dialog(
            "Edit Pattern Rule",
            "Filename Pattern:",
            "Target Folder:",
            pattern,
            folder
        )
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_pattern = pattern_input.text().strip()
            new_folder = folder_input.text().strip()
            
            if not new_pattern or not new_folder:
                QMessageBox.critical(self, "Error", "Both fields are required.")
                return
            
            item.setText(0, new_pattern)
            item.setText(1, new_folder)
    
    def _remove_pattern_rule(self):
        """Remove selected pattern rule."""
        selected_items = self.pattern_tree.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Info", "Please select a pattern to remove.")
            return
        
        item = selected_items[0]
        index = self.pattern_tree.indexOfTopLevelItem(item)
        self.pattern_tree.takeTopLevelItem(index)
    
    def _save_config(self):
        """Save current UI state to configuration."""
        try:
            # Build extension rules
            extensions = {}
            for i in range(self.ext_tree.topLevelItemCount()):
                item = self.ext_tree.topLevelItem(i)
                extensions[item.text(0)] = item.text(1)
            
            # Build pattern rules
            patterns = {}
            for i in range(self.pattern_tree.topLevelItemCount()):
                item = self.pattern_tree.topLevelItem(i)
                patterns[item.text(0)] = item.text(1)
            
            # Build complete config
            config = {
                'source_directory': self.source_dir_edit.text(),
                'destination_directory': self.dest_dir_edit.text(),
                'file_action': 'copy' if self.copy_radio.isChecked() else 'move',
                'monitoring': {
                    'enabled': self.monitoring_enabled_check.isChecked(),
                    'type': 'realtime' if self.realtime_radio.isChecked() else 'scheduled',
                    'interval': self.interval_spin.value()
                },
                'sorting_rules': {
                    'extensions': extensions,
                    'patterns': patterns,
                    'other': self.other_folder_edit.text() or 'Unsorted'
                }
            }
            
            # Save to file
            if self.config_manager.save_config(config):
                QMessageBox.information(self, "Success", "Configuration saved successfully.")
                self.config = config
                
                # Update file sorter with new config
                self.file_sorter.__init__(config)
                
                # Update file watcher with new config if running
                if self.file_watcher.running:
                    self.file_watcher.stop()
                    self.file_watcher.__init__(config, self.file_sorter)
                    self.file_watcher.start()
                else:
                    self.file_watcher.__init__(config, self.file_sorter)
                
                # Update status
                self._update_monitoring_status()
                self.status_bar.showMessage("Configuration saved successfully")
            else:
                QMessageBox.critical(self, "Error", "Failed to save configuration.")
                self.status_bar.showMessage("Failed to save configuration")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving: {str(e)}")
            logger.error(f"Error saving configuration: {str(e)}")
            self.status_bar.showMessage(f"Error: {str(e)}")
    
    def _run_sorting(self):
        """Execute file sorting operation."""
        source_dir = self.source_dir_edit.text()
        dest_dir = self.dest_dir_edit.text()
        
        if not source_dir:
            QMessageBox.critical(self, "Error", "Please specify a source directory.")
            return
        
        if not Path(source_dir).exists():
            QMessageBox.critical(self, "Error", "Source directory does not exist.")
            return
        
        # Show message about destination directory defaulting to source
        if not dest_dir:
            QMessageBox.information(
                self,
                "Destination Directory",
                "No destination directory specified. Files will be organized within the source directory."
            )
            # Ensure the config reflects this
            self.dest_dir_edit.setText("")  # Clear any potential whitespace
        elif not Path(dest_dir).exists():
            reply = QMessageBox.question(
                self, 
                "Destination Directory", 
                "The specified destination directory doesn't exist. Would you like to create it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    Path(dest_dir).mkdir(parents=True, exist_ok=True)
                    logger.info(f"Created destination directory: {dest_dir}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create destination directory: {str(e)}")
                    logger.error(f"Failed to create destination directory: {str(e)}")
                    return
            else:
                return
        
        # First, save the current configuration
        self._save_config()
        
        # Update status
        self.status_bar.showMessage("Sorting files...")
        
        # Run sorting in a separate thread
        self.sorter_thread = SorterThread(self.file_sorter)
        
        def on_success(success):
            if success:
                QMessageBox.information(self, "Success", "Files organized successfully!")
                self.status_bar.showMessage("Files organized successfully")
                self._refresh_activity_logs()
            else:
                QMessageBox.critical(self, "Error", "Failed to organize files. Check logs for details.")
                self.status_bar.showMessage("Failed to organize files")
        
        def on_error(error_msg):
            QMessageBox.critical(self, "Error", f"An error occurred: {error_msg}")
            self.status_bar.showMessage(f"Error: {error_msg}")
        
        self.sorter_thread.finished.connect(on_success)
        self.sorter_thread.error.connect(on_error)
        self.sorter_thread.start()
    
    def _start_monitoring(self):
        """Start the file watcher."""
        # First save current configuration
        self._save_config()
        
        # Check if source directory is valid
        source_dir = self.source_dir_edit.text()
        if not source_dir:
            QMessageBox.critical(self, "Error", "Please specify a source directory.")
            return
        
        if not Path(source_dir).exists():
            QMessageBox.critical(self, "Error", "Source directory does not exist.")
            return
        
        # Start monitoring
        try:
            success = self.file_watcher.start()
            if success:
                QMessageBox.information(self, "Success", "File monitoring started.")
                self.start_monitor_btn.setEnabled(False)
                self.stop_monitor_btn.setEnabled(True)
                self._update_monitoring_status()
                self.status_bar.showMessage("Monitoring started successfully")
            else:
                QMessageBox.critical(self, "Error", "Failed to start monitoring. Check logs for details.")
                self.status_bar.showMessage("Failed to start monitoring")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            logger.error(f"Error starting monitoring: {str(e)}", exc_info=True)
            self.status_bar.showMessage(f"Error: {str(e)}")
    
    def _stop_monitoring(self):
        """Stop the file watcher."""
        try:
            self.file_watcher.stop()
            QMessageBox.information(self, "Success", "File monitoring stopped.")
            self.start_monitor_btn.setEnabled(True)
            self.stop_monitor_btn.setEnabled(False)
            self._update_monitoring_status()
            self.status_bar.showMessage("Monitoring stopped")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            logger.error(f"Error stopping monitoring: {str(e)}", exc_info=True)
            self.status_bar.showMessage(f"Error: {str(e)}")
    
    def _update_monitoring_status(self):
        """Update the monitoring status display."""
        if self.file_watcher.running:
            if self.file_watcher.config.get('monitoring', {}).get('type') == 'realtime':
                status = "Real-time monitoring is active"
            else:
                interval = self.file_watcher.config.get('monitoring', {}).get('interval', 3600)
                status = f"Scheduled monitoring is active (checking every {interval} seconds)"
            
            self.monitor_status_label.setText(status)
            self.start_monitor_btn.setEnabled(False)
            self.stop_monitor_btn.setEnabled(True)
        else:
            self.monitor_status_label.setText("Monitoring is currently disabled")
            self.start_monitor_btn.setEnabled(True)
            self.stop_monitor_btn.setEnabled(False)
    
    def _get_selected_log_type(self):
        """Get the selected log type from radio buttons."""
        if self.filter_info_radio.isChecked():
            return "output"
        elif self.filter_error_radio.isChecked():
            return "error"
        elif self.filter_input_radio.isChecked():
            return "input"
        else:
            return "all"  # Default
    
    def _refresh_logs(self):
        """Refresh the log display in the logs tab."""
        try:
            log_type = self._get_selected_log_type()
            search_term = self.search_edit.text().strip()
            
            # Get logs based on search term if provided, otherwise get recent logs
            if search_term:
                logs = logger.search_logs(search_term, log_type)
            else:
                logs = logger.get_recent_logs(count=100, log_type=log_type)
            
            # Update the log text widget
            self.log_text.clear()
            
            if not logs:
                self.log_text.append("No log entries found.")
            else:
                for log in logs:
                    # Add color formatting based on log type
                    if "ERROR:" in log or "Error:" in log:
                        self.log_text.append(f"<span style='color:red;'>{log}</span>")
                    elif "INFO:" in log or "Output:" in log:
                        self.log_text.append(f"<span style='color:blue;'>{log}</span>")
                    else:
                        self.log_text.append(log)
            
            # Move cursor to the end
            cursor = self.log_text.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.log_text.setTextCursor(cursor)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to refresh logs: {str(e)}")
            logger.error(f"Error refreshing logs: {str(e)}", exc_info=True)
    
    def _refresh_activity_logs(self):
        """Refresh the recent activity log in the main tab."""
        try:
            logs = logger.get_recent_logs(count=10)
            
            # Update the activity log widget
            self.activity_log.clear()
            
            if not logs:
                self.activity_log.append("No recent activity.")
            else:
                for log in logs:
                    # Add color formatting based on log type
                    if "ERROR:" in log or "Error:" in log:
                        self.activity_log.append(f"<span style='color:red;'>{log}</span>")
                    elif "INFO:" in log or "Output:" in log:
                        self.activity_log.append(f"<span style='color:blue;'>{log}</span>")
                    else:
                        self.activity_log.append(log)
            
            # Move cursor to the end
            cursor = self.activity_log.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            self.activity_log.setTextCursor(cursor)
            
        except Exception as e:
            logger.error(f"Error refreshing activity logs: {str(e)}", exc_info=True)
    
    def _search_logs(self):
        """Search logs for specific text."""
        search_term = self.search_edit.text().strip()
        if not search_term:
            QMessageBox.information(self, "Info", "Please enter a search term.")
            return
        
        self._refresh_logs()  # This will use the search term from the search_edit
    
    def _clear_log_display(self):
        """Clear the log display (not the log file)."""
        self.log_text.clear()
    
    def _open_log_file(self):
        """Open the log file in the default text editor."""
        try:
            log_path = logger.log_path
            if Path(log_path).exists():
                if sys.platform == "win32":
                    os.startfile(log_path)
                elif sys.platform == "darwin":  # macOS
                    subprocess.run(["open", log_path])
                else:  # Linux/Unix
                    subprocess.run(["xdg-open", log_path])
                logger.info(f"Opened log file: {log_path}")
            else:
                QMessageBox.information(self, "Info", "Log file does not exist yet.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open log file: {str(e)}")
            logger.error(f"Error opening log file: {str(e)}", exc_info=True)

    def closeEvent(self, event):
        """Handle window close event."""
        logger.info("Shutting down The Manchester United File Organiser System")
        if self.file_watcher and self.file_watcher.running:
            self.file_watcher.stop()
        event.accept()

# ===============================
# APPLICATION ENTRY POINT
# ===============================

def main():
    logger.info("Starting The Manchester United File Organiser System")
    logger.info(f"Application directory: {APP_DIR}")
    
    # Initialize configuration
    config_manager = ConfigManager("config.json")
    config = config_manager.get_config()
    
    # Initialize file sorter
    file_sorter = FileSorter(config)
    
    # Initialize file watcher
    file_watcher = FileWatcher(config, file_sorter)
    
    # Create application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a more modern look
    
    # Set application name and company
    app.setApplicationName("The Manchester United File Organiser System")
    app.setOrganizationName("Akhtar Hasan Software Solutions")
    
    # Create and show the main window
    main_window = FileOrganizerApp(config_manager, file_sorter, file_watcher)
    main_window.show()
    
    # Start monitoring if enabled
    if config.get('monitoring', {}).get('enabled', False):
        file_watcher.start()
        main_window._update_monitoring_status()
    
    # Start the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()