from GameMenu import GameMenu
from PyQt6.QtWidgets import *
from PyQt6 import uic

#Controls the main menu and overworld functionality

#Main menu
#-New Game
#-Load Game
#-Options
#-Quit

#Overworld menu
#-Exploration buttons
#-Character Screen
#-Save Game
#-Options

#windowsLoaded is counted up after each window finishes loading, if all windows are loaded then the app is executed
def FinishedLoadingWindow(newWindowsLoaded):
    global windowsLoaded
    windowsLoaded += newWindowsLoaded
    if (windowsLoaded >= numberOfWindows):
        app.exec()

#Menu button functions
#Opens a world menu with starting values for everything
def on_newGameButton_clicked():
    gameWorld.ShowGameWindow()
    gameWorld.CreateNewCharacters()

#
def on_loadGameButton_clicked():
    alert = QMessageBox()
    alert.setText('Will load an existing game in the future')
    alert.exec()

#Launches a options window that edits the options file
def on_optionsButton_clicked():
    alert = QMessageBox()
    alert.setText('Will load an options window in the future')
    alert.exec()

#Closes out of the game
def on_quitButton_clicked():
    app.quit()

#Sets counting variables for window loading
#Main Menu, Options*, Game Menu, Character Window, Stat Increase Window, Battle Window
numberOfWindows = 5
windowsLoaded = 0

#Menu screen creation
Form, Window = uic.loadUiType("MainMenu.ui")
app = QApplication([])
mainMenuWindow = Window()
form = Form()
form.setupUi(mainMenuWindow)
form.newGameButton.clicked.connect(on_newGameButton_clicked)
form.loadGameButton.clicked.connect(on_loadGameButton_clicked)
form.optionsButton.clicked.connect(on_optionsButton_clicked)
form.quitButton.clicked.connect(on_quitButton_clicked)
mainMenuWindow.show()
FinishedLoadingWindow(1)

#Game Menu creation
#Which loads Character Screen, which loads Stat Increase Window
gameWorld = GameMenu()
FinishedLoadingWindow(gameWorld.LoadGameWindow())