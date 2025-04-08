from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from player import Player

import gameboard


class GameSquare:
    def __init__(self, name: str, price: int, rent: int, space: str, color: str, is_utility: bool, is_railroad: bool):
        """Constructor for the GameSquare class"""
        self.__name: str = name
        self.__price: int = price
        self.__rent: int  = rent
        self.__color: str = color
        self.__space: str = space
        self.__is_utility: bool = is_utility
        self.__is_railroad: bool = is_railroad
        self.__owner: Player | None = None

        #add an is_mortgaged attribute
        self.__is_mortgaged: bool = False

    # accessor methods
    @property
    def owner(self) -> Player | None:
        return self.__owner

    @owner.setter
    def owner(self, owner: Player | None):
        self.__owner = owner

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> int:
        return self.__price

    @property
    def rent(self) -> int:
        return self.__rent

    @property
    def color(self) -> str:
        return self.__color

    @property
    def space(self) -> str:
        return self.__space

    @property
    def is_utility(self) -> bool:
        return self.__is_utility

    @property
    def is_railroad(self) -> bool:
        return self.__is_railroad

    @property
    def is_mortgaged(self) -> bool:
        return self.__is_mortgaged

    #Add methods to mortgage and unmortgage a property
    #remember to add a 10% fee to unmortgage
    def mortgage(self) -> bool:
        assert self.owner != None
        """Function to mortgage a property
        return True if mortgaging was successful and False otherwise"""
        amt = self.price // 2
        if not self.__is_mortgaged:
            self.__is_mortgaged = True
            self.owner.money += amt
            return True
        return False

    def unmortgage(self) -> bool:
        assert self.owner != None
        """Function to unmortgage a property if the player has the money
        and the property is currently mortgaged
        return True if the unmortgage was successful and False otherwise"""
        # add a 10% fee to unmortgage
        amt = self.price // 2
        amt = amt + amt // 10

        if self.owner.money >= amt and self.__is_mortgaged:
            self.__is_mortgaged = False
            self.owner.money -= amt
            return True

        return False

    def can_be_purchased(self) -> bool:
        """Function to determine if a square can be purchased"""
        if self.owner is None:
            if (self.space == "Tax" or self.space == "Chance" or self.space == "Chest"
                    or self.space == "GoToJail" or self.space == "Jail"
                    or self.space == "Parking" or self.space == "Go"):
                return False
            else:
                return True
        else:
            return False

    def calculate_rent_or_tax(self, dice_sum) -> int:
        """Function to calculate the rent or tax for a square"""

        if self.owner is None and self.space != "Tax" or self.__is_mortgaged:
            return 0
        if self.is_utility:
            return 4 * dice_sum
        if self.is_railroad:
            assert self.owner != None
            return 25 * (2 ** (self.owner.railroad_count - 1))

        return self.rent

    def __str__(self) -> str:
        """Function to return a string representation of the GameSquare object"""
        return f"{self.name} - {self.price} - {self.rent}"
