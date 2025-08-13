from Entity import Entity
from PyQt6.QtWidgets import *
from PyQt6 import uic
import random

#BattleWindow definition table of contents:
#to be finished at a later date

class BattleWindow:
    def __init__(self):
        self.defaultName = "Nothing"
        self.defaultStats = {
            "Level": 0,
            "HP": 1,
            "Power": 0,
            "Defense": 0,
            "Speed": 0,
            "Luck": 0
        }

        #Boolean that tells if the battle is continuing, becomes false once the battle is won/lost
        self.isBattleActive = False
        #Boolean that tells if the battle was won or lost
        self.battleWon = False
        #Boolean that tells if the end of the battle is being processed, makes sure EndBattle() is only called once
        self.battleOver = False
        #Turn meter = 10/50/100/500 (based on highest speed value, only for reducing calculations needed)
        self.turnMeter = 500
        #Stores the current speed value of each entity
        #Once an entity reaches the value of the turnMeter, it will get to act
        self.speedValueArray = [0, 0, 0, 0, 0, 0]
        #Index of the entity whose turn it is
        self.indexOfActiveEntity = 0
        #Holds the index of each entity who is up for a turn
        self.activeEntityIndexArray = []
        #Boolean that tells if there is any entity queued for a turn
        self.entitiesWaitingForTurn = 0
        #Boolean that tells if it is a player turn and the game is waiting for input
        self.playerTurnActive = False

        #Set string constants
        #Target positions
        self.ABOVE_STRING = "Above"
        self.BEHIND_STRING = "Behind"
        self.FRONT_STRING = "Front"
        self.UNDER_STRING = "Under"
        #Targeted buttons text
        self.TOP_BUTTON_STRING = "v"
        self.RIGHT_BUTTON_STRING = "<"
        self.LEFT_BUTTON_STRING = ">"
        self.BOTTOM_BUTTON_STRING = "^"

        defaultEntity = Entity(self.defaultName, self.defaultStats)
        self.battleEntityArray = [defaultEntity, defaultEntity, defaultEntity, defaultEntity, defaultEntity, defaultEntity]
        self.playerChosenTarget = 3
        self.playerChosenPosition = self.FRONT_STRING
        self.playerChosenCharacterIndex = 0
        self.playerChosenActionIndex = 0

    #Takes a string and prints it onto the battle's action log
    def log(self, logMessage):
        battleForm.ActionLog.addItem(logMessage)
        battleForm.ActionLog.scrollToBottom()

    #Handles when tags are decreased on an entity
    #Decreases a proc tag or ticks all turn tags
    #Logs if any tags are removed
    def HandleTagDecrease(self, entity, tagName, amountDecreased):
        removedEffects = []
        #For ticking down all turn effects
        if tagName == "Turn Effects":
            removedEffects = entity.TickAllTurnEffects()
        #For completely removing an effect
        elif amountDecreased == "All":
            removedEffect = entity.RemoveEffectTag(tagName)
            if removedEffect:
                removedEffects.append(removedEffect)
        #For decreasing proc effects
        else:
            removedEffect = entity.DecreaseProcEffectValue(tagName, amountDecreased)
            if removedEffect:
                removedEffects.append(removedEffect)

        #Log all effects removed
        if removedEffects:
            for removedEffect in removedEffects:
                removedString = entity.GetName() + " lost the " + removedEffect + " effect"
                self.log(removedString)

    #Calls for the battle window to be shown
    #Starts the battle sequence
    def StartBattle(self, entityList):
        for i in range(6):
            self.battleEntityArray[i] = entityList[i]
            self.battleEntityArray[i].ClearAllEffects()

        #Initialize enemy health bars
        healthBars = [battleForm.Enemy1HealthBar, battleForm.Enemy2HealthBar, battleForm.Enemy3HealthBar]
        for i in range(3):
            characterHP = self.battleEntityArray[i + 3].GetHP()
            healthBars[i].setMaximum(characterHP)
            healthBars[i].setMinimum(0)

        #Set Enemy1 Front as the default target
        self.on_Enemy1TargetFront_clicked()
        self.ShowWindow()

        #Getting the battle started
        #Change the turnMeter max value based on the highest speed stat present in this battle
        #turnMeter needs to be higher than the highest speed stat, but a smaller value reduces the number of battle loops needed
        #Possible turnMeter values = 10/50/100/500
        highestSpeed = 0
        for entity in self.battleEntityArray:
            if entity.GetSpeed() > highestSpeed:
                highestSpeed = entity.GetSpeed()
        if (highestSpeed < 10):
            self.turnMeter = 10
        elif (highestSpeed > 10 and highestSpeed < 50):
            self.turnMeter = 50
        elif (highestSpeed > 50 and highestSpeed < 100):
            self.turnMeter = 100
        else:
            self.turnMeter = 500

        #Set other turn order and battle state variables to default
        self.isBattleActive = True
        self.battleOver = False
        self.speedValueArray = [0, 0, 0, 0, 0, 0]
        self.activeEntityIndexArray = []
        self.entitiesWaitingForTurn = False

        #Start the battle loop
        self.BattleLoop()

    #Handles ending the battle
    #Clears any temporary changes
    #Gives rewards to player if the battle is won
    #Closes battle window once everything is resolved
    def EndBattle(self):
        #Uses flag to make sure EndBattle is only called once
        if self.battleOver:
            return
        self.battleOver = True

        #Creates end of battle victory/defeat message
        #Also rewards xp if the battle was won
        alert = QMessageBox()
        RoseXP = 0
        OzXP = 0
        EliXP = 0
        if self.battleWon:
            RoseXP = self.CalculateEarnedXP(0)
            OzXP = self.CalculateEarnedXP(1)
            EliXP = self.CalculateEarnedXP(2)
            self.battleEntityArray[0].EarnXP(RoseXP)
            self.battleEntityArray[1].EarnXP(OzXP)
            self.battleEntityArray[2].EarnXP(EliXP)
            alert.setText('You won the battle!\n'
                          'Rose gained '+str(RoseXP)+' XP!\n'
                          'Oswald gained '+str(OzXP)+' XP!\n'
                          'Elijah gained '+str(EliXP)+' XP!')
        else:
            alert.setText('You lost the battle')
        gameWindow.BattleOver()
        gameWindow.UpdateUIElements()
        alert.exec()
        battleWindow.hide()

    #Calculates how much xp a character gets from the enemies defeated

    #levelDifference = enemyLevel - playerLevel
    #enemyXP * (1 + (levelDifference / 10))
    #Each difference in level modifies xp by 10%
    #levelDifference is positive if the enemy is a higher level
    def CalculateEarnedXP(self, characterIndex):
        xpEarned = 0
        character = self.battleEntityArray[characterIndex]
        #Adds appropriate xp for each enemy
        #XP modified by 10% per level difference with enemy
        #Enemy higher level means more xp granted
        for i in range(3, 6):
            enemy = self.battleEntityArray[i]
            levelDifference = enemy.GetLevel() - character.GetLevel()
            xpEarned += enemy.GetXPGiven() * (1 + (levelDifference / 10))
        xpEarned = int(xpEarned)
        return xpEarned

    #Counts up each entity's speed
    #Entity gets a turn if its speed value reaches the turnMeter
    #Loops until it is an entity's turn
    def CountSpeedTicks(self):
        while not self.entitiesWaitingForTurn:
            for i in range(6):
                currentEntity = self.battleEntityArray[i]
                #Don't increase speed if the entity is down
                if currentEntity.IsDown():
                    continue
                #"Frozen", entity does not get their next speed tick
                if currentEntity.HasEffectTag("Frozen"):
                    self.HandleTagDecrease(currentEntity, "Frozen", 1)
                    continue
                #"Haste", speed ticks a second time
                if currentEntity.HasEffectTag("Haste"):
                    self.speedValueArray[i] += currentEntity.GetSpeed()

                #Tick up an entity's turn meter value by their speed
                self.speedValueArray[i] += currentEntity.GetSpeed()
                if self.speedValueArray[i] >= self.turnMeter:
                    self.speedValueArray[i] -= self.turnMeter
                    self.activeEntityIndexArray.append(i)
                    self.entitiesWaitingForTurn += 1

    #Returns the index of the entity that should go next
    #Turn ties are broken based on highest turn meter value, and then highest speed stat, if both are the same then broken based on battle position (top/left entities go first, or lowest index in battleEntityArray goes first)
    def FindActiveEntity(self):
        #If more than one entity waiting, figure out which goes first
        if self.entitiesWaitingForTurn > 1:
            methodTie = False
            highestTurnMeter = -1
            highestSpeed = -1
            lowestIndex = 10
            self.indexOfActiveEntity = 10
            #Try to find the highest value on the turn meter
            for i in self.activeEntityIndexArray:
                if self.speedValueArray[i] > highestTurnMeter:
                    highestTurnMeter = self.speedValueArray[i]
                    self.indexOfActiveEntity = i
                elif self.speedValueArray[i] == highestTurnMeter:
                    methodTie = True
            #If there is a tie, try highest speed stat
            if methodTie:
                methodTie = False
                for i in self.activeEntityIndexArray:
                    if self.battleEntityArray[i].GetSpeed() > highestSpeed:
                        highestSpeed = self.battleEntityArray[i].GetSpeed()
                        self.indexOfActiveEntity = i
                    elif self.battleEntityArray[i].GetSpeed() == highestSpeed:
                        methodTie = True
                #If there is a tie, determine based off battle position
                if methodTie:
                    methodTie = False
                    for i in self.activeEntityIndexArray:
                        if i < lowestIndex:
                            lowestIndex = i
                    self.indexOfActiveEntity = lowestIndex
            #Removes entity from waiting array that is about to get a turn
            for i in range(len(self.activeEntityIndexArray)):
                    if self.activeEntityIndexArray[i] == self.indexOfActiveEntity:
                        self.activeEntityIndexArray.pop(i)
                        break
        #Only one entity is waiting for a turn
        else:
            self.indexOfActiveEntity = self.activeEntityIndexArray[0]
            self.activeEntityIndexArray.pop(0)
        return self.indexOfActiveEntity
    
    #Checks for conditions that would end the battle
    def CheckForBattleEnd(self):
        #Checks if the battle has ended by either side (left/right) being all defeated
        if (self.battleEntityArray[0].IsDown() and self.battleEntityArray[1].IsDown() and self.battleEntityArray[2].IsDown()):
            self.isBattleActive = False
            self.battleWon = False
        if (self.battleEntityArray[3].IsDown() and self.battleEntityArray[4].IsDown() and self.battleEntityArray[5].IsDown()):
            self.isBattleActive = False
            self.battleWon = True

    #Main battle loop
    #Handles participants turns based on their speed
    #Turn meter = 10/50/100/500 (based on highest speed value, only for reducing calculations needed)
    #Each tick each entity's speed is added, once it reaches the turn meter it takes a turn
    #Turn ties are broken based on highest turn meter value, and then highest speed stat, if both are the same then broken based on battle position (top/left entities go first, or lowest index in battleEntityArray goes first)
    #Called after any entity takes an action, and when the battle first begins
    def BattleLoop(self):
        #Loop continues while battle is still active, ends if all entities on left/right side are defeated
        if self.isBattleActive:
            #If no entities waiting for turn, count speed ticks until a turn is ready
            if not self.entitiesWaitingForTurn:
                self.CountSpeedTicks()

            if self.entitiesWaitingForTurn:
                #Determine entity who is taking a turn
                #Break turn ties if necessary
                #Removes that entity from the waiting array
                self.FindActiveEntity()
                #Give waiting entity a turn
                self.entitiesWaitingForTurn -= 1
                self.GiveTurn()

            self.CheckForBattleEnd()

        #Ends battle if it is no longer active
        if not self.isBattleActive:
            self.EndBattle()

    #Either give player character or enemy a turn based on the provided index
    def GiveTurn(self):
        activeEntity = self.battleEntityArray[self.indexOfActiveEntity]

        if not activeEntity.IsDown():
            #Start of turn message
            characterTurnString = "\n***It is " + activeEntity.GetName() + "'s turn!***"
            self.log(characterTurnString)
            #Ticks down on turn effects
            self.HandleTagDecrease(activeEntity, "Turn Effects", 1)
            #Calls for a player/enemy turn based on the entity
            if self.indexOfActiveEntity < 3:
                self.GivePlayerTurn()
            else:
                self.GiveEnemyTurn()
        else:
            self.BattleLoop()

    #Gives player character all start of turn bonuses
    #Sets the active character, allowing action buttons to be used by the player
    def GivePlayerTurn(self):
        #Tells the game that it is the players turn
        #Allows player skill buttons to execute their actions
        activeCharacter = self.battleEntityArray[self.indexOfActiveEntity]
        activeCharacter.ResetAP()
        gameWindow.UpdateUIElements()
        self.playerTurnActive = True

    #Executes all enemy actions on its turn
    #Then continues the battle loop
    def GiveEnemyTurn(self):
        activeEntity = self.battleEntityArray[self.indexOfActiveEntity]
        targetIndex = activeEntity.GetTargetIndex()
        target = self.battleEntityArray[targetIndex]
        action = activeEntity.GetIntentAction()

        #Temporarily changes the chosen position for the enemy's action(s)
        previousPosition = self.playerChosenPosition
        self.playerChosenPosition = activeEntity.GetTargetPosition()
        
        #Execute enemy's chosen action on the chosen target
        self.TakeAction(activeEntity, target, action)

        #Enemy chooses a new action and target
        activeEntity.ChooseNewAction()
        activeEntity.ChooseNewTarget()

        #Forces enemy to choose a new target if the chosen one is not viable
        newAction = activeEntity.GetIntentAction()
        newTarget = self.battleEntityArray[activeEntity.GetTargetIndex()]
        #If the enemy's action is aimed at a downed character and not a healing ability, choose target again
        while newTarget.IsDown() and not newAction.HasTag("Heal"):
            activeEntity.ChooseNewTarget()
            newAction = activeEntity.GetIntentAction()
            newTarget = self.battleEntityArray[activeEntity.GetTargetIndex()]

        #Resets chosen position to where the player had it
        self.playerChosenPosition = previousPosition

        #Continues the battle loop
        #Allows next entity to take a turn
        self.BattleLoop()

    #Executes the active entity's action on the chosen target
    #Calls other methods for some specific actions, ie Attack()
    def TakeAction(self, ActiveEntity, Target, Action):
        #Message strings that describe the action being taken
        #Variables within the string are filled with info from the battle entities
        #{ActionUserName} is from ActiveEntity
        #{TargetName} is from Target
        #{value} is from Action
        actionDescriptors = Action.GetDescriptionDictionary()

        #Check that the chosen action can target the chosen position
        #Return False if the action and position chosen are incompatible
        if not Action.CanTargetPosition(self.playerChosenPosition):
            return False

        #"Self" actions always target self
        if Action.HasTag("Self"):
            Target = ActiveEntity

        #Log that the action is trying to be used
        actionUsedMessage = actionDescriptors["Action Used"]
        if actionUsedMessage:
            actionUsedMessage = actionUsedMessage.format(ActionUserName=ActiveEntity.GetName(), TargetName=Target.GetName())
            self.log(actionUsedMessage)

        #"Attack" Actions
        numberOfAttacks = Action.HasTag("Attack")
        if numberOfAttacks:
            #Executes all of the action's attacks
            for i in range(numberOfAttacks):
                self.Attack(ActiveEntity, Target, Action)
            #Extra "Rally" attacks
            rallyAttacks = ActiveEntity.HasEffectTag("Rally")
            if rallyAttacks:
                rallyString = ActiveEntity.GetName()+" is Rallied and attacks more!"
                self.log(rallyString)
                for i in range(rallyAttacks):
                    self.Attack(ActiveEntity, Target, Action)
                #"Rally" is removed after one attack action
                self.HandleTagDecrease(ActiveEntity, "Rally", "All")
        #"Heal" Actions
        numberOfHeals = Action.HasTag("Heal")
        if numberOfHeals:
            #Executes all of the action's heals
            for i in range(numberOfHeals):
                self.Heal(ActiveEntity, Target, Action)
        #"Effect" Actions
        if Action.HasTag("Proc Effects") or Action.HasTag("Turn Effects"):
            #Applies all the action's effects
            self.ApplyEffects(ActiveEntity, Target, Action)

        gameWindow.UpdateUIElements()
        return True

    #Executes an attack action
    #Attacker is the entity instigating the attack
    #Target is the entity taking the attack
    #Action is the specific attack being executed
    #Every attack action has these tags: Attack, Power Multiplier, Crit Chance Multiplier, Crit Damage Multiplier
    def Attack(self, Attacker, Target, Action):
        #Message strings that describe the action being taken
        #Variables within the string are filled with info from the battle entities
        #{ActionUserName} is from Attacker
        #{TargetName} is from Target
        #{value} is from Action
        actionDescriptors = Action.GetDescriptionDictionary()

        actionDamage = Attacker.GetPower() * Action.GetTagValue("Power Multiplier")
        targetDefense = Target.GetDefense()

        #Roll for a crit
        #The range of randomRoll is the sum of both luck stats, and a crit buffer based on both entities' levels
        #critBuffer pads the range a bit and scales with entities' level, bringing the crit chance down some
        #the buffer keeps entities from having high crit chances like 50% when faced with an enemy of equal luck value and level
        critBuffer = 3 * (Target.GetLevel() + Attacker.GetLevel())
        attackerLuck = Attacker.GetLuck() * Action.GetTagValue("Crit Chance Multiplier")
        targetLuck = Target.GetLuck()
        rollRange = int(attackerLuck + targetLuck + critBuffer)

        #Make sure critical roll range is not less than 1
        if rollRange < 1:
            rollRange = 1

        #Determine if the attack crits
        randomRoll = random.randrange(rollRange)
        if randomRoll < attackerLuck:
            attackCrit = True
        else:
            attackCrit = False

        #"Slimed", an Attacker who is slimed cannot crit
        if Attacker.HasEffectTag("Slimed"):
            attackCrit = False

        #Calculate crit damage
        if attackCrit:
            actionDamage *= Action.GetTagValue("Crit Damage Multiplier")

        finalDamage = actionDamage - targetDefense
        #Damage can't be less than 0
        if finalDamage < 0:
            finalDamage = 0

        #"Shielded", halves the damage a Target is taking
        if Target.HasEffectTag("Shielded"):
            finalDamage *= 0.5
            #Effect feedback
            shieldedString = Target.GetName() + " took half damage because of their shield"
            self.log(shieldedString)

        #Makes sure finalDamage is an integer after all modifications
        finalDamage = int(finalDamage)

        #"Barrier", negates next attack's damage (will not consume barrier if damage is already 0)
        if Target.HasEffectTag("Barrier") and finalDamage > 0:
            finalDamage = 0
            #Effect feedback
            barrierString = Target.GetName() + "'s Barrier consumed the attack"
            self.log(barrierString)
            #Reduces effect
            self.HandleTagDecrease(Target, "Barrier", 1)

        targetAliveBeforeAttack = not Target.IsDown()
        targetIsDead = Target.TakeDamage(finalDamage)

        #Add attack feedback
        attackResult = actionDescriptors["Action Success"]
        attackResult = attackResult.format(ActionUserName=Attacker.GetName(), TargetName=Target.GetName(), value=finalDamage)
        self.log(attackResult)
        if attackCrit:
            critString = "A critical hit! The attack was much more effective!"
            self.log(critString)
        if targetAliveBeforeAttack and targetIsDead:
            self.log(Target.GetName() + " is now down!")

    #Executes a heal action
    #ActionUser is the entity instigating the heal
    #Target is the entity taking the heal
    #Action is the specific heal being executed
    #Every heal action has these tags: Heal, Power Multiplier
    def Heal(self, ActionUser, Target, Action):
        #Message strings that describe the action being taken
        #Variables within the string are filled with info from the battle entities
        #{ActionUserName} is from ActionUser
        #{TargetName} is from Target
        #{value} is from Action
        actionDescriptors = Action.GetDescriptionDictionary()

        actionHealing = ActionUser.GetPower() * Action.GetTagValue("Power Multiplier")

        #for future effects or abilities that modify healing

        finalHealing = actionHealing
        #Healing can't be less than 0
        if finalHealing < 0:
            finalHealing = 0
        targetDownBeforeAttack = Target.IsDown()
        targetIsAlive = Target.Heal(finalHealing)

        #Add heal feedback
        healResult = actionDescriptors["Action Success"]
        healResult = healResult.format(ActionUserName=ActionUser.GetName(), TargetName=Target.GetName(), value=finalHealing)
        self.log(healResult)
        if targetDownBeforeAttack and targetIsAlive:
            self.log(Target.GetName() + " is now up!")

    #Applies effects from an action
    #ActionUser is the entity instigating
    #Target is the entity taking the effects
    #Action is the specific action being executed
    #Every effects action has these tags: "Effects": {dictionary of effect tags}
    def ApplyEffects(self, ActionUser, Target, Action):
        #Message strings that describe the action being taken
        #Variables within the string are filled with info from the battle entities
        #{ActionUserName} is from ActionUser
        #{TargetName} is from Target
        #{value} is from Action
        actionDescriptors = Action.GetDescriptionDictionary()

        #Apply effect tags one by one
        typesOfEffects = ["Proc Effects", "Turn Effects"]
        for typeString in typesOfEffects:
            effectList = Action.HasTag(typeString)
            #Continues to next effect list if the current one is empty
            if not effectList:
                continue
            for effect in effectList:
                effectValue = effectList[effect]
                Target.AddEffectTag(effect, effectValue, typeString)

        #Log effect feedback
        effectResult = actionDescriptors["Effect Success"]
        effectResult = effectResult.format(ActionUserName=ActionUser.GetName(), TargetName=Target.GetName(), value=effectValue)
        self.log(effectResult)

    #Attempts to use the skill/item/action selected by the player
    #Is called by the character item buttons
    #Returns whether the action was successfully executed
    def UseCharacterSkill(self):
        #If not a player character's turn, don't execute their action
        if not self.playerTurnActive:
            return False

        #If correct character not selected then don't give a turn
        if self.playerChosenCharacterIndex != self.indexOfActiveEntity:
            self.log("It is not that character's turn!")
            return False

        activeCharacter = self.battleEntityArray[self.playerChosenCharacterIndex]
        targettedEntity = self.battleEntityArray[self.playerChosenTarget]
        action = activeCharacter.GetAction(self.playerChosenActionIndex)
        actionAPCost = action.GetAPCost()
        #Executes the players action and reduces their AP
        if activeCharacter.SpendAP(actionAPCost):
            #Try to take the action
            #If the action can't go through (ie action can't target the chosen position), then return their AP
            if not self.TakeAction(activeCharacter, targettedEntity, action):
                activeCharacter.GainAP(actionAPCost)
        else:
            self.log("You don't have enough AP for that!")
            return False
        
        #Checks if the battle has ended
        #Important for if it ends in the middle of a player turn
        self.CheckForBattleEnd()
        if not self.isBattleActive:
            activeCharacter.SetCurrentAP(0)
        
        #Once a character runs out of AP it is no longer their turn, and the battle loop continues
        if activeCharacter.GetCurrentAP() < 1:
            self.playerTurnActive = False
            self.BattleLoop()

    #Characters' item buttons
    #Sets chosen character and item slot
    #The battle loop is woken to try and execute a player action
    def on_RoseItem1_clicked(self):
        self.playerChosenCharacterIndex = 0
        self.playerChosenActionIndex = 0
        self.UseCharacterSkill()

    def on_RoseItem2_clicked(self):
        self.playerChosenCharacterIndex = 0
        self.playerChosenActionIndex = 1
        self.UseCharacterSkill()

    def on_OzItem1_clicked(self):
        self.playerChosenCharacterIndex = 1
        self.playerChosenActionIndex = 0
        self.UseCharacterSkill()

    def on_OzItem2_clicked(self):
        self.playerChosenCharacterIndex = 1
        self.playerChosenActionIndex = 1
        self.UseCharacterSkill()

    def on_EliItem1_clicked(self):
        self.playerChosenCharacterIndex = 2
        self.playerChosenActionIndex = 0
        self.UseCharacterSkill()

    def on_EliItem2_clicked(self):
        self.playerChosenCharacterIndex = 2
        self.playerChosenActionIndex = 1
        self.UseCharacterSkill()

    #Target buttons
    #Switches the active target to the entity and/or position that is clicked on
    #
    #Rose / Entity 0
    #
    def on_RoseTargetAbove_clicked(self):
        self.playerChosenTarget = 0
        self.playerChosenPosition = self.ABOVE_STRING
        self.ClearTargetButtonsText()
        battleForm.RoseTargetAbove.setText(self.TOP_BUTTON_STRING)

    def on_RoseTargetBehind_clicked(self):
        self.playerChosenTarget = 0
        self.playerChosenPosition = self.BEHIND_STRING
        self.ClearTargetButtonsText()
        battleForm.RoseTargetBehind.setText(self.LEFT_BUTTON_STRING)

    def on_RoseTargetFront_clicked(self):
        self.playerChosenTarget = 0
        self.playerChosenPosition = self.FRONT_STRING
        self.ClearTargetButtonsText()
        battleForm.RoseTargetFront.setText(self.RIGHT_BUTTON_STRING)

    def on_RoseTargetUnder_clicked(self):
        self.playerChosenTarget = 0
        self.playerChosenPosition = self.UNDER_STRING
        self.ClearTargetButtonsText()
        battleForm.RoseTargetUnder.setText(self.BOTTOM_BUTTON_STRING)

    #
    #Oz / Entity 1
    #
    def on_OzTargetAbove_clicked(self):
        self.playerChosenTarget = 1
        self.playerChosenPosition = self.ABOVE_STRING
        self.ClearTargetButtonsText()
        battleForm.OzTargetAbove.setText(self.TOP_BUTTON_STRING)

    def on_OzTargetBehind_clicked(self):
        self.playerChosenTarget = 1
        self.playerChosenPosition = self.BEHIND_STRING
        self.ClearTargetButtonsText()
        battleForm.OzTargetBehind.setText(self.LEFT_BUTTON_STRING)

    def on_OzTargetFront_clicked(self):
        self.playerChosenTarget = 1
        self.playerChosenPosition = self.FRONT_STRING
        self.ClearTargetButtonsText()
        battleForm.OzTargetFront.setText(self.RIGHT_BUTTON_STRING)

    def on_OzTargetUnder_clicked(self):
        self.playerChosenTarget = 1
        self.playerChosenPosition = self.UNDER_STRING
        self.ClearTargetButtonsText()
        battleForm.OzTargetUnder.setText(self.BOTTOM_BUTTON_STRING)

    #
    #Eli / Entity 2
    #
    def on_EliTargetAbove_clicked(self):
        self.playerChosenTarget = 2
        self.playerChosenPosition = self.ABOVE_STRING
        self.ClearTargetButtonsText()
        battleForm.EliTargetAbove.setText(self.TOP_BUTTON_STRING)

    def on_EliTargetBehind_clicked(self):
        self.playerChosenTarget = 2
        self.playerChosenPosition = self.BEHIND_STRING
        self.ClearTargetButtonsText()
        battleForm.EliTargetBehind.setText(self.LEFT_BUTTON_STRING)

    def on_EliTargetFront_clicked(self):
        self.playerChosenTarget = 2
        self.playerChosenPosition = self.FRONT_STRING
        self.ClearTargetButtonsText()
        battleForm.EliTargetFront.setText(self.RIGHT_BUTTON_STRING)

    def on_EliTargetUnder_clicked(self):
        self.playerChosenTarget = 2
        self.playerChosenPosition = self.UNDER_STRING
        self.ClearTargetButtonsText()
        battleForm.EliTargetUnder.setText(self.BOTTOM_BUTTON_STRING)

    #
    #Enemy1 / Entity 3
    #
    def on_Enemy1TargetAbove_clicked(self):
        self.playerChosenTarget = 3
        self.playerChosenPosition = self.ABOVE_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy1TargetAbove.setText(self.TOP_BUTTON_STRING)

    def on_Enemy1TargetBehind_clicked(self):
        self.playerChosenTarget = 3
        self.playerChosenPosition = self.BEHIND_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy1TargetBehind.setText(self.RIGHT_BUTTON_STRING)

    def on_Enemy1TargetFront_clicked(self):
        self.playerChosenTarget = 3
        self.playerChosenPosition = self.FRONT_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy1TargetFront.setText(self.LEFT_BUTTON_STRING)

    def on_Enemy1TargetUnder_clicked(self):
        self.playerChosenTarget = 3
        self.playerChosenPosition = self.UNDER_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy1TargetUnder.setText(self.BOTTOM_BUTTON_STRING)

    #
    #Enemy2 / Entity 4
    #
    def on_Enemy2TargetAbove_clicked(self):
        self.playerChosenTarget = 4
        self.playerChosenPosition = self.ABOVE_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy2TargetAbove.setText(self.TOP_BUTTON_STRING)

    def on_Enemy2TargetBehind_clicked(self):
        self.playerChosenTarget = 4
        self.playerChosenPosition = self.BEHIND_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy2TargetBehind.setText(self.RIGHT_BUTTON_STRING)

    def on_Enemy2TargetFront_clicked(self):
        self.playerChosenTarget = 4
        self.playerChosenPosition = self.FRONT_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy2TargetFront.setText(self.LEFT_BUTTON_STRING)

    def on_Enemy2TargetUnder_clicked(self):
        self.playerChosenTarget = 4
        self.playerChosenPosition = self.UNDER_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy2TargetUnder.setText(self.BOTTOM_BUTTON_STRING)

    #
    #Enemy3 / Entity 5
    #
    def on_Enemy3TargetAbove_clicked(self):
        self.playerChosenTarget = 5
        self.playerChosenPosition = self.ABOVE_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy3TargetAbove.setText(self.TOP_BUTTON_STRING)

    def on_Enemy3TargetBehind_clicked(self):
        self.playerChosenTarget = 5
        self.playerChosenPosition = self.BEHIND_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy3TargetBehind.setText(self.RIGHT_BUTTON_STRING)

    def on_Enemy3TargetFront_clicked(self):
        self.playerChosenTarget = 5
        self.playerChosenPosition = self.FRONT_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy3TargetFront.setText(self.LEFT_BUTTON_STRING)

    def on_Enemy3TargetUnder_clicked(self):
        self.playerChosenTarget = 5
        self.playerChosenPosition = self.UNDER_STRING
        self.ClearTargetButtonsText()
        battleForm.Enemy3TargetUnder.setText(self.BOTTOM_BUTTON_STRING)

    #Initialize battle window creation
    def LoadWindow(self, GameWindowObject):
        global gameWindow
        gameWindow = GameWindowObject
        global battleForm
        global battleWindow
        BForm, BWindow = uic.loadUiType("BattleWindow.ui")
        battleWindow = BWindow()
        battleForm = BForm()
        battleForm.setupUi(battleWindow)

        #Connect all of the item/action buttons
        battleForm.RoseItem1.clicked.connect(self.on_RoseItem1_clicked)
        battleForm.RoseItem2.clicked.connect(self.on_RoseItem2_clicked)
        battleForm.OzItem1.clicked.connect(self.on_OzItem1_clicked)
        battleForm.OzItem2.clicked.connect(self.on_OzItem2_clicked)
        battleForm.EliItem1.clicked.connect(self.on_EliItem1_clicked)
        battleForm.EliItem2.clicked.connect(self.on_EliItem2_clicked)
        
        #Connect all of the many target buttons
        #Left 3 entities
        battleForm.RoseTargetAbove.clicked.connect(self.on_RoseTargetAbove_clicked)
        battleForm.RoseTargetBehind.clicked.connect(self.on_RoseTargetBehind_clicked)
        battleForm.RoseTargetFront.clicked.connect(self.on_RoseTargetFront_clicked)
        battleForm.RoseTargetUnder.clicked.connect(self.on_RoseTargetUnder_clicked)
        battleForm.OzTargetAbove.clicked.connect(self.on_OzTargetAbove_clicked)
        battleForm.OzTargetBehind.clicked.connect(self.on_OzTargetBehind_clicked)
        battleForm.OzTargetFront.clicked.connect(self.on_OzTargetFront_clicked)
        battleForm.OzTargetUnder.clicked.connect(self.on_OzTargetUnder_clicked)
        battleForm.EliTargetAbove.clicked.connect(self.on_EliTargetAbove_clicked)
        battleForm.EliTargetBehind.clicked.connect(self.on_EliTargetBehind_clicked)
        battleForm.EliTargetFront.clicked.connect(self.on_EliTargetFront_clicked)
        battleForm.EliTargetUnder.clicked.connect(self.on_EliTargetUnder_clicked)
        #Right 3 entities
        battleForm.Enemy1TargetAbove.clicked.connect(self.on_Enemy1TargetAbove_clicked)
        battleForm.Enemy1TargetBehind.clicked.connect(self.on_Enemy1TargetBehind_clicked)
        battleForm.Enemy1TargetFront.clicked.connect(self.on_Enemy1TargetFront_clicked)
        battleForm.Enemy1TargetUnder.clicked.connect(self.on_Enemy1TargetUnder_clicked)
        battleForm.Enemy2TargetAbove.clicked.connect(self.on_Enemy2TargetAbove_clicked)
        battleForm.Enemy2TargetBehind.clicked.connect(self.on_Enemy2TargetBehind_clicked)
        battleForm.Enemy2TargetFront.clicked.connect(self.on_Enemy2TargetFront_clicked)
        battleForm.Enemy2TargetUnder.clicked.connect(self.on_Enemy2TargetUnder_clicked)
        battleForm.Enemy3TargetAbove.clicked.connect(self.on_Enemy3TargetAbove_clicked)
        battleForm.Enemy3TargetBehind.clicked.connect(self.on_Enemy3TargetBehind_clicked)
        battleForm.Enemy3TargetFront.clicked.connect(self.on_Enemy3TargetFront_clicked)
        battleForm.Enemy3TargetUnder.clicked.connect(self.on_Enemy3TargetUnder_clicked)

        windowsLoaded = 1
        return windowsLoaded
    
    def ShowWindow(self):
        battleForm.ActionLog.clear()
        self.ClearTargetButtonsText()
        gameWindow.UpdateUIElements()
        battleWindow.show()
        self.isBattleActive = True

    def ClearTargetButtonsText(self):
        #Left 3 entities
        battleForm.RoseTargetAbove.setText("")
        battleForm.RoseTargetBehind.setText("")
        battleForm.RoseTargetFront.setText("")
        battleForm.RoseTargetUnder.setText("")
        battleForm.OzTargetAbove.setText("")
        battleForm.OzTargetBehind.setText("")
        battleForm.OzTargetFront.setText("")
        battleForm.OzTargetUnder.setText("")
        battleForm.EliTargetAbove.setText("")
        battleForm.EliTargetBehind.setText("")
        battleForm.EliTargetFront.setText("")
        battleForm.EliTargetUnder.setText("")
        #Right 3 entities
        battleForm.Enemy1TargetAbove.setText("")
        battleForm.Enemy1TargetBehind.setText("")
        battleForm.Enemy1TargetFront.setText("")
        battleForm.Enemy1TargetUnder.setText("")
        battleForm.Enemy2TargetAbove.setText("")
        battleForm.Enemy2TargetBehind.setText("")
        battleForm.Enemy2TargetFront.setText("")
        battleForm.Enemy2TargetUnder.setText("")
        battleForm.Enemy3TargetAbove.setText("")
        battleForm.Enemy3TargetBehind.setText("")
        battleForm.Enemy3TargetFront.setText("")
        battleForm.Enemy3TargetUnder.setText("")
    
    #Updates battle window UI, including characters and enemies
    def UpdateUIElements(self):
        #Returns early if certain entities don't have necessary values yet
        for i in range(3):
            try:
                self.battleEntityArray[i].GetMaxAP()
            except:
                return False
            
        #Arrays for entities and their corresponding text labels in the UI
        nameGroupBoxes = [battleForm.Rose, battleForm.Oz, battleForm.Eli, battleForm.Enemy1, battleForm.Enemy2, battleForm.Enemy3]
        hpLabels = [battleForm.RoseHP, battleForm.OzHP, battleForm.EliHP]
        apLabels = [battleForm.RoseAP, battleForm.OzAP, battleForm.EliAP]
        action1Buttons = [battleForm.RoseItem1, battleForm.OzItem1, battleForm.EliItem1]
        action2Buttons = [battleForm.RoseItem2, battleForm.OzItem2, battleForm.EliItem2]
        actionArray = [action1Buttons, action2Buttons]
        healthBars = [battleForm.Enemy1HealthBar, battleForm.Enemy2HealthBar, battleForm.Enemy3HealthBar]
        enemyIntents = [battleForm.Enemy1Intent, battleForm.Enemy2Intent, battleForm.Enemy3Intent]
        intentTargets = [battleForm.Enemy1IntentTarget, battleForm.Enemy2IntentTarget, battleForm.Enemy3IntentTarget]

        #Update all group box titles with character names
        for entityIndex in range(len(self.battleEntityArray)):
            characterName = self.battleEntityArray[entityIndex].GetName()
            if self.battleEntityArray[entityIndex].IsDown():
                characterName += " (Down)"
            nameGroupBoxes[entityIndex].setTitle(characterName)

        #Update player characters' (entities 0-2) UI
        for characterIndex in range(3):
            #update HP
            characterMaxHP = self.battleEntityArray[characterIndex].GetHP()
            characterCurrentHP = self.battleEntityArray[characterIndex].GetCurrentHP()
            HPString = "HP: " + str(characterCurrentHP) + "/" + str(characterMaxHP)
            hpLabels[characterIndex].setText(HPString)

            #update AP
            characterMaxAP = self.battleEntityArray[characterIndex].GetMaxAP()
            characterCurrentAP = self.battleEntityArray[characterIndex].GetCurrentAP()
            APString = "AP: " + str(characterCurrentAP) + "/" + str(characterMaxAP)
            apLabels[characterIndex].setText(APString)

            #update Action buttons, text and tooltip
            for actionIndex in range(2):
                ActionName = self.battleEntityArray[characterIndex].GetAction(actionIndex).GetName()
                ActionDescription = self.battleEntityArray[characterIndex].GetAction(actionIndex).GetDescription()
                actionArray[actionIndex][characterIndex].setText(ActionName)
                actionArray[actionIndex][characterIndex].setToolTip(ActionDescription)

        #Update enemies' (entities 3-5) UI
        for enemyIndex in range(3, 6):
            #update health bar
            characterCurrentHP = self.battleEntityArray[enemyIndex].GetCurrentHP()
            if characterCurrentHP < 0:
                characterCurrentHP = 0
            healthBars[enemyIndex - 3].setValue(characterCurrentHP)

            #update intent
            enemyAction = self.battleEntityArray[enemyIndex].GetIntentAction()
            intentString = enemyAction.GetName()
            enemyIntents[enemyIndex - 3].setText(intentString)

            #update intent target
            targetIndex = self.battleEntityArray[enemyIndex].GetTargetIndex()
            targetString = self.battleEntityArray[targetIndex].GetName()
            intentTargets[enemyIndex - 3].setText(targetString)