from PyQt6.QtWidgets import *
from PyQt6 import uic

class StatIncreaseWindow:
    #button functions (5 +/-, reset, accept)
    def on_MaxHPIncrease_clicked(self):
        if (self.statPointsAvailable > 0):
            self.statPointsAvailable -= 1
            statChangeDictionary["MaxHP"] += 1
        gameWindow.UpdateUIElements()

    def on_MaxHPDecrease_clicked(self):
        if (statChangeDictionary["MaxHP"] > 0):
            self.statPointsAvailable += 1
            statChangeDictionary["MaxHP"] -= 1
        gameWindow.UpdateUIElements()

    def on_PowerIncrease_clicked(self):
        if (self.statPointsAvailable > 0):
            self.statPointsAvailable -= 1
            statChangeDictionary["Power"] += 1
        gameWindow.UpdateUIElements()

    def on_PowerDecrease_clicked(self):
        if (statChangeDictionary["Power"] > 0):
            self.statPointsAvailable += 1
            statChangeDictionary["Power"] -= 1
        gameWindow.UpdateUIElements()

    def on_DefenseIncrease_clicked(self):
        if (self.statPointsAvailable > 0):
            self.statPointsAvailable -= 1
            statChangeDictionary["Defense"] += 1
        gameWindow.UpdateUIElements()

    def on_DefenseDecrease_clicked(self):
        if (statChangeDictionary["Defense"] > 0):
            self.statPointsAvailable += 1
            statChangeDictionary["Defense"] -= 1
        gameWindow.UpdateUIElements()

    def on_SpeedIncrease_clicked(self):
        if (self.statPointsAvailable > 0):
            self.statPointsAvailable -= 1
            statChangeDictionary["Speed"] += 1
        gameWindow.UpdateUIElements()

    def on_SpeedDecrease_clicked(self):
        if (statChangeDictionary["Speed"] > 0):
            self.statPointsAvailable += 1
            statChangeDictionary["Speed"] -= 1
        gameWindow.UpdateUIElements()

    def on_LuckIncrease_clicked(self):
        if (self.statPointsAvailable > 0):
            self.statPointsAvailable -= 1
            statChangeDictionary["Luck"] += 1
        gameWindow.UpdateUIElements()

    def on_LuckDecrease_clicked(self):
        if (statChangeDictionary["Luck"] > 0):
            self.statPointsAvailable += 1
            statChangeDictionary["Luck"] -= 1
        gameWindow.UpdateUIElements()

    def on_ResetChangesButton_clicked(self):
        self.statPointsAvailable = CharacterObject.GetStatPoints()
        for key in statChangeDictionary:
            statChangeDictionary[key] = 0
        gameWindow.UpdateUIElements()

    def on_AcceptButton_clicked(self):
        CharacterObject.IncreaseStats(statChangeDictionary)
        self.on_ResetChangesButton_clicked()

    #Initialize stat increase window creation
    def LoadWindow(self, GameWindowObject):
        global gameWindow
        gameWindow = GameWindowObject
        global statForm
        global statWindow
        SForm, SWindow = uic.loadUiType("StatIncreaseWindow.ui")
        statWindow = SWindow()
        statForm = SForm()
        statForm.setupUi(statWindow)

        global statPointsAvailable
        statPointsAvailable = -1
        global statChangeDictionary
        statChangeDictionary = {
            "MaxHP": 0,
            "Power": 0,
            "Defense": 0,
            "Speed": 0,
            "Luck": 0
        }
        #connect buttons
        statForm.MaxHPIncrease.clicked.connect(self.on_MaxHPIncrease_clicked)
        statForm.MaxHPDecrease.clicked.connect(self.on_MaxHPDecrease_clicked)
        statForm.PowerIncrease.clicked.connect(self.on_PowerIncrease_clicked)
        statForm.PowerDecrease.clicked.connect(self.on_PowerDecrease_clicked)
        statForm.DefenseIncrease.clicked.connect(self.on_DefenseIncrease_clicked)
        statForm.DefenseDecrease.clicked.connect(self.on_DefenseDecrease_clicked)
        statForm.SpeedIncrease.clicked.connect(self.on_SpeedIncrease_clicked)
        statForm.SpeedDecrease.clicked.connect(self.on_SpeedDecrease_clicked)
        statForm.LuckIncrease.clicked.connect(self.on_LuckIncrease_clicked)
        statForm.LuckDecrease.clicked.connect(self.on_LuckDecrease_clicked)
        statForm.ResetChangesButton.clicked.connect(self.on_ResetChangesButton_clicked)
        statForm.AcceptButton.clicked.connect(self.on_AcceptButton_clicked)

        return 1
    
    #Opens a stat increase window
    #A character object is passed in so the stats ui can be updated
    #Will not open if a battle is in progress
    def ShowWindow(self, Character):
        #Returns if a battle is occurring
        if gameWindow.battleActive:
            return

        global CharacterObject
        CharacterObject = Character
        self.statPointsAvailable = CharacterObject.GetStatPoints()
        for key in statChangeDictionary:
            statChangeDictionary[key] = 0
        gameWindow.UpdateUIElements()
        statWindow.show()

    def HideWindow(self):
        statWindow.hide()

    #Updates UI elements based on the character that is passed in
    def UpdateUIElements(self):
        #Returns if stat window hasn't been given a character yet
        try:
            CharacterObject
        except NameError:
            return 0

        #Character name, level
        characterName = CharacterObject.GetName() + " Lv " + str(CharacterObject.GetLevel())
        statForm.CharacterName.setText(characterName)

        #Stat points available
        self.statPointsAvailable = CharacterObject.GetStatPoints()
        for key in statChangeDictionary:
            self.statPointsAvailable -= statChangeDictionary[key]
        statString = "Points Available: " + str(self.statPointsAvailable)
        statForm.StatChangeBox.setTitle(statString)

        #Current stat values and final stat values
        characterStat = CharacterObject.GetHP()
        statString = "Max HP: " + str(characterStat)
        statForm.MaxHP.setText(statString)
        statForm.MaxHP_2.setText(str(characterStat + statChangeDictionary["MaxHP"]))

        characterStat = CharacterObject.GetPower()
        statString = "Power: " + str(characterStat)
        statForm.Power.setText(statString)
        statForm.Power_2.setText(str(characterStat + statChangeDictionary["Power"]))

        characterStat = CharacterObject.GetDefense()
        statString = "Defense: " + str(characterStat)
        statForm.Defense.setText(statString)
        statForm.Defense_2.setText(str(characterStat + statChangeDictionary["Defense"]))

        characterStat = CharacterObject.GetSpeed()
        statString = "Speed: " + str(characterStat)
        statForm.Speed.setText(statString)
        statForm.Speed_2.setText(str(characterStat + statChangeDictionary["Speed"]))

        characterStat = CharacterObject.GetLuck()
        statString = "Luck: " + str(characterStat)
        statForm.Luck.setText(statString)
        statForm.Luck_2.setText(str(characterStat + statChangeDictionary["Luck"]))

        #Stat change values
        statForm.MaxHPChange.setText(str(statChangeDictionary["MaxHP"]))
        statForm.PowerChange.setText(str(statChangeDictionary["Power"]))
        statForm.DefenseChange.setText(str(statChangeDictionary["Defense"]))
        statForm.SpeedChange.setText(str(statChangeDictionary["Speed"]))
        statForm.LuckChange.setText(str(statChangeDictionary["Luck"]))