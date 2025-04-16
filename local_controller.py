import os
import random
import gameboard
from gamesquare import Player
import player as plr # avoid naming conflict with the player module
import observer

import json

class LocalController(observer.Observer):
    """Control the game flow"""

    def __init__(self):
        super().__init__()

        csv_path = os.path.join("resources", "data", "board.csv")
        players = self._create_players(3)
        self._gameboard: gameboard.GameBoard = gameboard.GameBoard(csv_path, players)

        self._add_listeners()

        self.__dice_rolled: bool = False

        self.__roll_count: int = 0

        observer.Event("update_state", f"{self._gameboard.get_current_player().name}'s turn")
        observer.Event("update_players_state", self._gameboard.to_dicts())

        self._set_expected_val()


    def _add_listeners(self):
        """Add listeners to the view"""
        self.observe("roll", "_roll_action")
        self.observe("end_turn", "_end_player_turn")
        self.observe("purchase", "_buy_square")
        self.observe("mortgage", "_mortgage")
        self.observe("mortgage_specific", "_mortgage_specific")
        self.observe("unmortgage", "_unmortgage")
        self.observe("save", "_save")
        self.observe("load", "_load")

    # TODO: Implement
    def _save(self, save_name: str):
        """Save the game to disk"""

        save_game = {}
        save_game |= {"dice_rolled": self.__dice_rolled, "roll_count": self.__roll_count}
        save_game |= {"board": self._gameboard.save()}

        save_path = os.path.join("saves", save_name+".json")
        with open(save_path, 'w') as file:
            json.dump(save_game, file)

    # TODO: Implement
    def _load(self, save_name: str):
        """Load the game from disk"""
        save_game = {}

        save_path = os.path.join("saves", save_name+".json")
        with open(save_path, 'r') as file:
            save_game = json.load(file)
        
        self.__roll_count = save_game['roll_count']
        self.__dice_rolled = save_game['dice_rolled']

        self._gameboard.load(save_game['board'])

        observer.Event("update_players_state", self._gameboard.to_dicts())
        observer.Event("update_card", self._gameboard.get_current_player().position)

        
            
    def _test_observers(self, data):
        """Test the observer pattern"""
        print("observed event roll")

    def _create_players(self, num_players: int) -> list[Player]:
        """Create num_players players and return a list of them"""
        players = []
        for i in range(num_players):
            player = plr.Player(i, f"Player {i}", 1500)
            players.append(player)
        return players

    def _set_expected_val(self):
        ev = self._gameboard.calculate_expected_value(self._gameboard.get_current_player().position, 0)
        ev = round(ev, 2)
        observer.Event("update_state", f"Expected value: {ev}")

        player = self._gameboard.get_current_player()
        # add the expected value to the player's luck
        player.luck += ev

    def _roll_dice(self):
        """Simulate the rolling of two dice
            :return the sum of two random dice values
        """
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        dice_sum = dice1 + dice2

        self.__dice_rolled = True
        self.__roll_count += 1

        if dice1 == dice2:
            #double rolled
            observer.Event("update_state", f"Doubles rolled: {dice1}+{dice2} = {dice_sum}")
            self.__dice_rolled = False
        else:
            observer.Event("update_state", f"Dice rolled: {dice1} + {dice2} = {dice_sum}")
        return dice_sum

    def _handle_roll_dice(self):
        """Function to handle the roll dice button click event"""

        if self.__dice_rolled:
            #only one roll per turn
            observer.Event("update_state", "One roll per turn or Doubles required")
            return False

        dice_sum = self._roll_dice()
        player = self._gameboard.get_current_player()

        #move the player if posible
        if player.can_move:
            player.move(dice_sum)
        position = player.position
        square = self._gameboard.get_square(position)

        if square.space == "GoToJail":
            print("Going to jail")
            player.goto(40) # Teleport player to jail

            position = player.position
            square = self._gameboard.get_square(position)

        #pay the rent
        #should check if the player has money and if not
        #give them the chance to trade or mortgage
        rent = player.pay_rent(square,dice_sum)
        if rent != 0:
            print(f"rent paid: {rent}")
            player.luck -= rent
            observer.Event("update_state", f"Rent paid: {rent}")

        #no money left?
        if player.money < 0:
            player.declare_bankrupt()

        return True

    def _end_player_turn(self, callback):
        """End the current player's turn"""

        if not self.__dice_rolled:
            #player must roll the dice first
            observer.Event("update_state", "Roll the dice first")
            return
        self.__dice_rolled = False
        self.__roll_count = 0
        player_name = self._gameboard.next_turn()
        observer.Event("update_players_state", self._gameboard.to_dicts())
        observer.Event("update_card", self._gameboard.get_current_player().position)
        callback()
        observer.Event("update_state", f"{player_name}'s turn")

        self._set_expected_val()

    def _buy_square(self, data):
        """try to buy the square the active player is currently on"""

        if (self.__roll_count == 0):
            observer.Event("update_state", "Roll the dice first")
            return
        player = self._gameboard.get_current_player()
        position = player.position
        square = self._gameboard.get_square(position)
        buy = player.buy_property(square)
        if buy:
            print(f"Square bought {square}")
            observer.Event("update_state",f"Square bought: {square}" )
        else:
            observer.Event("update_state",f"Square not bought: {square}" )

        observer.Event("update_players_state", self._gameboard.to_dicts())

    def _mortgage(self, data):
        """Player has indicated an interest in mortgaging a property
        return their choices as a list of names"""
        player = self._gameboard.get_current_player()
        deeds = player.properties
        # only return the deeds that can be mortgaged
        observer.Event("choice", [d.name for d in deeds if not d.is_mortgaged])
        observer.Event("update_players_state", self._gameboard.to_dicts())


    def _mortgage_specific(self, deed_name):
        """Mortgage a specific property"""
        player = self._gameboard.get_current_player()
        res = player.mortgage_property(deed_name)
        print(deed_name)
        if res:
            observer.Event("update_state", f"{deed_name} mortgaged")
        else:
            observer.Event("update_state", f"attempt to mortgage {deed_name} failed")

    def _unmortgage(self, data):
        """Player has indicated an interest in unmortgaging a property
            they must unmortgage in a FIFO order
        """
        player = self._gameboard.get_current_player()
        deed_name = player.unmortgage_property()
        if deed_name != "":
            observer.Event("update_state", f"Unmortgaged: {deed_name}")
            observer.Event("update_players_state", self._gameboard.to_dicts())


    def button_clicked(self, button):
        """Handle View button click events"""
        print(f"Button clicked: {button}")
        self._roll_action(None)

    def _roll_action(self, data):
        player = self._gameboard.get_current_player()

        if not self._handle_roll_dice():
            return

        square = self._gameboard.get_square(player.position)
        money = player.money

        msg = f"{player.name} landed on {square}."

        observer.Event("update_state", msg)
        observer.Event("update_players_state", self._gameboard.to_dicts())
        observer.Event("update_card", player.position)




