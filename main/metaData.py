# Some code in this file was generously sponsored by the amazing team over at SolSweepers!
# Feel free to check out their amazing project and see how they are using Blend_My_NFTs:
# https://discord.gg/QTT7dzcuVs

# Purpose:
# This file returns the specified meta data format to the Exporter.py for a given NFT DNA.

import bpy
import os
import json
import re


KeywordAttributeDict = {
    new_key: new_val
    for keys, new_val in [(["Shirt"], "Tops"),
                         (["Pant"], "Bottoms"),
                         (["Outfit"], "Outfit"),
                         (["Feet"], "Shoes"),
                         (["Head"], "Headwear"),
                         (["Gloves", "Forearm"], "Armwear"),
                         (["Face"], "Facewear"),
                         (["Hair"], "Hairstyle"),
                         (["Earring", "Calf", "Neck", "Hands"], "Accessories"),
                         (["Backpack"], "Backwear"),
                         (["Plane", "Background", "Particles"], "Environment"),
                         (["Expression"], "Expression")]
    for new_key in keys
}

KeywordKeys = [
    "Null",
    "Character",
    "Theme",
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





# def returnCardanoMetaData(name, NFT_DNA, NFT_Variants):
#     metaDataDictCardano = {"721": {
#         "<policy_id>": {
#             name: {
#                 "name": name,
#                 "image": "",
#                 "mediaType": "",
#                 "description": "",

#             }
#         },
#         "version": "1.0"
#     }}

#     for i in NFT_Variants:
#         metaDataDictCardano["721"]["<policy_id>"][name][i] = NFT_Variants[i]

#     return metaDataDictCardano

# def returnSolanaMetaData(name, NFT_DNA, NFT_Variants):
#     metaDataDictSolana = {"name": name, "symbol": "", "description": "", "seller_fee_basis_points": None,
#                           "image": "", "animation_url": "", "external_url": ""}

#     attributes = []

#     for i in NFT_Variants:
#         dictionary = {
#             "trait_type": i,
#             "value": NFT_Variants[i]
#         }

#         attributes.append(dictionary)

#     metaDataDictSolana["attributes"] = attributes
#     metaDataDictSolana["collection"] = {
#         "name": "",
#         "family": ""
#     }

#     metaDataDictSolana["properties"] = {
#         "files": [{"uri": "", "type": ""}],
#         "category": "",
#         "creators": [{"address": "", "share": None}]
#     }
#     return metaDataDictSolana

# def returnErc721MetaData(name, NFT_DNA, NFT_Variants):
#     metaDataDictErc721 = {
#         "name": name,
#         "description": "",
#         "image": "",
#         "attributes": None,
#     }

#     attributes = []

#     for i in NFT_Variants:
#         dictionary = {
#             "trait_type": i,
#             "value": NFT_Variants[i]
#         }

#         attributes.append(dictionary)

#     metaDataDictErc721["attributes"] = attributes

#     return metaDataDictErc721



def returnERC721MetaDataCustom(name, DNA, NFTDict, batch_num):

    keys = list(NFTDict.keys())

    metaDataDictErc721 = {
        "name": name,
        "description": "This is a test meta data file",
        "image": "Link to IPFS?",
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

    if not element.startswith("None"):
        ele_style, ele_type = element.split('-')
        if ele_style == 'All':
            attributes.append({"trait_type": "Element", "value": "Elemental"})
        elif ele_style == 'Skin':
            attributes.append({"trait_type": "Element", "value": "Elemental Skin"})
        elif ele_style == 'Outfit':
            attributes.append({"trait_type": "Element", "value": "Elemental Outfit"})

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

                # split_variant_name = ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', variant)).split()) # this one leaves a space between every captial
                # full_variant_name = [split_variant_name]
                variant = variant[0].upper() + variant[1:]
                split_variant_name = ' '.join(re.sub("([a-z])([A-Z])","\g<1> \g<2>",variant).split())

                full_variant_name = [split_variant_name]
                # if color_key != 'Empty':
                #     full_variant_name.insert(0, color_key)
                if len(bpy.data.collections[itemKey].objects) > 1:
                    full_variant_name.append(texture)

                full_variant_name = ' '.join(full_variant_name)
                # full_variant_name = full_variant_name[0].upper() + full_variant_name[1:]

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
