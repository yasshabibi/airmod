from colored import fg, bg, attr
from objects import Context
import datetime

class Colors:
    PINK 		= '{}'.format(fg(171))
    BLUE 		= '{}'.format(fg(4))
    GREEN 		= '{}'.format(fg(118))
    YELLOW 		= '{}'.format(fg(226))
    RED 		= '{}'.format(fg(1))
    ENDC 		= '{}'.format(attr(0))
    BOLD 		= '{}'.format(attr('bold'))
    UNDERLINE 	= '{}'.format(attr("underlined"))


def printAscii():
    print("""{R}                                                                   
                                                  @@@                           
                                        &#####################@                 
                                    ##############################@             
                                 #######################{W}%.../{R}########@          
                              ,####################{W},.            ..{R}#####        
                             ####################{W}.@                 .{R}####@      
                            ####################{W}.                     .{R}####     
                           #####################{W}.                       .{R}###@   
                          ######################{W},                       ,{R}####@  
                          ######################{W}.                        .{R}####@ 
                         @#######################{W}.                       .{R}##### 
                          ########################@{W}@                    .{R}#######
  {W}@        @              {R}##########################@{W}#                *.{R}########
                           ############################@.{W}@         (.%{R}##########
                    {W}@      .{R} #############################{W}##########{R}#############
                             ###################################################
                              @#################################################
 {W}@                              {R} @##############################################@
                                   ############################################ 
                        {W}#              {R} #######################################  
                                           ##################################   
     {W}*                                       {R} ###############################    
                            {W}.                {R}  ############################@     
       {W} @                                     {R}  ##########################       
          {W}@                                  {R}   ########################         
                                               #####################@           
               {W}*                            {R}   ###################@              
                   {W}%                        {R}  #################                  
                      {W} ,                {R}   ###############@                      
                               {W}&   {R}   %############@                                    
""".format(R = fg(197), W = Colors.ENDC))

def write(string:str,  noNL:bool=False)->None:
    if  noNL:
        print(string, end="")
        Context.runtimeLog.write(string)
    else:
        print(string)
        Context.runtimeLog.write(string + "\n")


def writeColored(string:str, color:Colors, noNL:bool=False)->None:
    if  noNL:
        print(f"{color}{string}{Colors.ENDC}", end="")
        Context.runtimeLog.write(string)
    else:
        print(f"{color}{string}{Colors.ENDC}")
        Context.runtimeLog.write(string + "\n")

def writeFailure():
    writeColored("Failure", Colors.RED)

def writeSuccess():
    writeColored("Success", Colors.GREEN)

def writeCaution():
    writeColored("Caution", Colors.YELLOW)


def debug(string):
    if Context.debug:
        x = datetime.datetime.now()
        print("{}[{}] DEBUG - {}{}".format(Colors.PINK, x.strftime("%Y-%m-%d %H:%M:%S"), string, Colors.ENDC))
        Context.runtimeLog.write("[{}] DEBUG - {}".format(x.strftime("%Y-%m-%d %H:%M:%S"), string))

def caut(string):
    x = datetime.datetime.now()
    print("{}[{}] CAUTION - {}{}".format(Colors.YELLOW, x.strftime("%Y-%m-%d %H:%M:%S"), string, Colors.ENDC))
    Context.runtimeLog.write("[{}] CAUTION - {}".format(x.strftime("%Y-%m-%d %H:%M:%S"), string))

def chat(message, fro, to):
    x = datetime.datetime.now()
    print("{}[{}] CHAT - ({} => {}) :  {}{}".format(Colors.BLUE, x.strftime("%Y-%m-%d %H:%M:%S"), fro, to, message, Colors.ENDC))
    Context.runtimeLog.write("[{}] CHAT - {}".format(x.strftime("%Y-%m-%d %H:%M:%S"), message))

def info(string):
    x = datetime.datetime.now()
    print("{}[{}] INFO{} - {}".format(Colors.GREEN, x.strftime("%Y-%m-%d %H:%M:%S"),  Colors.ENDC, string))
    Context.runtimeLog.write("[{}] INFO - {}".format(x.strftime("%Y-%m-%d %H:%M:%S"), string))

def error(string):
    x = datetime.datetime.now()
    print("{}[{}] ERROR - {}{}".format(Colors.RED, x.strftime("%Y-%m-%d %H:%M:%S"),  string, Colors.ENDC))
    Context.runtimeLog.write("[{}] ERROR - {}".format(x.strftime("%Y-%m-%d %H:%M:%S"), string))