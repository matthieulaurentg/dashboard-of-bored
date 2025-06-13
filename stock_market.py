#!/usr/bin/env python3
"""
Stock Market Trading System for Three Card Roulette
"""
import random

class StockMarket:
    def __init__(self, translation_func):
        self.t = translation_func
        self.stocks = {
            'TECH': {'price': 100.0, 'name': 'Tech Corp', 'volatility': 0.15},
            'GOLD': {'price': 150.0, 'name': 'Gold Mining', 'volatility': 0.08},
            'OIL': {'price': 80.0, 'name': 'Oil Giant', 'volatility': 0.12},
            'CRYPTO': {'price': 200.0, 'name': 'CryptoCoin', 'volatility': 0.25},
            'FOOD': {'price': 60.0, 'name': 'Food Chain', 'volatility': 0.06}
        }
    
    def update_stock_prices(self):
        """Update stock prices with realistic volatility"""
        for symbol, data in self.stocks.items():
            # Random price movement based on volatility
            change_percent = random.uniform(-data['volatility'], data['volatility'])
            data['price'] *= (1 + change_percent)
            # Keep prices above $1
            data['price'] = max(1.0, data['price'])
    
    def get_stocks(self):
        """Return current stock data"""
        return self.stocks
    
    def display_market(self, inventory_shares):
        """Display current stock market prices"""
        print(f"\n{self.t('stock_menu')}")
        print("=" * 50)
        
        stock_list = list(self.stocks.keys())
        for i, symbol in enumerate(stock_list, 1):
            data = self.stocks[symbol]
            owned = inventory_shares[symbol]
            print(f"{i}. {symbol} ({data['name']})")
            print(f"   Price: ${data['price']:.2f}")
            print(f"   Shares Owned: {owned}")
            print()
    
    def stock_trading_menu(self, game_instance):
        """Main stock trading interface"""
        self.update_stock_prices()  # Update prices when entering market
        
        print(f"\n{self.t('stock_menu')}")
        print(f"1. {self.t('buy_stocks')}")
        print(f"2. {self.t('sell_stocks')}")
        print(f"3. {self.t('view_market')}")
        print()
        
        while True:
            try:
                choice = int(input(self.t('enter_stock_choice')))
                if choice in [1, 2, 3]:
                    break
                print("Please enter 1, 2, or 3")
            except ValueError:
                print(self.t('valid_number'))
        
        if choice == 1:
            self.buy_stocks(game_instance)
        elif choice == 2:
            self.sell_stocks(game_instance)
        elif choice == 3:
            self.display_market(game_instance.inventory['shares'])
            input(self.t('press_enter'))
        
        return True
    
    def buy_stocks(self, game_instance):
        """Buy shares of stocks"""
        try:
            print(f"\n{self.t('buy_stocks')}")
            
            # Display market
            self.display_market(game_instance.inventory['shares'])
            
            stock_list = list(self.stocks.keys())
            while True:
                try:
                    choice = int(input(self.t('enter_stock_symbol')))
                    if 1 <= choice <= len(stock_list):
                        symbol = stock_list[choice - 1]
                        break
                    print(f"Please enter 1-{len(stock_list)}")
                except ValueError:
                    print(self.t('valid_number'))
            
            # Get number of shares
            while True:
                try:
                    shares = int(input(self.t('enter_shares')))
                    if shares > 0:
                        break
                    print("Must be greater than 0")
                except ValueError:
                    print(self.t('valid_number'))
            
            # Calculate cost
            cost = shares * self.stocks[symbol]['price']
            
            if cost > game_instance.balance:
                print(self.t('insufficient_funds'))
                input(self.t('press_enter'))
                return
            
            # Execute purchase
            game_instance.balance -= cost
            game_instance.inventory['shares'][symbol] += shares
            
            print(f"\n✅ Bought {shares} shares of {symbol} for ${cost:.2f}")
            print(self.t('new_balance', game_instance.balance))
            
            # Check for stock master achievement
            total_shares = sum(game_instance.inventory['shares'].values())
            if total_shares >= 100 and self.t('trophy_stock_master') not in game_instance.inventory['trophies']:
                game_instance.unlock_achievement(self.t('trophy_stock_master'))
            
            # Track stock trading activity
            game_instance.stats['stock_wins'] += 1
            
            # Auto-save
            if game_instance.balance > 0:
                game_instance.save_game()
            
            input(self.t('press_enter'))
            
        except Exception as e:
            print(f"Error in buy_stocks: {e}")
            input("Press Enter to continue...")
            return
    
    def sell_stocks(self, game_instance):
        """Sell shares of stocks"""
        try:
            print(f"\n{self.t('sell_stocks')}")
            
            # Check if player owns any stocks
            total_owned = sum(game_instance.inventory['shares'].values())
            if total_owned == 0:
                print("You don't own any stocks!")
                input(self.t('press_enter'))
                return
            
            # Display market
            self.display_market(game_instance.inventory['shares'])
            
            stock_list = list(self.stocks.keys())
            while True:
                try:
                    choice = int(input(self.t('enter_stock_symbol')))
                    if 1 <= choice <= len(stock_list):
                        symbol = stock_list[choice - 1]
                        break
                    print(f"Please enter 1-{len(stock_list)}")
                except ValueError:
                    print(self.t('valid_number'))
            
            owned_shares = game_instance.inventory['shares'][symbol]
            if owned_shares == 0:
                print(self.t('insufficient_shares'))
                input(self.t('press_enter'))
                return
            
            # Get number of shares to sell
            while True:
                try:
                    shares = int(input(f"{self.t('enter_shares')} (Max: {owned_shares}): "))
                    if 0 < shares <= owned_shares:
                        break
                    print(f"Must be between 1 and {owned_shares}")
                except ValueError:
                    print(self.t('valid_number'))
            
            # Calculate earnings
            earnings = shares * self.stocks[symbol]['price']
            
            # Execute sale
            game_instance.balance += earnings
            game_instance.inventory['shares'][symbol] -= shares
            
            print(f"\n✅ Sold {shares} shares of {symbol} for ${earnings:.2f}")
            print(self.t('new_balance', game_instance.balance))
            
            # Check for millionaire achievement
            if game_instance.balance >= 1000 and self.t('trophy_millionaire') not in game_instance.inventory['trophies']:
                game_instance.unlock_achievement(self.t('trophy_millionaire'))
            
            # Auto-save
            game_instance.save_game()
            
            input(self.t('press_enter'))
            
        except Exception as e:
            print(f"Error in sell_stocks: {e}")
            input("Press Enter to continue...")
            return