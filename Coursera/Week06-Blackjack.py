# Week 06 Project - Blackjack
# Paste into www.codeskulptor.org to see it run

# ------------------------
# --- Import Libraries ---
# ------------------------
import random
import simplegui

# ---------------------------
# --- Define Global State ---
# ---------------------------

#Canvas
HEIGHT = 320
WIDTH = 550
FONT_SIZE = 28
FONT_FACE = 'monospace'

#Cards
# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

#Game State
dealer = None
player = None
player_score = 0
player_turn = False
message = ""
deck = None
show_hole = False

# ---------------
# --- Classes ---
# ---------------

# Class representing a playing card
class Card:
    SUITS = ('C', 'S', 'H', 'D')
    RANKS = ('A', '2', '3', '4', '5', '6' ,'7', '8', '9', 'T', 'J', 'Q', 'K')
    VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
    
    # Constructor
    def __init__(self, suit, rank):
        if (suit in Card.SUITS) and (rank in Card.RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card:,", suit, rank
    
    # To-String
    def __str__(self):
        if (self.suit != None) and (self.rank != None):
            return self.suit + self.rank
        else:
            return "N/A"
    
    # Return the card's suit
    def get_suit(self):
        return self.suit
    
    # Return the card's rank
    def get_rank(self):
        return self.rank
    
    # Draw the card at the given tuple position pos
    #  representing the upper-left corner of the card
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * Card.RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * Card.SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        pass
        
# Class representing a Blackjack hand
class Hand:
    # Constructor
    def __init__(self):
        self.cards = []
        self.has_ace = False
    
    # To-String
    def __str__(self):
        hand_string = "Hand contains "
        for card in self.cards:
            hand_string += str(card) + " "
        
        return hand_string
    
    # Add a card to the hand
    def add_card(self, card):
        self.cards.append(card)
        if (card.get_rank() == 'A'):
            self.has_ace = True
        pass
    
    # Return true if the hand contains an ace
    def has_an_ace(self):
        return self.has_ace
    
    # Calculate the hand's value for Blackjack
    #  Aces count as 10 unless it would bust the hund
    def get_value(self):
        has_ace = False
        value = 0
        for card in self.cards:
            value += Card.VALUES[card.get_rank()]
        
        if (value < 12) and self.has_ace:
            value += 10
            
        return value
    
    # Return whether or not the hand is busted
    #  (if the value is over 21)
    def is_busted(self):
        return (self.get_value() > 21)
    
    # Draw up to the first 5 cards of a hand starting
    #  at the tuple position pos representing the top-left
    #  corner of the 1st card
    #  Draw card backs of cards 3-5 if show_hole is False
    def draw(self, canvas, pos, show_hole):
        offset = 0
        for card in self.cards[:5]:
            if (offset < CARD_SIZE[0]) or show_hole:
                card.draw(canvas, (pos[0] + offset, pos[1]))
            else:
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, \
                                  [pos[0] + offset + CARD_BACK_CENTER[0], \
                                   pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
            offset += CARD_SIZE[0]
        pass

# Class representing a deck of playing cards
class Deck:
    # Constructor
    def __init__(self):
        self.cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.cards.append(Card(suit, rank))
    
    # To-String
    def __str__(self):
        deck_string = "Deck contains "
        for card in self.cards:
            deck_string += str(card) + " "
        
        return deck_string
    
    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)
        pass
    
    # Deal a card off the top of the deck
    def deal_card(self):
        if (len(self.cards) > 0):
            return self.cards.pop(0)
        else:
            return None
        
# ------------------------
# --- Helper Functions ---
# ------------------------

# return the X coordinate such that text is centered in the canvas
def center_text(text):
    return (WIDTH - frame.get_canvas_textwidth(text, FONT_SIZE, FONT_FACE)) // 2

# draw the message in the center of the screen
#  alter the font size to fit the message if necessary
def draw_message(canvas):
    global message
    
    font_pt = FONT_SIZE
    x_pos = (WIDTH - 20 - frame.get_canvas_textwidth(message, font_pt, FONT_FACE)) // 2
  
    while (x_pos < 0):
        font_pt -= 2
        x_pos = (WIDTH - 20 - frame.get_canvas_textwidth(message, font_pt, FONT_FACE)) // 2

    canvas.draw_text(message, (x_pos + 20, (HEIGHT + FONT_SIZE) // 2 - 4), font_pt, 'white', FONT_FACE)
    pass

# draw the title on the left side of the screen
def draw_title(canvas, title):
    spacing = HEIGHT // len(title)
    spacer = 0
    for letter in title:
        canvas.draw_text(letter, (3, spacer + 18), 18, 'green')
        spacer += spacing
        
    pass
# -----------------------
# --- Define Handlers ---
# -----------------------

# draw the blackjack game
def draw_handler(canvas): 
    global dealer, player, player_score, message, show_hole
    
    #Draw title
    canvas.draw_polygon([(0, 0), (19, 0), (19, HEIGHT - 1), (0, HEIGHT - 1)], 1, 'black', 'white')
    draw_title(canvas, "BLACKJACK")
    
    #Draw Dealer Info
    canvas.draw_text("DEALER", (40, FONT_SIZE - 4), FONT_SIZE, 'red', FONT_FACE)
    canvas.draw_line((20, FONT_SIZE),(WIDTH - 1, FONT_SIZE), 2, 'gray')
    dealer.draw(canvas, (20, FONT_SIZE + 4), show_hole)
    
    #Draw Player Info
    canvas.draw_text("PLAYER (Score: " + str(player_score) + ")", (40, HEIGHT - CARD_SIZE[1] - 12), FONT_SIZE, 'blue', FONT_FACE)
    canvas.draw_line((20, HEIGHT - CARD_SIZE[1] - 5), (WIDTH - 1, HEIGHT -CARD_SIZE[1] - 5), 2, 'gray')
    player.draw(canvas, (20, HEIGHT - CARD_SIZE[1] - 1), True)
    
    #Draw Game Message
    canvas.draw_line((20, FONT_SIZE + CARD_SIZE[1] + 9), (WIDTH -1, FONT_SIZE + CARD_SIZE[1] + 9), 2, 'gray')
    canvas.draw_line((20, HEIGHT - FONT_SIZE - CARD_SIZE[1] - 9), (WIDTH -1, HEIGHT - FONT_SIZE - CARD_SIZE[1] - 9), 2, 'gray')
    draw_message(canvas)
    pass

# deal a new hand
def deal():
    global dealer, player, player_turn, deck, show_hole, message, player_score
    
    if (player_turn) or (timer.is_running()):
        player_score -= 1
    
    timer.stop()
    show_hole = False
    player_turn = True
        
    deck = Deck()
    deck.shuffle()
    
    dealer = Hand()
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    
    player = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    
    message = "Hit or Stay?"
    pass

# player hits for a card
def hit():
    global player, deck, player_turn
    if (player_turn):
        player.add_card(deck.deal_card())
        if (player.is_busted()):
            player_turn = False
            timer.start()
            timer_handler()
    pass

# player stays
def stay():
    global player_turn
    if (player_turn == True):
        player_turn = False
        timer.start()
        timer_handler()
    pass

# walk through the dealer's turns and scoring
def timer_handler():
    global dealer, player, player_turn, deck, show_hole, message, player_score
    
    if (not player_turn):
        if (player.is_busted()):
            message = "Player is bust! Press 'DEAL' for next game"
            player_score -= 1
            show_hole = True
            timer.stop()
        elif (not show_hole):
            message = "Dealer has " + str(dealer.get_value()) + ", Player has " + str(player.get_value())
            show_hole = True
        elif ((not dealer.is_busted()) and \
              (dealer.get_value() < 17)):    
            message = "Dealer Hits"
            dealer.add_card(deck.deal_card());
        elif (not dealer.is_busted()):
            message = "Dealer has " + str(dealer.get_value()) + ", Player has " + str(player.get_value()) + ": "
            if (player.get_value() > dealer.get_value()):
                message += "Player Wins! Press 'DEAL' for next game"
                player_score += 1
            else:
                message += "Dealer Wins! Press 'DEAL' for next game"
                player_score -= 1
            timer.stop()
        else:
            message = "Dealer is bust! Press 'DEAL' for next game"
            player_score += 1
            timer.stop()
    pass
        
# --------------------
# --- Create Frame ---
# --------------------

frame = simplegui.create_frame('Blackjack', WIDTH, HEIGHT)

# -------------------------
# --- Register Handlers ---
# -------------------------

frame.set_draw_handler(draw_handler)
timer = simplegui.create_timer(1500, timer_handler)
frame.add_button('DEAL', deal, 75)
frame.add_button('HIT', hit, 75)
frame.add_button('STAY', stay, 75)

# ----------------------------
# --- Start Frame & Timers ---
# ----------------------------

deal()
frame.start()
