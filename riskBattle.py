import random
import time

# Automate Risk Battles

# attackers is total number of attacking armies (must be greater than 1)
# defenders is total number of defending armies (must be greater than 0)
# attackerCutoff is a threshold for continuing the attack. The attcker will continue the attack if there are 
# more than attackerCutoff armies left (must be greater than 0).
# Set attackerCutoff = 5 to guarantee that there will be at least 4 remaining attacking armies.
# Set attackerCutoff = 3 to always roll 3 dice (and stop if you cannot roll 3 dice). There will be at least 2 remaining attacking armies.
# Set attackerCutoff = 1 to attack until there is only 1 attacking army remaining or there are no defending armies (all out attack without threshold).
# attackDice is the number of dice the attacker will roll (must be 1, 2, or 3)
# defenseDice is the number of dice the defender will roll (must be 1 or 2)

# verbose <= 0: print nothing
# verbose == 1: print results only
# verbose == 2: print results and army amounts
# verbose >= 3: print results, army amounts, and rolls

def battle(attackers, defenders, attackerCutoff, attackDice, defenseDice, diceSides, verbose=3):
    if not attackers > 1:
        print "The total number of attackers must be greater than 1."
        return
    if not defenders > 0:
        print "The total number of defenders must be greater than 0."
        return
    if not attackerCutoff > 0:
        print "The attacker cutoff must be greater than 0."
        return
    if not attackDice in [1,2,3]:
        print "The attacker must roll 1, 2, or 3 dice."
        return
    if not defenseDice in [1,2]:
        print "The defender must roll 1 or 2 dice."
        return
    roll = 0
    delay = 0
    initialAttackers = attackers
    initialDefenders = defenders
    attackersWin = 0
    defendersWin = 0
    if verbose > 1:
        print "--- Attackers ---> Defenders --- {0} ---> {1} ---".format(attackers, defenders)
    while attackers > attackerCutoff and defenders > 0:
        time.sleep(delay)
        roll += 1
        numAttackDice = 0
        numDefenseDice = 0
        # calculate number of attack dice
        if attackers > 3:
            numAttackDice = 3
        else:
            numAttackDice = attackers - 1
        if numAttackDice > attackDice:
            numAttackDice = attackDice
        # calculate number of defense dice
        if defenders > 1:
            numDefenseDice = 2
        else:
            numDefenseDice = defenders
        if numDefenseDice > defenseDice:
            numDefenseDice = defenseDice

        dice = {}
        dice["attack"] =  sorted(list(random.randint(1, diceSides) for i in xrange(numAttackDice)),  reverse=True)
        dice["defense"] = sorted(list(random.randint(1, diceSides) for i in xrange(numDefenseDice)), reverse=True)
        for key in ["attack", "defense"]:
            stringKey = "%sString" % key
            dice[stringKey] = ""
            for d in dice[key]:
                dice[stringKey] += "%d " % d
            if verbose > 2:
                print "Roll {0} {1} dice:\t{2}".format(roll, key, dice[stringKey])

        matching = min(numAttackDice, numDefenseDice)
        for i in xrange(matching):
            if dice["attack"][i] > dice["defense"][i]:
                defenders -= 1
            else:
                attackers -= 1
        if verbose > 1:
            print "--- Attackers ---> Defenders --- {0} ---> {1} ---".format(attackers, defenders)
    
    if defenders == 0:
        attackersWin = 1
        if verbose > 0:
            print "---------------------------------"
            print "- The attackers are victorious! -"
            print "---------------------------------"
    else:
        defendersWin = 1
        if verbose > 0:
            print "---------------------------------"
            print "- The defenders are victorious! -"
            print "---------------------------------"

    if verbose > 0:
        print "Number of rolls: {0}".format(roll)
        print "Initial attackers: {0}, attackers destroyed: {1}, remaining attackers: {2}".format(initialAttackers, initialAttackers - attackers, attackers)
        print "Initial defenders: {0}, defenders destroyed: {1}, remaining defenders: {2}".format(initialDefenders, initialDefenders - defenders, defenders)

    result = {}
    result["initial_attackers"] = initialAttackers
    result["initial_defenders"] = initialDefenders
    result["remaining_attackers"] = attackers
    result["remaining_defenders"] = defenders
    result["attackers_win"] = attackersWin
    result["defenders_win"] = defendersWin
    return result

if __name__ == "__main__":
    print "Please input all values as integers."
    verbose = input("Please input verbosity (0, 1, 2, 3): ")
    attackers = input("Total number of attacking armies (must be greater than 1): ")
    defenders = input("Total number of defending armies (must be greater than 0): ")
    attackerCutoff = input("Continue attack if there are more than this cutoff (must be greater than 0): ")
    attackDice = input("Number of attacking dice (1, 2, or 3): ")
    defenseDice = input("Number of defending dice (1 or 2): ")
    diceSides = 6
    battle(attackers, defenders, attackerCutoff, attackDice, defenseDice, diceSides, verbose)



