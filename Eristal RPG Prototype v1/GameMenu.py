from CharacterScreen import CharacterScreen
from BattleWindow import BattleWindow
from PlayerCharacter import PlayerCharacter
from Enemy import Enemy
from Action import Action
from PyQt6.QtWidgets import *
from PyQt6 import uic
import random

#Opens windows for each of the world actions, Explore, Character Screen, Save Game, Options
#Handles ui and buttons for the Game Window and Character Screen
class GameMenu:
    def __init__(self):
        global Rose
        global Oz
        global Eli
        Rose = PlayerCharacter("Rose")
        Oz = PlayerCharacter("Oswald")
        Eli = PlayerCharacter("Elijah")

    #Creates each of the characters in their default state
    def CreateNewCharacters(self):
        Rose.ResetCharacter()
        Oz.ResetCharacter()
        Eli.ResetCharacter()
        #Rose actions 1 and 2
        axeStrings = {
            "Name": "Battleaxe",
            "Description": "A heavy two-handed battleaxe. Deals 1.5x physical damage to the Front of an enemy. 0.5x critical chance and 3x critical damage",
            "Action Used": "{ActionUserName} swings the Battleaxe at {TargetName}!",
            "Action Success": "The blade strikes and deals {value} physical damage to {TargetName}!",
            "Action Fail": "The blade can't land on {TargetName} and no damage is dealt"
        }
        axeTags = {
            "Attack": 1, #One attack
            "Power Multiplier": 1.5, #Deals 150% of power
            "Crit Chance Multiplier": 0.5, #Halves attack crit chance
            "Crit Damage Multiplier": 3, #Triples damage on a crit
            "Physical": True #Deals physical damage type (does nothing currently)
        }
        battleaxe = Action(1, axeStrings, ["Front"], axeTags)
        Rose.SetActions(battleaxe, battleaxe)
        #Oz action 1
        healStrings = {
            "Name": "Heal",
            "Description": "A single target spell that cures wounds. Heals 1x",
            "Action Used": "{ActionUserName} chants a holy word and casts Heal on {TargetName}",
            "Action Success": "The magic swirls around {TargetName} and heals {value} HP!",
            "Action Fail": "The magic is unable to reach {TargetName} and cannot heal them"
        }
        healTags = {
            "Heal": 1, #One heal
            "Power Multiplier": 1, #Heals 100% of power
            "Spell": True #Labelled as a spell (does nothing currently)
        }
        heal = Action(1, healStrings, ["Above", "Behind", "Front", "Under"], healTags)
        #Oz action 2
        shieldStrings = {
            "Name": "Shield",
            "Description": "A sturdy shield that can block damage. Applies the Shielded effect to self, halving damage taken for 1 turn",
            "Action Used": "{ActionUserName} holds up their shield and prepares to be attacked",
            "Effect Success": "{ActionUserName} is Shielded for {value} turn(s)",
            "Effect Fail": "{ActionUserName} tries to utilize their shield but is unable to keep it held aloft"
        }
        shieldTags = {
            "Self": True, #Only targets self
            "Turn Effects": {"Shielded": 1} #Adds the Shielded (halves damage taken) effect for 1 turn
        }
        shield = Action(1, shieldStrings, ["Above", "Behind", "Front", "Under"], shieldTags)
        Oz.SetActions(heal, shield)
        #Eli action 1
        icicleStrings = {
            "Name": "Icicle",
            "Description": "A spell which fires a sharp ice spike at the Front of an enemy. Deals 1x Ice damage. Will apply 2 Frozen to the target",
            "Action Used": "{ActionUserName} crafts an Icicle in the air and fires it towards {TargetName}",
            "Action Success": "The Icicle stabs through {TargetName} and deals {value} Ice damage!",
            "Action Fail": "The ice breaks against {TargetName}'s form. No damage was dealt",
            "Effect Success": "{value} Frozen is applied to {TargetName}",
            "Effect Fail": "Frost grows across {TargetName}'s form but melts away just as quickly. No Frozen was applied"
        }
        icicleTags = {
            "Attack": 1, #One attack
            "Power Multiplier": 1, #Deals 100% of power
            "Crit Chance Multiplier": 1, #Normal crit chance
            "Crit Damage Multiplier": 1.5, #1.5x damage on a crit
            "Spell": True, #Labelled as a spell (does nothing currently)
            "Ice": True, #Deals ice damage type (does nothing currently)
            "Proc Effects": {"Frozen": 2} #Applies 2 Frozen (cancels the target's next 2 speed ticks) to the target
        }
        icicle = Action(1, icicleStrings, ["Front"], icicleTags)
        #Eli action 2
        barrierStrings = {
            "Name": "Barrier",
            "Description": "Conjures a barrier of magic to absorb the damage of an attack. Applies 1 Barrier to the target",
            "Action Used": "{ActionUserName} attempts to conjure a Barrier to protect {TargetName}",
            "Effect Success": "A wall of magic energy forms around {TargetName}! {TargetName} gains {value} Barrier",
            "Effect Fail": "{ActionUserName}'s spell dissapates and no barrier forms"
        }
        barrierTags = {
            "Spell": True, #Labelled as a spell (does nothing currently)
            "Proc Effects": {"Barrier": 1} #Applies 1 Barrier (negates 1 instance of damage)
        }
        barrier = Action(1, barrierStrings, ["Above", "Behind", "Front", "Under"], barrierTags)
        Eli.SetActions(icicle, barrier)
        self.UpdateUIElements()

    #Loads game information from a save file
    #Loads character information and other game data
    def LoadGame(self, saveFileIndex):
        #Future functionality, no save/load files currently
        pass

    #Called by BattleWindow once a battle has ended
    def BattleOver(self):
        self.battleActive = False

    def on_battleButton_clicked(self):
        #Can't start a new battle if there is already a battle occurring
        if self.battleActive:
            return
        self.battleActive = True
        characterScreen.HideStatIncreaseWindow()

        #Enemy base stats and random level ups
        #Temp enemy creation, will be moved to exploration areas in the future
        baseStats = {
            "Level": 1,
            "HP": 4,
            "Power": 2,
            "Defense": 0,
            "Speed": 1,
            "Luck": 1
        }
        powerlvup = {
            "HP": 1,
            "Power": 2,
            "Defense": 0,
            "Speed": 1,
            "Luck": 0
        }
        healthlvup = {
            "HP": 3,
            "Power": 0,
            "Defense": 1,
            "Speed": 0,
            "Luck": 0
        }
        lucklvup = {
            "HP": 1,
            "Power": 1,
            "Defense": 0,
            "Speed": 0,
            "Luck": 2
        }
        speedlvup = {
            "HP": 1,
            "Power": 0,
            "Defense": 0,
            "Speed": 2,
            "Luck": 1
        }
        defenselvup = {
            "HP": 1,
            "Power": 1,
            "Defense": 2,
            "Speed": 0,
            "Luck": 0
        }

        #Enemy actions
        #Stone Soldier
        actionStrings = {
            "Name": "Stone Sword",
            "Action Used": "{ActionUserName} swings his stone sword at {TargetName}!",
            "Action Success": "The blade strikes and deals {value} physical damage to {TargetName}!",
            "Action Fail": "The blade can't land on {TargetName} and no damage is dealt"
        }
        actionTags = {
            "Attack": 1, #One attack
            "Power Multiplier": 1, #Deals 100% of power
            "Crit Chance Multiplier": 0.5, #Halves attack crit chance
            "Crit Damage Multiplier": 1.5, #1.5x damage on a crit
            "Physical": True #Deals physical damage type (does nothing currently)
        }
        stoneSword = Action(1, actionStrings, ["Front"], actionTags)
        #Green Slime
        actionStrings = {
            "Name": "Acid Spit",
            "Action Used": "{ActionUserName} spits corrosive acid at {TargetName}!",
            "Action Success": "{TargetName} is coated in acid and takes {value} acid damage!",
            "Action Fail": "The acid covers {TargetName} but does not harm them"
        }
        actionTags = {
            "Attack": 1, #One attack
            "Power Multiplier": 1.5, #Deals 150% of power
            "Crit Chance Multiplier": 0, #Cannot crit
            "Crit Damage Multiplier": 1, #1x damage on a crit
            "Acid": True #Deals acid damage type (does nothing currently)
        }
        acidSpit = Action(1, actionStrings, ["Front"], actionTags)

        actionStrings = {
            "Name": "Slime Bubble",
            "Action Used": "{ActionUserName} lobs a bubble of slime in {TargetName}'s direction!",
            "Effect Success": "The slime lands on {TargetName} and covers them completely! {TargetName} is Slimed for {value} turn(s)",
            "Effect Fail": "The slime slides right off of {TargetName} with no effect"
        }
        actionTags = {
            "Turn Effects": {"Slimed": 1} #Applies Slimed (target cannot crit) for 1 turn
        }
        slimeBubble = Action(1, actionStrings, ["Above"], actionTags)
        #Monster Captain
        actionStrings = {
            "Name": "Spear Stab",
            "Action Used": "{ActionUserName} stabs their spear at {TargetName}!",
            "Action Success": "The spear connects and deals {value} physical damage to {TargetName}!",
            "Action Fail": "The point can't land on {TargetName} and no damage is dealt"
        }
        actionTags = {
            "Attack": 2, #Two attacks
            "Power Multiplier": 0.50, #Deals 50% of power
            "Crit Chance Multiplier": 1, #1x attack crit chance
            "Crit Damage Multiplier": 2, #2x damage on a crit
            "Physical": True #Deals physical damage type (does nothing currently)
        }
        spearStab = Action(1, actionStrings, ["Front"], actionTags)

        actionStrings = {
            "Name": "Rally",
            "Action Used": "{ActionUserName} tries to boost the morale of {TargetName}!",
            "Effect Success": "{TargetName} is inspired and ready to fight with more vigor! {TargetName} gets {value} Rally",
            "Effect Fail": "{TargetName} does not react to {ActionUserName}'s Rallying cry"
        }
        actionTags = {
            "Proc Effects": {"Rally": 1}, #Applies 1 Rally (1 more attack on their next attack action)
            "Friendly": True #Labelled as a friendly action, enemies will target Friendly actions at other enemies
        }
        rally = Action(1, actionStrings, ["Front"], actionTags)
        #Skeleton
        actionStrings = {
            "Name": "Broken Bone",
            "Action Used": "{ActionUserName} jabs at {TargetName} with the broken bone of their arm!",
            "Action Success": "The bone stabs {TargetName} and deals {value} physical damage!",
            "Action Fail": "The point can't land on {TargetName} and no damage is dealt"
        }
        actionTags = {
            "Attack": 1, #One attack
            "Power Multiplier": 0.75, #Deals 50% of power
            "Crit Chance Multiplier": 2, #2x attack crit chance
            "Crit Damage Multiplier": 2, #2x damage on a crit
            "Physical": True #Deals physical damage type (does nothing currently)
        }
        brokenBone = Action(1, actionStrings, ["Front"], actionTags)
        #Animated Books
        actionStrings = {
            "Name": "Fire Bolt",
            "Action Used": "A bolt of fire flies from {ActionUserName} towards {TargetName}",
            "Action Success": "The bolt bursts in a flurry of sparks and leaves a dark singe mark on {TargetName}, who takes {value} Fire damage",
            "Action Fail": "The bolt strikes {TargetName} but seems to dissipate with no effect"
        }
        actionTags = {
            "Attack": 1, #One attack
            "Power Multiplier": 1.5, #Deals 150% of power
            "Crit Chance Multiplier": 0.5, #0.5x crit chance
            "Crit Damage Multiplier": 2, #2x damage on a crit
            "Spell": True, #Labelled as a spell (does nothing currently)
            "Fire": True, #Deals fire damage type (does nothing currently)
        }
        fireBolt = Action(1, actionStrings, ["Front"], actionTags)

        actionStrings = {
            "Name": "Haste",
            "Description": "n/a",
            "Action Used": "{ActionUserName} attempts to cast Haste on {TargetName}!",
            "Effect Success": "{TargetName} is enveloped in transmutation magic and begins to move much faster! {TargetName} gains Haste for {value} turn(s)",
            "Effect Fail": "The Haste spell alights upon {TargetName} but cannot hold and evaporates into the air"
        }
        actionTags = {
            "Turn Effects": {"Haste": 1}, #Applies 1 Haste (speed ticks twice for 1 turn)
            "Friendly": True #Labelled as a friendly action, enemies will target Friendly actions at other enemies
        }
        haste = Action(1, actionStrings, ["Front"], actionTags)

        #Add player characters and random enemies to battle array
        battleParticipantList = [Rose, Oz, Eli]
        for i in range(3):
            r = random.randrange(5)
            if r == 0:
                chosenEnemy = Enemy("Stone Soldier", baseStats)
                chosenEnemy.AddLevelUpDictionaries([defenselvup, powerlvup, healthlvup])
                chosenEnemy.AddActions([stoneSword])
                chosenEnemy.SetActionStrategy("Sequential")
                chosenEnemy.SetTargetStrategy("Sequential")
            elif r == 1:
                chosenEnemy = Enemy("Green Slime", baseStats)
                chosenEnemy.AddLevelUpDictionaries([lucklvup, powerlvup, healthlvup])
                chosenEnemy.AddActions([acidSpit, slimeBubble])
                chosenEnemy.SetActionStrategy("Random")
                chosenEnemy.SetTargetStrategy("Random")
            elif r == 2:
                chosenEnemy = Enemy("Monster Captain", baseStats)
                chosenEnemy.AddLevelUpDictionaries([speedlvup, powerlvup])
                chosenEnemy.AddActions([spearStab, rally])
                chosenEnemy.SetActionStrategy("Sequential")
                chosenEnemy.SetTargetStrategy("Sequential")
            elif r == 3:
                chosenEnemy = Enemy("Skeleton", baseStats)
                chosenEnemy.AddLevelUpDictionaries([powerlvup, speedlvup])
                chosenEnemy.AddActions([brokenBone])
                chosenEnemy.SetActionStrategy("Sequential")
                chosenEnemy.SetTargetStrategy("Random")
            elif r == 4:
                chosenEnemy = Enemy("Animated Books", baseStats)
                chosenEnemy.AddLevelUpDictionaries([lucklvup, speedlvup])
                chosenEnemy.AddActions([fireBolt, haste])
                chosenEnemy.SetActionStrategy("Sequential")
                chosenEnemy.SetTargetStrategy("Sequential")
            chosenEnemy.SetXPGiven(25)
            battleParticipantList.append(chosenEnemy)
        #Scale random enemies up to the party's level
        for lv in range(Rose.GetLevel() - 1):
            for i in range(3, 6):
                battleParticipantList[i].LevelUp()

        battleWindow.StartBattle(battleParticipantList)
        self.UpdateUIElements()

    def on_characterScreenButton_clicked(self):
        characterScreen.ShowWindow()
        self.UpdateUIElements()

    def on_saveGameButton_clicked(self):
        alert = QMessageBox()
        alert.setText('Will save your progress in the future')
        alert.exec()
        self.UpdateUIElements()

    def on_optionsButton_clicked(self):
        alert = QMessageBox()
        alert.setText('Will load an options window in the future')
        alert.exec()
        self.UpdateUIElements()

    #Initial game window creation
    def LoadGameWindow(self):
        #Boolean shows whether a battle is currently in progress
        self.battleActive = False

        global gameForm
        global gameWindow
        GForm, GWindow = uic.loadUiType("GameWindow.ui")
        gameWindow = GWindow()
        gameForm = GForm()
        gameForm.setupUi(gameWindow)
        gameForm.battleButton.clicked.connect(self.on_battleButton_clicked)

        gameForm.characterScreenButton.clicked.connect(self.on_characterScreenButton_clicked)
        gameForm.saveGameButton.clicked.connect(self.on_saveGameButton_clicked)
        gameForm.optionsButton.clicked.connect(self.on_optionsButton_clicked)

        #Calls for other windows to be loaded
        global characterScreen
        characterScreen = CharacterScreen(Rose, Oz, Eli)
        global battleWindow
        battleWindow = BattleWindow()
        windowsLoaded = 1 + characterScreen.LoadWindow(self) + battleWindow.LoadWindow(self)
        return windowsLoaded #returning the number of windows that have been loaded
    
    def ShowGameWindow(self):
        gameWindow.show()
        self.UpdateUIElements()

    #Updates all UI elements in the Game Window
    #Calls UI update functions in all subsequent windows
    def UpdateUIElements(self):
        #Call for Character Screen update
        characterScreen.UpdateUIElements()

        #Call for Battle Window update
        battleWindow.UpdateUIElements()

        #Arrays for entities and their corresponding text labels in the UI
        entities = [Rose, Oz, Eli]
        nameLabels = [gameForm.RoseName, gameForm.OzName, gameForm.EliName]
        hpLabels = [gameForm.RoseHP, gameForm.OzHP, gameForm.EliHP]

        #Game Window levels and hp
        for i in range(len(entities)):
            characterLevel = entities[i].GetLevel()
            characterName = entities[i].GetName()
            levelString = characterName + ": Lv " + str(characterLevel)
            nameLabels[i].setText(levelString)

            characterMaxHP = entities[i].GetHP()
            characterCurrentHP = entities[i].GetCurrentHP()
            HPString = str(characterCurrentHP) + "/" + str(characterMaxHP)
            hpLabels[i].setText(HPString)

        