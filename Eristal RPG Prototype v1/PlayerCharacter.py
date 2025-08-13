from Entity import Entity
from Action import Action

#Child of entity
#Parent class for the three player characters
class PlayerCharacter(Entity):
    def __init__(self, inputName):
        self.startingStats = {
            "Level": 1,
            "HP": 5,
            "Power": 1,
            "Defense": 1,
            "Speed": 1,
            "Luck": 1
        }

        #Calling Entity.py __init__
        Entity.__init__(self, inputName, self.startingStats)

        self.ResetCharacter()

        #Default Action values for when no Actions are supplied
        self.defaultActionDescriptions = {
            "Name": "null",
            "Description": "This is a default action that has not been given any values. It does nothing",
            "Action Used": "You used the default null action, and nothing happens",
            "Action Success": "Congrats! You successfully did nothing",
            "Action Fail": "You failed at doing nothing, with the outcome of nothing happening. A strange paradox indeed"
        }

        #The character's two equipped actions
        self.equippedActions = [Action(1, self.defaultActionDescriptions, ["Front"], {}), Action(1, self.defaultActionDescriptions, ["Front"], {})]

    #Resets character to level 1, essentually creating a new default character
    def ResetCharacter(self):
        self.maxAP = 2
        self.currentAP = 2
        self.currentXP = 0
        self.XPToLevelUp = 100
        self.statPoints = 0
        self.skillPoints = 0

        self.level = self.startingStats["Level"]
        self.maxHP = self.startingStats["HP"]
        self.power = self.startingStats["Power"]
        self.defense = self.startingStats["Defense"]
        self.speed = self.startingStats["Speed"]
        self.luck = self.startingStats["Luck"]
        self.currentHP = self.maxHP
        self.down = False

    #Sets the equipped action to a new action, if it is provided
    #Action1 must be the first argument, and Action2 must be the second argument
    def SetActions(self, newAction1=None, newAction2=None):
        if newAction1:
            self.equippedActions[0] = newAction1
        if newAction2:
            self.equippedActions[1] = newAction2

    #Tries to spend a number of action points
    #Returns true if enough AP was available and was spent
    #Returns false if there was not enough AP to spend
    def SpendAP(self, spentPoints):
        if spentPoints > self.currentAP:
            return False
        else:
            self.currentAP -= spentPoints
            return True
        
    #Increases current action points up to the character's maximum
    def GainAP(self, pointsGained):
        self.currentAP += pointsGained
        if self.currentAP > self.maxAP:
            self.currentAP = self.maxAP
        
    #Resets character's action points to the maximum
    def ResetAP(self):
        self.currentAP = self.maxAP

    #Sets AP to an exact value, can't be more than character's maximum
    def SetCurrentAP(self, value):
        self.currentAP = value
        if self.currentAP > self.maxAP:
            self.currentAP = self.maxAP

    #Adds earned xp and checks if the character levels up
    def EarnXP(self, xpAmount):
        self.currentXP += xpAmount
        self.CheckForLevelUp()

    #Loops the LevelUp function until character can't level up anymore
    def CheckForLevelUp(self):
        while (self.currentXP >= self.XPToLevelUp):
            self.LevelUp()

    #Increases stats, gives stat and skill points, and resets xp
    def LevelUp(self):
        self.level += 1
        self.currentHP += 1
        self.maxHP += 1

        self.statPoints += 3
        self.skillPoints += 1

        self.currentXP -= self.XPToLevelUp

    #Only called by StatIncreaseWindow for spending stat points
    #Apply stat changes and reduce stat points by however many were spent
    def IncreaseStats(self, StatAdditionDictionary):
        self.maxHP += StatAdditionDictionary["MaxHP"]
        self.currentHP += StatAdditionDictionary["MaxHP"]
        self.power += StatAdditionDictionary["Power"]
        self.defense += StatAdditionDictionary["Defense"]
        self.speed += StatAdditionDictionary["Speed"]
        self.luck += StatAdditionDictionary["Luck"]
        for key in StatAdditionDictionary:
            self.statPoints -= StatAdditionDictionary[key]

    def GetMaxAP(self):
        return self.maxAP
    
    def GetCurrentAP(self):
        return self.currentAP
    
    def GetCurrentXP(self):
        return self.currentXP
    
    def GetXPToLevelUp(self):
        return self.XPToLevelUp

    def GetStatPoints(self):
        return self.statPoints
    
    def GetSkillPoints(self):
        return self.skillPoints
    
    def GetAction(self, index):
        return self.equippedActions[index]