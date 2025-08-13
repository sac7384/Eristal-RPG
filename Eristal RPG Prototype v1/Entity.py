#Parent class for all entities in combat
class Entity:
    def __init__(self, inputName, loadedStats):
        self.name = inputName
        self.level = loadedStats["Level"]
        self.maxHP = loadedStats["HP"]
        self.power = loadedStats["Power"]
        self.defense = loadedStats["Defense"]
        self.speed = loadedStats["Speed"]
        self.luck = loadedStats["Luck"]
        self.currentHP = self.maxHP
        self.down = False

        #Dictionaries that store all the effects that can be applied to an entity
        #Effects that reduce their value when procced
        self.procEffectTags = {}
        #Effects that last a certain number of turns
        #Are reduced by one at the start of turn
        self.turnEffectTags = {}

    #Increases hp based on input
    #Returns if the entity is up
    def Heal(self, healthRegained):
        self.currentHP += healthRegained
        if self.currentHP > self.maxHP:
            self.currentHP = self.maxHP
        if self.currentHP > 0:
            self.down = False
        return self.down

    #Reduces hp based on damage taken
    #Returns if the entity is down
    def TakeDamage(self, damageTaken):
        self.currentHP -= damageTaken
        if self.currentHP <= 0:
            self.down = True
        return self.down
    
    def IsDown(self):
        return self.down

    def GetName(self):
        return self.name
    
    def GetLevel(self):
        return self.level
    
    def GetCurrentHP(self):
        return self.currentHP

    def GetHP(self):
        return self.maxHP
    
    def GetPower(self):
        return self.power
    
    def GetDefense(self):
        return self.defense

    def GetSpeed(self):
        return self.speed
    
    def GetLuck(self):
        return self.luck
    
    def GetProcEffects(self):
        return self.procEffectTags
    
    def GetTurnEffects(self):
        return self.turnEffectTags
    
    #Returns true if entity has the inputted effect, false if not
    #Also returns the value of the effect
    def HasEffectTag(self, effectName):
        for effect in self.procEffectTags:
            if effect == effectName:
                return self.procEffectTags[effect]
        for effect in self.turnEffectTags:
            if effect == effectName:
                return self.turnEffectTags[effect]
        return False
    
    #Adds a new effect with name and value inputted
    #Adds the effect to the appropriate dictionary based on the inputted effectType
    def AddEffectTag(self, name, value, effectType):
        alreadyHasEffect = False
        if self.HasEffectTag(name):
            alreadyHasEffect = True
        if effectType == "Turn Effects":
            if alreadyHasEffect:
                self.turnEffectTags[name] += value
            else:
                self.turnEffectTags[name] = value
        elif effectType == "Proc Effects":
            if alreadyHasEffect:
                self.procEffectTags[name] += value
            else:
                self.procEffectTags[name] = value

    #Removes inputted effect from effect arrays
    #Returns the name of the effect
    def RemoveEffectTag(self, name):
        try:
            self.procEffectTags.pop(name)
            return name
        except:
            pass
        try:
            self.turnEffectTags.pop(name)
            return name
        except:
            pass

    #Removes all effect tags
    def ClearAllEffects(self):
        self.procEffectTags = {}
        self.turnEffectTags = {}

    #Reduces the value of in inputted effect
    #If that value reaches 0 the effect is removed
    #Returns the name of the effect if it is removed, false otherwise
    def DecreaseProcEffectValue(self, effectName, amountDecreased):
        try:
            self.procEffectTags[effectName]
        except:
            return False
        self.procEffectTags[effectName] -= amountDecreased
        if self.procEffectTags[effectName] <= 0:
            self.procEffectTags.pop(effectName)
            return effectName
        return False

    #All effects with a turn counter have their values reduced by 1
    #If one of those effects reaches 0 it is removed
    #Returns an array of the effects removed, or false if none were removed
    def TickAllTurnEffects(self):
        endedEffects = []
        for effect in self.turnEffectTags:
            self.turnEffectTags[effect] -= 1
            if self.turnEffectTags[effect] <= 0:
                endedEffects.append(effect)
        for i in endedEffects:
            self.turnEffectTags.pop(i)
        try:
            endedEffects[0]
        except:
            return False
        else:
            return endedEffects
    
    def PrintStats(self):
        levelString = str(self.name) + " Lv " + str(self.level)
        print(levelString)
        print(str(self.power))
        print(str(self.defense))
        print(str(self.speed))
        print(str(self.luck))