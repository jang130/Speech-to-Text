'''
Project group 14th - Speech to text application
'''

#Importing libraries
import speech_recognition as speech
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5 import QtCore
import STT_ui 
import sys


class App(QWidget, STT_ui.Ui_Dialog):
    '''
    Class of dialog window
    '''
    def __init__(self, parent=None):
        '''
        This method initializes GUI
        '''
        super(App, self).__init__(parent)
        self.setupUi(self)
        self.app_working()
        
    def app_working(self):
        '''
        This method reacts to the record button click
        '''
        self.recordButton.clicked.connect(self.on_click)
        self.show()
        
    def on_click(self):
        try:
            lng = self.check_language()
            self.STTConversion(lng)
        except UnboundLocalError:
            self.recordLabel.setText("Please select language")

        
    def check_language(self):
        '''
        This method checks which language is choosen to recognition of speech
        and returns language variable.
        '''
        if self.German_tick.isChecked() == True:
            language = "de"
            txt = "Dein text ist: "
        elif self.Turkish_tick.isChecked() == True:
            language = "tr"
            txt = "Konuşma metniniz: "
        elif self.Polish_tick.isChecked() == True:
            language = "pl"
            txt = "Twój tekst to: " 
        elif self.Spanish_tick.isChecked() == True:
            language = "es"
            txt = "Su texto es: "
        elif self.English_tick.isChecked() == True:
            language = "en"
            txt = "Your text: "
        return language, txt
    
    def copy_to_clipboard(self, text):
        '''
        This method does a copy of text and puts it to clipboard
        '''
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)
    
    def STTConversion(self, lng):
        '''
        This method does all needed things to transcript the voice to speech in
        a given language.
        '''
        self.recordLabel.setText("Listening...") #Changes label text to Listening...
        QtCore.QCoreApplication.processEvents() #Makes gui reacts to every label change
        with speech.Microphone() as source: #Setting up voice recognition features
            SpeakToText = speech.Recognizer() #
            SpeakToText.adjust_for_ambient_noise(source)
            audio = SpeakToText.listen(source)
            try:
                self.recordLabel.setText("Transcripting...") #Changes label text to Transcripting...
                STT = SpeakToText.recognize_google(audio, language=lng[0]) #Does conversion
                self.recordLabel.setText("Transcription succeded") #Changes label text to Transcription succeded
                QMessageBox.question(self, 'Transcription succeded', lng[1] + STT.lower(), QMessageBox.Ok)
                self.copy_to_clipboard(STT) #Calls function that copies to clipboard
            except speech.UnknownValueError: #Expects error
                self.recordLabel.setText("Could not understand")
     

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App() #Creating App class object
    window.show() #Launching UI
    sys.exit(app.exec_()) #Proper closing



    