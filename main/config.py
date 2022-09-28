Characters = ["Nef", "Kae", "Rem"]

MasterMaterialName = 'MasterV01'

texture_suffixes = {64: '_64', 128: '_128', 256: '_256', 512: '_512', 1024: '_1k', 2048: '_2k', 4096: ''}
image_extensions = ['jpg','jpeg', 'bmp', 'png', 'tif']

EmptyTypes = ["Expression", "ExpressionLowerNone", "HeadShortNone", "FeetShortNone", 'Background', "Particles"]
# Elements = ["Bismuth","Bismuth_02","Gold", "Gold_02", "Gold_03", "Oxygen", "Sulphur", "SpiritOfWine", "Mercury", "Salt"]
Elements = ["Cinnabar", "Bismuth","Gold_02", "Oxygen", "Sulphur", "SpiritOfWine", "Mercury", "Salt", "Magnesium", "AquaFortis",
             "Vitriol", "Brimstone", "AquaRegia", "Tin", "Silver", "Arsenic", "Phlogiston", "Amalgum", "SalAmmoniac",
             "Acid", "Lead", "Iron",  "Copper", "Antimony", "Cobalt", "Manganese", "Nickel", "Phosphorus", "Platinum", "Zinc"] 

Textiles = ["Corn", "OceanSwirl","QuiltedShells", "MetalGate", "Salmon"]   

fallback_texture_set_name = 'Standard'

Slots = {"inputUT": ("01-UT", "Upper Torso"),
    "inputMT": ("02-MT", "Mid Torso"),
    "inputFA": ("03-FA", "Forearms"),
    "inputW": ("04-W", "Wrists"),
    "inputH": ("05-H", "Hands"),
    "inputPTK": ("06-PTK", "Pelvis Thick"),
    "inputPTN": ("07-PTN", "Pelvis Thin"),
    "inputC": ("08-C", "Calf"),
    "inputA": ("09-A", "Ankle"),
    "inputF": ("10-F", "Feet"),
    "inputHL": ("11-HL", "Hair Long"),
    "inputHS": ("12-HS", "Hair Short"),
    "inputHA": ("13-HA", "Accessories"),
    "inputN": ("14-N", "Neck"),
    "inputMH": ("15-MH", "Mid Head"),
    "inputLH": ("16-LH", "Lower Head"),
    "inputES": ("18-ES", "Earrings Short"),
    "inputEL": ("17-EL", "Earrings Long"),
    "inputBP": ("20-BP", "Backpack"),
    "inputEX": ("19-EX", "Expression"),
    "inputENV": ("21-ENV", "Environment"),
    "inputBG": ("22-BG", "Background")}


class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR

ShouldPrintOrigin = False
LoggingEnabled = True

def custom_print(message, parent='', col=bcolors.RESET):
    if LoggingEnabled:
        if ShouldPrintOrigin:
            print(f"{col}({parent}): {message}{bcolors.RESET}")
        else:
            print(f"{col}{message}{bcolors.RESET}")
    return