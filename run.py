#!/usr/bin/env python3
import requests
import json
import time
import sys
import os
import random
from datetime import datetime
import shutil

# Premium Color Scheme
class Colors:
    # Basic colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    
    # Bright colors
    BRIGHT_RED = '\033[1;91m'
    BRIGHT_GREEN = '\033[1;92m'
    BRIGHT_YELLOW = '\033[1;93m'
    BRIGHT_BLUE = '\033[1;94m'
    BRIGHT_MAGENTA = '\033[1;95m'
    BRIGHT_CYAN = '\033[1;96m'
    
    # Styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    
    # Reset
    END = '\033[0m'

def get_terminal_width():
    """Get terminal width"""
    return shutil.get_terminal_size().columns

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def animated_text(text, speed=0.03, color=Colors.WHITE, style=""):
    """Typewriter effect with smooth animation"""
    sys.stdout.write(f"{style}{color}")
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(f"{Colors.END}\n")

def loading_spinner(message="PROCESSING", duration=2):
    """Smooth loading spinner"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < duration:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r{Colors.CYAN}{frame} {message}{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    
    sys.stdout.write("\r" + " " * 50 + "\r")

def progress_bar(progress, total=100, prefix="", suffix=""):
    """Animated progress bar"""
    bar_length = 40
    filled = int(bar_length * progress / total)
    bar = '█' * filled + '░' * (bar_length - filled)
    
    sys.stdout.write(f"\r{Colors.CYAN}{prefix} |{bar}| {progress}% {suffix}{Colors.END}")
    sys.stdout.flush()
    
    if progress == total:
        sys.stdout.write("\n")

def matrix_effect(duration=2):
    """Matrix rain effect - smooth and clean"""
    chars = "01"
    width = min(get_terminal_width() - 2, 80)
    drops = [random.randint(0, 20) for _ in range(width)]
    
    start_time = time.time()
    while time.time() - start_time < duration:
        sys.stdout.write('\033[32m')
        for i in range(width):
            if drops[i] == 0:
                if random.random() > 0.95:
                    drops[i] = random.randint(1, 15)
                sys.stdout.write(' ')
            else:
                sys.stdout.write(random.choice(chars))
                drops[i] -= 1
        sys.stdout.write('\033[0m\n')
        sys.stdout.flush()
        time.sleep(0.03)

def display_banner():
    """Modern animated banner"""
    clear_screen()
    
    # Top spacing
    print("\n" * 2)
    
    # Animated title
    title = "PAKISTANI SIM DATABASE"
    subtitle = "LOOKUP SYSTEM"
    
    # Color sequence for title
    colors = [Colors.CYAN, Colors.BLUE, Colors.MAGENTA, Colors.PURPLE] if hasattr(Colors, 'PURPLE') else [Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
    
    # Animate title
    for i, char in enumerate(title):
        color = colors[i % len(colors)]
        sys.stdout.write(f"{Colors.BOLD}{color}{char}{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.04)
    
    print()
    
    # Animate subtitle
    for char in subtitle:
        sys.stdout.write(f"{Colors.BOLD}{Colors.WHITE}{char}{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.03)
    
    print("\n")
    
    # Team info
    animated_text("TEAM ATHEX CYBER INTELLIGENCE", 0.02, Colors.YELLOW, Colors.BOLD)
    print()
    
    # Version info
    animated_text("v2.0 - Professional Edition", 0.01, Colors.GRAY, Colors.DIM)
    print("\n")
    
    # Decorative line
    width = get_terminal_width()
    line = "─" * min(width - 4, 70)
    animated_text(line, 0.001, Colors.CYAN, Colors.DIM)
    print()

def lookup_sim(number):
    """Query the SIM database API"""
    url = f"https://fam-official.serv00.net/api/database.php?number={number}"
    
    try:
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        data = response.json()
        return data, json.dumps(data, indent=2, ensure_ascii=False)
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Network error: {str(e)}"}, None
    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid response from server"}, None

def display_result(data, raw_json, number):
    """Professional animated result display"""
    clear_screen()
    
    # Header with animation
    print("\n")
    animated_text("QUERY RESULTS", 0.05, Colors.BRIGHT_CYAN, Colors.BOLD)
    print()
    
    # Animated separator
    for i in range(20):
        sys.stdout.write(f"\r{Colors.CYAN}{'█' * i}{'░' * (20-i)}{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.02)
    print("\n")
    
    # Phone number with reveal animation
    sys.stdout.write(f"{Colors.WHITE}📱 Number: ")
    for char in number:
        sys.stdout.write(f"{Colors.BRIGHT_GREEN}{char}{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.05)
    print()
    
    # Timestamp
    current_time = datetime.now().strftime('%H:%M:%S')
    sys.stdout.write(f"{Colors.GRAY}🕐 Time: {Colors.WHITE}{current_time}{Colors.END}\n")
    print()
    
    if data.get("success"):
        # Success indicator with pulse
        for _ in range(3):
            sys.stdout.write(f"\r{Colors.BRIGHT_GREEN}● STATUS: SUCCESSFUL{Colors.END}")
            sys.stdout.flush()
            time.sleep(0.3)
            sys.stdout.write(f"\r{Colors.GREEN}○ STATUS: SUCCESSFUL{Colors.END}")
            sys.stdout.flush()
            time.sleep(0.3)
        print("\n")
        
        # Animated data reveal
        print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")
        
        # Icons mapping
        icons = {
            'name': '👤',
            'cnic': '🪪',
            'address': '📍',
            'network': '📡',
            'operator': '📞',
            'sim_type': '💳',
            'status': '🔴',
            'issue_date': '📅',
            'expiry_date': '⏰',
            'location': '🗺️',
            'city': '🏙️',
            'province': '🗾',
            'district': '🏛️',
            'tehsil': '🏘️',
            'postal_code': '📮',
            'msisdn': '🔢',
            'sim_owner': '👤'
        }
        
        # Animate each field
        for key, value in data.items():
            if key not in ["success", "credit"]:
                icon = icons.get(key, '📋')
                key_display = key.replace('_', ' ').title()
                
                # Loading dots animation
                sys.stdout.write(f"{Colors.GRAY}{icon} {key_display}: ")
                sys.stdout.flush()
                time.sleep(0.2)
                
                # Value reveal with typewriter
                value_str = str(value)
                color = random.choice([Colors.BRIGHT_CYAN, Colors.BRIGHT_WHITE, Colors.BRIGHT_YELLOW])
                
                for char in value_str:
                    sys.stdout.write(f"{color}{char}{Colors.END}")
                    sys.stdout.flush()
                    time.sleep(0.02)
                
                print()
                time.sleep(0.1)
        
        # Credits
        if "credit" in data:
            print(f"{Colors.CYAN}{'─' * 50}{Colors.END}")
            sys.stdout.write(f"{Colors.GRAY}👨‍💻 ")
            for char in str(data['credit']):
                sys.stdout.write(f"{Colors.DIM}{char}{Colors.END}")
                sys.stdout.flush()
                time.sleep(0.02)
            print()
    else:
        # Error display
        print(f"{Colors.BRIGHT_RED}● STATUS: FAILED{Colors.END}")
        print()
        
        if "error" in data:
            sys.stdout.write(f"{Colors.RED}⚠️ ")
            for char in str(data['error']):
                sys.stdout.write(f"{Colors.RED}{char}{Colors.END}")
                sys.stdout.flush()
                time.sleep(0.02)
            print()
        
        if "usage" in data:
            sys.stdout.write(f"{Colors.YELLOW}📖 ")
            for char in str(data['usage']):
                sys.stdout.write(f"{Colors.YELLOW}{char}{Colors.END}")
                sys.stdout.flush()
                time.sleep(0.02)
            print()
    
    # Footer
    print(f"\n{Colors.CYAN}{'═' * 50}{Colors.END}")
    
    # JSON viewer option
    if raw_json:
        sys.stdout.write(f"{Colors.GRAY}💾 View raw JSON? (y/n): {Colors.END}")
        choice = input().strip().lower()
        
        if choice == 'y':
            print(f"\n{Colors.DIM}{'─' * 50}{Colors.END}")
            print(f"{Colors.WHITE}{Colors.BOLD}RAW JSON RESPONSE:{Colors.END}")
            print()
            
            # Animate JSON display
            for line in raw_json.split('\n'):
                if ':' in line:
                    # Highlight keys and values
                    parts = line.split(':', 1)
                    key = parts[0].strip()
                    value = parts[1].strip() if len(parts) > 1 else ""
                    
                    sys.stdout.write(f"{Colors.GREEN}{key}{Colors.END}: ")
                    sys.stdout.write(f"{Colors.CYAN}{value}{Colors.END}\n")
                    sys.stdout.flush()
                    time.sleep(0.02)
                else:
                    print(line)
                    time.sleep(0.01)
            
            print(f"{Colors.DIM}{'─' * 50}{Colors.END}")

def get_user_input():
    """Get user input with animation"""
    print(f"\n{Colors.CYAN}──────────────────────────────────────{Colors.END}")
    print(f"{Colors.WHITE}📱 Enter SIM number {Colors.GRAY}(e.g., 3001234567){Colors.END}")
    print(f"{Colors.GRAY}Commands: q=quit | b=banner | c=clear | m=matrix{Colors.END}")
    print(f"{Colors.CYAN}──────────────────────────────────────{Colors.END}")
    
    # Animated prompt
    for frame in ["➤", "➜", "➤", "➜"]:
        sys.stdout.write(f"\r{Colors.BRIGHT_GREEN}{frame} {Colors.END}")
        sys.stdout.flush()
        time.sleep(0.1)
    
    user_input = input().strip()
    return user_input

def main():
    """Main program loop"""
    display_banner()
    
    while True:
        user_input = get_user_input()
        
        if user_input.lower() == 'q':
            # Exit animation
            print("\n")
            animated_text("Thank you for using the tool!", 0.03, Colors.BRIGHT_YELLOW, Colors.BOLD)
            animated_text("Goodbye! 👋", 0.05, Colors.BRIGHT_GREEN, Colors.BOLD)
            break
        
        elif user_input.lower() == 'b':
            display_banner()
            continue
        
        elif user_input.lower() == 'c':
            clear_screen()
            continue
        
        elif user_input.lower() == 'm':
            matrix_effect(2)
            continue
        
        elif not user_input:
            print(f"{Colors.YELLOW}⚠️ Please enter a SIM number{Colors.END}")
            continue
        
        elif not user_input.isdigit() or len(user_input) < 10:
            print(f"{Colors.RED}❌ Invalid format! Use 10-11 digits.{Colors.END}")
            continue
        
        # Loading with progress
        print(f"\n{Colors.CYAN}🔍 Searching database...{Colors.END}")
        loading_spinner(f"QUERYING {user_input}", 2)
        
        # Query API
        result, raw_json = lookup_sim(user_input)
        
        # Display result
        display_result(result, raw_json, user_input)
        
        # Continue prompt
        print(f"\n{Colors.GRAY}Press Enter to continue...{Colors.END}", end='')
        input()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️ Program interrupted{Colors.END}")
        print(f"{Colors.GREEN}👋 Goodbye!{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}💥 Error: {str(e)}{Colors.END}")
