import pandas
import pathlib
import textwrap
from typing import Literal, Optional

class ShopItem:
    '''
    Class to handle shop menu items with different CSV head row indexes, as long as some remain in common.

    Attributes:
        item_name:   str          : The name of the item
        cost:        str          : The item cost in the shop (string to add units)
        description: str          : The item description
        details:     dict[str:str]: The other columns in the shop menu gathered in a dictionary
    '''
    def __init__(
        self,
        shop_item_csv_row:pandas.Series,
        indexes:Optional[dict[str,str]]={
            "item_name_index":"Name",
            "cost_index":"Cost",
            "description_index":"Description",
            }
        ):
        self.item_name = shop_item_csv_row[indexes["item_name_index"]]
        self.cost = shop_item_csv_row[indexes["cost_index"]]
        self.description = shop_item_csv_row[indexes["description_index"]]
        index_list = list(indexes.values())
        self.details = dict(
                [
                    i for i in shop_item_csv_row.items()
                    if i[0] not in index_list
                ]
            )
    def __str__(self):
        out = f"**{self.item_name}**, **{self.cost}** \n"
        for key,det in self.details.items():
            if det != "" and det != "-":
                if "source" in key or "Source" in key:
                    out += f"*__{key}__: {det}*  \n"
                else:
                    out += f"__{key}__: {det}  \n"
        if self.description != "" and self.description != "-":
            out += f"{self.description} \n"
        return out


class ShopMenu:
    '''
    Class to handle shop menus with different CSV head row indexes, as long as some remain in common.
    
    Attributes:
        shop_items:   list[ShopItem]: ?
        indexes:
            item_name_index:   str: The name of the item, it has to have the CSV head row index "Name" or "name"
            cost_index:        str: The item cost in the shop (string to add units), it has to have the CSV head row index "Cost" or "cost", or "Price" or "price"
            description_index: str: The item description, it has to have the CSV head row index "Description" or "description"
    
    The indexes will be detected before use.
    '''
    def __init__(
        self,
        sourcefile:pandas.DataFrame,
        shop_name: str,
        ):
        # first matches only
        self.indexes = {
            "item_name_index":[ind for ind in ["Name","name"] if ind in sourcefile.columns][0],
            "cost_index":[ind for ind in ["Cost","cost","Price","price"] if ind in sourcefile.columns][0],
            "description_index":[ind for ind in ["Description","description"] if ind in sourcefile.columns][0]
            }
        self.shop_items = [ShopItem(sourcefile.loc[x],self.indexes) for x in range(len(sourcefile))]
        self.shop_name = shop_name
    def __str__(self):
        out = f"## {self.shop_name} \n\n"
        item_list = []
        for item in self.shop_items:
            item_title = textwrap.dedent(f"""
            <h3>{item.item_name}
                <span style='display:inline; float: right;'>
                    <em>{item.cost}</em>
                </span>
            </h3>  \n\n\n""")
            list_add = item_title + \
                    str(item)\
                    .replace(f"**{item.item_name}**, **{item.cost}** \n","")
            item_list.append(list_add)
        out += "  \n\n".join(item_list)
        return out