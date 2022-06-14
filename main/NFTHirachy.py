from pickle import NONE
import bpy
import os
import re
import copy
import time
import json
import random
import importlib
from functools import partial

from . import config


def createHirachy():
   # rarity_from_name = bool whether rarity in new heirarchy should use either 'collection custom property rarity' or 'collection name rarity'
   unsortedttributeList = {} 
   coll = bpy.context.scene.collection.children
   
   for i in range(len(coll)):
      unsortedttributeList[coll[i].name] = {}

   if "Script_Ignore" in unsortedttributeList:
      del unsortedttributeList["Script_Ignore"]

   if "Scene Collection" in unsortedttributeList:
      del unsortedttributeList["Scene Collection"]

   if "Master Collection" in unsortedttributeList:
      del unsortedttributeList["Master Collection"]

   sortedAttributeKeys = sorted(unsortedttributeList)
   sortedAttibutes = {}
   for key in sortedAttributeKeys:
      sortedAttibutes[key] = unsortedttributeList[key]

   #loop through all atributes in scene
   for attribute in sortedAttibutes:
      unsortedAttributeType = {}
      _attributeTypes = bpy.data.collections[attribute].children

      for i in range(len(_attributeTypes)):
         Varients = {}
         _varients = bpy.data.collections[_attributeTypes[i].name].children
         
         for j in range(len(_varients)):

            if not _varients[j].name.rpartition('_')[2] in config.Characters: # check if char variation mesh
               Varients[_varients[j].name] = attributeData(_varients[j], _attributeTypes[i], attribute)

         #Varients.sort()
         unsortedAttributeType[_attributeTypes[i].name] = Varients

      sortedAttributeTypeKeys = sorted(unsortedAttributeType)
      sortedAttibutetype = {}
      for key in sortedAttributeTypeKeys:
         sortedAttibutetype[key] = unsortedAttributeType[key]
      
      sortedAttibutes[attribute] = sortedAttibutetype
   return sortedAttibutes


def attributeData(attributeVariantColl, attributeTypeColl, attribute):
   attributeVariant = attributeVariantColl.name
   eachObject={}
   """
   Creates a dictionary of each attribute
   """

   def getName(i):
      """
      Returns the name of "i" attribute name, attribute genre, attribute variant
      """
      name = i.split("_")
      return name

   def getOrder_rarity(i):
      """
      Returns the "order", "type_rarity", varient_rarity and texture rarity
      """
      a = [''] * 8
      a[0] = i.rsplit('_', 1)[1]
      
      if(attributeTypeColl.get('rarity') is not None):
         a[1] = attributeTypeColl.get('rarity')
      else:
         a[1] = attributeTypeColl['rarity'] = 50

      if(attributeVariantColl.get('rarity') is not None):
         a[2] = attributeVariantColl.get('rarity')
      else:
         a[2] = attributeVariantColl['rarity'] = 50

      # if(attributeTextureColl.get('rarity') is not None):
      #    a[3] = attributeTextureColl.get('rarity')
      # else:
      #    a[3] = attributeTextureColl['rarity'] = 50

      # if(attributeVariantColl.get('Style') is not None):
      #    a[3] = attributeVariantColl.get('Style')
      # else:
      #    a[3] = attributeVariantColl['Style'] = "Temp_Style"

      # if(attributeVariantColl.get('color_primary') is not None):
      #    a[4] = attributeVariantColl.get('color_primary')
      # else:
      #    a[4] = attributeVariantColl['color_primary'] = "0"

      # if(attributeVariantColl.get('color_secondary') is not None):
      #    a[5] = attributeVariantColl.get('color_secondary')
      # else:
      #    a[5] = attributeVariantColl['color_secondary'] = "0"

      # if(attributeVariantColl.get('color_tertiary') is not None):
      #    a[6] = attributeVariantColl.get('color_tertiary')
      # else:
      #    a[6] = attributeVariantColl['color_tertiary'] = "0"

      # x = re.sub(r'[a-zA-Z]', "", i)
      # a = x.split("_")
      # del a[0] #Remove Attribute Name
      # del a[0] #Remove Genre Name
      # del a[0] #Remove ItemName Name
      return list(a)

   def get_textureSets(variant_coll):
      textures = {}
      for mesh in variant_coll.objects:
         # print(mesh.material_slots[0])
         if mesh.get('rarity') is not None:
            textures[mesh.name] = int(mesh.get('rarity'))
         else:
            textures[mesh.name] = 50
         # textures.append(mesh.name)
      return textures
      
   name = getName(attributeVariant)
   orderRarity = getOrder_rarity(attributeVariant)

   if len(orderRarity) == 0:
      return

   elif len(orderRarity) > 0:
      
      item_attribute = attribute
      item_type = attributeTypeColl.name
      number = name[2]
      item_variant = name[3]
      textureSets = get_textureSets(attributeVariantColl)

      if(item_type != "Null"):
         type_rarity = orderRarity[1]
         variant_rarity = orderRarity[2]
      else:
         type_rarity = 0.0
         variant_rarity = 0.0

      
      eachObject = {"item_attribute" : item_attribute, "item_type": item_type, "item_variant": item_variant, "item_index": number,
                     "type_rarity": type_rarity, "variant_rarity": variant_rarity, "textureSets": textureSets}
      
   return eachObject