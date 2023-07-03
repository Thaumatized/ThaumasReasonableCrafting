import os

recipeTemplate = '''{
    "type": "minecraft:stonecutting",
    "ingredient": {
        "item": "minecraft:INGREDIENT"
    },
    "result": "minecraft:RESULT",
    "count": COUNT
}
'''

def Clean():
    folder = "ThaumasReasonableCrafting/data/better_cutter/recipes"
    files = os.listdir(folder)
    for file in files:
        filePath = os.path.join(folder, file)
        os.remove(filePath)

def Make(ingredient, result, count = 1):
    count = str(count)
    print("Making " + ingredient + " to " + result)
    path = os.path.join("ThaumasReasonableCrafting/data/better_cutter/recipes", ingredient + "_to_" + result + ".json")
    f = open(path, "w")
    f.write(recipeTemplate.replace("INGREDIENT", ingredient).replace("RESULT", result).replace("COUNT", count))

def id_join(a, b):
    if "*" in b:
        return b.replace("*", a)
    else:
        return a + "_" + b
    
recipes = []
    
def Cobble():
    recipes.append(["stone", "cobblestone", 1])
    recipes.append(["stone", "cobblestone_slab", 2])
    recipes.append(["stone", "cobblestone_stairs", 1])
    recipes.append(["stone", "cobblestone_wall", 1])
    recipes.append(["deepslate", "chiseled_deepslate", 1])

    for block in \
    [
        "cobbled_deepslate",
        "polished_deepslate",
        "deepslate_bricks",
        "deepslate_tiles"
    ]:
        recipes.append(["deepslate", block, 1])
        if block[-1:] == "s":
            block = block[:-1]
        for variant in \
        [
            ["slab", 2],
            ["stairs", 1],
            ["wall", 1]
        ]:
            recipes.append(["deepslate", id_join(block, variant[0]), variant[1]])

def Saw():
    logWoods = \
    [
        "oak",
        "birch",
        "spruce",
        "dark_oak",
        "acacia",
        "jungle",
        "mangrove",
        "cherry",
    ]

    logTypes = \
    [
        "log",
        "wood",
        "stripped_*_log",
        "stripped_*_wood",
    ]
    
    shroomWoods = \
    [
        "crimson",
        "warped"
    ]

    shroomTypes = \
    [
        "stem",
        "hyphae",
        "stripped_*_stem",
        "stripped_*_hyphae",
    ]

    bambooWoods = \
    [
        "bamboo"
    ]

    bambooTypes = \
    [
        "*_block",
        "stripped_*_block"
    ]

    #wood logs
    for wood in logWoods:
        recipes.append([id_join(wood, logTypes[0]), id_join(wood, logTypes[1]), 1])
        recipes.append([id_join(wood, logTypes[0]), id_join(wood, logTypes[2]), 1])
        recipes.append([id_join(wood, logTypes[0]), id_join(wood, logTypes[3]), 1])
        recipes.append([id_join(wood, logTypes[1]), id_join(wood, logTypes[3]), 1])
        recipes.append([id_join(wood, logTypes[2]), id_join(wood, logTypes[3]), 1])
        recipes.append([id_join(wood, logTypes[3]), id_join(wood, "planks"), 4])

    #shroom logs
    for wood in shroomWoods:
        recipes.append([id_join(wood, shroomTypes[0]), id_join(wood, shroomTypes[1]), 1])
        recipes.append([id_join(wood, shroomTypes[0]), id_join(wood, shroomTypes[2]), 1])
        recipes.append([id_join(wood, shroomTypes[0]), id_join(wood, shroomTypes[3]), 1])
        recipes.append([id_join(wood, shroomTypes[1]), id_join(wood, shroomTypes[3]), 1])
        recipes.append([id_join(wood, shroomTypes[2]), id_join(wood, shroomTypes[3]), 1])
        recipes.append([id_join(wood, shroomTypes[3]), id_join(wood, "planks"), 4])

    #bamboo "logs"
    for wood in bambooWoods:
        recipes.append([id_join(wood, bambooTypes[0]), id_join(wood, bambooTypes[1]), 1])
        recipes.append([id_join(wood, bambooTypes[1]), id_join(wood, "planks"), 2])

    plankWoods = logWoods + shroomWoods + ["bamboo"]

    plankBlockTypes = \
    [
        ["stairs", 1],
        ["slab", 2],
        ["fence", 1],
        ["fence_gate", 1],
        ["door", 1],
        ["trapdoor", 1]
    ]

    mosaicBlockTypes = \
    [
        ["stairs", 1],
        ["slab", 2],
    ]

    for wood in plankWoods:
        for blockType in plankBlockTypes:
            recipes.append([id_join(wood, "planks"), id_join(wood, blockType[0]), blockType[1]])
            
    for wood in bambooWoods:
        recipes.append([id_join(wood, "planks"), id_join(wood, "mosaic"), 1])
        mosaic = id_join(wood, "mosaic")
        for blockType in mosaicBlockTypes:
            recipes.append([mosaic, id_join(mosaic, blockType[0]), blockType[1]])

# Make sure that blocks can make stuff that can be made from stuff that is made from them.
# eg. logs > planks > stairs = logs > stairs
def ReverseInheritRecipes():
    changed = True
    while changed:
        changed = False
        print("Reverse Inheriting Recipes")

        for i in range(len(recipes)):
            for j in range(len(recipes)):
                if recipes[i][1] == recipes[j][0]:
                    found = False
                    for l in range(len(recipes)):
                        if recipes[l][0] == recipes[i][0] and recipes[l][1] == recipes[j][1]:
                            found = True
                            if recipes[l][2] < recipes[i][2] * recipes[j][2]:
                                changed = True
                                recipes[l][2] = recipes[i][2] * recipes[j][2]
                    if not found:
                        changed = True
                        recipes.append([recipes[i][0], recipes[j][1], recipes[i][2] * recipes[j][2]])

Clean()
Cobble()
Saw()
ReverseInheritRecipes()
for recipe in recipes:
    Make(recipe[0], recipe[1], recipe[2])