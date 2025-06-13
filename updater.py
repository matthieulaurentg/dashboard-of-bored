#!/usr/bin/env python3
"""
Auto-updater system for Three Card Roulette
Checks for updates and downloads new versions automatically
"""
import requests
import json
import os
import sys
import subprocess
import tempfile
import zipfile
from datetime import datetime

class GameUpdater:
    def __init__(self):
        self.current_version = self.get_current_version()
        self.github_api_url = "https://api.github.com/repos/matthieu/three-card-roulette"
        self.update_check_url = f"{self.github_api_url}/releases/latest"
        self.game_dir = os.path.dirname(os.path.abspath(__file__))
        
    def get_current_version(self):
        """Get current game version"""
        version_file = os.path.join(os.path.dirname(__file__), 'version.txt')
        try:
            with open(version_file, 'r') as f:
                return f.read().strip()
        except:
            return '1.0.0'
    
    def check_for_updates(self, silent=False):
        """Check if updates are available"""
        try:
            if not silent:
                print("🔍 Checking for updates...")
            
            response = requests.get(self.update_check_url, timeout=10)
            response.raise_for_status()
            
            release_data = response.json()
            latest_version = release_data['tag_name'].lstrip('v')
            
            if self.is_newer_version(latest_version, self.current_version):
                if not silent:
                    print(f"📦 New version available: {latest_version} (current: {self.current_version})")
                return True, latest_version, release_data
            else:
                if not silent:
                    print(f"✅ You have the latest version: {self.current_version}")
                return False, self.current_version, None
                
        except requests.RequestException as e:
            if not silent:
                print(f"❌ Could not check for updates: {e}")
            return False, self.current_version, None
        except Exception as e:
            if not silent:
                print(f"❌ Update check failed: {e}")
            return False, self.current_version, None
    
    def is_newer_version(self, latest, current):
        """Compare version strings"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Pad shorter version with zeros
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            return latest_parts > current_parts
        except:
            return False
    
    def download_update(self, release_data):
        """Download and install update"""
        try:
            print("⬬ Downloading update...")
            
            # Find the download URL for the source code
            download_url = release_data['zipball_url']
            
            # Download to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                response = requests.get(download_url, stream=True)
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        tmp_file.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r⬬ Progress: {percent:.1f}%", end='', flush=True)
                
                print("\n✅ Download complete!")
                return tmp_file.name
                
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return None
    
    def install_update(self, zip_path, release_data):
        """Install the downloaded update"""
        try:
            print("🔧 Installing update...")
            
            # Create backup directory
            backup_dir = os.path.join(self.game_dir, f"backup_{self.current_version}")
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Backup current files
            game_files = ['game.py', 'languages.py', 'stock_market.py', 'achievements.py', 'card_game.py']
            for file in game_files:
                src_path = os.path.join(self.game_dir, file)
                if os.path.exists(src_path):
                    dst_path = os.path.join(backup_dir, file)
                    import shutil
                    shutil.copy2(src_path, dst_path)
            
            # Extract update
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Get the root directory name in the zip
                zip_contents = zip_ref.namelist()
                root_dir = zip_contents[0].split('/')[0]
                
                # Extract game files
                for file in game_files:
                    zip_file_path = f"{root_dir}/{file}"
                    if zip_file_path in zip_contents:
                        # Extract to temporary location first
                        zip_ref.extract(zip_file_path)
                        # Move to game directory
                        src = os.path.join(root_dir, file)
                        dst = os.path.join(self.game_dir, file)
                        import shutil
                        shutil.move(src, dst)
            
            # Update version file
            new_version = release_data['tag_name'].lstrip('v')
            version_file = os.path.join(self.game_dir, 'version.txt')
            with open(version_file, 'w') as f:
                f.write(new_version)
            
            # Cleanup
            os.unlink(zip_path)
            import shutil
            if os.path.exists(root_dir):
                shutil.rmtree(root_dir)
            
            print(f"✅ Update installed successfully! Version {new_version}")
            print("🔄 Please restart the game to use the new version.")
            return True
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            print("🔙 You can restore from backup if needed.")
            return False
    
    def auto_update(self):
        """Perform automatic update check and install"""
        has_update, version, release_data = self.check_for_updates()
        
        if has_update:
            response = input(f"🎮 Update to version {version}? (y/n): ").lower()
            if response in ['y', 'yes']:
                zip_path = self.download_update(release_data)
                if zip_path:
                    if self.install_update(zip_path, release_data):
                        input("Press Enter to exit and restart the game...")
                        sys.exit(0)
                else:
                    print("❌ Update failed!")
        
        return has_update
    
    def update_check_at_startup(self):
        """Silent update check at game startup"""
        try:
            has_update, version, release_data = self.check_for_updates(silent=True)
            if has_update:
                print(f"💡 New version {version} available! Use 'Auto-Update' option in main menu.")
            return has_update
        except:
            return False

def check_updates():
    """Standalone function to check for updates"""
    updater = GameUpdater()
    updater.auto_update()

if __name__ == "__main__":
    check_updates()