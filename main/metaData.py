# Some code in this file was generously sponsored by the amazing team over at SolSweepers!
# Feel free to check out their amazing project and see how they are using Blend_My_NFTs:
# https://discord.gg/QTT7dzcuVs

# Purpose:
# This file returns the specified meta data format to the Exporter.py for a given NFT DNA.

import bpy
import os
import sys
import importlib
import json
import re

# MetadataAttributeDict = {
#     new_key: new_val
#     for keys, new_val in [(['Null', 'Nulll'], "Null"),
#                          (['Coats','TShirts','LongShirts', 'LongCoats', 'VestHoodie', 'CropShirts'], "Tops"),
#                          (["ThickShorts", "Shorts", "ThickPants", "ThickQuaterPants", "ThinPants", "ThinShorts"], "Bottoms"),
#                          (["ShoesHigh", "ShoesMiddle", "ShoesLow"], "Shoes"),
#                          (["HairLong", "HairShort"], "Headstyle"),
#                          (["Mask", "Glasses"], "Head"),
#                          (["Pack"], "Bag"),
#                          (["Gloves", "LSleave", "RSleave"], "Hands"),
#                          (["NeckWear", "EaringSmall"], "Jewellery"),
#                          (["Plane"], "Background"),
#                          ([""], "Character"),
#                          ([""], "Element")]
#     for new_key in keys
# }
# MetaDataKeys = [
#     "Null",
#     "Character",
#     "Tops",
#     "Bottoms",
#     "Shoes",
#     "Headstyle",
#     "Head",
#     "Bag",
#     "Hands",
#     "Jewellery",
#     "Background",
#     "Element"
#     ]
# # make dict with metadata keys to sort order later
# MetadataAttributeOrder = {MetaDataKeys[v]: v for v in range(len(MetaDataKeys))} 



KeywordAttributeDict = {
    new_key: new_val
    for keys, new_val in [(["Shirt"], "Tops"),
                         (["Pant"], "Bottoms"),
                         (["Outfit"], "Outfit"),
                         (["Feet"], "Shoes"),
                         (["Head", "Face"], "Head"),
                         (["Earing", "Backpack", "Calf", "Neck", "Forearm", "Hands"], "Accessories"),
                         (["Plane", "Background", "Particles"], "Environment"),
                         (["Expression"], "Expression")]
    for new_key in keys
}

KeywordKeys = [
    "Null",
    "Character",
    "Expression",
    # "Color Style",
    "Head",
    "Outfit",
    "Tops",
    "Bottoms",
    "Shoes",
    "Accessories",
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
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(int(batch_num)), "_NFTRecord_{:03d}.json".format(int(batch_num)))      
    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]

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

    attributes.append({"trait_type": "Character", "value": character})

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
                split_variant_name = ' '.join(re.sub("([a-z])([A-Z])","\g<1> \g<2>",variant).split())
                # full_variant_name = [split_variant_name]
                variant = variant[0].upper() + variant[1:]

                full_variant_name = [variant]
                if color_key != 'Empty':
                    full_variant_name.insert(0, color_key)
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


    # split_col_style = ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', style)).split())
    # attributes.append({"trait_type": "Color Style", "value": split_col_style})
    
    # for strand in range(len(DNAString)):
    #     DNASplit = DNAString[strand].split('-')
    #     atttype_index = DNASplit[0]
    #     variant_index = DNASplit[1]
    #     texture_index = DNASplit[2]

    #     slot = list(hierarchy.items())[strand]
    #     att_type = list(slot[1].items())[int(atttype_index)]
    #     variant = list(att_type[1].items())[int(variant_index)][0]

    #     variant_name = variant.split('_')[-1]
    #     split_variant_name = ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', variant_name)).split())

    #     full_variant_name = "{} {}".format(split_variant_name, str(chr(int(texture_index) + 65)))
    #     type_name = str(att_type[0])[3:]
    #     keyword = None
    #     for key in list(KeywordAttributeDict.keys()):
    #         if type_name.startswith(key):
    #             keyword = KeywordAttributeDict[key]
    #             break
            
    #     if keyword:
    #         if not variant_name.endswith("Null"):
    #             dict = {"trait_type": keyword, "value": full_variant_name}
    #             attributes.append(dict)

    attributes = sorted(attributes, key = lambda i:KeywordAttributeOrder[i["trait_type"]])
    metaDataDictErc721["attributes"] = attributes

    return metaDataDictErc721



if __name__ == '__main__':
    returnERC721MetaDataCustom()
