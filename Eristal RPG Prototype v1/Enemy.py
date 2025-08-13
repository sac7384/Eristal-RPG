from Entity import Entity
import random

#Child of Entity
class Enemy(Entity):
    def __init__(self, inputName, loadedStats):
        #Calling Entity.py __init__
        Entity.__init__(self, inputName, loadedStats)

        #Default Action values for when no Actions are supplied
        defaultActionDescription = {
            "Name": "null",
            "Description": "This is a default action that has not been given any values. It does nothing",
            "Action Used": "You used the default null action, and nothing happens",
            "Action Success": "Congrats! You successfully did nothing",
            "Action Fail": "You failed at doing nothing, with the outcome of nothing happening. A strange paradox indeed"
        }
        #Action(1, defaultActionDescription, ["Front"], {})

        #Enemy specific
        self.xpGiven = 0
        self.levelUpDictionaries = []
        self.actionStrategy = "Random"
        self.actionArray = []
        self.currentActionIndex = 0
        self.targetStrategy = "Random"
        self.targetIndex = 0
        self.targetPosition = "Front"

        #Booleans to track the first action/target chosen
        #Used to make sure the initial action/target is chosen correctly
        self.firstActionChoice = True
        self.firstTargetChoice = True
    
    #Chooses a new action to take based off of the enemy's actionStrategy
    #Random: Chooses a random action from actionArray
    #Sequential: Chooses the next action in the list, ie after action 2 will choose action 3
    def ChooseNewAction(self):
        #Exception for if no Actions have been supplied
        try:
            self.actionArray[0]
        except:
            return False

        if self.actionStrategy == "Random":
            #Randomly choose an action from the array, all actions have equal weight
            self.currentActionIndex = random.randrange(len(self.actionArray))
        elif self.actionStrategy == "Sequential":
            #Move to next action in the array
            self.currentActionIndex += 1
            #If past the end of the array, move to the beginning
            if self.currentActionIndex >= len(self.actionArray):
                self.currentActionIndex = 0
            #Makes sure the first action is at the beginning of the array
            if self.firstActionChoice:
                self.currentActionIndex = 0
                self.firstActionChoice = False
        self.intentAction = self.actionArray[self.currentActionIndex]

        #Choose target position based on the chosen action
        self.ChooseNewPosition()

    #Chooses the position to target on an opponent based on the enemy's chosen action
    def ChooseNewPosition(self):
        #Temporarily chooses a random position from the Action's possible positions
        positionArray = self.intentAction.GetPositionArray()
        self.targetPosition = positionArray[random.randrange(len(positionArray))]

    #Chooses a new target based off of the enemy's targetStrategy
    #Random: Chooses a random entity to target, will target left side with harmful actions and right side with beneficial actions
    #Sequential: Chooses the next target in the battle, ie after entity 0 will target entity 1
    def ChooseNewTarget(self):
        if self.targetStrategy == "Random":
            #Randomly choose a target from the array, all targets have equal weight
            self.targetIndex = random.randrange(3)
            #Targets a fellow enemy if the ability chosen is beneficial
            if self.actionArray[self.currentActionIndex].HasTag("Friendly"):
                self.targetIndex += 3
        elif self.targetStrategy == "Sequential":
            #Move to next target on the field
            self.targetIndex += 1
            #If past the end of the array, move to the beginning
            if self.targetIndex >= 3:
                self.targetIndex = 0
            #Makes sure the first target is at the beginning of the battle array
            if self.firstTargetChoice:
                self.targetIndex = 0
                self.firstTargetChoice = False

            #Targets a fellow enemy if the ability chosen is beneficial
            if self.actionArray[self.currentActionIndex].HasTag("Friendly"):
                self.targetIndex += 3

    def SetActionStrategy(self, newStrategy):#SetActionStrategy
        self.actionStrategy = newStrategy
        self.firstActionChoice = True
        self.ChooseNewAction()

    def SetTargetStrategy(self, newStrategy):
        self.targetStrategy = newStrategy
        self.firstTargetChoice = True
        self.ChooseNewTarget()

    #Takes an array of actions as input
    #Adds those actions to this enemy's action array
    def AddActions(self, addedActions):
        for action in addedActions:
            self.actionArray.append(action)

    #Takes an array of dictionaries
    #Input must have elements HP, Power, Defense, Speed, Luck
    def AddLevelUpDictionaries(self, statDictionaries):
        for dictionary in statDictionaries:
            self.levelUpDictionaries.append(dictionary)

    #Randomly chooses a level up from levelUpDictionaries
    #Applies those stat increases to self
    def LevelUp(self):
        #Exception for if no levelUpDictionaries have been supplied
        try:
            self.levelUpDictionaries[0]
        except:
            return False
        
        chosenLevelUp = random.choice(self.levelUpDictionaries)
        self.level += 1
        self.currentHP += chosenLevelUp["HP"]
        self.maxHP += chosenLevelUp["HP"]
        self.power += chosenLevelUp["Power"]
        self.defense += chosenLevelUp["Defense"]
        self.speed += chosenLevelUp["Speed"]
        self.luck += chosenLevelUp["Luck"]

        #May also increase the capabilities of enemy's actions in the future

    def SetXPGiven(self, xp):
        self.xpGiven = xp

    def GetXPGiven(self):
        return self.xpGiven
    
    def GetIntentAction(self):
        return self.actionArray[self.currentActionIndex]
    
    def GetTargetIndex(self):
        return self.targetIndex
    
    def GetTargetPosition(self):
        return self.targetPosition
    
    def PrintLvUpDictionaries(self):
        levelString = str(self.name) + " Lv " + str(self.level)
        print(levelString)
        for dictionary in self.levelUpDictionaries:
            print("Start")
            for stat in dictionary:
                print(dictionary[stat])