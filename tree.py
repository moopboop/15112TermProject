from environmentItemClass import *

tree1Str = '''         -===
       ====++= =
      ===++*+=+++=
  -----=++******++
  -==++*#*+******====
 ==++**********++++++==
  +*****************++
   +***####***++****++
 ==+***####*********+==
 =***+******####***+++
=+******##**####****++
++**###########****++==
++*#####*##*********+==+=
 +*#####%#######%####***+=
 =+**#%%####%%####*####*++
 ++*#####%%%%%%%########*++
++*########%%##########**
++*##**##**###***##**+
  +***     |||
           |||
           |||
           |||
           |||
           |||
         ||||||| 
'''
tree1BrownChars = {'|'}
tree1Brown = rgb(65,40,10)
tree1BrownMoving = []

tree1GreenChars = {c for c in tree1Str} - tree1BrownChars - set(string.whitespace)
tree1Green = rgb(60,190,70)
tree1GreenMoving = ['-', '=', '+', '*', '#', '%']

TREE1 = EnvironmentItem(tree1Str, [tree1BrownChars, tree1GreenChars], [tree1Brown, tree1Green], [tree1BrownMoving, tree1GreenMoving]).item




tree2Str = '''              =-                
         =====+=-  -            
          **#*#*++=++==         
    -=   +*##%*+**%%##*         
   =+***######%#**#%#**++==     
 ==*#%@%||%%@@%%%%#%%%#*#*+*    
  *##*##||%@@@%%%%%%%%##*+==    
   +#####||%%%%%||@%##%%##*||   
   +*#%%%%||%%||%@@@%%#%%%||+=  
   *#%%@@@@%||@%@@@%@%%##|||*+= 
  ##%%%@@@@||@@@%@@@@@%|||###**+=
 *#%%%%%@||@@@%%@|||%||||%%%%#*+ 
%##|||%%||%##@%%%@%%||%%%%%##*  
%%%%@||||||@@%%@@@@||%||#%%%#*#+
*####%%%%#||%%%@@@||@@@||%##**  
  ##%##%#%%|||@@@||%@@%%@%#%*   
          #%|||||||  @          
              |||
              |||
              |||
              |||
              |||
              |||               
'''

tree2BrownChars = {'|'}
tree2Brown = rgb(41, 29, 14)
tree2BrownMoving = []

tree2GreenChars = {c for c in tree2Str} - tree2BrownChars - set(string.whitespace)
tree2Green = rgb(25, 176, 37)
tree2GreenMoving = ['=','+','-','+','*','#','%','@']

TREE2 = EnvironmentItem(tree2Str, [tree2BrownChars, tree2GreenChars], [tree2Brown, tree2Green], [tree2BrownMoving, tree2GreenMoving]).item




tree3Str = '''               =*++#*           
            +=#@#*+%%+          
        +###*##@@@@@@@@%#       
      *%##@@*%#@@@@@@@@@@%      
      %@@@@@@@@@@@@@@@@@%%#%%   
       %@@@@@%*%@@@@@@@@@@@@@   
    **#+*%%@@@@@#@@@@@@@@%@@@   
    ###*%@@@%@@#@@@@@@@@@@@@    
   *#@%@@@@@@@*%@@@%@@@@@@      
      @@@@@@%%#@@@%@@@@@@@@     
             =#@@@  @@@@@@      
              |||    @@         
              |||               
              ||||              
              ||||              
              ||||              
              ||||              
              ||||             
           |||||||||         
'''

tree3BrownChars = {'|'}
tree3Brown = rgb(36, 21, 3)
tree3BrownMoving = []

tree3GreenChars = {c for c in tree3Str} - tree3BrownChars - set(string.whitespace)
tree3Green = rgb(53, 135, 60)
tree3GreenMoving = ['=', '*', '+', '#', '@', '%']

TREE3 = EnvironmentItem(tree3Str, [tree3BrownChars, tree3GreenChars], [tree3Brown, tree3Green], [tree3BrownMoving, tree3GreenMoving]).item
