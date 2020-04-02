# DMBot.py
 
Requirements:  
-----------
Python 3  
Discord.py (https://discordpy.readthedocs.io/en/latest/index.html)  
python-dotenv (https://pypi.org/project/python-dotenv/)  

To Start:  
-----------
Modify the .env file with your Discord token and guild  
Run the "DMBot.py" file  


Commands:
--------

!roll                                                 --> Roll a d20  
!roll [XdY]                                           --> Rolls a Y-sided die, X times.  
!roll ["adv" / "disadv"]                              --> Rolls with Advantage or Disadvantage. Can be used with most roll commands  
!roll [XdY] ["drophigh" / "droplow"] [X]              --> Subtracts the highest/lowest X dice  
!roll [XdY] ["keephigh" / "keeplow"] [X]              --> Counts the number of die that rolled above/below the value X  
!roll custom [die definition]                         --> Rolls a die with custom faces. Example: !roll custom 1-10-20-30-32  
!savecustom [die name] [die definition]               --> Saves a specific custom die with the alias [die name] to be used with !rollcustom  
!savecustom [die name] [die definition] -overwrite    --> Overwrites a previously saved custom die  
!rollcustom [die name]                                --> Rolls a previously saved custom die  
!loadchar                                             --> Associates you with a character with the same name as your discord username  
!loadchar [character name]                            --> Associates you with a character with the given name. Do not use spaces!  
!stats                                                --> Prints out the stats of the character you are currently associated with  
!stats [character name]                               --> Prints out the stats of the character name provided. No spaces allowed  
!addstat [stat name] [stat value]                     --> Saves the stat name and value to your currently associated character  
                                                        --> It will overwrite if it already exists  
!removestat [stat name] [y]                           --> Deletes the stat from your currently associated character, if it exists  
