import discord
import random
import os
import re

lChars = {}

def process_command_help(message):
    s = "```Commands:\n\n"
    s = s + "!roll\t\t\t\t\t\t\t\t\t\t\t\t --> Roll a d20\n"
    s = s + "!roll [XdY]\t\t\t\t\t\t\t\t\t\t   --> Rolls a Y-sided die, X times.\n"
    s = s + "!roll [\"adv\" / \"disadv\"]\t\t\t\t\t\t\t  --> Rolls with Advantage or Disadvantage. Can be used with most roll commands\n"
    s = s + "!roll [XdY] [\"drophigh\" / \"droplow\"] [X]\t\t\t  --> Subtracts the highest/lowest X dice\n"
    s = s + "!roll [XdY] [\"keephigh\" / \"keeplow\"] [X]\t\t\t  --> Counts the number of die that rolled above/below the value X\n"
    s = s + "!roll custom [die definition]\t\t\t\t\t\t --> Rolls a die with custom faces. Example: !roll custom 1-10-20-30-32\n"
    s = s + "!savecustom [die name] [die definition]\t\t\t   --> Saves a specific custom die with the alias [die name] to be used with !rollcustom\n"
    s = s + "!savecustom [die name] [die definition] -overwrite\t--> Overwrites a previously saved custom die\n"
    s = s + "!rollcustom [die name]\t\t\t\t\t\t\t\t--> Rolls a previously saved custom die\n"
    s = s + "!loadchar\t\t\t\t\t\t\t\t\t\t\t --> Associates you with a character with the same name as your discord username\n"
    s = s + "\t\t\t\t\t\t\t\t\t\t\t\t\t\t--> Example: Richard Nixon#0517\n"
    s = s + "!loadchar [character name]\t\t\t\t\t\t\t--> Associates you with a character with the given name. Do not use spaces!\n"
    s = s + "!stats\t\t\t\t\t\t\t\t\t\t\t\t--> Prints out the stats of the character you are currently associated with\n"
    s = s + "!stats [character name]\t\t\t\t\t\t\t   --> Prints out the stats of the character name provided. No spaces allowed\n"
    s = s + "!addstat [stat name] [stat value]\t\t\t\t\t --> Saves the stat name and value to your currently associated character\n"
    s = s + "\t\t\t\t\t\t\t\t\t\t\t\t\t\t--> It will overwrite if it already exists\n"
    s = s + "!removestat [stat name] [y]\t\t\t\t\t\t   --> Deletes the stat from your currently associated character, if it exists\n"
    s = s + "```"
    return s

def process_command_roll(message):
    mtokens = message.content.split(" ")
    #print(str(mtokens))
    
    drophigh = 0
    droplow = 0
    keepabove = 0
    keepbelow = 0
    adv = False
    disadv = False

    for i in range(len(mtokens)):
        if mtokens[i] == "disadv":
            disadv = True
        if mtokens[i] == "adv":
            adv = True
        if mtokens[i] == "drophigh":
            drophigh = int(mtokens[i+1])
        if mtokens[i] == "droplow":
            droplow = int(mtokens[i+1])
        if mtokens[i] == "keepabove":
            keepabove = int(mtokens[i+1])
        if mtokens[i] == "keepbelow":
            keepbelow = int(mtokens[i+1])
    mtokens = message.content.replace(" adv", "").replace(" disadv", "").split(" ")
        
    
    if mtokens[0] == "!roll":
        #Possible parameters:
        # drophigh
        # droplow
        # keepabove
        # keepbelow
        # XdY
        # adv
        # disadv
        # custom

        rolls = []
        response = ""

        #Basic die roll
        if len(mtokens) == 1:
            singleRoll = random.randint(1, 20)
            secondRoll = random.randint(1, 20)
            print("firstRoll: ", singleRoll, "secondRoll: ", secondRoll)
            if (adv and secondRoll > singleRoll) or (disadv and secondRoll < singleRoll):
                rolls.append(secondRoll)
            else:
                rolls.append(singleRoll)
            
        #Otherwise, arguments were provided
        else:

            #Roll a single die of specified type
            if len(mtokens) == 2 and mtokens[1].isdigit():
                singleRoll = random.randint(1, int(mtokens[1]))
                secondRoll = random.randint(1, int(mtokens[1]))
                if (adv and int(secondRoll) > int(singleRoll)) or (disadv and int(secondRoll) < int(singleRoll)):
                    rolls.append(secondRoll)
                else:
                    rolls.append(singleRoll)
            
            #Roll number of type of die specified
            elif len(mtokens[1].split("d")) == 2 and mtokens[1].split("d")[0].isdigit() and mtokens[1].split("d")[1].isdigit():
                
                #Too many dice
                if int(mtokens[1].split("d")[0]) > 20:
                    return "Why can't I hold all these dice?! Please use 20 or less."
                else:

                    #Correct number of dice
                    for i in range(1, int(mtokens[1].split("d")[0]) + 1):
                        rolls.append(random.randint(1,int(mtokens[1].split("d")[1])))
                        
            #Roll custom specified die
            elif mtokens[1] == "custom":
                customdie = mtokens[2].split("-")
                singleRoll = customdie[random.randint(0, len(customdie) - 1)]
                secondRoll = customdie[random.randint(0, len(customdie) - 1)]
                print("firstRoll: ", singleRoll, "secondRoll: ", secondRoll)
                if (adv and int(secondRoll) > int(singleRoll)) or (disadv and int(secondRoll) < int(singleRoll)):
                    rolls.append(secondRoll)
                else:
                    rolls.append(singleRoll)
            #else:
                
    else:
        return response


    if response == "":
        sortedRolls = list(rolls)
        sortedRolls.sort()
        total = 0
        for roll in rolls:
            total = total + int(roll)

        if drophigh >= len(sortedRolls) or droplow >= len(sortedRolls):
            return "You're trying to remove too many rolls, you dumbass. Try again."
        else:
            #drophigh
            if drophigh > 0 and drophigh < len(sortedRolls):
                for i in range(len(sortedRolls) - 1, len(sortedRolls) - 1 - drophigh, -1):
                    print("i: ", i, "subtracting: ", sortedRolls[i])
                    total = total - sortedRolls[i]

            #droplow
            if droplow > 0 and droplow < len(sortedRolls):
                for i in range(droplow):
                    print("i: ", i, "subtracting: ", sortedRolls[i])
                    total = total - sortedRolls[i]

            #keepabove
            if keepabove > 0:
                total = 0
                for i in range(len(sortedRolls)):
                    if sortedRolls[i] > keepabove:
                        total = total + 1

            #keepbelow
            if keepbelow > 0:
                total = 0
                for i in range(len(sortedRolls)):
                    if sortedRolls[i] < keepbelow:
                        total = total + 1
            
            response = str(total) + " : " + str(rolls)
            return response
    else:
        return response

def process_command_savecustom(message):
    mtokens = message.content.split(" ")

    #     Command Arguments
    # mtokens[0] = "!savecustom"
    # mtokens[1] = [dice name]
    # mtokens[2] = [dice definition]
    # mtokens[3] = "-overwrite"

    response = ""

    if mtokens[0] == "!savecustom":
        try:
            #open the saved file
            inFile = open(os.getcwd() + "/data/CustomDice.txt", "r+")
        except:
            #create the saved file
            inFile = open(os.getcwd() + "/data/CustomDice.txt", "w+")

        response = ""
        matchFound = False
        updated = False

        #Load the custom dice definitions
        savedDice = list()
        for line in inFile:
            savedDice.append(line)
        inFile.close()


        for i in range(len(savedDice)):
            if savedDice[i].split("=")[0] == mtokens[1]:
                matchFound = True
                #print("len(mtokens): " + str(len(mtokens)))
                if len(mtokens) > 3:
                    #print("mtokens[3]:" + mtokens[3])
                    if mtokens[3] == "-o" or mtokens[3] == "-overwrite":
                        savedDice[i] = mtokens[1] + "=" + mtokens[2] + "\n"
                        
                        updated = True
                    else:
                        return "Dice [" + mtokens[1] + "] already exists! Add -o to overwrite."
                else:
                    return "Dice [" + mtokens[1] + "] already exists! Add -o to overwrite."
        if not updated:
            savedDice.append(mtokens[1] + "=" + mtokens[2] + "\n")
        response =  "Dice definition for [" + mtokens[1] + "] saved. You can now use it with !rollcustom [name]"
    else:
        return "Error with mtokens: prefix changed?" 

    outFile = open(os.getcwd() + "/data/CustomDice.txt", "w+")
    outFile.seek(0)
    for dice in savedDice:
        outFile.write(dice)
    outFile.truncate()
    outFile.close()
    if updated:
        return "Dice definition for [" + mtokens[1] + "] has been overwritten."
    else:
        return response



def process_command_rollcustom(message):
    mtokens = message.content.split(" ")

    #     Command Arguments
    # mtokens[0] = "!rollcustom"
    # mtokens[1] = [dice name]
    
    try:
        #open the saved file
        inFile = open(os.getcwd() + "/data/CustomDice.txt", "r+")
    except:
        return "Couldn't find any dice named [" + mtokens[1] + "]"

    #inFile = open(os.getcwd() + "/data/CustomDice.txt", "r+")
    savedDice = list()
    for line in inFile:
        savedDice.append(line)
    inFile.close()

    for dice in savedDice:
        if dice.split("=")[0] == mtokens[1]:
            message.content = "!roll custom " + dice.split("=")[1]
            return process_command_roll(message)

    return "Couldn't find any dice named [" + mtokens[1] + "]"

def process_command_loadchar(message):
    mtokens = message.content.split(" ")

    if len(mtokens) == 1:
        lChars[str(message.author)] = str(message.author)
    else:
        lChars[str(message.author)] = mtokens[1]

    try:  
        with open(os.getcwd() + "/CharacterData/" + lChars[str(message.author)] + ".txt", "a") as my_file:
            my_file
            return "You are now associated with the character: [" + lChars[str(message.author)] + "]"
        return "Something went wrong. Please let me know about this."
    except:
        return "Something went wrong. Please let me know about this."

def process_command_stats(message):
    mtokens = message.content.split(" ")

    #    Command Arguments
    # mtokens[0] = "!stats"
    # mtokens[1] = [character name]

    if len(mtokens) == 1:
        try:
            #a = lChars[str(message.author)]
            mtokens.append(lChars[str(message.author)])
        except:
            return "Please specify a character's name or use !loadchar to associate yourself with a character."

    try:
        #open file with character's data
        inFile = open(os.getcwd() + "/CharacterData/" + mtokens[1] + ".txt", "r+")
    except:
        return "Couldn't find any character named [" + mtokens[1] + "]"

    charStats = list()
    for line in inFile:
        charStats.append(line)
    inFile.close()

    if len(mtokens) == 2:
        i = 0
        strlist = [mtokens[1] + "'s stats:\n"]
        for x in charStats:
            strlist.append(x)
        return "".join(strlist)
    else:
        return "Too many arguments. Try again, por favor."

def process_command_addstats(message):
    mtokens = message.content.split(" ")

    #    Command Arguments
    # mtokens[0] = "!addstats"
    # mtokens[1] = [stat name]
    # mtokens[2] = [stat value]

    #check for badly structured command
    if len(mtokens) != 3:
        print("Invalid # of arguments")
        return "Invalid number of arguments. Try that again, but right this time."


    #check for a character association
    try:
        print(str(message.author) + ": " + lChars[str(message.author)])
    except:
        return "You currently have no character association. Use !loadchar [char name] first."


    #open file with associated character's data
    try:
        with open(os.getcwd() + "/CharacterData/" + lChars[str(message.author)] + ".txt", "r") as inFile:
            lines = inFile.read()
    except:
        return "You aren't currently associated with a character. Please use !loadchar first."


    #print("mtokens[1]: " + mtokens[1])
    #print("mtokens[2]: " + mtokens[2])
    
    r1 = re.search(mtokens[1] + ":.*\n", lines)
    if r1:
        #print("Found mtokens[1].")
        lines = re.sub(mtokens[1] + ":.*\n", mtokens[1] + ":" + mtokens[2] + "\n", lines)
        with open(os.getcwd() + "/CharacterData/" + lChars[str(message.author)] + ".txt", "w") as outFile:
            outFile.write(lines)
        return "[" + mtokens[1] + "]" + " has been successfully updated to the value: " + mtokens[2]     
    else:
        #print("Didn't find it. Must add.")
        with open(os.getcwd() + "/CharacterData/" + lChars[str(message.author)] + ".txt", "a") as outFile:
            outFile.write(mtokens[1] + ":" + mtokens[2] + "\n")
        return "[" + mtokens[1] + "]" + " has been successfully set to the value: " + mtokens[2]

    return "Ended unexpectedly. Please let me know about this error."
    
    
def process_command_removestats(message):
    mtokens = message.content.split(" ")

    #    Command Arguments
    # mtokens[0] = "!removestats"
    # mtokens[1] = [stat name]
    # mtokens[2] = [confirm: y]

    #check for badly structured command
    if len(mtokens) != 3:
        return "Invalid number of arguments for this command. Try: !removestats [stat name] [y]"

    #check for a character association
    try:
        print(str(message.author) + ": " + lChars[str(message.author)])
    except:
        return "You currently have no character association. Use !loadchar [char name] first."

    print("mtokens[2]: " + mtokens[2])
    #check for safety flag
    if not mtokens[2] == "y":
        return "Safety flag not set. This is for your own protection. Try: !removestats [stat name] [y]"

    #open file with associated character's data
    try:
        with open(os.getcwd() + "/CharacterData/" + lChars[str(message.author)] + ".txt", "r") as inFile:
            lines = inFile.read()
    except:
        return "You aren't currently associated with a character. Please use !loadchar first."


    #remove the stat    
    r1 = re.search(mtokens[1] + ":.*\n", lines)
    
    if r1:
        #print("Found mtokens[1].")
        lines = re.sub(mtokens[1] + ":.*\n", "", lines)
        with open(os.getcwd() + "/CharacterData/" + lChars[str(message.author)] + ".txt", "w") as outFile:
            outFile.write(lines)
        return "Successfully removed the stat [" + mtokens[1] + "] from character: [" + lChars[str(message.author)] + "]"
    else:
        #print("Didn't find it. Nothing to update.")
        return "[" + lChars[str(message.author)] + "] does not have the stat: [" + mtokens[1] + "]. No action taken." 

    return "Ended unexpectedly. Please let me know about this error."
