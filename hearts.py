import random
from operator import attrgetter, truediv
from dataclasses import dataclass, field
from typing import List

# SUIT_RANK = ["Spades", "Hearts", "Clubs", "Diamonds"]
# VALUE_RANK = ["Ace", "King", "Queen", "Jack", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
# SUIT_DISPLAY = ["\u2660", "\u2665", "\u2663", "\u2666"]
# SUIT_DISPLAY = ["\u2664", "\u2661", "\u2667", "\u2662"]
SUITS = ['♠', '♡', '♣', '♢']
TRUMP_SUIT = 1
VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
PLAYER_COUNT = 4

@dataclass
class Flag():
    """
    Struct to keep track of game state flags.
    """
    trumped: bool = False
    first_trick: bool = True

@dataclass
class Card():
    """
    Card model
    """
    suit: int
    value: int
    def __str__(self):
        return "{0}{1}".format(
            VALUES[self.value],
            SUITS[self.suit],
        )

@dataclass
class Trick():
    """
    Trick model
    """

    cards_played: List[Card]
    # suit: int
    player_order: List[int]
    winner: int = -1
    points: int = 0

    def __str__(self):
        return "Card order: {}\nPlayer order: {}\nWinner: {}\nPoints: {}".format(
            self.cards_played,
            self.player_order,
            self.winner,
            self.points,
        )
    def describe_trick(self):
        """
        Utility method to detail what happened in this trick.
        """
        cards_played_in_order = ""
        for player_i in range(PLAYER_COUNT):
            cards_played_in_order = str(self.cards_played[player_i]) + " " + cards_played_in_order
            print("P{} -> {}".format(
                player_i,
                cards_played_in_order,
            ))
        print("Player {} won with high card {}, gaining {} points.".format(
            self.winner,
            cards_played[player_order.index(self.winner)],
            self.points,
        ))
    def resolve(self) -> List[int]:
        """
        Counts points in this trick
        """
        current_winning_value = -1
        for player_index, card in enumerate(self.cards_played):
            # Find winner
            if card.suit == self.cards_played[0].suit and card.value > current_winning_value:
                current_winning_value = card.value
                self.winner = self.player_order[player_index]
            # Count points
            if card.suit == 1:
                self.points += 1
            elif card.suit == 0 and card.value == 10:
                self.points += 13
def display_cards(cards: List[Card]) -> None:
    """
    Reveals cards
    """
    if len(cards) == 0:
        print("The card list is empty!")
    else:
        card_string = ""
        for card in cards:
            card_string += str(card) + " "
        print(card_string)


@dataclass
class Player():
    """
    Player model
    """
    number: int
    hand: List[Card]
    def sort_hand(self) -> None:
        """
        Sort a given hand by suit and then value
        """
        self.hand.sort(key=attrgetter('suit', 'value'))
    def play_card(self, played_cards: List[Card], flag: Flag) -> Card:
        """
        Player deliberates and then pops a card from his hand.
        """
        playable_cards = []

        # First player of the trick
        if not played_cards:
            if flag.first_trick:
                for card in self.hand:
                    if card.suit == 2:
                        playable_cards.append(card)
                flag.first_trick = False
            elif trumped:
                for card in self.hand:
                    playable_cards.append(card)
            else:
                for card in self.hand:
                    if card.suit != TRUMP_SUIT:
                        playable_cards.append(card)
        
        # Other players' turn
        else:
            trick_suit = played_cards[0].suit

            print("Trick suit is: {}".format(SUITS[trick_suit]))

            for card in self.hand:
                if card.suit == trick_suit:
                    playable_cards.append(card)

        if not playable_cards:
            playable_cards = self.hand[:]
        print("Hand:")
        display_cards(self.hand)
        print("Playable cards:")
        display_cards(playable_cards)
        
        card_to_play_index = self.hand.index(random.choice(playable_cards))
        card_to_play = self.hand.pop(card_to_play_index)
        
        print("Playing card: {}".format(card_to_play))

        return card_to_play
            




def add_players(number_of_players, hand_list: List[List[Card]]) -> List[Player]:
    """
    Returns a list of players that already have their hands.
    """
    players = []
    for player_index in range(number_of_players):
        player = Player(
            number=player_index,
            hand=hand_list[player_index],
        )
        players.append(player)
    return players

class Dealer():
    """Helper class for deck-related methods"""
    deck: List[Card]
    def __init__(self):
        deck = []
        for suit_index in range(len(SUITS)):
            for value_index in range(len(VALUES)):
                new_card = Card(suit_index, value_index)
                deck.append(new_card)
                # print("Adding {} to the deck.".format(
                #     str(new_card),
                # ))
        self.deck = deck
    def shuffle(self) -> None:
        """
        Shuffles the deck
        """
        random.shuffle(self.deck)
    def deal_a_card(self) -> Card:
        """
        Deals a card
        """
        return self.deck.pop()
    def divide_deck_into_hands(self, number_of_players: int) -> List[List[Card]]:
        """
        Deals hands from the deck given the number of players
        """
        hand_list = []
        starting_index = 0
        while starting_index < 4:
            hand_list.append(self.deck[starting_index::number_of_players])
            starting_index += 1
        # for hearts, consider clearing self.deck -> empty
        return hand_list

        










if __name__ == "__main__":
    # test_card = Card(suit=0, value=0)
    # print(test_card)

    # test_deck = Dealer.build()
    # test_hand_list = Dealer.divide_deck(test_deck, 4)
    # for test_hand in test_hand_list:
    #     Dealer.display_cards(test_hand)
    #     print("\n")

    dealer = Dealer()
    dealer.shuffle()
    players = add_players(
        PLAYER_COUNT,
        dealer.divide_deck_into_hands(PLAYER_COUNT)
    )
    flag = Flag()


    for player in players:
        player.sort_hand()
    
    tricks = []
    trumped = False

    for trick_i in range(13):
        print("\nRound: {}".format(trick_i + 1))
        cards_played = []
        player_order = []
        for player in players:
            print("\nPlayer {}'s turn ========".format(player.number))
            print("First trick = {}".format(flag.first_trick))

            card_played = player.play_card(cards_played, flag)

            if card_played.suit == TRUMP_SUIT:
                trumped = True

            cards_played.append(card_played)
            player_order.append(player.number)

        trick = Trick(cards_played, player_order)
        trick.resolve()
        trick.describe_trick()
        print(trick)
        tricks.append(trick)
    # print(tricks)



    
    # display_cards(dealer.deck)
    # for player in players:
    #     print("\nPlayer #{}'s hand is {} big:".format(
    #         player.number + 1,
    #         len(player.hand),
    #     ))
    #     # Dealer.display_cards(player.hand)
    #     player.sort_hand()
    #     display_cards(player.hand)


