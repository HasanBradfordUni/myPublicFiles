import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor

from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QComboBox, QTextEdit, QPushButton, QLabel, 
                             QFrame, QScrollArea, QGridLayout)

from aiModels import aiModels
from geminiPrompt import generate_response

class AIChatbotInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        # Define all the option lists
        self.modes = ["Default", "Q & A", "Writing", "Coding", "Creative", "Analysis"]
        
        self.tones = ["Formal", "Casual", "Funny", "Professional", "Friendly", 
                      "Academic", "Creative", "Persuasive", "Informative"]
        
        # Define type options for each mode
        self.type_options = {
            "Default": ["General Chat", "Help", "Information", "Advice"],
            "Q & A": ["General Knowledge", "Technical", "Educational", "Scientific",
                     "Historical", "Current Events", "How-to", "Explanation"],
            "Writing": ["Essay", "Cover Letter", "Autobiography", "Non-fictional Novel", 
                       "Email", "Text Message", "Instagram Post", "Blog Post", "Article",
                       "Resume", "Letter", "Story", "Poem", "Script"],
            "Coding": ["Python", "Java", "JavaScript", "HTML", "CSS", "C++", "C#", 
                      "PHP", "Ruby", "Go", "Rust", "RegEx", "SQL", "Maths for Computing",
                      "Algorithm Design", "Data Structures", "Debugging"],
            "Creative": ["Story Writing", "Poetry", "Song Lyrics", "Character Development",
                        "World Building", "Dialogue", "Plot Ideas", "Creative Prompts"],
            "Analysis": ["Text Analysis", "Data Interpretation", "Research", "Comparison",
                        "Summary", "Review", "Critique", "Report"]
        }
        
        self.initUI()

        self.ai = aiModels("Default", "Formal")  # Initialize with default mode and tone
        
    def initUI(self):
        self.setWindowTitle("Ultimate AI Chatbot")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set the color scheme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #FFD700;
            }
            QComboBox {
                background-color: #2d2d2d;
                border: 2px solid #FFD700;
                border-radius: 5px;
                padding: 5px;
                color: #FFD700;
                font-weight: bold;
                font-size: 16px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                border: none;
            }
            QTextEdit {
                background-color: #2d2d2d;
                border: 2px solid #FFD700;
                border-radius: 5px;
                padding: 10px;
                color: #FF0000;
                font-size: 16px;
                font-family: Arial;
            }
            QPushButton {
                background-color: #FFD700;
                color: #000000;
                border: none;
                border-radius: 5px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #FFA500;
            }
            QPushButton:pressed {
                background-color: #B8860B;
            }
            QLabel {
                color: #FFD700;
                font-weight: bold;
                font-size: 16px;
            }
            QFrame {
                background-color: #2d2d2d;
                border-radius: 10px;
            }
        """)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Akhtar Hasan Ultimate AI Chatbot")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Control panel
        control_frame = QFrame()
        control_layout = QGridLayout(control_frame)
        control_layout.setSpacing(15)
        
        # Mode selection
        mode_label = QLabel("Mode:")
        mode_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(self.modes)
        self.mode_combo.currentTextChanged.connect(self.update_type_options)
        
        # Type selection
        type_label = QLabel("Type:")
        type_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.type_combo = QComboBox()
        
        # Tone selection
        tone_label = QLabel("Tone:")
        tone_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.tone_combo = QComboBox()
        self.tone_combo.addItems(self.tones)
        
        # Add to grid
        control_layout.addWidget(mode_label, 0, 0)
        control_layout.addWidget(self.mode_combo, 0, 1)
        control_layout.addWidget(type_label, 0, 2)
        control_layout.addWidget(self.type_combo, 0, 3)
        control_layout.addWidget(tone_label, 0, 4)
        control_layout.addWidget(self.tone_combo, 0, 5)
        
        main_layout.addWidget(control_frame)
        
        # Chat area
        chat_frame = QFrame()
        chat_layout = QVBoxLayout(chat_frame)
        
        # Input area
        input_label = QLabel("Your Input:")
        input_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.input_text = QTextEdit()
        self.input_text.setMaximumHeight(150)
        self.input_text.setPlaceholderText("Enter your message here...")
        self.input_text.setFont(QFont("Arial", 16))
        
        # Send button
        self.send_button = QPushButton("Send Message")
        self.send_button.clicked.connect(self.send_message)
        
        # Output area
        output_label = QLabel("AI Response:")
        output_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("AI responses will appear here...")
        self.output_text.setFont(QFont("Arial", 16))
        
        # Add to chat layout
        chat_layout.addWidget(input_label)
        chat_layout.addWidget(self.input_text)
        chat_layout.addWidget(self.send_button)
        chat_layout.addWidget(output_label)
        chat_layout.addWidget(self.output_text)
        
        main_layout.addWidget(chat_frame)
        
        # Initialize type options
        self.update_type_options()
        
    def update_type_options(self):
        current_mode = self.mode_combo.currentText()
        self.type_combo.clear()
        
        # Get the type options for the current mode
        if current_mode in self.type_options:
            self.type_combo.addItems(self.type_options[current_mode])
    
    def send_message(self):
        user_input = self.input_text.toPlainText().strip()
        if not user_input:
            return
            
        mode = self.mode_combo.currentText()
        type_selection = self.type_combo.currentText()
        tone = self.tone_combo.currentText()
        
        # Format the message with context
        formatted_message = f"[Mode: {mode}] [Type: {type_selection}] [Tone: {tone}]\n\n{user_input}"
        
        # Display user message with larger font
        self.output_text.append(f"<b style='color: #FFD700; font-size: 18px;'>You:</b> <span style='color: #FF0000; font-size: 16px;'>{user_input}</span>")
        self.output_text.append(f"<i style='color: #FFA500; font-size: 14px;'>Settings: {mode} - {type_selection} - {tone}</i>")
        
        # Placeholder for AI response (you would integrate your AI model here)
        self.ai.change_mode_and_tone(mode, tone)
        mode = self.ai.choose_mode()
        ai_response = generate_response(mode, type_selection, tone, user_input)
        self.output_text.append(f"<b style='color: #00FF00; font-size: 18px;'>AI:</b> <span style='color: #FF0000; font-size: 16px;'>{ai_response}</span>")
        self.output_text.append("")
        
        # Clear input
        self.input_text.clear()
        
        # Scroll to bottom
        self.output_text.verticalScrollBar().setValue(
            self.output_text.verticalScrollBar().maximum()
        )

def main():
    app = QApplication(sys.argv)
    window = AIChatbotInterface()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()