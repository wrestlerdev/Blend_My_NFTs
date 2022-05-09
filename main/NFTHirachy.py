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
            Textures = {}
            _textures = _varients[j].children

            for k in range(len(_textures)):
               print(_textures[k])
               if not _textures[k].name.rpartition('_')[2] in config.Characters: # check if char variation mesh
                  Textures[_textures[k].name] = attributeData(_textures[k], _varients[j], _attributeTypes[i])

            if not _varients[j].name.rpartition('_')[2] in config.Characters: # check if char variation mesh
               Varients[_varients[j].name] = Textures

         #Varients.sort()
         unsortedAttributeType[_attributeTypes[i].name] = Varients

      sortedAttributeTypeKeys = sorted(unsortedAttributeType)
      sortedAttibutetype = {}
      for key in sortedAttributeTypeKeys:
         sortedAttibutetype[key] = unsortedAttributeType[key]
      
      sortedAttibutes[attribute] = sortedAttibutetype
   return sortedAttibutes


def attributeData(attributeTextureColl, attributeVariantColl, attributeTypeColl):
   attributeVariant = attributeVariantColl.name
   attributeTexture = attributeTextureColl.name
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

      if(attributeTextureColl.get('rarity') is not None):
         a[3] = attributeTextureColl.get('rarity')
      else:
         a[3] = attributeTextureColl['rarity'] = 50

      a[4] = attributeTextureColl["color_style"]
      a[5] = attributeTextureColl["color_primary"]
      a[6] = attributeTextureColl["color_secondary"]
      a[7] = attributeTextureColl["color_tertiary"]

      # x = re.sub(r'[a-zA-Z]', "", i)
      # a = x.split("_")
      # del a[0] #Remove Attribute Name
      # del a[0] #Remove Genre Name
      # del a[0] #Remove ItemName Name
      return list(a)

   def get_textureSet():

      textureSet = name[4]
      return textureSet
      

   name = getName(attributeTexture)
   orderRarity = getOrder_rarity(attributeTexture)

   if len(orderRarity) == 0:
      return

   elif len(orderRarity) > 0:
      number = name[3]
      slotName = name[0]
      clothingGenre = name[1]
      clothingItem = name[2]
      textureSet = get_textureSet()
      colorstyle = name[4]
      colorprimary = name[5]
      colorseoncdary = name[6]
      colortertiary = name[7]

      if(clothingGenre != "Null"):
         type_rarity = orderRarity[1]
         variant_rarity = orderRarity[2]
         texture_rarity = orderRarity[3]
      else:
         type_rarity = 0.0
         variant_rarity = 0.0
         texture_rarity = 0.0



      
      
      eachObject = {"slotName" : slotName, "clothingGenre": clothingGenre, "clothingItem": clothingItem, "clothingVersion": number,
                     "textureSet": textureSet, "texture_rarity": texture_rarity, "variant_rarity": variant_rarity, "type_rarity": type_rarity, 
                     "color_style": colorstyle, "color_primary": colorprimary, "color_secondary": colorseoncdary, "color_tertiary": colortertiary }
      
   return eachObject