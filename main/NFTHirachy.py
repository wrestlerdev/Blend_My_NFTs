import bpy
import os
import re
import copy
import time
import json
import random
import importlib
from functools import partial


def createHirachy():
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
            Varients[_varients[j].name] = attributeData(_varients[j].name)

         #Varients.sort()
         unsortedAttributeType[_attributeTypes[i].name] = Varients

      sortedAttributeTypeKeys = sorted(unsortedAttributeType)
      sortedAttibutetype = {}
      for key in sortedAttributeTypeKeys:
         sortedAttibutetype[key] = unsortedAttributeType[key]
      
      sortedAttibutes[attribute] = sortedAttibutetype

   firstAttribute = list(sortedAttibutes.values())[0]
   firstType = list(firstAttribute.values())[0]
   firstVarient = list(firstType.values())[0]

   print(firstVarient)
   print(sortedAttibutes)
   return sortedAttibutes


def attributeData(attributeVariant):
   eachObject={}
   """
   Creates a dictionary of each attribute
   """
   
   def getName(i):
      """
      Returns the name of "i" attribute name, attribute genre, attribute variant
      """
      name = i.split("_")[:3]
      return name

   def getOrder_rarity(i):
      """
      Returns the "order", "rarity" and "color" (if enabled) of i attribute variant in a list
      """
      x = re.sub(r'[a-zA-Z]', "", i)
      a = x.split("_")
      del a[0] #Remove Attribute Name
      del a[0] #Remove Genre Name
      del a[0] #Remove ItemName Name
      return list(a)
      

   name = getName(attributeVariant)
   orderRarity = getOrder_rarity(attributeVariant)

   if len(orderRarity) == 0:
      return

   elif len(orderRarity) > 0:
      number = orderRarity[0]
      rarity = orderRarity[1]
      color = "0"

      slotName = name[0]
      clothingGenre = name[1]
      clothingItem = name[2]
      
      eachObject = {"slotName" : slotName, "clothingGenre": clothingGenre, "clothingItem": clothingItem, "number": number, "rarity": rarity, "color": color}
   return eachObject