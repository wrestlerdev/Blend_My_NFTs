Characters = ["Nef", "Kae", "Rem"]

MasterMaterialName = 'MasterV01'

texture_suffixes = {64: '_64', 128: '_128', 256: '_256', 512: '_512', 1024: '_1k', 2048: '_2k', 4096: ''}
image_extensions = ['jpg','jpeg', 'bmp', 'png', 'tif']

EmptyTypes = ["Expression", "ExpressionLowerNone", "HeadShortNone", "FeetShortNone", 'Background', "Particles"]

Slots = {"inputUpperTorso": ("01-UpperTorso", "Upper Torso"),
    "inputMiddleTorso": ("02-MiddleTorso", "Mid Torso"),
    "inputForeArms": ("03-ForeArms", "Forearms"),
    "inputWrists": ("04-Wrists", "Wrists"),
    # "inputRForeArm": ("05-RForeArm", "Right Forearm"),
    # "inputWrists": ("06-Wrists", "Right Wrist"),
    "inputHands": ("05-Hands", "Hands"),
    "inputPelvisThick": ("06-PelvisThick", "Pelvis Thick"),
    "inputPelvisThin": ("07-PelvisThin", "Pelvis Thin"),
    "inputCalf": ("08-Calf", "Calf"),
    "inputAnkle": ("09-Ankle", "Ankle"),
    "inputFeet": ("10-Feet", "Feet"),
    "inputHairLong": ("11-HairLong", "Hair Long"),
    "inputHairShort": ("12-HairShort", "Hair Short"),
    "inputHeadAccessories": ("20-HeadAccessories", "Head Accessories"),
    "inputNeck": ("13-Neck", "Neck"),
    "inputMiddleHead": ("14-MiddleHead", "Mid Head"),
    "inputLowerHead": ("15-LowerHead", "Lower Head"),
    "inputEarrings": ("17-Earrings", "Earrings Short"),
    "inputEarringsLong": ("16-EarringsLong", "Earrings Long"),
    "inputBackpack": ("19-Backpack", "Backpack"),
    "inputExpression": ("18-Expression", "Expression"),
    "inputEnvironment": ("21-Environment", "Environment"),
    "inputBackground": ("22-Background", "Background")}


class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR