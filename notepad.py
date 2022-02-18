import PySimpleGUI as sg
import pathlib
import os

#  Overall Layout
sg.ChangeLookAndFeel('GreenTan')

file = None
filename = 'Untitled'
width = 90
height = 25

menu = [['File',['New', 'Open', 'Save', 'Save As', '---', 'Exit']],
        ['Tools', ['Word Count']],
        ['View', ['Reset Size', 'Maximize']],
        ['Help', ['About']]]

layout = [[sg.Menu(menu)],
          [sg.Text('Zenote', font=('DK Lemon Yellow Sun', 16), size=(width, 1))],
          [sg.Multiline(font=('Times New Roman', 12), 
                        size=(width, height), key = '_body_')]]

window = sg.Window(title=filename, layout=layout, 
                   margins=(0, 0), resizable=True, 
                   return_keyboard_events=True, finalize=True)

# Functionality
class Notepad():
    
    def new_file(self):
        ''' Resets multiline body and window title '''
        window['_body_'].update(value='')
        window.set_title('Untitled')
        file = None
        return file
    
    def open_file(self):
        ''' Opens file and updates window title '''
        filename = sg.popup_get_file('Open', no_window=True)
        if filename:
            file = pathlib.Path(filename)
            window['_body_'].update(value=file.read_text())
            title = os.path.basename(file.absolute()).split('.')[0]
            window.set_title(title)
            return file
    
    def save(self, file):
        ''' Saves file if file exist else Save As '''
        if file:
            file.write_text(values.get('_body_'))
        else:
            self.save_as()
    
    def save_as(self):
        ''' Saves file with a filename inputted on pop-up '''
        filename = sg.popup_get_file('Save as', 
                                     save_as=True, no_window=True)
        if filename:
            file = pathlib.Path(filename)
            file.write_text(values.get('_body_'))
            title = os.path.basename(file.absolute()).split('.')[0]
            window.set_title(title)
            return file
        
    def word_count(self):
        ''' Displays word count '''
        words = [word for word in values['_body_'].split(' ') 
                 if word !='\n']
        word_count = len(words)
        sg.popup('Word Count: {:,d}'.format(word_count))

    def about(self):
        sg.popup('''
        Zenote is a basic note-taking made on Python 3 with 
        PySimpleGUI

        Follow the creator at https://github.com/29yabuki
                 ''')
        
# Main Event Loop
notepad = Notepad()
while True:
    event, values = window.read()
    if event in ('New', 'n:78'):
        file = notepad.new_file()
    if event in ('Open', 'o:79'):
        file = notepad.open_file()
    if event in ('Save', 's:83'):
        notepad.save(file)
    if event in ('Save As',):
        file = notepad.save_as()
    if event in ('Word Count',):
        notepad.word_count()
    if event in ('Maximize',):
        window.maximize()
        window['_body_'].expand(expand_x=True, expand_y=True)
    if event in ('Reset Size',):
        window.normal()
    if event in ('About',):
        notepad.about()
    if event in ('Exit',):
        break