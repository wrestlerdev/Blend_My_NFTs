Characters = ["Nef", "Kae", "Rem"]

MasterMaterialName = 'MasterV01'

texture_suffixes = {64: '_64', 128: '_128', 256: '_256', 512: '_512', 1024: '_1k', 2048: '_2k', 4096: ''}
image_extensions = ['jpg','jpeg', 'bmp', 'png', 'tif']

EmptyTypes = ["Expression", "ExpressionLowerNone", "HeadShortNone", "FeetShortNone", 'Background']

Slots = {"inputUpperTorso": ("01-UpperTorso", "Upper Torso"),
    "inputMiddleTorso": ("02-MiddleTorso", "Mid Torso"),
    "inputLForeArm": ("03-LForeArm", "Left Forearm"),
    "inputLWrist": ("04-LWrist", "Left Wrist"),
    "inputRForeArm": ("05-RForeArm", "Right Forearm"),
    "inputRWrist": ("06-RWrist", "Right Wrist"),
    "inputHands": ("07-Hands", "Hands"),
    "inputPelvisThick": ("08-PelvisThick", "Pelvis Thick"),
    "inputPelvisThin": ("09-PelvisThin", "Pelvis Thin"),
    "inputCalf": ("10-Calf", "Calf"),
    "inputAnkle": ("11-Ankle", "Ankle"),
    "inputFeet": ("12-Feet", "Feet"),
    "inputNeck": ("13-Neck", "Neck"),
    "inputLowerHead": ("14-LowerHead", "Lower Head"),
    "inputMiddleHead": ("15-MiddleHead", "Mid Head"),
    "inputEarings": ("16-Earings", "Earrings"),
    "inputUpperHead": ("17-UpperHead", "Upper Head"),
    "inputBackpack": ("18-Backpack", "Backpack"),
    "inputBackground": ("19-Background", "Background"),
    "inputExpression": ("20-Expression", "Expression")}


class bcolors:
   '''
   The colour of console messages.
   '''
   OK = '\033[92m'  # GREEN
   WARNING = '\033[93m'  # YELLOW
   ERROR = '\033[91m'  # RED
   RESET = '\033[0m'  # RESET COLOR