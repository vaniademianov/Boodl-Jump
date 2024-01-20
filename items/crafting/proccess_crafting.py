import pygame
from inventory.slot import Slot 
import os, pathlib
import importlib
from items.crafting.crafting_ingredient import CraftingIngredient
class ProcessCraft:
    def __init__(self, grid_type,input_slots: list[Slot], result_slot: Slot) -> None:
        self.input_slots = input_slots
        self.result_slot = result_slot
        self.grid_type = grid_type
        # LOAD RECIPES
        self.recipes = []
        self.crafting_recipes_dir = "items/crafting/crafting_recipes"
        for recipe_name in os.listdir(self.crafting_recipes_dir):
            if os.path.isfile(os.path.join(self.crafting_recipes_dir, recipe_name)):
                recipe_imported = importlib.import_module('items.crafting.crafting_recipes.' +recipe_name.split(".")[0])
                recipe_class = recipe_imported.Recipe()
                self.recipes.append(recipe_class)
        self.last_r = None 
    def take(self):
        if self.last_r != None: 
            self.last_r.take_it(self.input_slots, self.grid_type.lines)
    def tick(self):
        # check slots 
        for recipe in self.recipes:
            ev:CraftingIngredient = recipe.eval(self.input_slots, self.grid_type.lines)
            if ev.item != None: 
                # we found the recipe 
                if self.result_slot.item == None: 
                    self.result_slot.count = ev.count
                    self.result_slot.update_activity(ev.item,False)
                    self.last_r = recipe
                    return self.take 
                break   
        
if __name__ == "__main__":
    p = ProcessCraft()