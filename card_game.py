#!/usr/bin/env python3
"""
Card Game Logic for Three Card Roulette
"""
import random

class CardGame:
    def __init__(self, translation_func):
        self.t = translation_func
        self.cards = ['Hearts', 'Diamonds', 'Clubs', 'Spades', 'Joker']
    
    def get_card_color(self, card):
        """Get the color of a card"""
        if card in ['Hearts', 'Diamonds']:
            return self.t('red')
        elif card in ['Clubs', 'Spades']:
            return self.t('black')
        return None  # Joker has no color
    
    def get_translated_card(self, card):
        """Get translated card name"""
        card_map = {
            'Hearts': self.t('hearts'),
            'Diamonds': self.t('diamonds'),
            'Clubs': self.t('clubs'),
            'Spades': self.t('spades'),
            'Joker': 'Joker'
        }
        return card_map.get(card, card)
    
    def calculate_winnings(self, drawn_card, bet):
        """Calculate winnings for a bet"""
        if bet['type'] == self.t('color'):
            card_color = self.get_card_color(drawn_card)
            if card_color == bet['choice']:
                return bet['amount'] * 2  # 2:1 payout
        elif bet['type'] == self.t('exact'):
            if self.get_translated_card(drawn_card) == bet['choice']:
                return bet['amount'] * 3  # 3:1 payout
        return 0
    
    def place_color_bet(self, language):
        """Handle color betting input"""
        while True:
            choice = input(self.t('bet_color')).upper()
            if language == 'es':
                if choice in ['R', 'N']:
                    return self.t('red') if choice == 'R' else self.t('black')
            elif language == 'fr':
                if choice in ['R', 'N']:
                    return self.t('red') if choice == 'R' else self.t('black')
            elif language == 'de':
                if choice in ['R', 'S']:
                    return self.t('red') if choice == 'R' else self.t('black')
            else:  # English
                if choice in ['R', 'B']:
                    return self.t('red') if choice == 'R' else self.t('black')
            print(self.t('enter_rb'))
    
    def place_exact_bet(self):
        """Handle exact suit betting input"""
        print(self.t('choose_suit'))
        print(f"1. {self.t('hearts_red')}")
        print(f"2. {self.t('diamonds_red')}")
        print(f"3. {self.t('clubs_black')}")
        print(f"4. {self.t('spades_black')}")
        while True:
            try:
                choice = int(input(self.t('enter_1234')))
                if choice == 1:
                    return self.t('hearts')
                elif choice == 2:
                    return self.t('diamonds')
                elif choice == 3:
                    return self.t('clubs')
                elif choice == 4:
                    return self.t('spades')
                else:
                    print(self.t('enter_1234_msg'))
            except ValueError:
                print(self.t('valid_number'))
    
    def get_bet_amount(self, balance):
        """Get bet amount from user"""
        while True:
            try:
                amount = int(input(self.t('enter_amount', min(100, balance))))
                if 1 <= amount <= min(100, balance):
                    return amount
                else:
                    print(self.t('invalid_amount', min(100, balance)))
            except ValueError:
                print(self.t('valid_number'))
    
    def add_single_bet(self, balance, language):
        """Add a single bet for multiple betting mode"""
        print(f"\n{self.t('choose_bet_type')}")
        print(f"1. {self.t('color_bet_short')}")
        print(f"2. {self.t('exact_bet_short')}")
        
        while True:
            try:
                bet_type = int(input(self.t('enter_12')))
                break
            except ValueError:
                print(self.t('valid_number'))
        
        amount = self.get_bet_amount(balance)
        
        if bet_type == 1:  # Color bet
            choice = self.place_color_bet(language)
            return {'type': self.t('color'), 'choice': choice, 'amount': amount}
        elif bet_type == 2:  # Exact card bet
            choice = self.place_exact_bet()
            return {'type': self.t('exact'), 'choice': choice, 'amount': amount}
        else:
            print(self.t('invalid_choice'))
            return None
    
    def place_multiple_bets(self, game_instance):
        """Handle multiple betting mode"""
        bets = []
        total_bet = 0
        
        print(f"\n{self.t('multiple_mode')}")
        
        while True:
            if total_bet >= game_instance.balance:
                print(self.t('balance_limit'))
                break
                
            bet = self.add_single_bet(game_instance.balance - total_bet, game_instance.language)
            if bet and total_bet + bet['amount'] <= game_instance.balance:
                bets.append(bet)
                total_bet += bet['amount']
                print(f"\n{self.t('bet_added', bet['type'], bet['choice'], bet['amount'])}")
                print(self.t('total_bets', total_bet))
                
                if total_bet < game_instance.balance:
                    continue_betting = input(f"\n{self.t('add_another')}").lower()
                    yes_responses = ['y', 's', 'o', 'j']  # yes, sí, oui, ja
                    if continue_betting not in yes_responses:
                        break
                else:
                    break
            elif bet:
                print(self.t('exceed_balance', game_instance.balance))
            
        return bets
    
    def draw_card_sequence(self, game_instance, achievement_manager):
        """Handle the card drawing sequence with joker logic"""
        print(f"\n{self.t('shuffling')}")
        input(self.t('press_draw'))
        
        draw_count = 0
        while True:
            draw_count += 1
            drawn_card = random.choice(self.cards)
            
            if drawn_card == 'Joker':
                print(f"\n{self.t('joker_reroll', draw_count)}")
                
                # Track consecutive jokers for Triple Rare achievement
                game_instance.stats['consecutive_jokers'] += 1
                if game_instance.stats['consecutive_jokers'] > game_instance.stats['max_consecutive_jokers']:
                    game_instance.stats['max_consecutive_jokers'] = game_instance.stats['consecutive_jokers']
                
                # Check for Triple Rare achievement
                if (game_instance.stats['consecutive_jokers'] >= 3 and 
                    self.t('trophy_triple_rare') not in game_instance.inventory['trophies']):
                    achievement_manager.unlock_achievement(game_instance, self.t('trophy_triple_rare'))
                
                input(self.t('press_another'))
                continue
            else:
                # Reset consecutive jokers when a regular card is drawn
                game_instance.stats['consecutive_jokers'] = 0
                translated_card = self.get_translated_card(drawn_card)
                print(f"\n{self.t('draw_num', draw_count, self.t('winning'), translated_card)}")
                return drawn_card