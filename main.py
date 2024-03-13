import itertools
import queue
import random
import threading
import time
from collections import Counter
from tkinter import *

from PIL import Image, ImageTk


# Entry Point 
def main():
    class Card(object):
        def __init__(self, value, suit):
            self.value = value
            self.suit = suit
            self.showing = True

        def __repr__(self):
            value_name = ""
            suit_name = ""
            if self.showing:
                if self.value == 0:
                    value_name = "Two"
                if self.value == 1:
                    value_name = "Three"
                if self.value == 2:
                    value_name = "Four"
                if self.value == 3:
                    value_name = "Five"
                if self.value == 4:
                    value_name = "Six"
                if self.value == 5:
                    value_name = "Seven"
                if self.value == 6:
                    value_name = "Eight"
                if self.value == 7:
                    value_name = "Nine"
                if self.value == 8:
                    value_name = "Ten"
                if self.value == 9:
                    value_name = "Jack"
                if self.value == 10:
                    value_name = "Queen"
                if self.value == 11:
                    value_name = "King"
                if self.value == 12:
                    value_name = "Ace"
                if self.suit == 0:
                    suit_name = "Diamonds"
                if self.suit == 1:
                    suit_name = "Clubs"
                if self.suit == 2:
                    suit_name = "Hearts"
                if self.suit == 3:
                    suit_name = "Spades"
                return value_name + " of " + suit_name
            else:
                return "[CARD]"

        class StandardDeck(list):
            def __init__(self):
                super().__init__()
                suits = list(range(4))
                values = list(range(13))
                [[self.append(Card(i, j)) for j in suits] for i in values]

            def __repr__(self):
                return f"Standard Deck Of Cards\n{len(self)} Cards Remaining"

            def shuffle(self):
                random.shuffle(self)
                print("\n\n--Deck Shuffled")

            def deal(self, location, times=1):
                for i in range(times):
                    location.cards.append(self.pop(0))

            def burn(self):
                self.pop(0)

        class Player(object):
            def __init__(self, name=None):
                self.name = name
                self.chips = 0
                self.stake = 0
                self.stake_gap = 0
                self.cards = []
                self.score = []
                self.fold = False
                self.ready = False
                self.all_in = False
                self.list_of_special_attributes = []
                self.win = False

            def __repr__ (self):
                name = self.name
                return name

        class Game(object):
            def __init__(self):
                self.need_raise_info = False
                self.game_over = False
                self.acting_player = Player()
                self.possible_responses = []
                self.round_counter = 0
                self.cards = []
                self.pot = 0
                self.pot_dict = {}
                self.pot_in_play = 0
                self.list_of_player_names = []
                self.dealer = Player()
                self.small_blind = Player()
                self.big_blind = Player()
                self.first_actor = Player()
                self.winners = []
                self.deck = StandardDeck()
                self.list_of_scores_from_eligible_winners = []
                self.setup = ask_app("Start?")
                while True:
                    try:
                        self.number_of_players = len(self.setup["Players"])
                        break
                    except ValueError:
                        print("Invalid Response")
                if 1 < self.number_of_players < 11:
                    pass
                else:
                    print("Invalid Number Of Players")
                    main()
                self.list_of_players = [Player(name) for name in self.setup["Players"] if name != ""]
                while True:
                    try:
                        self.starting_chips = int(self.setup["Chips"][0])
                        if self.starting_chips > 0:
                            break
                        print("Invalid Number, Try Greater Than 0")
                    except ValueError:
                        print("invalid Response")
                        continue
                for player in self.list_of_players:
                    player.chips = self.starting_chips
                self.ready_list = []
                while True:
                    try:
                        self.small_blind_amount = int(self.setup["Chips"][1])
                        if self.starting_chips > self.small_blind_amount > 0:
                            break
                        print("Invalid Number, Try Bigger Than Zero, Smaller Than Starting Chips")
                    except ValueError:
                        print("Invalid Response")
                        continue
                while True:
                    try:
                        self.big_blind_amount = int(self.setup["Chips"][2])
                        if self.starting_chips > self.big_blind_amount > self.small_blind_amount:
                            break
                        print("Invalid Number, Try Bigger Than Small Blind, Smaller Than Starting Chips")
                    except ValueError:
                        print("Invalid Response")
                        continue
                self.winner = None
                self.action_counter = 0
                self.attribute_list = ["D", "SB", "BB", "FA"]
                self.highest_stake = 0
                self.fold_list = []
                self.not_fold_list = []
                self.round_ended = False
                self.fold_out = False
                self.list_of_scores_eligible = []
                self.list_of_players_not_out = list(set(self.list_of_players))
                self.number_of_player_not_out = int(len(set(self.list_of_players)))

            def print_game_info(self):
                pass

            def print_round_info(self):
                print("\n")
                print(f"Name: {player.name}")
                print(f"Cards: {player.cards}")
                print(f"Player Score: {player.score}")
                print(f"Chips: {player.chips}")
                print(f"Special Attributes: {player.list_of_special_attributes}")
                if player.fold:
                    print(f"Folded")
                if player.all_in:
                    print(f"All In")
                print(f"Stake: {player.stake}")
                print(f"Stake-Gap: {player.stake_gap}")
                print("\n")
            print(f"Pot: {self.pot}")
            print(f"Community Cards: {self.cards}")
            print("\n")

        def establish_player_attributes(self):
            address_assignment = 0
            self.dealer = self.list_of_players_not_out[address_assignment]
            address_assignment += 1
            address_assignment %= len(self.list_of_players_not_out)
            self.small_blind = self.list_of_players_not_out[address_assignment]
            self.small_blind.list_of_special_attributes.append("Small Blind")
            address_assignment += 1
            address_assignment %= len(self.list_of_players_not_out)
            self.big_blind = self.list_of_players_not_out[address_assignment]
            self.big_blind.list_of_special_attributes.append("Big Blind")
            address_assignment += 1
            address_assignment %= len(self.list_of_players_not_out)
            self.first_actor = self.list_of_players_not_out[address_assignment]
            self.first_actor.list_of_special_attributes.append("First Actor")
            self.list_of_players_not_out.append(self.list_of_players_not_out.pop(0))

        def deal_hole(self):
            for player in self.list_of_players_not_out:
                self.deck.deal(player, 2)

        def deal_flop(self):
            self.deck.burn()
            self.deck.deal(self, 3)

        def deal_turn(self):
            self.deck.burn()
            print("\n--Card Burned--")
            self.deck.deal(self, 1)
            print(f"\nCommunity Cards: {self.cards}")

        def deal_river(self):
            self.deck.burn()
            print("\n--Card Burned--")
            self.deck.deal(self, 1)
            print(f"\n\nCommunity Cards: {self.cards}")

        def hand_scorer(self, player):
            seven_cards = player.cards + self.cards
            all_hand_combos = list(itertools.combinations(seven_cards, 5))
            list_of_all_score_possibilites = []
            for i in all_hand_combos:
                suit_list = []
                value_list = []
                for j in i:
                    suit_list.append(j.suit)
                    value_list.append(j.value)
                initial_value_check = list(reversed(sorted(value_list)))
                score1 = 0
                score2 = 0
                score3 = 0
                score4 = initial_value_check.pop(0)
                score5 = initial_value_check.pop(0)
                score6 = initial_value_check.pop(0)
                score7 = initial_value_check.pop(0)
                score8 = initial_value_check.pop(0)
                list_of_pair_values = []
                other_cards_not_special = []
                pair_present = False
                pair_value = int
                value_counter = dict(Counter(value_list))
                for value_name, count in value_counter.items():
                    if count == 2:
                        pair_present = True
                        pair_value = value_name
                        list_of_pair_values.append(value_name)
                    if pair_present:
                        for value in value_list:
                            if value not in list_of_pair_values:
                                other_cards_not_special.append(value)
                            other_cards_not_special = list(reversed(sorted(other_cards_not_special)))
                            if len(set(list_of_pair_values)) == 1:
                                score1 = 1
                                score2 = max(list_of_pair_values)
                                try:
                                    score3 = other_cards_not_special.pop(0)
                                    score4 = other_cards_not_special.pop(0)
                                    score5 = other_cards_not_special.pop(0)
                                    score6 = other_cards_not_special.pop(0)
                                    score7 = other_cards_not_special.pop(0)
                                    score8 = other_cards_not_special.pop(0)
                                except IndexError:
                                    pass
                            if len(set(list_of_pair_values)) == 2:
                                list_of_pair_values = list(reversed(sorted(list_of_pair_values)))
                                score1 = 2
                                score2 = list_of_pair_values.pop(0)
                                score3 = list_of_pair_values.pop(0)
                                try:
                                    score4 = other_cards_not_special.pop(0)
                                    score5 = other_cards_not_special.pop(0)
                                    score6 = other_cards_not_special.pop(0)
                                    score7 = other_cards_not_special.pop(0)
                                    score8 = other_cards_not_special.pop(0)
                                except IndexError:
                                    pass
                            three_of_a_kind_value = int
                            other_cards_not_special = []
                            three_of_a_kind_present = False
                            for value_name, count in value_counter.items():
                                if count == 3:
                                    three_of_a_kind_present = True
                                    three_of_a_kind_value = value_name
                            if three_of_a_kind_present:
                                for value in value_list:
                                    if value != three_of_a_kind_value:
                                        other_cards_not_special.append(value)
                                other_cards_not_special = list(reversed(sorted(other_cards_not_special)))
                                score1 = 3
                                score2 = three_of_a_kind_value
                                try:
                                    score3 = other_cards_not_special.pop(0)
                                    score4 = other_cards_not_special.pop(0)
                                    score5 = other_cards_not_special.pop(0)
                                    score6 = other_cards_not_special.pop(0)
                                    score7 = other_cards_not_special.pop(0)
                                    score8 = other_cards_not_special.pop(0)
                                except IndexError:
                                    pass
                            if sorted(value_list) == list(range(min(value_list), max(value_list) + 1)):
                                score1 = 4
                                score2 = max(value_list)
                            if sorted(value_list) == [0, 1, 2, 3, 12]:
                                score1 = 4
                                score2 = 3
                            if len(set(suit_list)) == 1:
                                score1 = 6
                                score2 = three_of_a_kind_value
                                score3 = pair_value
                            four_of_a_kind_value = int
                            other_card_value = int
                            four_of_a_kind = False
                            for value_name, count in value_counter.items():
                                if count == 4:
                                    four_of_a_kind_value = value_name
                                    four_of_a_kind: True
                                for value in value_list:
                                    if value != four_of_a_kind_value:
                                        other_card_value = value
                                if four_of_a_kind:
                                    score1 = 7
                                    score2 = four_of_a_kind_value
                                    score3 = other_card_value
                                if sorted(value_list) == [0, 1, 2, 3, 12] and len(set(suit_list)) == 1:
                                    score1 = 8
                                    score2 = 3
                                if sorted(value_list) == list(range(min(value_list), max(value_list) + 1)) and len(set(suit_list)) == 1:
                                    score1 = 8
                                    score2 = max(value_list)
                                    if max(value_list) == 12:
                                        score1 = 9
                                list_of_all_score_possibilites.append([score1, score2, score3, score4, score5, score6, score7, score8])
                                player.score = best_score

                            def score_all(self):
                                for player in self.list_of_players_not_out:
                                    self.hand_scorer(player)

                            def find_winners(self):
                                if self.fold_out:
                                    for player in list(set(self.winners)):
                                        player.chips += int((self.pot / len(list(set(self.winners)))))
                                        print(f"{player.name} Wins {int((self.pot / len(list(set(self.winners)))))} Chips!")
                                    else:
                                        list_of_stakes = []
                                        for player in self.list_of_players_not_out:
                                            list_of_stakes.append(player.stake)
                                        list_of_stakes = list(set(list_of_stakes))
                                        list_of_stakes = sorted(list_of_stakes)
                                        for stake in list_of_stakes:
                                            print(stake)
                                        for player in self.list_of_players_not_out:
                                            print(player.name)
                                            print(player.stake)
                                        print(self.list_of_players_not_out)
                                        list_of_players_at_stake = []
                                        list_of_list_of_players_at_stake = []
                                        for i in range(len(list_of_stakes)):
                                            for player in self.list_of_players_not_out:
                                                if player.stake >= list_of_stakes[i]:
                                                    list_of_players_at_stake.append(player)
                                            list_of_list_of_players_at_stake.append(list(set(list_of_players_at_stake)))
                                            list_of_players_at_stake.clear()
                                        print(list_of_list_of_players_at_stake)
                                        list_of_pot_chips = []
                                        for i in list_of_stakes:
                                            list_of_pot_chips.append(i)
                                        list_of_pot_chips.reverse()
                                        for i in range(len(list_of_pot_chips)):
                                            try:
                                                list_of_pot_chips[i] -= list_of_pot_chips[i + 1]
                                            except IndexError:
                                                pass
                                        list_of_pot_chips.reverse()
                                        list_of_pots = []
                                        for i in range(len(list_of_pot_chips)):
                                            print(len(list_of_list_of_players_at_stake[i]))
                                        for i in range(len(list_of_pot_chips)):
                                            list_of_pots.append(list_of_pot_chips[i] * len(list_of_list_of_players_at_stake[i]))
                                        for i in range(len(list_of_pots)):
                                            winners = []
                                            self.list_of_scores_eligible.clear()
                                            for player in list_of_list_of_players_at_stake[i]:
                                                if player.fold:
                                                    pass
                                                else:
                                                    self.list_of_scores_eligible.append(player.score)
                                            max_score = max(self.list_of_scores_eligible)
                                            for player in list_of_list_of_players_at_stake[i]:
                                                if player.fold:
                                                    pass
                                                else:
                                                    if player.score == max_score:
                                                        player.win = True
                                                        winners.append(player)
                                            prize = int(list_of_pots[i] / len(winners))




