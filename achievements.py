#!/usr/bin/env python3
"""
Achievement System for Three Card Roulette
"""

class AchievementManager:
    def __init__(self, translation_func):
        self.t = translation_func
        
    def unlock_achievement(self, game_instance, trophy_name):
        """Unlock an achievement"""
        if trophy_name not in game_instance.inventory['trophies']:
            game_instance.inventory['trophies'].append(trophy_name)
            print(f"\n{self.t('achievement_unlocked', trophy_name)}")
            input(self.t('press_enter'))
    
    def check_achievements(self, game_instance):
        """Check for achievement unlocks"""
        # All Gamemode Achiever
        if (game_instance.stats['color_wins'] > 0 and 
            game_instance.stats['exact_wins'] > 0 and 
            game_instance.stats['multiple_wins'] > 0 and 
            game_instance.stats['stock_wins'] > 0 and
            self.t('trophy_all_gamemode') not in game_instance.inventory['trophies']):
            self.unlock_achievement(game_instance, self.t('trophy_all_gamemode'))
        
        # Millionaire achievement
        if (game_instance.balance >= 1000 and 
            self.t('trophy_millionaire') not in game_instance.inventory['trophies']):
            self.unlock_achievement(game_instance, self.t('trophy_millionaire'))
        
        # Stock Master achievement
        total_shares = sum(game_instance.inventory['shares'].values())
        if (total_shares >= 100 and 
            self.t('trophy_stock_master') not in game_instance.inventory['trophies']):
            self.unlock_achievement(game_instance, self.t('trophy_stock_master'))
        
        # Triple Rare achievement (checked in card game logic)
        if (game_instance.stats['max_consecutive_jokers'] >= 3 and 
            self.t('trophy_triple_rare') not in game_instance.inventory['trophies']):
            self.unlock_achievement(game_instance, self.t('trophy_triple_rare'))
    
    def display_inventory(self, game_instance, stock_market):
        """Display player inventory with shares and trophies"""
        print(f"\n{self.t('inventory_title')}")
        print("=" * 50)
        
        # Calculate portfolio value
        portfolio_value = 0
        for symbol, shares in game_instance.inventory['shares'].items():
            portfolio_value += shares * stock_market.stocks[symbol]['price']
        
        print(self.t('portfolio_value', portfolio_value))
        print()
        
        # Display shares
        print("📈 SHARES OWNED:")
        has_shares = False
        for symbol, shares in game_instance.inventory['shares'].items():
            if shares > 0:
                value = shares * stock_market.stocks[symbol]['price']
                print(f"  {symbol}: {shares} shares (${value:.2f})")
                has_shares = True
        
        if not has_shares:
            print("  No shares owned")
        
        print()
        
        # Display trophies
        print(self.t('trophies_title'))
        if game_instance.inventory['trophies']:
            for trophy in game_instance.inventory['trophies']:
                print(f"  🏆 {trophy}")
        else:
            print(f"  {self.t('no_trophies')}")
        
        print("=" * 50)
        input(self.t('press_enter'))