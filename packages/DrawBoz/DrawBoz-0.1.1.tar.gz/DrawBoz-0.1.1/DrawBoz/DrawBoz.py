import os


class _Box:

    ############CHARACTERS############
    URC: str = "╮" # Up Right Conner
    ULC: str = "╭" # Up Left Conner
    DRC: str = "╯" # Down Right Conner
    DLC: str = "╰" # Down Left Conner
    DC: str = "─"  # Dash Character
    UC: str = "│"  # Upward Character
    SPACE:str = " " # Space
    UW: str = "╭────────────────────────────────────────────────────────╮\n" # Upward Wall
    DW: str = "╰────────────────────────────────────────────────────────╯\n" # Upward Wall
    ##################################
    
    def __init__(self, text: str=""):
        self.text = text
        self.printOutput: str = ""

    
    
    def Run(self):
        os.system("cls" if os.name == 'nt' else "clear")
        print(self.printOutput)
    
    def PrintEmptyRow(self) -> str:
            return f"{_Box.UC}{_Box.SPACE * 56}{_Box.UC}\n"
    
    def PrintTextRow(self) -> str:              # Prints row with text centered
        centered_text: str = self.text.center(56)
        return f"│{centered_text}│\n"
    

    
#           The main idea
#   1. make a array [].  ✅
#   2. then add text into arrays with a function [AddText("Text", line_number, isInverted)].✅
#   3. then using a empty list, add those text into the empty function making 
#      the data for the whole box. ✅
#   4. and decode them and make it into a string ready to be printed. ✅

# More TODOs: Remove that paradox with the Draw instalization (atlest try) ❌, Its almost impossible,
# you have to refactor the whole code

class DrawBoz:

    DefaultArray: list[str] = ["null", "null", "null",           # "null" here stands for empty row
                               "null", "null", "null", 
                               "null", "null", "null", 
                               "null", "null", "null"]

    def __init__(self, Array: list):    
        self.InputArray = Array
        self.CompleteArray = DrawBoz.DefaultArray

    def InvertTextColors(self, text: str) -> str:
        return  f"\x1b[7m{text}\x1b[0m"



    def AddText(self, Text: str, LineNumber: int=0, isInverted: bool=False) -> list: # should only be used in Array varible
        text = Text
        if isInverted:
            text = f'\033[7m{Text}\033[0m'

        return [text, LineNumber, isInverted]
    
    def MigrateInputArrayToCompleteArray(self):
        for text, LineNumber, isInverted in self.InputArray:
            if 0 <= LineNumber < len(self.CompleteArray):
                self.CompleteArray[LineNumber] = [text, LineNumber, isInverted]

    def RenderString(self) -> str:  
        BoxClass = _Box()
        OutputString = ""
        OutputString += _Box.UW 
        for i in range(len(self.CompleteArray)):

            if self.CompleteArray[i] == "null":
                OutputString += _Box.PrintEmptyRow(BoxClass) 

            elif isinstance(self.CompleteArray[i], list) and i == self.CompleteArray.index(self.CompleteArray[i]) and self.CompleteArray[i][2] == False:
                OutputString += f"{BoxClass.UC}{(self.CompleteArray[i][0]).center(56)}{BoxClass.UC}\n"

            elif isinstance(self.CompleteArray[i], list) and i == self.CompleteArray.index(self.CompleteArray[i]) and self.CompleteArray[i][2] == True:
                OutputString += BoxClass.UC + f"\x1b[7m{self.CompleteArray[i][0]}".center(68) + BoxClass.UC + "\n"
            
        OutputString += _Box.DW 
        return OutputString






    