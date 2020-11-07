import random
from operator import attrgetter
from dataclasses import dataclass, field
from typing import List

# SUIT_RANK = ["Spades", "Hearts", "Clubs", "Diamonds"]
# VALUE_RANK = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
# SUIT_DISPLAY = ["\u2660", "\u2665", "\u2663", "\u2666"]
# SUIT_DISPLAY = ["\u2664", "\u2661", "\u2667", "\u2662"]
SUITS = ['♠', '♡', '♣', '♢']
VALUES = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
PLAYER_COUNT = 4

@dataclass
class Card():
    """Card model"""
    suit: int
    value: int
    def __str__(self):
        return "{0}{1}".format(
            VALUES[self.value],
            SUITS[self.suit],
        )
def display_cards(cards: List[Card]) -> None:
    """Reveals cards"""
    if len(cards) == 0:
        print("The card list is empty!")
    else:
        card_string = ""
        for card in cards:
            card_string += str(card) + " "
        print(card_string)
@dataclass
class Dealer():
    """Helper class for deck-related methods"""
    # deck: List[Card] = field(default_factory=Dealer.build())
    # deck: List[Card] = field(default=[])
    # deck: List[Card] = []
    deck: List[Card]
    def build(self) -> None:
        """Construct in-order deck"""
        deck = []
        for suit_index in range(len(SUITS)):
            for value_index in range(len(VALUES)):
                new_card = Card(
                    suit=suit_index,
                    value=value_index,
                )
                deck.append(new_card)
                # print("Adding {} to the deck.".format(
                #     str(new_card),
                # ))
        self.deck = deck
    def shuffle(self) -> None:
        """Shuffles the deck"""
        random.shuffle(self.deck)
    def deal_a_card(self) -> Card:
        """Deals a card"""
        return self.deck.pop()
    def divide_deck_into_hands(self, number_of_players: int) -> List[List[Card]]:
        """Deals hands from the deck given the number of players"""
        hand_list = []
        starting_index = 0
        while starting_index < 4:
            hand_list.append(self.deck[starting_index::number_of_players])
            starting_index += 1
        # for hearts, consider clearing self.deck -> empty
        return hand_list
@dataclass
class Player():
    """Player class"""
    number: int
    hand: list
    def sort_hand(self) -> None:
        """Sort a given hand by suit and then value"""
        self.hand.sort(key=attrgetter('suit', 'value'))
@dataclass
class Hearts():
    """Game of Hearts"""
    players: List[Player]
    dealer: Dealer = field(default=Dealer([]))
    def start(self) -> None:
        """Initialize game"""
        self.dealer.build()
        self.dealer.shuffle()
        hand_list = self.dealer.divide_deck_into_hands(PLAYER_COUNT)
        for player_index in range(PLAYER_COUNT):
            player = Player(
                number=player_index,
                hand=hand_list[player_index],
            )
            self.players.append(player)
    def reveal_player_hands(self) -> None:
        """Show all players' hands"""
        for player in self.players:
            print("\nPlayer #{}'s hand is {} big:".format(
                player.number + 1,
                len(player.hand),
            ))
            # Dealer.display_cards(player.hand)
            player.sort_hand()
            display_cards(player.hand)
if __name__ == "__main__":
    # test_card = Card(suit=0, value=0)
    # print(test_card)

    # test_deck = Dealer.build()
    # test_hand_list = Dealer.divide_deck(test_deck, 4)
    # for test_hand in test_hand_list:
    #     Dealer.display_cards(test_hand)
    #     print("\n")

    game = Hearts([])
    game.start()
    display_cards(game.dealer.deck)
    game.reveal_player_hands()

