#Stores all necessary info for an action taken by an entity
class Action:
    #Initializes Action's values and tags
    #Takes APCost int, dictionary of description strings, array with target positions, and dictionary of tags
    def __init__(self, apCost, stringsDictionary, targetArray, tagDictionary):
        self.APCost = apCost

        #Strings with descriptor text
        #Printed to the action log in battle
        #Example:
        #Name: "Fire Bolt"
        #Description: "A spell that shoots a small bolt of fire at the front of an enemy. Deals 1x fire damage"
        #Action Used: "A bolt of fire flies from Elijah's fingertip towards the Front of the Pyromancer"
        #Action Success: "The bolt bursts in a flurry of sparks and leaves a dark singe mark on its target"
        #Action Fail: "The bolt strikes the Pyromancer but seems to dissipate with no effect"
        self.ActionDescriptions = stringsDictionary

        #Which of the 4 directions can be targetted with this action
        #"Above", "Behind", "Front", "Under"
        self.targetPositions = targetArray

        #Tags that describe attributes of the action
        #Examples:
        #"Attack": 2 - Attacks twice
        #"DamageMultiplier": 1.5 - Multiplier for attack damage
        #"Spell": True - This action counts as a spell
        #"AOE": True - AOE hits all entities on the left/right side of the battle
        #"Effects": {"Barrier": 1} - Applies these effects to the target
        #"TurnEffects": {"Shielded": 1, "Haste": 1} - Applies these turn effects to the target
        self.tags = tagDictionary

    #Returns true if Action has the inputted tag, false if not
    #Also returns the value of the tag
    def HasTag(self, tagName):
        for tag in self.tags:
            if tag == tagName:
                return self.tags[tag]
        return False
    
    #Adds a new tag with name and value inputted
    def AddTag(self, name, value):
        self.tags[name] = value

    #Removes inputted effect from effect arrays
    def RemoveEffectTag(self, name):
        try:
            self.tags.pop(name)
        except:
            pass

    #Returns true if this action can target the inputted position, false otherwise
    def CanTargetPosition(self, position):
        for pos in self.targetPositions:
            if pos == position:
                return True
        return False
    
    def GetPositionArray(self):
        return self.targetPositions

    def GetName(self):
        return self.ActionDescriptions["Name"]
    
    def GetDescription(self):
        return self.ActionDescriptions["Description"]
    
    def GetAPCost(self):
        return self.APCost
    
    def GetDescriptionDictionary(self):
        return self.ActionDescriptions
    
    def GetTagValue(self, name):
        return self.tags[name]