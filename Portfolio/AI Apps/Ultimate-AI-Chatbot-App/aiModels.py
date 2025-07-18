
class aiModels:
    def __init__(self, mode, tone):
        self.mode = mode
        self.tone = tone

    def choose_mode(self):
        #Call different functions based on the modes selected in the GUI"
        #The different modes are: 'Analysis', 'Creative', 'Coding', 'Writing', 'Q & A', 'Default'"
        if self.mode == "Analysis":
            return self.analysis_mode()
        elif self.mode == "Creative":
            return self.creative_mode()
        elif self.mode == "Coding":
            return self.coding_mode()
        elif self.mode == "Writing":
            return self.writing_mode()
        elif self.mode == "Q & A":
            return self.qa_mode()
        else:
            return self.default_mode()
        
    def default_mode(self):
        #Default mode is used for general chat, help, information and advice
        return f"You are a general purpose AI assistant. Your tone should be {self.tone}. You can help with general chat, provide information, and give advice."
        
    def qa_mode(self):
        #Q & A mode is used for general knowledge, technical, educational, scientific, historical, current events, how-to and explanation
        return f"You are a Q & A AI assistant. Your tone should be {self.tone}. You can help with general knowledge, technical questions, educational content, scientific queries, historical facts, current events, how-to guides and explanations."
    
    def writing_mode(self):
        #Writing mode is used for writing, editing, proofreading, grammar, spelling, punctuation, style and tone
        return f"You are a writing AI assistant. Your tone should be {self.tone}. You can help with writing, editing, proofreading, grammar, spelling, punctuation, style and tone."
    
    def coding_mode(self):
        #Coding mode is used for programming, coding, debugging, code review, code generation, code optimization and code documentation
        return f"You are a coding AI assistant. Your tone should be {self.tone}. You can help with programming, coding, debugging, code review, code generation, code optimization and code documentation."
    
    def creative_mode(self):
        #Creative mode is used for creative writing, storytelling, poetry, music, art, design and creativity
        return f"You are a creative AI assistant. Your tone should be {self.tone}. You can help with creative writing, storytelling, poetry, music, art, design and creativity."
    
    def analysis_mode(self):
        #Analysis mode is used for data analysis, data visualization, data science, machine learning, statistics and research
        return f"You are an analysis AI assistant. Your tone should be {self.tone}. You can help with data analysis, data visualization, data science, machine learning, statistics and research."
    
    def change_tone(self, new_tone):
        #Change the tone of the AI assistant
        self.tone = new_tone
        return f"The tone has been changed to {self.tone}."
    
    def change_mode(self, new_mode):
        #Change the mode of the AI assistant
        self.mode = new_mode
        return f"The mode has been changed to {self.mode}."
    
    def change_mode_and_tone(self, new_mode, new_tone):
        #Change both the mode and tone of the AI assistant
        self.mode = new_mode
        self.tone = new_tone
        return f"The mode has been changed to {self.mode} and the tone has been changed to {self.tone}."
    
    def get_mode(self):
        #Get the current mode of the AI assistant
        return self.mode
    
    def get_tone(self):
        #Get the current tone of the AI assistant
        return self.tone