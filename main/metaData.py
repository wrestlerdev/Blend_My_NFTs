# Some code in this file was generously sponsored by the amazing team over at SolSweepers!
# Feel free to check out their amazing project and see how they are using Blend_My_NFTs:
# https://discord.gg/QTT7dzcuVs

# Purpose:
# This file returns the specified meta data format to the Exporter.py for a given NFT DNA.

import bpy
import os
import json
import re
from . import config


KeywordAttributeDict = {
    new_key: new_val
    for keys, new_val in [(["Shirt"], "Tops"),
                         (["Pant"], "Bottoms"),
                         (["Outfit"], "Outfit"),
                         (["Feet"], "Shoes"),
                         (["Head"], "Headwear"),
                        #  (["Tattoo"], "Tattoo"),
                         (["Gloves", "Forearm"], "Armwear"),
                         (["Face"], "Facewear"),
                         (["Hair"], "Hairstyle"),
                         (["Earring", "Calf", "Neck", "Hand", "Tattoo"], "Accessories"),
                         (["Backpack"], "Backwear"),
                         (["Plane", "Background", "Particles"], "Environment"),
                         (["Expression"], "Expression")]
    for new_key in keys
}

KeywordKeys = [ # this is the order attributes will be listed in the metadata
    "Null",
    "Character",
    "Theme",
    "Element",
    # "Tattoo",
    "Expression",
    "Outfit",
    "Tops",
    "Bottoms",
    "Shoes",
    "Hairstyle",
    "Facewear",
    "Headwear",
    "Armwear",
    "Accessories",
    "Backwear",
    "Environment"
    ]
KeywordAttributeOrder = {KeywordKeys[v]: v for v in range(len(KeywordKeys))} 


def returnERC721MetaDataCustom(name, DNA, NFTDict, batch_num):
    keys = list(NFTDict.keys())
    metaDataDictErc721 = {
        "name": name,
        "description": "description should be inserted here",
        "image": "Link to image file?",
        "video": "Link to link to video?",
        "DNA": DNA,
        "data": "Link to data json?",
        "attributes": None,
        
    }

    attributes = []
    DNAString = DNA.split(",")
    character = DNAString.pop(0)
    element = DNAString.pop(0)
    style = DNAString.pop(0)

    attributes.append({"trait_type": "Character", "value": character})

    if style != 'Elemental':
        attributes.append({"trait_type": "Theme", "value": style})
    else:
        ele_style, ele_type = element.split('-')
        if ele_style == 'All':
            attributes.append({"trait_type": "Theme", "value": "Elemental"})
        elif ele_style == 'Outfit':
            attributes.append({"trait_type": "Theme", "value": "Elemental Outfit"})
        attributes.append({"trait_type": "Element", "value": ele_type})

    for key in keys:
        for itemKey in NFTDict[key]:
            if(NFTDict[key] != "Null"):
                itemDictionary = NFTDict[key][itemKey]
                color_key = itemDictionary["color_key"] 
                slot = itemDictionary["item_attribute"]
                type = itemDictionary["item_type"]
                variant = itemDictionary["item_variant"]
                texture = itemDictionary["item_texture"].rpartition('_')[2]

                # if "Tattoo" in type:
                #     if "Forearm" in type:
                #         dict = {"trait_type": "Tattoo", "value": "On Forearm"}
                #     elif "Calf" in type:
                #         dict = {"trait_type": "Tattoo", "value": "On Calf"}
                #     elif "Neck" in type:
                #         dict = {"trait_type": "Tattoo", "value": "On Neck"}
                #     attributes.append(dict)
                #     tattoo_symbol = ' '.join(re.sub("((?<=[a-z])[A-Z]|[A-Z](?=[a-z]))",r' \1', texture).split())
                #     dict = {"trait_type": "Tattoo", "value": "{} Symbol".format(tattoo_symbol)}
                #     attributes.append(dict)
                #     continue

                # split_variant_name = ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', variant)).split()) # this one leaves a space between every captial
                # full_variant_name = [split_variant_name]
                variant = variant[0].upper() + variant[1:] # capitilize variant
                # split_variant_name = ' '.join(re.sub("([a-z])([A-Z])","\g<1> \g<2>",variant).split())
                split_variant_name = ' '.join(re.sub("((?<=[a-z])[A-Z]|[A-Z](?=[a-z]))",r' \1', variant).split())
                if "ExpressionLowerNone" in type or "FeetShortNone" in type or "Expression" == type[3:]:
                    full_variant_name = split_variant_name
                else:
                    texture_name = ' '.join(re.sub("((?<=[a-z])[A-Z]|[A-Z](?=[a-z]))",r' \1', texture[3:]).split())
                    full_variant_name = "{} ({})".format(split_variant_name, texture_name)

                type_name = type[3:]
                keyword = None
                for key in list(KeywordAttributeDict.keys()):
                    if type_name.startswith(key):
                        keyword = KeywordAttributeDict[key]
                        break
                if keyword:
                    if not variant.endswith("Null"):
                        dict = {"trait_type": keyword, "value": full_variant_name}
                        attributes.append(dict)

    attributes = sorted(attributes, key = lambda i:KeywordAttributeOrder[i["trait_type"]])
    metaDataDictErc721["attributes"] = attributes
    return metaDataDictErc721


if __name__ == '__main__':
    returnERC721MetaDataCustom()
