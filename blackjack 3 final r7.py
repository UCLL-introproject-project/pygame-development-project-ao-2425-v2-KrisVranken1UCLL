# black jack in python wth pygame!
import copy
import random
import pygame
import os

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Pygame: 2 player Blackjack')

# game variables
records = [0,0,0,0,0,0] # P1 win, P1 loss, P1 draw, P2 win, P2 loss, P2 draw
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
suits = ['hearts', 'diamonds', 'spades', 'clubs']  
deck = [f"{rank}_of_{suit}" for rank in cards for suit in suits]  # All 52 cards
one_deck = 4 * cards
decks = 4
WIDTH = 1575
HEIGHT = 900
fps = 4
clr_black = (5,5,5)
clr_hit = (255,0,0)
clr_stand = (144,238,144)
clr_deal = (255,215,0)
timer = pygame.time.Clock()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
sound_effects = [
    "/sounds/card_dealing1.mp3",
    "/sounds/card_dealing2.mp3",
    "/sounds/card_dealing3.mp3",
    "/sounds/card_dealing4.mp3"
]

active = False

# define exact location of the script
base_path = os.path.dirname(__file__)  # Pad naar de map van het script
image_path = os.path.join(base_path, "images/blackjack_background.png")
cards_path = os.path.join(base_path, "images/cards/")

background = pygame.image.load(image_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font = pygame.font.Font(base_path + "/font/Magic Retro.ttf", 44)  # 44 is font size
smaller_font = pygame.font.Font(base_path + "/font/Magic Retro.ttf", 32)  # 32 is font size

# play a random card flick sound
def play_carddeal_sound():
    sound_file = random.choice(sound_effects)
    sound = pygame.mixer.Sound(base_path + sound_file)
    sound.play()

def play_cardshuffle_sound():
    sound_file = random.choice(sound_effects)
    sound = pygame.mixer.Sound(base_path + "/sounds/shuffle_cards.mp3")
    sound.play()


# reset parameters
def reset_game(act, intd, hact, adds):
    global active, initial_deal, player_1_hand, player_2_hand
    global player_1_score, player_2_score, player_1_stand, player_2_stand
    global dealer_hand, dealer_score, reveal_dealer, hand_active, add_score
    
    active = act
    initial_deal = intd
    player_1_hand = []
    player_2_hand = []
    player_1_score = 0
    player_2_score = 0
    player_1_stand = False
    player_2_stand = False
    dealer_hand = []
    dealer_score = 0
    reveal_dealer = False
    hand_active = hact
    add_score = adds

reset_game(False, False, False, False)

# deal cards by selecting randomly from deck, and make function for one card at a time
def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card -1)
    return current_hand, current_deck

# draw cards visually onto screen
def draw_cards(player_1, player_2, dealer, reveal):
    for i, card in enumerate(player_1):
        cards = len(player_1)+1
        start_pos_x = 420 - ((cards*102)/2)
        card_image = load_card_image(card)
        screen.blit(card_image, (start_pos_x + (70 * i), 400+(i*5)))
    
    for i, card in enumerate(player_2):
        cards = len(player_2)+1
        start_pos_x = 1200 - ((cards*102)/2)
        card_image = load_card_image(card)
        screen.blit(card_image, (start_pos_x + (70 * i), 400+(i*5)))

    for i, card in enumerate(dealer):
        cards = len(dealer)
        start_pos_x = (WIDTH /2) - ((cards * 102)/2) -6
        if i == 0 and not reveal:
            screen.blit(card_back, (start_pos_x + (70 * i), 140+(i*5)))  # hide first card
        else:
            card_image = load_card_image(card)
            screen.blit(card_image, (start_pos_x + (70 * i), 140+(i*5)))

# function to load card image
def load_card_image(card_name):
    path = os.path.join(cards_path, f"{card_name}.png")
    card = pygame.image.load(path)
    card = pygame.transform.scale(card, (172, 250))

    # create a transparent Surface for shadow
    shadow = pygame.Surface((172, 250), pygame.SRCALPHA)
    # create rectangular with rounded corners as shadow
    pygame.draw.rect(shadow, (0, 0, 0, 70), shadow.get_rect(), border_radius=10)
   
    # create new surface to combine shadow and card
    card_with_shadow = pygame.Surface((177, 255), pygame.SRCALPHA)
    card_with_shadow.blit(shadow, (0, 5))  # place shadow bottom right
    card_with_shadow.blit(card, (5, 0))  # place card on top

    return card_with_shadow

# backside of the card
card_back = load_card_image("back")

# draw scores for player and dealer on screen
def draw_scores(player_1, player_2, dealer):
    screen.blit(font.render(f'Player 1 ~[{player_1}]~', True, 'black'), (243,333))
    screen.blit(font.render(f'Player 1 ~[{player_1}]~', True, 'white'), (240,330))
    screen.blit(font.render(f'Player 2 ~[{player_2}]~', True, 'black'), (1020,333))
    screen.blit(font.render(f'Player 2 ~[{player_2}]~', True, 'white'), (1017,330))
    if reveal_dealer:
        screen.blit(font.render(f'Dealer ~[{dealer}]~', True, 'black'), (666,73))
        screen.blit(font.render(f'Dealer ~[{dealer}]~', True, 'white'), (663,70))

def draw_result(player, result):
    if player == 1:
        px = 330
    if player == 2:
        px = 1110
    box_width = 120
    box_height = 60
    box_x = px
    box_y = 620
    shadow = pygame.Surface((box_width + 10, box_height + 10), pygame.SRCALPHA)
    pygame.draw.rect(shadow, (0, 0, 0, 100), (0, 0, box_width, box_height), border_radius=5)
    screen.blit(shadow, (box_x + 3, box_y + 3))  
    rectangle = pygame.draw.rect(screen, 'brown', (box_x, box_y, box_width, box_height), border_radius=5)
    text = result.capitalize()
    button_text = smaller_font.render(text, True, 'white')
    text_width, text_height = button_text.get_size()
    text_x = box_x + (box_width - text_width) // 2
    text_y = box_y + (box_height - text_height) // 2
    screen.blit(button_text, (text_x, text_y))

def draw_button(screen, text, font, bg_color, border_color, text_color, width, height, x, y):
    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, (0, 0, 0, 70), (0, 0, width, height), border_radius=5)
    screen.blit(rect_surface, (x+5, y+5))

    button_rect = pygame.draw.rect(screen, bg_color, [x, y, width, height], 0, 5)
    pygame.draw.rect(screen, border_color, [x, y, width, height], 3, 5)
    button_text = font.render(text, True, text_color)
    
    text_width, text_height = button_text.get_size()
    text_x = x + (width - text_width) // 2
    text_y = y + (height - text_height) // 2
    screen.blit(button_text, (text_x, text_y))
    return button_rect

# draw game conditions and buttons
def draw_game(active, record, result):
    button_list = {}
    # initially on startup (not active) only option is to deal new hand
    if not active:
        deal_button = draw_button(screen, "Start Game", font, clr_black, clr_deal, clr_deal, 300, 100, WIDTH // 2 - 150, 20)
        button_list["deal_btn"] = deal_button
    
    # once game started, show hit and stand buttons and win/loss records
    else:
        if not player_1_stand:
            hit_button_1 = draw_button(screen, "Hit me", font, clr_black, clr_hit, clr_hit, 240, 70, 110, 680)
            button_list["p1_hit_btn"] = hit_button_1
            stand_button_1 = draw_button(screen, "Stand", font, clr_black, clr_stand, clr_stand, 240, 70, 410, 680)
            button_list["p1_stand_btn"] = stand_button_1
        else:
            hit_button_1 = draw_button(screen, "Hit me", font, 'black', 'black', 'black', 240, 70, 110, 2000)
            button_list["p1_hit_btn"] = hit_button_1
            stand_button_1 = draw_button(screen, "Stand", font, 'black', 'black', 'black', 240, 70, 110, 2000)
            button_list["p1_stand_btn"] = stand_button_1
        if not player_2_stand:
            hit_button_2 = draw_button(screen, "Hit me", font, clr_black, clr_hit, clr_hit, 240, 70, 900, 680)
            button_list["p2_hit_btn"] = hit_button_2
            stand_button_2 = draw_button(screen, "Stand", font, clr_black, clr_stand, clr_stand, 240, 70, 1200, 680)
            button_list["p2_stand_btn"] = stand_button_2
        else:
            hit_button_2 = draw_button(screen, "Hit me", font, 'black', 'black', 'black', 240, 70, 110, 2000)
            button_list["p2_hit_btn"] = hit_button_2
            stand_button_2 = draw_button(screen, "Stand", font, 'black', 'black', 'black', 240, 70, 110, 2000)
            button_list["p2_stand_btn"] = stand_button_2

        score_text = smaller_font.render(f'~   Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}         ~     •     ~         Wins: {record[3]}   Losses: {record[4]}   Draws: {record[5]}     ~', True, (15,15,15))
        score_rect = score_text.get_rect(center=(787, 790))
        screen.blit(score_text, score_rect)
        score_text = smaller_font.render(f'~   Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}         ~     •     ~         Wins: {record[3]}   Losses: {record[4]}   Draws: {record[5]}     ~', True, 'white')
        score_rect = score_text.get_rect(center=(784, 787))
        screen.blit(score_text, score_rect)

         # if there is an outcome for the hand that was played, display a restart button and tell user what happened
        if not hand_active and reveal_dealer:
            if len(result) != 0:
                # shows win, bust, loss or draw
                draw_result(1, result[0])
                draw_result(2, result[1])
            newhand_button = draw_button(screen, "New Hand", font, (5, 5, 5), (255, 215, 0), (255, 215, 0), 300, 70, 637, 240)
            button_list["newhand_btn"] = newhand_button
    
    return button_list

def extract_card_value(card_name):      
    return card_name.split("_")[0]  # extract first number from card name

# pass in player or dealer hand and get best score possible
def calculate_score(hand):
    # calculate hand score fresh every time, check how many aces we have
    hand_score = 0
    #aces_count = hand.count('ace')
    aces_count = sum(1 for card in hand if card.split("_")[0]=='ace')
    for card in hand:
        card_value = card.split("_")[0]
        # 2 until 9: convert to integer and add
        if card_value.isdigit():
            hand_score += int(card_value)
        # for 10 and face cards, add 10
        elif card_value in ['10', 'jack', 'queen', 'king']:
            hand_score += 10
        # for aces start by adding 11, we'll check if we need to reduce afterwards
        elif card_value == 'ace':
            hand_score += 11
    # check how many aces have to become 1 instead of 11 in order to get under 21 if possible
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10
    return hand_score

# check endgame conditions function
def check_endgame(hand_active, dealer_score, player_1_score, player_2_score, result, totals, add):
    result1 = '*'
    result2 = '*'
    if not hand_active and dealer_score >= 17: # both players busted
        if player_1_score > 21:
            result1 = "bust"
        elif player_1_score < dealer_score <= 21:
            result1 = "loss"
        elif dealer_score < player_1_score <= 21 or dealer_score > 21: 
            result1 = "win"
        else: 
            result1 = "draw"
        
        if player_2_score > 21:
            result2 = "bust"
        elif player_2_score < dealer_score <= 21:
            result2 = "loss"
        elif dealer_score < player_2_score <= 21 or dealer_score > 21:
            result2 = "win"
        else: 
            result2 = "draw"
     
        if add:
            if result1 == "win":
                totals[0] += 1
            elif result1 == "bust" or result1 == "loss":
                totals[1] += 1
            elif result1 == "draw":
                totals[2] += 1
            if result2 == "win":
                totals[3] += 1
            elif result2 == "bust" or result2 == "loss":
                totals[4] += 1
            elif result2 == "draw":
                totals[5] += 1
        result = [result1, result2]
        add = False
    return result, totals, add

# main game loop
run = True
result_arr = []
while run:
    # run game at our framerate and fill screen with bg color
    timer.tick(fps)
    screen.blit(background, (0,0))
    black_strip = pygame.Surface((WIDTH, 180), pygame.SRCALPHA)
    black_strip.fill((0, 0, 0, 128))
    screen.blit(black_strip, (0, HEIGHT - 180))

    if active:
        black_strip = pygame.Surface((WIDTH-40, 170), pygame.SRCALPHA)
        pygame.draw.rect(black_strip, (0, 0, 0, 128), black_strip.get_rect(), border_radius=20)
        screen.blit(black_strip, (20, HEIGHT - 190))

    # initial deal to player 1, player 2 and dealer
    if initial_deal:
        for i in range(2):
            player_1_hand, game_deck = deal_cards(player_1_hand, game_deck)
            player_2_hand, game_deck = deal_cards(player_2_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
    # once game is activated, and dealt, calculate scores and display cards
    if active:
        player_1_score = calculate_score(player_1_hand)
        player_2_score = calculate_score(player_2_hand)
        draw_cards(player_1_hand, player_2_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_1_score, player_2_score, dealer_score)
    buttons = draw_game(active, records, result_arr)

    # event handling, if quit pressed, then exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons["deal_btn"].collidepoint(event.pos):
                    play_cardshuffle_sound()
                    reset_game(True, True, True, True)
                    game_deck = copy.deepcopy(deck)
                    
            else:
                # if player 1 or player 2 can hit, allow them to draw a card
                if buttons["p1_hit_btn"].collidepoint(event.pos) and player_1_score < 21 and hand_active:
                    play_carddeal_sound()
                    hit_button_1 = draw_button(screen, "Hit me", font, 'black', 'black', 'black', 240, 70, 110, 2000)
                    player_1_hand, game_deck = deal_cards(player_1_hand, game_deck)
                    
                if buttons["p1_stand_btn"].collidepoint(event.pos) and not reveal_dealer:
                    player_1_stand = True

                if buttons["p2_hit_btn"].collidepoint(event.pos) and player_2_score < 21 and hand_active:
                    play_carddeal_sound()
                    player_2_hand, game_deck = deal_cards(player_2_hand, game_deck)
                if buttons["p2_stand_btn"].collidepoint(event.pos) and not reveal_dealer:
                    player_2_stand = True

                if player_1_stand and player_2_stand and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                
                elif len(buttons) == 5:
                    if buttons["newhand_btn"].collidepoint(event.pos):
                        play_cardshuffle_sound()
                        reset_game(True, True, True, True)
                        game_deck = copy.deepcopy(deck)
                        
        # if player busts, automatically end turn - treat like a stand
    if hand_active and player_1_score >= 21 and player_2_score >= 21:
        player_1_stand = True
        player_2_stand = True
        hand_active = False
        reveal_dealer = True
    if player_1_score >= 21:
        player_1_stand = True
    if player_2_score >= 21 and player_1_stand:
        player_2_stand = True
        hand_active = False
        reveal_dealer = True

    result_arr, records, add_score = check_endgame(hand_active, dealer_score, player_1_score, player_2_score, result_arr, records, add_score)

    pygame.display.flip()
pygame.quit()