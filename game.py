#!/usr/bin/env python3
"""
Main Game File for Three Card Roulette
Combines card gambling with real-time stock trading and achievements
"""
import os
import json
import tempfile
from datetime import datetime

# Import our custom modules
from languages import TRANSLATIONS
from stock_market import StockMarket
from achievements import AchievementManager
from card_game import CardGame
from updater import GameUpdater

class ThreeCardRoulette:
    def __init__(self):
        self.balance = 100
        self.bets = []  # List to store multiple bets
        self.language = 'en'  # Default language
        
        # Use temp directory for save file to avoid permission issues
        try:
            self.save_file = os.path.join(tempfile.gettempdir(), 'three_card_roulette_save.json')
        except:
            self.save_file = 'three_card_roulette_save.json'
        
        # Statistics tracking
        self.stats = {
            'total_bets': 0,
            'total_wins': 0,
            'total_losses': 0,
            'total_amount_bet': 0,
            'total_amount_won': 0,
            'total_amount_lost': 0,
            'games_played': 0,
            'highest_balance': 100,
            'sessions': [],
            'color_wins': 0,
            'exact_wins': 0,
            'multiple_wins': 0,
            'stock_wins': 0,
            'consecutive_jokers': 0,
            'max_consecutive_jokers': 0
        }
        
        # Inventory system
        self.inventory = {
            'shares': {
                'TECH': 0,
                'GOLD': 0,
                'OIL': 0,
                'CRYPTO': 0,
                'FOOD': 0
            },
            'trophies': []
        }
        
        # Session stats (reset each time game starts)
        self.session_stats = {
            'bets': 0,
            'wins': 0,
            'losses': 0
        }
        
        # Initialize game modules
        self.stock_market = StockMarket(self.t)
        self.achievement_manager = AchievementManager(self.t)
        self.card_game = CardGame(self.t)
        self.updater = GameUpdater()
    
    def t(self, key, *args):
        """Translation function"""
        text = TRANSLATIONS[self.language].get(key, key)
        if args:
            return text.format(*args)
        return text
    
    def save_game(self):
        """Save game state to file"""
        save_data = {
            'balance': self.balance,
            'language': self.language,
            'stats': self.stats,
            'inventory': self.inventory,
            'stocks': self.stock_market.stocks,
            'timestamp': datetime.now().isoformat()
        }
        try:
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self):
        """Load game state from file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    save_data = json.load(f)
                
                self.balance = save_data.get('balance', 100)
                self.language = save_data.get('language', 'en')
                self.stats = save_data.get('stats', self.stats)
                self.inventory = save_data.get('inventory', self.inventory)
                
                # Load stocks if available
                if 'stocks' in save_data:
                    self.stock_market.stocks = save_data['stocks']
                
                # Update highest balance if current is higher
                if self.balance > self.stats['highest_balance']:
                    self.stats['highest_balance'] = self.balance
                
                return True
            return False
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    def update_stats(self, bet_amount, winnings):
        """Update game statistics"""
        self.stats['total_bets'] += 1
        self.stats['total_amount_bet'] += bet_amount
        self.session_stats['bets'] += 1
        
        if winnings > 0:
            self.stats['total_wins'] += 1
            self.stats['total_amount_won'] += winnings
            self.session_stats['wins'] += 1
        else:
            self.stats['total_losses'] += 1
            self.stats['total_amount_lost'] += bet_amount
            self.session_stats['losses'] += 1
        
        # Update highest balance
        if self.balance > self.stats['highest_balance']:
            self.stats['highest_balance'] = self.balance
    
    def display_statistics(self):
        """Display comprehensive game statistics"""
        print("\n" + "=" * 50)
        print(f"    {self.t('stats_title')}")
        print("=" * 50)
        
        # Basic stats
        print(self.t('total_bets_made', self.stats['total_bets']))
        print(self.t('total_wins_count', self.stats['total_wins']))
        print(self.t('total_losses_count', self.stats['total_losses']))
        
        # Win rate
        if self.stats['total_bets'] > 0:
            win_rate = (self.stats['total_wins'] / self.stats['total_bets']) * 100
            print(self.t('win_rate', win_rate))
        
        print()
        
        # Money stats
        print(self.t('total_bet_amount', self.stats['total_amount_bet']))
        print(self.t('total_won_amount', self.stats['total_amount_won']))
        print(self.t('total_lost_amount', self.stats['total_amount_lost']))
        
        net_profit = self.stats['total_amount_won'] - self.stats['total_amount_lost']
        print(self.t('net_profit', net_profit))
        print(self.t('highest_balance_ever', self.stats['highest_balance']))
        
        print()
        
        # Session stats
        print(self.t('session_stats', self.session_stats['bets'], 
                     self.session_stats['wins'], self.session_stats['losses']))
        
        print("=" * 50)
        input(self.t('press_enter'))
    
    def display_credits(self):
        """Display credits and ASCII art"""
        print("\n" + "=" * 60)
        print(f"    {self.t('credits_title')}")
        print("=" * 60)
        print()
        print(self.t('ascii_art'))
        print()
        print(f"    {self.t('game_by')}")
        print(f"    {self.t('coding_by')}")
        print()
        print("=" * 60)
        input(self.t('press_enter'))
    
    def select_language(self):
        """Language selection at game start"""
        self.clear_screen()
        print("=" * 60)
        print(self.t('select_language'))
        print("=" * 60)
        print(f"1. {self.t('english')}")
        print(f"2. {self.t('spanish')}")
        print(f"3. {self.t('french')}")
        print(f"4. {self.t('german')}")
        print()
        
        while True:
            try:
                choice = int(input(self.t('enter_lang')))
                if choice == 1:
                    self.language = 'en'
                    break
                elif choice == 2:
                    self.language = 'es'
                    break
                elif choice == 3:
                    self.language = 'fr'
                    break
                elif choice == 4:
                    self.language = 'de'
                    break
                else:
                    print("Please enter 1, 2, 3, or 4")
            except ValueError:
                print("Please enter a valid number.")
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome(self):
        print("=" * 50)
        print(f"    {self.t('welcome')}")
        print("=" * 50)
        print(self.t('balance', self.balance))
        print()
    
    def display_betting_options(self):
        print(self.t('betting_options'))
        print(f"1. {self.t('color_bet')}")
        print(f"2. {self.t('exact_bet')}")
        print(f"3. {self.t('multiple_bets')}")
        print(f"4. {self.t('stock_trading')}")
        print(f"5. {self.t('inventory')}")
        print(f"6. {self.t('view_stats')}")
        print(f"7. Auto-Update")
        print(f"8. {self.t('credits')}")
        print(f"9. {self.t('quit_game')}")
        print()
        print(self.t('joker_note'))
        print()
    
    def play_round(self):
        self.display_betting_options()
        
        while True:
            try:
                choice = int(input(self.t('choose_option')))
                break
            except ValueError:
                print(self.t('valid_number'))
        
        self.bets = []  # Reset bets
        
        if choice == 1:  # Color bet
            bet = {'type': self.t('color'), 'choice': self.card_game.place_color_bet(self.language), 'amount': self.card_game.get_bet_amount(self.balance)}
            self.bets.append(bet)
            
        elif choice == 2:  # Exact card bet
            bet = {'type': self.t('exact'), 'choice': self.card_game.place_exact_bet(), 'amount': self.card_game.get_bet_amount(self.balance)}
            self.bets.append(bet)
            
        elif choice == 3:  # Multiple bets
            self.bets = self.card_game.place_multiple_bets(self)
            if not self.bets:
                return True  # No bets placed, continue
            
        elif choice == 4:  # Stock trading
            return self.stock_market.stock_trading_menu(self)
            
        elif choice == 5:  # Inventory
            self.achievement_manager.display_inventory(self, self.stock_market)
            return True
            
        elif choice == 6:  # View statistics
            self.display_statistics()
            return True
            
        elif choice == 7:  # Auto-Update
            self.updater.auto_update()
            return True
            
        elif choice == 8:  # Credits
            self.display_credits()
            return True
            
        elif choice == 9:  # Quit
            return False
            
        else:
            print(self.t('invalid_choice'))
            return True
        
        # Process card game bets
        if self.bets:
            # Deduct total bets from balance
            total_bet = sum(bet['amount'] for bet in self.bets)
            self.balance -= total_bet
            
            # Draw the winning card
            drawn_card = self.card_game.draw_card_sequence(self, self.achievement_manager)
            
            # Calculate total winnings
            total_winnings = 0
            for bet in self.bets:
                winnings = self.card_game.calculate_winnings(drawn_card, bet)
                total_winnings += winnings
                
                # Update stats for each bet
                self.update_stats(bet['amount'], winnings)
                
                # Track wins by game mode
                if winnings > 0:
                    if bet['type'] == self.t('color'):
                        self.stats['color_wins'] += 1
                    elif bet['type'] == self.t('exact'):
                        self.stats['exact_wins'] += 1
                    
                    # Check if this is a multiple bet round
                    if len(self.bets) > 1:
                        self.stats['multiple_wins'] += 1
                
                # Auto-save after each individual bet
                if self.balance > 0:
                    self.save_game()
                
                if winnings > 0:
                    print(self.t('bet_wins', bet['type'], bet['choice'], bet['amount'], winnings))
                else:
                    print(self.t('bet_loses', bet['type'], bet['choice'], bet['amount']))
            
            if total_winnings > 0:
                self.balance += total_winnings
                print(f"\n{self.t('total_winnings', total_winnings)}")
            else:
                print(f"\n{self.t('total_loss', total_bet)}")
            
            print(self.t('new_balance', self.balance))
            
            # Check achievements after each round
            self.achievement_manager.check_achievements(self)
            
            # Check for game over
            if self.balance <= 0:
                print(f"\n{self.t('game_over')}")
                self.display_statistics()
                print(f"\n{self.t('restarting_game')}")
                self.balance = 100  # Reset to starting balance
                input(self.t('press_enter'))
            else:
                # Auto-save after each round (only if not broke)
                self.save_game()
        
        input(f"\n{self.t('press_enter')}")
        return True
    
    def run(self):
        # Check for updates at startup
        try:
            self.updater.update_check_at_startup()
        except:
            pass  # Continue if update check fails
        
        # Try to load saved game first
        if self.load_game():
            print(self.t('game_loaded'))
            input(self.t('press_enter'))
        else:
            print(self.t('no_save_file'))
            self.select_language()
        
        while True:
            self.clear_screen()
            self.display_welcome()
            
            if not self.play_round():
                break
        
        # Save final game state (only if not broke)
        if self.balance > 0:
            self.save_game()
        print(f"\n{self.t('thanks')}")
        print(self.t('final_balance', self.balance))

def main():
    """Main entry point for the game"""
    game = ThreeCardRoulette()
    game.run()

if __name__ == "__main__":
    main()