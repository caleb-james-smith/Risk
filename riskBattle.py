import optparse
import random
import time

# attackers is total number of attacking armies (must be greater than 1)
# defenders is total number of defending armies (must be greater than 0)
# attackerCutoff is a threshold for continuing the attack. The attcker will continue the attack if there are 
# more than attackerCutoff armies left (must be greater than 0).
# Set attackerCutoff = 5 to guarantee that there will be at least 4 remaining attacking armies.
# Set attackerCutoff = 3 to always roll 3 dice (and stop if you cannot roll 3 dice). There will be at least 2 remaining attacking armies.
# Set attackerCutoff = 1 to attack until there is only 1 attacking army remaining or there are no defending armies (all out attack without threshold).
# attackDice is the number of dice the attacker will roll (must be 1, 2, or 3)
# defenseDice is the number of dice the defender will roll (must be 1 or 2)
def battle(attackers, defenders, attackerCutoff, attackDice, defenseDice):
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
    diceSides = 6
    roll = 0
    delay = 0.1
    initialAttackers = attackers
    initialDefenders = defenders
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
            print "Roll {0} {1} dice:\t{2}".format(roll, key, dice[stringKey])

        matching = min(numAttackDice, numDefenseDice)
        for i in xrange(matching):
            if dice["attack"][i] > dice["defense"][i]:
                defenders -= 1
            else:
                attackers -= 1
        print "--- Attackers ---> Defenders --- {0} ---> {1} ---".format(attackers, defenders)
    
    if defenders == 0:
        print "---------------------------------"
        print "- The attackers are victorious! -"
        print "---------------------------------"
    else:
        print "---------------------------------"
        print "- The defenders are victorious! -"
        print "---------------------------------"

    print "Number of rolls: {0}".format(roll)
    print "Initial attackers: {0}, attackers destroyed: {1}, remaining attackers: {2}".format(initialAttackers, initialAttackers - attackers, attackers)
    print "Initial defenders: {0}, defenders destroyed: {1}, remaining defenders: {2}".format(initialDefenders, initialDefenders - defenders, defenders)

if __name__ == "__main__":
    parser = optparse.OptionParser("usage: %prog [options]\n")
    parser.add_option("-s", "--simulation", dest='simulation', action='store_true', default=False, help="Run simulation of many battles.")
    options, args = parser.parse_args()
    if options.simulation:
        print "Running simulation of many battles."
    else:
        print "Please input all values as integers."
        attackers = input("Total number of attacking armies (must be greater than 1): ")
        defenders = input("Total number of defending armies (must be greater than 0): ")
        attackerCutoff = input("Continue attack if there are more than this cutoff (must be greater than 0): ")
        attackDice = input("Number of attacking dice (1, 2, or 3): ")
        defenseDice = input("Number of defending dice (1 or 2): ")
        battle(attackers, defenders, attackerCutoff, attackDice, defenseDice)



