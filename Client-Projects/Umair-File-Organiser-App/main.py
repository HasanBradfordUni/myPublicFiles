import os
import sys
import json
import time
import shutil
import logging
import threading
import tkinter as tk
import subprocess
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
from pathlib import Path
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
        self.logger = logging.getLogger("FileOrganizer")
        self.logger.setLevel(logging.INFO)
        
        # Clear any existing handlers to avoid duplicates
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create file handler for standard logging
        file_handler = logging.FileHandler(log_dir / self.log_file)
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
        with open(self.log_path, 'a') as logger:
            logger.write("Output:\n")
            message = message.replace("  ", "\n")
            logger.write(message + "\n")
    
    def _add_to_error_logs(self, error_message):
        """Add custom formatted error logs"""
        with open(self.log_path, 'a') as logger:
            logger.write("Error:\n")
            error_message = error_message.replace("  ", "\n")
            logger.write(error_message + "\n")
    
    def _add_to_input_logs(self, input_prompt, input_statement):
        """Add custom formatted input logs"""
        with open(self.log_path, 'a') as logger:
            logger.write("User Input:\n")
            logger.write(input_prompt + " " + input_statement + "\n")
    
    def search_logs(self, search_term, log_type="all"):
        """Search logs for a specific term"""
        try:
            with open(self.log_path, 'r') as logger:
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
            with open(self.log_path, 'r') as logger:
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
        self.rules = config.get('sorting_rules', {})
        self.action = config.get('file_action', 'move')  # 'move' or 'copy'
        
    def sort_files(self):
        """Sort all files in the source directory according to rules."""
        if not self.source_dir.exists():
            logger.error(f"Source directory does not exist: {self.source_dir}")
            return False
            
        logger.info(f"Starting file sorting in {self.source_dir}")
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
                target_folder = Path(self.source_dir) / self.rules['extensions'][extension]
                return self._move_or_copy_file(file_path, target_folder)
            
            # Check pattern-based rules (e.g., filename contains certain text)
            for pattern, folder in self.rules.get('patterns', {}).items():
                if pattern.lower() in file_path.name.lower():
                    target_folder = Path(self.source_dir) / folder
                    return self._move_or_copy_file(file_path, target_folder)
            
            # Handle uncategorized files
            if 'other' in self.rules:
                target_folder = Path(self.source_dir) / self.rules['other']
                return self._move_or_copy_file(file_path, target_folder)
                
            return False
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return False
    
    def _move_or_copy_file(self, file_path, target_folder):
        """Move or copy file to target folder based on configuration."""
        try:
            # Create target folder if it doesn't exist
            target_folder.mkdir(parents=True, exist_ok=True)
            
            # Handle duplicate files
            target_file = target_folder / file_path.name
            if target_file.exists():
                # Rename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
                target_file = target_folder / new_name
            
            # Move or copy based on configuration
            if self.action == 'move':
                shutil.move(str(file_path), str(target_file))
                logger.info(f"Moved: {file_path.name} → {target_file.relative_to(self.source_dir)}")
            else:  # copy
                shutil.copy2(str(file_path), str(target_file))
                logger.info(f"Copied: {file_path.name} → {target_file.relative_to(self.source_dir)}")
            
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
# MAIN APPLICATION GUI
# ===============================

class FileOrganizerApp:
    def __init__(self, root, config_manager, file_sorter, file_watcher):
        self.root = root
        self.config_manager = config_manager
        self.file_sorter = file_sorter
        self.file_watcher = file_watcher
        self.config = config_manager.get_config()
        
        # Setup the main window
        self.root.title("File Organizer")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create main tabs
        self.main_tab = ttk.Frame(self.notebook)
        self.rules_tab = ttk.Frame(self.notebook)
        self.monitor_tab = ttk.Frame(self.notebook)
        self.logs_tab = ttk.Frame(self.notebook)
        self.about_tab = ttk.Frame(self.notebook)
        
        # Add tabs to the notebook
        self.notebook.add(self.main_tab, text="Main")
        self.notebook.add(self.rules_tab, text="Sorting Rules")
        self.notebook.add(self.monitor_tab, text="Monitoring")
        self.notebook.add(self.logs_tab, text="Logs")
        self.notebook.add(self.about_tab, text="About")
        
        # Build each tab's UI
        self._build_main_tab()
        self._build_rules_tab()
        self._build_monitor_tab()
        self._build_logs_tab()
        self._build_about_tab()
        
        # Status bar at the bottom
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Load configuration into UI
        self._load_config_to_ui()
    
    def _build_main_tab(self):
        """Build the main tab UI."""
        # Source directory section
        source_frame = ttk.LabelFrame(self.main_tab, text="Source Directory", padding="10")
        source_frame.pack(fill=tk.X, pady=5)
        
        self.source_dir_var = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.source_dir_var, width=50).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        ttk.Button(source_frame, text="Browse", command=self._browse_directory).pack(side=tk.RIGHT)
        
        # Action frame
        action_frame = ttk.LabelFrame(self.main_tab, text="File Action", padding="10")
        action_frame.pack(fill=tk.X, pady=5)
        
        self.action_var = tk.StringVar(value="move")
        ttk.Radiobutton(action_frame, text="Move Files", variable=self.action_var, value="move").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(action_frame, text="Copy Files", variable=self.action_var, value="copy").pack(side=tk.LEFT, padx=10)
        
        # Operation buttons
        button_frame = ttk.Frame(self.main_tab)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(
            button_frame, 
            text="Run Now", 
            command=self._run_sorting,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame, 
            text="Save Configuration", 
            command=self._save_config
        ).pack(side=tk.LEFT, padx=5)
        
        # Activity log in main tab
        log_frame = ttk.LabelFrame(self.main_tab, text="Recent Activity", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrolled text widget for logs
        self.activity_log = scrolledtext.ScrolledText(log_frame, height=10)
        self.activity_log.pack(fill=tk.BOTH, expand=True)
        self.activity_log.config(state=tk.DISABLED)  # Make it read-only
        
        # Refresh logs button
        ttk.Button(
            log_frame,
            text="Refresh Logs",
            command=self._refresh_activity_logs
        ).pack(side=tk.RIGHT, pady=5)
    
    def _build_rules_tab(self):
        """Build the rules tab UI."""
        # Extension rules frame
        ext_frame = ttk.LabelFrame(self.rules_tab, text="File Extension Rules", padding="10")
        ext_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollable frame for extensions
        scroll = ttk.Scrollbar(ext_frame)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.ext_tree = ttk.Treeview(ext_frame, columns=("Extension", "Folder"), show="headings", yscrollcommand=scroll.set)
        self.ext_tree.heading("Extension", text="Extension")
        self.ext_tree.heading("Folder", text="Target Folder")
        self.ext_tree.column("Extension", width=100)
        self.ext_tree.column("Folder", width=300)
        self.ext_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scroll.config(command=self.ext_tree.yview)
        
        # Buttons for extensions
        ext_buttons_frame = ttk.Frame(ext_frame)
        ext_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(ext_buttons_frame, text="Add Rule", command=self._add_extension_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(ext_buttons_frame, text="Edit Rule", command=self._edit_extension_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(ext_buttons_frame, text="Remove Rule", command=self._remove_extension_rule).pack(side=tk.LEFT, padx=5)
        
        # Pattern rules frame
        pattern_frame = ttk.LabelFrame(self.rules_tab, text="Filename Pattern Rules", padding="10")
        pattern_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollable frame for patterns
        pattern_scroll = ttk.Scrollbar(pattern_frame)
        pattern_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.pattern_tree = ttk.Treeview(pattern_frame, columns=("Pattern", "Folder"), show="headings", yscrollcommand=pattern_scroll.set)
        self.pattern_tree.heading("Pattern", text="Pattern")
        self.pattern_tree.heading("Folder", text="Target Folder")
        self.pattern_tree.column("Pattern", width=100)
        self.pattern_tree.column("Folder", width=300)
        self.pattern_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        pattern_scroll.config(command=self.pattern_tree.yview)
        
        # Buttons for patterns
        pattern_buttons_frame = ttk.Frame(pattern_frame)
        pattern_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(pattern_buttons_frame, text="Add Pattern", command=self._add_pattern_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(pattern_buttons_frame, text="Edit Pattern", command=self._edit_pattern_rule).pack(side=tk.LEFT, padx=5)
        ttk.Button(pattern_buttons_frame, text="Remove Pattern", command=self._remove_pattern_rule).pack(side=tk.LEFT, padx=5)
        
        # "Other" files configuration
        other_frame = ttk.LabelFrame(self.rules_tab, text="Uncategorized Files", padding="10")
        other_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(other_frame, text="Folder for uncategorized files:").pack(side=tk.LEFT, padx=5)
        
        self.other_folder_var = tk.StringVar(value="Unsorted")
        ttk.Entry(other_frame, textvariable=self.other_folder_var, width=30).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
    def _build_monitor_tab(self):
        """Build the monitoring tab UI."""
        # Monitoring options frame
        monitor_frame = ttk.LabelFrame(self.monitor_tab, text="File Monitoring Settings", padding="10")
        monitor_frame.pack(fill=tk.X, pady=5)
        
        # Enable monitoring checkbox
        self.monitoring_enabled_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            monitor_frame, 
            text="Enable automatic monitoring", 
            variable=self.monitoring_enabled_var
        ).pack(anchor=tk.W, pady=5)
        
        # Monitoring type
        monitor_type_frame = ttk.Frame(monitor_frame)
        monitor_type_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(monitor_type_frame, text="Monitoring Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.monitor_type_var = tk.StringVar(value="scheduled")
        ttk.Radiobutton(
            monitor_type_frame, 
            text="Scheduled (periodic checks)", 
            variable=self.monitor_type_var, 
            value="scheduled"
        ).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        ttk.Radiobutton(
            monitor_type_frame, 
            text="Real-time (immediate processing)", 
            variable=self.monitor_type_var, 
            value="realtime"
        ).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Interval settings
        interval_frame = ttk.LabelFrame(self.monitor_tab, text="Schedule Settings", padding="10")
        interval_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(interval_frame, text="Check interval (seconds):").pack(side=tk.LEFT, padx=5)
        
        self.interval_var = tk.IntVar(value=3600)
        interval_spinner = ttk.Spinbox(
            interval_frame, 
            from_=60, 
            to=86400, 
            increment=60, 
            textvariable=self.interval_var, 
            width=10
        )
        interval_spinner.pack(side=tk.LEFT, padx=5)
        
        # Common intervals
        ttk.Label(interval_frame, text="Presets:").pack(side=tk.LEFT, padx=(20, 5))
        
        ttk.Button(
            interval_frame, 
            text="5 min", 
            command=lambda: self.interval_var.set(300)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            interval_frame, 
            text="30 min", 
            command=lambda: self.interval_var.set(1800)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            interval_frame, 
            text="1 hour", 
            command=lambda: self.interval_var.set(3600)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            interval_frame, 
            text="6 hours", 
            command=lambda: self.interval_var.set(21600)
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            interval_frame, 
            text="12 hours", 
            command=lambda: self.interval_var.set(43200)
        ).pack(side=tk.LEFT, padx=2)
        
        # Monitoring control buttons
        control_frame = ttk.Frame(self.monitor_tab)
        control_frame.pack(fill=tk.X, pady=20)
        
        self.start_button = ttk.Button(
            control_frame, 
            text="Start Monitoring", 
            command=self._start_monitoring
        )
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(
            control_frame, 
            text="Stop Monitoring", 
            command=self._stop_monitoring,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Monitor status
        status_frame = ttk.LabelFrame(self.monitor_tab, text="Monitoring Status", padding="10")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.monitor_status_var = tk.StringVar(value="Monitoring is currently disabled")
        ttk.Label(
            status_frame, 
            textvariable=self.monitor_status_var, 
            font=("", 10, "bold")
        ).pack(fill=tk.X, padx=5, pady=10)
    
    def _build_logs_tab(self):
        """Build the logs tab UI."""
        # Search frame
        search_frame = ttk.Frame(self.logs_tab)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Search logs:").pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        ttk.Button(
            search_frame,
            text="Search",
            command=self._search_logs
        ).pack(side=tk.LEFT, padx=5)
        
        # Log type filter
        filter_frame = ttk.Frame(self.logs_tab)
        filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(filter_frame, text="Filter by:").pack(side=tk.LEFT, padx=5)
        
        self.log_type_var = tk.StringVar(value="all")
        ttk.Radiobutton(filter_frame, text="All", variable=self.log_type_var, value="all").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Information", variable=self.log_type_var, value="output").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="Errors", variable=self.log_type_var, value="error").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(filter_frame, text="User Input", variable=self.log_type_var, value="input").pack(side=tk.LEFT, padx=5)
        
        # Log viewer
        log_view_frame = ttk.LabelFrame(self.logs_tab, text="Log Messages", padding="10")
        log_view_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrolled text widget for logs
        self.log_text = scrolledtext.ScrolledText(log_view_frame)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)  # Make it read-only
        
        # Log control buttons
        log_buttons_frame = ttk.Frame(self.logs_tab)
        log_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(
            log_buttons_frame,
            text="Refresh Logs",
            command=self._refresh_logs
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            log_buttons_frame,
            text="Clear Display",
            command=self._clear_log_display
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            log_buttons_frame,
            text="Open Log File",
            command=self._open_log_file
        ).pack(side=tk.RIGHT, padx=5)
    
    def _build_about_tab(self):
        """Build the about tab UI."""
        about_frame = ttk.Frame(self.about_tab, padding="20")
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        # App title and version
        title_label = ttk.Label(
            about_frame, 
            text="File Organizer", 
            font=("", 16, "bold")
        )
        title_label.pack(pady=10)
        
        version_label = ttk.Label(
            about_frame, 
            text="Version 1.0"
        )
        version_label.pack()
        
        # Description
        description = """
        File Organizer is a utility to automatically sort files into folders 
        based on file types and naming patterns.
        
        Features:
        • Organize files by extension or filename patterns
        • Move or copy files to categorized folders
        • Real-time or scheduled monitoring
        • Detailed logging and activity tracking
        
        This application was built using Python and Tkinter.
        """
        
        desc_label = ttk.Label(
            about_frame,
            text=description,
            wraplength=500,
            justify=tk.CENTER
        )
        desc_label.pack(pady=20)
        
        # Credits
        credits_label = ttk.Label(
            about_frame,
            text="Created by: Umair\n© 2025",
            justify=tk.CENTER
        )
        credits_label.pack(pady=10)

        # App directory info
        app_dir_label = ttk.Label(
            about_frame,
            text=f"Application Directory:\n{APP_DIR}",
            justify=tk.CENTER,
            font=("", 8)
        )
        app_dir_label.pack(pady=20)

    def _load_config_to_ui(self):
        """Load configuration into the UI elements."""
        # Source directory
        self.source_dir_var.set(self.config.get('source_directory', ''))
        
        # File action
        self.action_var.set(self.config.get('file_action', 'move'))
        
        # Monitoring
        monitoring = self.config.get('monitoring', {})
        self.monitoring_enabled_var.set(monitoring.get('enabled', False))
        self.monitor_type_var.set(monitoring.get('type', 'scheduled'))
        self.interval_var.set(monitoring.get('interval', 3600))
        
        # Other folder
        self.other_folder_var.set(self.config.get('sorting_rules', {}).get('other', 'Unsorted'))
        
        # Extension rules
        self.ext_tree.delete(*self.ext_tree.get_children())
        for ext, folder in self.config.get('sorting_rules', {}).get('extensions', {}).items():
            self.ext_tree.insert('', tk.END, values=(ext, folder))
            
        # Pattern rules
        self.pattern_tree.delete(*self.pattern_tree.get_children())
        for pattern, folder in self.config.get('sorting_rules', {}).get('patterns', {}).items():
            self.pattern_tree.insert('', tk.END, values=(pattern, folder))
        
        # Update monitoring status
        self._update_monitoring_status()
        
        # Load recent logs
        self._refresh_logs()
        self._refresh_activity_logs()
    
    def _browse_directory(self):
        """Open directory browser dialog."""
        directory = filedialog.askdirectory(initialdir=self.source_dir_var.get())
        if directory:
            self.source_dir_var.set(directory)
    
    def _add_extension_rule(self):
        """Add a new extension rule."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Extension Rule")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="File Extension:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ext_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=ext_var, width=20).grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Target Folder:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        folder_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=folder_var, width=30).grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        def save_rule():
            ext = ext_var.get().strip()
            folder = folder_var.get().strip()
            
            if not ext or not folder:
                messagebox.showerror("Error", "Both fields are required.")
                return
                
            self.ext_tree.insert('', tk.END, values=(ext, folder))
            dialog.destroy()
            
        ttk.Button(dialog, text="Save", command=save_rule).grid(row=2, column=0, columnspan=2, pady=10)
    
    def _edit_extension_rule(self):
        """Edit selected extension rule."""
        selected = self.ext_tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select a rule to edit.")
            return
            
        item = self.ext_tree.item(selected[0])
        ext, folder = item['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Extension Rule")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="File Extension:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        ext_var = tk.StringVar(value=ext)
        ttk.Entry(dialog, textvariable=ext_var, width=20).grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Target Folder:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        folder_var = tk.StringVar(value=folder)
        ttk.Entry(dialog, textvariable=folder_var, width=30).grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        def update_rule():
            new_ext = ext_var.get().strip()
            new_folder = folder_var.get().strip()
            
            if not new_ext or not new_folder:
                messagebox.showerror("Error", "Both fields are required.")
                return
                
            self.ext_tree.item(selected[0], values=(new_ext, new_folder))
            dialog.destroy()
            
        ttk.Button(dialog, text="Update", command=update_rule).grid(row=2, column=0, columnspan=2, pady=10)
    
    def _remove_extension_rule(self):
        """Remove selected extension rule."""
        selected = self.ext_tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select a rule to remove.")
            return
            
        self.ext_tree.delete(selected[0])
    
    def _add_pattern_rule(self):
        """Add a new pattern rule."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Pattern Rule")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Filename Pattern:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        pattern_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=pattern_var, width=20).grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Target Folder:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        folder_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=folder_var, width=30).grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        def save_rule():
            pattern = pattern_var.get().strip()
            folder = folder_var.get().strip()
            
            if not pattern or not folder:
                messagebox.showerror("Error", "Both fields are required.")
                return
                
            self.pattern_tree.insert('', tk.END, values=(pattern, folder))
            dialog.destroy()
            
        ttk.Button(dialog, text="Save", command=save_rule).grid(row=2, column=0, columnspan=2, pady=10)
    
    def _edit_pattern_rule(self):
        """Edit selected pattern rule."""
        selected = self.pattern_tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select a pattern to edit.")
            return
            
        item = self.pattern_tree.item(selected[0])
        pattern, folder = item['values']
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Pattern Rule")
        dialog.geometry("400x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Filename Pattern:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        pattern_var = tk.StringVar(value=pattern)
        ttk.Entry(dialog, textvariable=pattern_var, width=20).grid(row=0, column=1, padx=10, pady=10, sticky=tk.W)
        
        ttk.Label(dialog, text="Target Folder:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        folder_var = tk.StringVar(value=folder)
        ttk.Entry(dialog, textvariable=folder_var, width=30).grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)
        
        def update_rule():
            new_pattern = pattern_var.get().strip()
            new_folder = folder_var.get().strip()
            
            if not new_pattern or not new_folder:
                messagebox.showerror("Error", "Both fields are required.")
                return
                
            self.pattern_tree.item(selected[0], values=(new_pattern, new_folder))
            dialog.destroy()
            
        ttk.Button(dialog, text="Update", command=update_rule).grid(row=2, column=0, columnspan=2, pady=10)
    
    def _remove_pattern_rule(self):
        """Remove selected pattern rule."""
        selected = self.pattern_tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select a pattern to remove.")
            return
            
        self.pattern_tree.delete(selected[0])
    
    def _save_config(self):
        """Save current UI state to configuration."""
        try:
            # Build extension rules
            extensions = {}
            for item_id in self.ext_tree.get_children():
                item = self.ext_tree.item(item_id)
                ext, folder = item['values']
                extensions[ext] = folder
            
            # Build pattern rules
            patterns = {}
            for item_id in self.pattern_tree.get_children():
                item = self.pattern_tree.item(item_id)
                pattern, folder = item['values']
                patterns[pattern] = folder
            
            # Build complete config
            config = {
                'source_directory': self.source_dir_var.get(),
                'file_action': self.action_var.get(),
                'monitoring': {
                    'enabled': self.monitoring_enabled_var.get(),
                    'type': self.monitor_type_var.get(),
                    'interval': self.interval_var.get()
                },
                'sorting_rules': {
                    'extensions': extensions,
                    'patterns': patterns,
                    'other': self.other_folder_var.get() or 'Unsorted'
                }
            }
            
            # Save to file
            if self.config_manager.save_config(config):
                messagebox.showinfo("Success", "Configuration saved successfully.")
                self.config = config
                # Update file sorter with new config
                self.file_sorter.__init__(config)
                
                # Update file watcher with new config if it's running
                if self.file_watcher.running:
                    self.file_watcher.stop()
                    self.file_watcher.__init__(config, self.file_sorter)
                    self.file_watcher.start()
                else:
                    self.file_watcher.__init__(config, self.file_sorter)
                    
                # Update status
                self._update_monitoring_status()
                self.status_var.set("Configuration saved successfully")
            else:
                messagebox.showerror("Error", "Failed to save configuration.")
                self.status_var.set("Failed to save configuration")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving: {str(e)}")
            logger.error(f"Error saving configuration: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
    
    def _run_sorting(self):
        """Execute file sorting operation."""
        source_dir = self.source_dir_var.get()
        if not source_dir:
            messagebox.showerror("Error", "Please specify a source directory.")
            return
            
        if not Path(source_dir).exists():
            messagebox.showerror("Error", "Source directory does not exist.")
            return
        
        # First, save the current configuration
        self._save_config()
        
        # Update status
        self.status_var.set("Sorting files...")
        
        # Run sorting in a separate thread to keep UI responsive
        def sorting_thread():
            try:
                success = self.file_sorter.sort_files()
                if success:
                    messagebox.showinfo("Success", "Files organized successfully!")
                    self.status_var.set("Files organized successfully")
                    self._refresh_activity_logs()  # Refresh the activity log
                else:
                    messagebox.showerror("Error", "Failed to organize files. Check logs for details.")
                    self.status_var.set("Failed to organize files")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
                logger.error(f"Error during sorting operation: {str(e)}", exc_info=True)
                self.status_var.set(f"Error: {str(e)}")
        
        threading.Thread(target=sorting_thread).start()
    
    def _start_monitoring(self):
        """Start the file watcher."""
        # First save current configuration
        self._save_config()
        
        # Check if source directory is valid
        source_dir = self.source_dir_var.get()
        if not source_dir:
            messagebox.showerror("Error", "Please specify a source directory.")
            return
            
        if not Path(source_dir).exists():
            messagebox.showerror("Error", "Source directory does not exist.")
            return
        
        # Start monitoring
        try:
            success = self.file_watcher.start()
            if success:
                messagebox.showinfo("Success", "File monitoring started.")
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self._update_monitoring_status()
                self.status_var.set("Monitoring started successfully")
            else:
                messagebox.showerror("Error", "Failed to start monitoring. Check logs for details.")
                self.status_var.set("Failed to start monitoring")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            logger.error(f"Error starting monitoring: {str(e)}", exc_info=True)
            self.status_var.set(f"Error: {str(e)}")
    
    def _stop_monitoring(self):
        """Stop the file watcher."""
        try:
            self.file_watcher.stop()
            messagebox.showinfo("Success", "File monitoring stopped.")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self._update_monitoring_status()
            self.status_var.set("Monitoring stopped")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            logger.error(f"Error stopping monitoring: {str(e)}", exc_info=True)
            self.status_var.set(f"Error: {str(e)}")
    
    def _update_monitoring_status(self):
        """Update the monitoring status display."""
        if self.file_watcher.running:
            if self.file_watcher.config.get('monitoring', {}).get('type') == 'realtime':
                status = "Real-time monitoring is active"
            else:
                interval = self.file_watcher.config.get('monitoring', {}).get('interval', 3600)
                status = f"Scheduled monitoring is active (checking every {interval} seconds)"
            
            self.monitor_status_var.set(status)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.monitor_status_var.set("Monitoring is currently disabled")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def _refresh_logs(self):
        """Refresh the log display in the logs tab."""
        try:
            log_type = self.log_type_var.get()
            search_term = self.search_var.get().strip()
            
            # Get logs based on search term if provided, otherwise get recent logs
            if search_term:
                logs = logger.search_logs(search_term, log_type)
            else:
                logs = logger.get_recent_logs(count=100, log_type=log_type)
            
            # Update the log text widget
            self.log_text.config(state=tk.NORMAL)
            self.log_text.delete("1.0", tk.END)
            
            if not logs:
                self.log_text.insert(tk.END, "No log entries found.")
            else:
                for log in logs:
                    # Add color formatting based on log type
                    if "ERROR:" in log or "Error:" in log:
                        self.log_text.insert(tk.END, f"{log}\n", "error")
                    elif "INFO:" in log or "Output:" in log:
                        self.log_text.insert(tk.END, f"{log}\n", "info")
                    else:
                        self.log_text.insert(tk.END, f"{log}\n")
            
            self.log_text.config(state=tk.DISABLED)
            
            # Scroll to the end
            self.log_text.see(tk.END)
            
            # Configure tags for coloring
            self.log_text.tag_configure("error", foreground="red")
            self.log_text.tag_configure("info", foreground="blue")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh logs: {str(e)}")
            logger.error(f"Error refreshing logs: {str(e)}", exc_info=True)
    
    def _refresh_activity_logs(self):
        """Refresh the recent activity log in the main tab."""
        try:
            logs = logger.get_recent_logs(count=10)
            
            # Update the activity log widget
            self.activity_log.config(state=tk.NORMAL)
            self.activity_log.delete("1.0", tk.END)
            
            if not logs:
                self.activity_log.insert(tk.END, "No recent activity.")
            else:
                for log in logs:
                    # Add color formatting based on log type
                    if "ERROR:" in log or "Error:" in log:
                        self.activity_log.insert(tk.END, f"{log}\n", "error")
                    elif "INFO:" in log or "Output:" in log:
                        self.activity_log.insert(tk.END, f"{log}\n", "info")
                    else:
                        self.activity_log.insert(tk.END, f"{log}\n")
            
            self.activity_log.config(state=tk.DISABLED)
            
            # Scroll to the end
            self.activity_log.see(tk.END)
            
            # Configure tags for coloring
            self.activity_log.tag_configure("error", foreground="red")
            self.activity_log.tag_configure("info", foreground="blue")
            
        except Exception as e:
            logger.error(f"Error refreshing activity logs: {str(e)}", exc_info=True)
    
    def _search_logs(self):
        """Search logs for specific text."""
        search_term = self.search_var.get().strip()
        if not search_term:
            messagebox.showinfo("Info", "Please enter a search term.")
            return
            
        self._refresh_logs()  # This will use the search term if provided
    
    def _clear_log_display(self):
        """Clear the log display (not the log file)."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
    
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
                messagebox.showinfo("Info", "Log file does not exist yet.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open log file: {str(e)}")
            logger.error(f"Error opening log file: {str(e)}", exc_info=True)

# Global variables to be used in on_closing() function
root = None
file_watcher = None

def on_closing():
    """Handle the window close event."""
    global file_watcher, root
    logger.info("Shutting down File Organizer application")
    if file_watcher and file_watcher.running:
        file_watcher.stop()
    if root:
        root.destroy()

# ===============================
# APPLICATION ENTRY POINT
# ===============================

def main():
    global root, file_watcher
    logger.info("Starting File Organizer application")
    logger.info(f"Application directory: {APP_DIR}")
    
    # Initialize configuration
    config_manager = ConfigManager("config.json")
    config = config_manager.get_config()
    
    # Initialize file sorter
    file_sorter = FileSorter(config)
    
    # Initialize file watcher
    file_watcher = FileWatcher(config, file_sorter)
    
    # Start monitoring if enabled
    if config.get('monitoring', {}).get('enabled', False):
        file_watcher.start()
    
    return config_manager, file_sorter, file_watcher

if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    root.title("File Organizer")
    root.geometry("900x700")
    
    # Initialize app components
    config_manager, file_sorter, file_watcher = main()
    
    # Configure style for the app
    style = ttk.Style()
    if 'clam' in style.theme_names():
        style.theme_use('clam')
    
    # Create accent button style
    style.configure("Accent.TButton", font=("", 10, "bold"))
    
    # Initialize the application
    app = FileOrganizerApp(root, config_manager, file_sorter, file_watcher)
    
    # Set the close protocol to handle cleanup
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the Tkinter main loop
    root.mainloop()
