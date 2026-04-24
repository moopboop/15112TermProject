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
tree1BrownMoving = []

tree1GreenChars = {c for c in tree1Str} - tree1BrownChars - set(string.whitespace)
tree1GreenMoving = ['-', '=', '+', '*', '#', '%']


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
tree2BrownMoving = []

tree2GreenChars = {c for c in tree2Str} - tree2BrownChars - set(string.whitespace)
tree2GreenMoving = ['=','+','-','+','*','#','%','@']


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
tree3BrownMoving = []

tree3GreenChars = {c for c in tree3Str} - tree3BrownChars - set(string.whitespace)
tree3GreenMoving = ['=', '*', '+', '#', '@', '%']

def getTree(tree):
  assert(tree <= 3 and tree >= 1)
  brownShades = [rgb( 36,  21,   3), rgb( 41,  29,  14), rgb( 65,  40,  10)]
  greenShades = [rgb( 53, 135,  60), rgb( 25, 176,  37), rgb( 60, 190,  70)]
  brownShade = brownShades[random.randint(0,len(brownShades) - 1)]
  greenShade = greenShades[random.randint(0,len(greenShades) - 1)]
  if tree == 1:
    return EnvironmentItem(tree1Str, [tree1BrownChars, tree1GreenChars], [brownShade, greenShade], [tree1BrownMoving, tree1GreenMoving]).item
  elif tree == 2:
    return EnvironmentItem(tree2Str, [tree2BrownChars, tree2GreenChars], [brownShade, greenShade], [tree2BrownMoving, tree2GreenMoving]).item
  else:
    return EnvironmentItem(tree3Str, [tree3BrownChars, tree3GreenChars], [brownShade, greenShade], [tree3BrownMoving, tree3GreenMoving]).item