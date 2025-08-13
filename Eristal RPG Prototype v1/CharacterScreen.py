from StatIncreaseWindow import StatIncreaseWindow
from PyQt6.QtWidgets import *
from PyQt6 import uic

class CharacterScreen:
    def __init__(self, RoseObject, OzObject, EliObject):
        global Rose
        global Oz
        global Eli
        Rose = RoseObject
        Oz = OzObject
        Eli = EliObject

    #Open a new stat increase window for the relevent character
    def on_RoseStatPointsButton_clicked(self):
        #check if battle is in progress
        statIncreaseWindow.ShowWindow(Rose)

    def on_OzStatPointsButton_clicked(self):
        #check if battle is in progress
        statIncreaseWindow.ShowWindow(Oz)

    def on_EliStatPointsButton_clicked(self):
        #check if battle is in progress
        statIncreaseWindow.ShowWindow(Eli)

    #Opens a new skill tree window for the relevent character
    def on_RoseSkillPointsButton_clicked(self):
        #skillTreeWindow.ShowWindow(Rose)
        pass

    def on_OzSkillPointsButton_clicked(self):
        #skillTreeWindow.ShowWindow(Oz)
        pass

    def on_EliSkillPointsButton_clicked(self):
        #skillTreeWindow.ShowWindow(Eli)
        pass

    #Initialize character screen creation
    def LoadWindow(self, GameWindowObject):
        global gameWindow
        gameWindow = GameWindowObject

        global characterForm
        global characterWindow
        CForm, CWindow = uic.loadUiType("CharacterScreen.ui")
        characterWindow = CWindow()
        characterForm = CForm()
        characterForm.setupUi(characterWindow)

        characterForm.RoseStatPointsButton.clicked.connect(self.on_RoseStatPointsButton_clicked)
        characterForm.OzStatPointsButton.clicked.connect(self.on_OzStatPointsButton_clicked)
        characterForm.EliStatPointsButton.clicked.connect(self.on_EliStatPointsButton_clicked)
        #connect 3 skill point buttons

        #create a StatIncreaseWindow and load it
        global statIncreaseWindow
        statIncreaseWindow = StatIncreaseWindow()

        windowsLoaded = 1 + statIncreaseWindow.LoadWindow(gameWindow)
        return windowsLoaded
    
    def ShowWindow(self):
        gameWindow.UpdateUIElements()
        characterWindow.show()

    def HideStatIncreaseWindow(self):
        statIncreaseWindow.HideWindow()
    
    #Updates Character Window level, health, stats, and skill/stat point buttons
    def UpdateUIElements(self):
        #Update stat increase UI
        statIncreaseWindow.UpdateUIElements()

        #Arrays for entities and their corresponding text labels in the UI
        entities = [Rose, Oz, Eli]
        levelLabels = [characterForm.RoseLevel, characterForm.OzLevel, characterForm.EliLevel]
        hpLabels = [characterForm.RoseHP, characterForm.OzHP, characterForm.EliHP]
        powerLabels = [characterForm.RosePower, characterForm.OzPower, characterForm.EliPower]
        defenseLabels = [characterForm.RoseDefense, characterForm.OzDefense, characterForm.EliDefense]
        speedLabels = [characterForm.RoseSpeed, characterForm.OzSpeed, characterForm.EliSpeed]
        luckLabels = [characterForm.RoseLuck, characterForm.OzLuck, characterForm.EliLuck]
        statPointButtons = [characterForm.RoseStatPointsButton, characterForm.OzStatPointsButton, characterForm.EliStatPointsButton]
        skillPointButtons = [characterForm.RoseSkillPointsButton, characterForm.OzSkillPointsButton, characterForm.EliSkillPointsButton]
        xpLabels = [characterForm.RoseXP, characterForm.OzXP, characterForm.EliXP]


        #Update UI in character screen
        for i in range(len(entities)):
            characterLevel = entities[i].GetLevel()
            levelString = "Level: " + str(characterLevel)
            levelLabels[i].setText(levelString)

            characterMaxHP = entities[i].GetHP()
            characterCurrentHP = entities[i].GetCurrentHP()
            HPString = "HP: " + str(characterCurrentHP) + "/" + str(characterMaxHP)
            hpLabels[i].setText(HPString)

            characterStat = entities[i].GetPower()
            statString = "Power: " + str(characterStat)
            powerLabels[i].setText(statString)

            characterStat = entities[i].GetDefense()
            statString = "Defense: " + str(characterStat)
            defenseLabels[i].setText(statString)

            characterStat = entities[i].GetSpeed()
            statString = "Speed: " + str(characterStat)
            speedLabels[i].setText(statString)

            characterStat = entities[i].GetLuck()
            statString = "Luck: " + str(characterStat)
            luckLabels[i].setText(statString)

            characterStat = entities[i].GetStatPoints()
            statString = "Stat Pts: " + str(characterStat)
            statPointButtons[i].setText(statString)

            characterStat = entities[i].GetSkillPoints()
            statString = "Skill Pts: " + str(characterStat)
            skillPointButtons[i].setText(statString)

            characterCurrentXP = entities[i].GetCurrentXP()
            characterNeededXP = entities[i].GetXPToLevelUp()
            statString = "XP: " + str(characterCurrentXP) + "/" +str(characterNeededXP)
            xpLabels[i].setText(statString)

        