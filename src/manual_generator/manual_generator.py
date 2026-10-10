import pandas
import pathlib
from typing import Literal, Optional

FILE_MONSTER_DROPS = pathlib.Path("../assets/monster_drops_all_dm.csv")
MONSTER_DROPS = pandas.read_csv(FILE_MONSTER_DROPS, sep=",", quotechar='"', quoting=0)
FILE_README = pathlib.Path("../README.md")
with open(FILE_README, 'r') as f:
    README = f.read()

class Item:
    '''
    Class to handle Items as an object with string representation and attributes.

    Attributes:
        item_name:       str                : The name of the item
        storage:         str                : The item one would use to store the item
        monsters:        list[str]          : The monsters that might drop the item
        item_type:       str                : The kind of item
        ingredient_type: list[str]          : If used as an ingredient, things can this item make
        crafting_value:  str                : If used as an ingredient, how much money does it replace
        use:             str                : Use category of the item
        description:     str                : Effect or description of the item
        cooking_effect:  str                : Effect when cooked in a meal
        find_checks:     dict[str:list[str]]: Ability checks one might use to harvest or find the item as treasure
        find_dc:         dict[str:list[str]]: The DC for the Ability checks to find or harvest the item
        location:        dict[str:list[str]]: The location that the monsters that drop the item are in
    '''
    def __init__(
            self,
            item_name:str,
            storage:str,
            monsters:str,
            item_type:str,
            ingredient_type:str,
            crafting_value:str,
            use:str,
            description:str,
            cooking_effect:str,
            find_checks:str,
            find_dc:str,
            location:str,
            source:str,
            ):
        self.item_name = item_name
        self.storage = storage
        monsters = [m.strip() for m in monsters.split(",") if m.strip()!=""]
        self.monsters = monsters
        self.item_type = item_type
        self.item_category = item_type.split("(")[0].strip()
        self.rarity = item_type.split("(")[1].strip()[:-1] if "(" in item_type else item_type
        self.attunement = "Requires Attunement" in item_type
        self.ingredient_type = [ing.strip() for ing in ingredient_type.split(",") if ing.strip()!=""]
        self.crafting_value = [crf.strip() for crf in crafting_value.split(", ") if crf.strip()!=""]
        self.use = [u.strip() for u in use.split(",") if u.strip()!=""]
        self.description = description
        self.cooking_effect = cooking_effect
        checks = [fch.strip() for fch in find_checks.split(",") if fch.strip()!=""]
        self.find_checks = {
            monster:[
                fch.split("(")[0].strip() for fch in checks
                if f"({monster})" in fch or not "(" in fch
                ]
            for monster in self.monsters
        }
        dcs = [dc.strip() for dc in find_dc.split(",")]
        find_dcs = {
            monster:[
                dc for dc in dcs
                if f"({monster})" in dc or len(dc.split(")"))<3
                ]
            for monster in self.monsters
        }
        find_dc = dict()
        for mon,mdcs in find_dcs.items():
            priority_dcs = [mdc.replace(f"({mon})","") for mdc in mdcs if mon in mdc]
            priority_dcs_num = [pdc.split("(")[0] for pdc in priority_dcs]
            other_dcs = [mdc for mdc in mdcs if mon not in mdc and mdc.split("(")[0] not in priority_dcs_num]
            all_dcs = sorted(priority_dcs + other_dcs)
            find_dc[mon]=all_dcs
        self.find_dc = find_dc
        locs = [loc.strip() for loc in location.split(",")]
        self.location = {
            monster:[
                loc.replace(f"({monster})","") for loc in locs
                if f"({monster})" in loc 
                or not "(" in loc 
                or not any(mon in loc for mon in self.monsters)
                ]
            for monster in self.monsters
        }
        sources = [src.strip() for src in source.split(",")]
        self.source = {
            monster:[
                src.split("(")[0].strip() for src in sources
                if f"({monster})" in src or not "(" in src
                ]
            for monster in self.monsters
        }
    def __str__(self):
        out = f"**{self.item_name}**  \n"
        out+= f"---  \n"
        out+= f"**Monster(s)**: {", ".join(self.monsters)}  \n"
        all_sources = [src for src in self.source.values()]
        if len(self.monsters)>1 and not all(x==all_sources[0] for x in all_sources):
            out += f""
            for mon, sources in self.source.items():
                out += f"**Source ({mon})**: {", ".join(sources)}  \n"
            out = out[:-4]
            out += "  \n"
        else:
            out+= f"**Source**: {", ".join(self.source[self.monsters[0]])}  \n"
        if self.item_type[0]!="-":
            out+= f"_{self.item_type}_  \n"
        if self.ingredient_type[0]!="-":
            out+= f"**Use as ingredient for**: _{", ".join(self.ingredient_type)}_  \n"
        if self.crafting_value[0]!="-":
            out+= f"**Crafting Value (when used as ingredient)**: _{", ".join(self.crafting_value)}_  \n"
        if self.use[0]!="-":
            out+= f"**Use**: _{", ".join(self.use)}_  \n"
        if self.description != "-":
            out+= f"**Description**: {self.description}  \n\n"
        if self.cooking_effect != "-":
            out+= f"**Cooking Effect**: {self.cooking_effect}  \n\n"
        if len(self.monsters)>1:
            out += f""
            for mon, checks in self.find_checks.items():
                if "-" not in checks and "Crafted Item" not in checks:
                    out += f"**Find Checks ({mon})**: {", ".join(checks)}  \n"
            if self.find_checks[self.monsters[0]][0] == "Crafted Item":
                out+= f"_Crafted Item_  \n"
            out = out[:-3]
            out += "  \n"
        else:
            if self.find_checks[self.monsters[0]][0] == "Crafted Item":
                out+= f"_Crafted Item_  \n"
            elif self.find_checks[self.monsters[0]][0] != "-":
                out+= f"**Find Checks**: {", ".join(self.find_checks[self.monsters[0]])}  \n"
        if len(self.monsters)>1:
            out += f""
            for mon, dcs in self.find_dc.items():
                if "-" not in dcs:
                    out += f"**Find DCs ({mon})**: {", ".join(dcs)}  \n"
            out = out[:-3]
            out += "  \n"
        else:
            if self.find_dc[self.monsters[0]][0] != "-":
                out+= f"**Find DCs**: {", ".join(self.find_dc[self.monsters[0]])}  \n"
        if len(self.monsters)>1:
            out += f""
            for mon, loc in self.location.items():
                if "-" not in loc:
                    out += f"**Locations ({mon})**: {", ".join(loc)}  \n"
            out = out[:-3]
            out += "  \n"
        else:
            if self.location[self.monsters[0]][0] != "-":
                out+= f"**Locations**: {", ".join(self.location[self.monsters[0]])}  \n"
        return out


class ManualGenerator:
    '''
    Class to output items organized by different things. For now:
        by_item()   : A simple output of the CSV as Markdown
        by_monster(): A filtered output organized by monster, with repeated items when it is dropped by other monsters
    '''
    def __init__(
            self,
            version:Literal[
                "dm",
                "player"
                ]="dm",
            mode:Literal[
                "by_item",
                "by_monster",
                ]="by_item",
            sourcefile:Optional[pandas.DataFrame]=None,
            ):
        self.version = version
        self.mode = mode
        sourcefile = MONSTER_DROPS if sourcefile is None else sourcefile
        if self.version=="dm":
            self.items = [Item(*sourcefile.loc[x]) for x in range(len(sourcefile))]
        elif self.version=="player":
            self.items = []
            for x in range(len(sourcefile)):
                row = sourcefile.loc[x]
                self.items.append(Item(
                    item_name=row.item_name,
                    storage=row.storage,
                    monsters=row.monsters,
                    item_type=row.item_type.split("(DM Eyes only:")[0],
                    ingredient_type=row.ingredient_type.split("(DM Eyes only:")[0],
                    crafting_value=row.crafting_value.split("(DM Eyes only:")[0],
                    use=row.use.split("(DM Eyes only:")[0],
                    description=row.description.split("(DM Eyes only:")[0],
                    cooking_effect=row.cooking_effect.split("(DM Eyes only:")[0],
                    find_checks="Crafted Item" if "Crafted Item" in row.find_checks else "-",
                    find_dc="-",
                    location="-",
                    source=row.source,
                    ))
    def by_item(self):
        if self.version == "dm":
            out = "  \n\n".join(
                [
                    f"### {item.item_name}  \n\n" + \
                    str(item)\
                    .replace(f"**{item.item_name}**  \n","")
                    for item in self.items
                ]
            )
        else:
            out = "  \n\n".join(
                [
                    f"### {item.item_name}  \n\n" + \
                    str(item)\
                    .replace(f"**{item.item_name}**  \n","")\
                    .replace(f"**Monster(s)**: {", ".join(item.monsters)}  \n","")
                    for item in self.items
                ]
            )
        return out
    @classmethod
    def item_to_items_by_monster(cls, item):
        if len(item.monsters)==1:
            items = [item]
        else:
            items = []
            for monster in item.monsters:
                items.append(Item(
                    item_name=item.item_name,
                    storage=item.storage,
                    monsters=monster,
                    item_type=item.item_type,
                    ingredient_type=", ".join(item.ingredient_type),
                    crafting_value=", ".join(item.crafting_value),
                    use=", ".join(item.use),
                    description=item.description,
                    cooking_effect=item.cooking_effect,
                    find_checks=f"({monster}), ".join(item.find_checks[monster]),
                    find_dc=f"({monster}), ".join(item.find_dc[monster]),
                    location=f"({monster}), ".join(item.location[monster]),
                    source=f"({monster}), ".join(item.source[monster]),
                    ))
        return items
    def by_monster(self):
        monsters = sorted(list(set([mon for item in self.items for mon in item.monsters])))
        out = ""
        for monster in monsters:
            out+= f"### {monster}  \n\n"
            gen_items = [item for item in self.items if monster in item.monsters]
            monster_items = []
            for gi in gen_items:
                split_items = self.item_to_items_by_monster(gi)
                monster_items += [item for item in split_items if monster in item.monsters]
            out+="  \n\n".join(
                [
                    f"#### {mi.item_name}  \n\n" + \
                    str(mi)\
                    .replace(f"**{mi.item_name}**  \n","")\
                    .replace(f"Monster(s): {monster}  \n","")
                    for mi in monster_items
                ]
            )
            out+="  \n\n"
        return out
    def __str__(self):
        out = ""
        out+= README
        out+= "\n  \n\n"
        if self.mode=="by_item":
            out+= "## Harvesting Items (By item and in order of appearance)  \n\n"
            out+= self.by_item()
        elif self.mode=="by_monster":
            out+= "## Harvesting Items (By Monster, repeating items where necessary)  \n\n"
            out+= self.by_monster()
        return out
    
