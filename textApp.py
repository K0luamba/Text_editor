import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

def shift(list, elem): #paste elem on last position, but saves all except first
    i = 1
    while i < len(list):
        list[i-1] = list[i]
        i = i + 1
    list[len(list)-1] = elem
    return list

class Example(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #all enabled fonts
        self.fonts = ['Segoe Print', 'Arial', 'Arial Black', 'Calibri', 'Comic Sans MS', 'Courier New', 'Franklin Gothic Medium', 'Impact', 'Lucida Console', 'Times New Roman', 'Verdana'] 
        self.font_num = 0 #number of in massive of fonts
        self.fontSize = 11
        self.textEdit = QTextEdit() #built-in simple text-edit window
        self.textEdit.setFontFamily(self.fonts[self.font_num]) #default
        self.textEdit.setFontPointSize(self.fontSize)
        self.setCentralWidget(self.textEdit) #it will cover all empty space in centre
        self.fileFlag = 0 #mark, that by default there are no link to file
        self.fname = ["empty","empty"]
        exitAction = QAction(QIcon('exit.png'), 'Exit', self) #define all actions, what they can do
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Shortcut - Ctrl+Q')
        exitAction.triggered.connect(self.close)
        fontUpAction = QAction(QIcon('font+.png'), 'Increase font size', self)
        fontUpAction.setShortcut('Ctrl+W')
        fontUpAction.setStatusTip('Shortcut - Ctrl+W')
        fontUpAction.triggered.connect(self.font_plus)
        fontDownAction = QAction(QIcon('font-.png'), 'Decrease font size', self)
        fontDownAction.setShortcut('Ctrl+E')
        fontDownAction.setStatusTip('Shortcut - Ctrl+E')
        fontDownAction.triggered.connect(self.font_minus)
        fontNextAction = QAction(QIcon('change.png'), 'Change font', self)
        fontNextAction.setShortcut('Ctrl+R')
        fontNextAction.setStatusTip('Shortcut - Ctrl+R')
        fontNextAction.triggered.connect(self.font_next)
        saveTextAction = QAction(QIcon('save.png'), 'Save new file', self)
        saveTextAction.setShortcut('Ctrl+S')
        saveTextAction.setStatusTip('Shortcut - Ctrl+S')
        saveTextAction.triggered.connect(self.save_file_new)
        openFileAction = QAction(QIcon('open.png'), 'Open File', self)
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.setStatusTip('Shortcut - Ctrl+O')
        openFileAction.triggered.connect(self.open_file)
        updateAction = QAction(QIcon('update.png'), 'Update', self)
        updateAction.setShortcut('Ctrl+U')
        updateAction.setStatusTip('Shortcut - Ctrl+U')
        updateAction.triggered.connect(self.update)
        codeAction = QAction(QIcon('code.png'), 'Code text', self)
        codeAction.setShortcut('Ctrl+T')
        codeAction.setStatusTip('Shortcut - Ctrl+T')
        codeAction.triggered.connect(self.code)
        decodeAction = QAction(QIcon('decode.png'), 'Decode text', self)
        decodeAction.setShortcut('Ctrl+Y')
        decodeAction.setStatusTip('Shortcut - Ctrl+Y')
        decodeAction.triggered.connect(self.decode)
        undoAction = QAction(QIcon('undo.png'), 'Undo last change', self)
        undoAction.setShortcut('Ctrl+D')
        undoAction.setStatusTip('Shortcut - Ctrl+D')
        undoAction.triggered.connect(self.undo)
        self.textEdit.textChanged.connect(self.save_file) #enable auto-save using signal
        self.statusBar()
        self.statusBar().showMessage('Font size: ' + str(self.fontSize) + ', ' + self.fonts[self.font_num])
        #menubar = self.menuBar()
        #fileMenu = menubar.addMenu('File')
        #fileMenu.addAction(exitAction)
        toolbar = self.addToolBar('Exit')
        toolbar.setIconSize(QSize(35, 35))
        toolbar.addAction(exitAction) #add all actions from left to right
        toolbar.addAction(openFileAction)
        toolbar.addAction(saveTextAction)
        toolbar.addAction(updateAction)
        toolbar.addAction(undoAction)
        toolbar.addAction(codeAction)
        toolbar.addAction(decodeAction)
        toolbar.addAction(fontNextAction)
        toolbar.addAction(fontUpAction)
        toolbar.addAction(fontDownAction)
        self.conditions = []

        self.setGeometry(300,300,550,450)
        self.setWindowTitle('My Editor')
        self.setWindowIcon(QIcon('icon.png'))
        self.show()

    def font_plus(self):
        self.fontSize += 1
        self.textEdit.setFontPointSize(self.fontSize)
        self.statusBar().showMessage('Font size: ' + str(self.fontSize) + ', ' + self.fonts[self.font_num])

    def font_minus(self):
        self.fontSize -= 1
        self.textEdit.setFontPointSize(self.fontSize)
        self.statusBar().showMessage('Font size: ' + str(self.fontSize) + ', ' + self.fonts[self.font_num])

    def font_next(self):
        self.font_num += 1
        if self.font_num == 11:
            self.font_num = 0 #enable cycling on massive
        self.textEdit.setFontFamily(self.fonts[self.font_num]) #use our massive of fonts
        self.statusBar().showMessage('Font size: ' + str(self.fontSize) + ', ' + self.fonts[self.font_num])

    def open_file(self):
        self.conditions.clear() #clear history of previous file
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', '/home') #save name of the file in our object
        #print('open ' + self.fname[0] + ' ' + self.fname[1])
        f = open(self.fname[0], 'r') 
        with f:
            data = f.read()
            print(data)
            self.textEdit.setText(data) #output file
        self.fileFlag = 1
        
    def save_file(self):
        mytext = self.textEdit.toPlainText() #our text in string value
        if len(self.conditions) < 10:
            self.conditions.append(mytext)
        else:
            self.conditions= shift(self.conditions, mytext)
        #print(self.conditions)
        if self.fileFlag != 0: #if working with already created file
            #print('save ' + self.fname[0])
            with open(self.fname[0], 'w') as f:
                f.write(mytext)
                
    def save_file_new(self):
        mytext = self.textEdit.toPlainText()
        cash = self.fname[0]
        self.fname = ["empty","empty"] 
        self.fname[0], ok = QInputDialog.getText(self, 'Save new file', 'Enter the full name of your file:')
        if ok:
            #print('new save ' + self.fname[0])
            with open(self.fname[0], 'w') as f: #create new file
                f.write(mytext)
        else:
            self.fname[0] = cash
        if not self.fileFlag:
            self.fileFlag = 1

    def update(self): #check changes of the file
        if self.fileFlag != 0:
            f = open(self.fname[0], 'r') #open file again
            with f:
                data = f.read()
                self.textEdit.setText(data) #output file
        else:
            self.statusBar().showMessage("No file")

    def code(self):
        str = self.textEdit.toPlainText()
        if str == '':
            self.statusBar().showMessage('No text to code')
        else:
            code, ok = QInputDialog.getText(self, 'Coding text', 'Enter your codeword or coding phrase. \nEncoding will be by substitution cypher:')
            if ok:
                text = list(str)
                i = 0
                j = 0
                for c in str:
                    text[i] = chr(ord(c) + ord(code[j]) + 174) #substitution in Unicode table
                    i += 1
                    j += 1
                    if j == len(code):
                        j = 0
                str = ''.join(text) #list -> string
                self.textEdit.setText(str)

    def decode(self):
        str = self.textEdit.toPlainText()
        if str == '':
            self.statusBar().showMessage('No text to decode')
        else:
            code, ok = QInputDialog.getText(self, 'Decoding text', 'Enter your codeword or coding phrase:')
            if ok:
                text = list(str)
                i = 0
                j = 0
                for c in str:
                    text[i] = chr(ord(c) - ord(code[j]) - 174)
                    i += 1
                    j += 1
                    if j == len(code):
                        j = 0
                str = ''.join(text)
                self.textEdit.setText(str)

    def undo(self):
        if self.conditions == [] or len(self.conditions) == 1: #previous condition was empty|other file|limit os saved reached
            self.statusBar().showMessage("Buffer is empty")
        else:
            prevText = self.conditions.pop()
            prevText = self.conditions.pop()
            self.textEdit.setText(prevText)
          
app = QApplication(sys.argv)
ex = Example()
sys.exit(app.exec_())
