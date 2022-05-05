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

MetadataAttributeDict = {
    new_key: new_val
    for keys, new_val in [(['Null', 'Nulll'], "Null"),
                         (['Coats','TShirts','LongShirts', 'LongCoats', 'VestHoodie', 'CropShirts'], "Tops"),
                         (["ThickShorts", "Shorts", "ThickPants", "ThickQuaterPants", "ThinPants", "ThinShorts"], "Bottoms"),
                         (["ShoesHigh", "ShoesMiddle", "ShoesLow"], "Shoes"),
                         (["HairLong", "HairShort"], "Headstyle"),
                         (["Mask", "Glasses"], "Head"),
                         (["Pack"], "Bag"),
                         (["Gloves", "LSleave", "RSleave"], "Hands"),
                         (["NeckWear", "EaringSmall"], "Jewellery"),
                         (["Plane"], "Background"),
                         ([""], "Character"),
                         ([""], "Element")]
    for new_key in keys
}

MetaDataKeys = [
    "Null",
    "Character",
    "Tops",
    "Bottoms",
    "Shoes",
    "Headstyle",
    "Head",
    "Bag",
    "Hands",
    "Jewellery",
    "Background",
    "Element"
    ]
# make dict with metadata keys to sort order later
MetadataAttributeOrder = {MetaDataKeys[v]: v for v in range(len(MetaDataKeys))} 


def returnCardanoMetaData(name, NFT_DNA, NFT_Variants):
    metaDataDictCardano = {"721": {
        "<policy_id>": {
            name: {
                "name": name,
                "image": "",
                "mediaType": "",
                "description": "",

            }
        },
        "version": "1.0"
    }}

    for i in NFT_Variants:
        metaDataDictCardano["721"]["<policy_id>"][name][i] = NFT_Variants[i]

    return metaDataDictCardano

def returnSolanaMetaData(name, NFT_DNA, NFT_Variants):
    metaDataDictSolana = {"name": name, "symbol": "", "description": "", "seller_fee_basis_points": None,
                          "image": "", "animation_url": "", "external_url": ""}

    attributes = []

    for i in NFT_Variants:
        dictionary = {
            "trait_type": i,
            "value": NFT_Variants[i]
        }

        attributes.append(dictionary)

    metaDataDictSolana["attributes"] = attributes
    metaDataDictSolana["collection"] = {
        "name": "",
        "family": ""
    }

    metaDataDictSolana["properties"] = {
        "files": [{"uri": "", "type": ""}],
        "category": "",
        "creators": [{"address": "", "share": None}]
    }
    return metaDataDictSolana

def returnErc721MetaData(name, NFT_DNA, NFT_Variants):
    metaDataDictErc721 = {
        "name": name,
        "description": "",
        "image": "",
        "attributes": None,
    }

    attributes = []

    for i in NFT_Variants:
        dictionary = {
            "trait_type": i,
            "value": NFT_Variants[i]
        }

        attributes.append(dictionary)

    metaDataDictErc721["attributes"] = attributes

    return metaDataDictErc721



def returnERC721MetaDataCustom(name, DNA):
    batch_json_save_path = bpy.context.scene.my_tool.batch_json_save_path
    NFTRecord_save_path = os.path.join(batch_json_save_path, "Batch_{:03d}".format(1), "_NFTRecord_{:03d}.json".format(1))      
    DataDictionary = json.load(open(NFTRecord_save_path))
    hierarchy = DataDictionary["hierarchy"]

    metaDataDictErc721 = {
        "name": name,
        # "name": "Kae #0257",
        "description": "This is a test meta data file",
        "image": "Link to IPFS?",
        "attributes": None,
    }

    attributes = []

    DNAString = DNA.split(",")
    character = DNAString.pop(0)
    # metaDataDictErc721["name"] = str(character + ": #0123")

    attributes.append({"trait_type": "Character", "value": character})

    for strand in range(len(DNAString)):
        DNASplit = DNAString[strand].split('-')
        atttype_index = DNASplit[0]
        variant_index = DNASplit[1]
        texture_index = DNASplit[2]

        slot = list(hierarchy.items())[strand]

        atttype = list(slot[1].items())[int(atttype_index)]
        variant = list(atttype[1].items())[int(variant_index)][0]

        variant_type = variant.split('_')[1]
        description = variant.split('_')[2]
        split_description = ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', description)).split())
        split_variant_type = ' '.join(re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', variant_type)).split())

        attribute_type = "{} {}".format(split_variant_type, split_description)
        attribute = MetadataAttributeDict[variant.split('_')[1]]
        if variant_type not in ["Null", "Nulll", "Block"]:
            dict = {"trait_type": attribute, "value": attribute_type}
            attributes.append(dict)

    attributes = sorted(attributes, key = lambda i:MetadataAttributeOrder[i["trait_type"]])
    metaDataDictErc721["attributes"] = attributes
    metaDataObj = json.dumps(metaDataDictErc721, indent=1, ensure_ascii=True)
    with open("TestMetaData.json", "w") as outfile:
            outfile.write(metaDataObj)
    return metaDataDictErc721





if __name__ == '__main__':
    returnSolanaMetaData()
    returnCardanoMetaData()
    returnErc721MetaData()
