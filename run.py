#!/usr/bin/env python3
import requests
import json
import time
import sys
import os
import random
from datetime import datetime
import shutil
import webbrowser
import tempfile

# Premium Color Scheme for Terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BRIGHT_RED = '\033[1;91m'
    BRIGHT_GREEN = '\033[1;92m'
    BRIGHT_YELLOW = '\033[1;93m'
    BRIGHT_BLUE = '\033[1;94m'
    BRIGHT_MAGENTA = '\033[1;95m'
    BRIGHT_CYAN = '\033[1;96m'
    BRIGHT_WHITE = '\033[1;97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    END = '\033[0m'

def get_terminal_width():
    return shutil.get_terminal_size().columns

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def animated_text(text, speed=0.02, color=Colors.WHITE, style=""):
    sys.stdout.write(f"{style}{color}")
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(f"{Colors.END}\n")

def display_ascii_banner():
    clear_screen()
    
    ascii_art = f"""
{Colors.CYAN}{Colors.BOLD}
    ██████╗  █████╗ ██╗  ██╗      ███████╗██╗███╗   ███╗
    ██╔══██╗██╔══██╗██║ ██╔╝      ██╔════╝██║████╗ ████║
    ██████╔╝███████║█████╔╝       ███████╗██║██╔████╔██║ 
    ██╔═══╝ ██╔══██║██╔═██╗       ╚════██║██║██║╚██╔╝██║ 
    ██║     ██║  ██║██║  ██╗      ███████║██║██║ ╚═╝ ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝      ╚══════╝╚═╝╚═╝     ╚═╝
{Colors.END}
{Colors.BRIGHT_YELLOW}{Colors.BOLD}
    ██████╗  █████╗ ████████╗ █████╗ ██████╗  █████╗ ███████╗███████╗
    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██║  ██║███████║   ██║   ███████║██████╔╝███████║███████╗█████╗  
    ██║  ██║██╔══██║   ██║   ██╔══██║██╔══██╗██╔══██║╚════██║██╔══╝  
    ██████╔╝██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║███████║███████╗
    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
{Colors.END}
{Colors.BRIGHT_GREEN}{Colors.BOLD}
     
{Colors.END}
{Colors.BRIGHT_MAGENTA}
                        TEAM ATHEX            
                 PROFESSIONAL SIM DATABASE TOOL                  

{Colors.END}
    """
    
    lines = ascii_art.split('\n')
    for line in lines:
        if line.strip():
            print(line)
            time.sleep(0.02)
        else:
            print()
            time.sleep(0.01)
    
    print(f"\n{Colors.GRAY}Version 5.0 | Raw Data Display | Build: {datetime.now().strftime('%Y-%m-%d')}{Colors.END}")
    print(f"{Colors.GRAY}{'=' * 70}{Colors.END}\n")

def loading_animation(message="PROCESSING", duration=2):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    colors = [Colors.CYAN, Colors.BRIGHT_CYAN, Colors.BLUE, Colors.BRIGHT_BLUE]
    start_time = time.time()
    i = 0
    
    while time.time() - start_time < duration:
        elapsed = time.time() - start_time
        progress = int((elapsed / duration) * 100)
        frame = frames[i % len(frames)]
        color = colors[i % len(colors)]
        
        bar_length = 30
        filled = int(bar_length * progress / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        
        sys.stdout.write(f"\r{color}{frame} {message} [{bar}] {progress}%{Colors.END}")
        sys.stdout.flush()
        time.sleep(0.05)
        i += 1
    
    sys.stdout.write("\r" + " " * 80 + "\r")

def lookup_sim(number):
    """Query the SIM database API and return raw response"""
    url = f"https://athex-sim-data-base-api.athex-black-hat.workers.dev/?number={number}"
    
    try:
        response = requests.get(url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        # Return both parsed JSON and raw text
        data = response.json()
        raw_text = response.text
        return data, raw_text
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"Network error: {str(e)}"}, str({"success": False, "error": f"Network error: {str(e)}"})
    except json.JSONDecodeError:
        return {"success": False, "error": "Invalid response"}, response.text if 'response' in locals() else "Invalid response"

def generate_html_report(raw_data, number):
    """Generate HTML report with exact API response data"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Parse raw data if it's a string
    if isinstance(raw_data, str):
        try:
            data_dict = json.loads(raw_data)
        except:
            data_dict = {"raw_response": raw_data}
    else:
        data_dict = raw_data
    
    # Format phone number
    formatted_number = f"+92 {number[-10:-7]} {number[-7:-4]} {number[-4:]}" if len(number) >= 10 else number
    
    # Build HTML data sections dynamically from API response
    data_sections = ""
    
    if isinstance(data_dict, dict):
        for key, value in data_dict.items():
            if isinstance(value, dict):
                # Nested dictionary
                data_sections += f'''
                <div class="section">
                    <div class="section-title">📋 {key.replace('_', ' ').title()}</div>
                    <div class="info-grid">
                '''
                for sub_key, sub_value in value.items():
                    data_sections += f'''
                        <div class="info-item">
                            <div class="info-label">{sub_key.replace('_', ' ').title()}</div>
                            <div class="info-value">{sub_value}</div>
                        </div>
                    '''
                data_sections += '''
                    </div>
                </div>
                '''
            elif isinstance(value, list):
                # List data
                data_sections += f'''
                <div class="section">
                    <div class="section-title">📋 {key.replace('_', ' ').title()}</div>
                    <div class="info-grid">
                '''
                for item in value:
                    data_sections += f'''
                        <div class="info-item">
                            <div class="info-value">{item}</div>
                        </div>
                    '''
                data_sections += '''
                    </div>
                </div>
                '''
            else:
                # Simple key-value pair
                data_sections += f'''
                <div class="section">
                    <div class="section-title">📋 {key.replace('_', ' ').title()}</div>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">{key.replace('_', ' ').title()}</div>
                            <div class="info-value">{value}</div>
                        </div>
                    </div>
                </div>
                '''
    
    # Also show raw JSON
    raw_json_pretty = json.dumps(data_dict, indent=2, ensure_ascii=False)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIM Database Report - {formatted_number}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            animation: gradientShift 10s ease infinite;
        }}
        
        @keyframes gradientShift {{
            0% {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
            25% {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }}
            50% {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }}
            75% {{ background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }}
            100% {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        }}
        
        .container {{
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            width: 100%;
            max-width: 800px;
            margin: 0 auto;
            overflow: hidden;
            animation: slideIn 0.5s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{
                transform: translateY(-50px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 10s linear infinite;
        }}
        
        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
            position: relative;
            z-index: 1;
        }}
        
        .header .number {{
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 2px;
            position: relative;
            z-index: 1;
            animation: pulse 2s ease infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 8px 16px;
            border-radius: 25px;
            font-weight: bold;
            margin-top: 15px;
            position: relative;
            z-index: 1;
            animation: glow 1.5s ease infinite;
        }}
        
        .status-success {{
            background: #4CAF50;
            color: white;
        }}
        
        .status-error {{
            background: #f44336;
            color: white;
        }}
        
        @keyframes glow {{
            0%, 100% {{ box-shadow: 0 0 20px rgba(76, 175, 80, 0.5); }}
            50% {{ box-shadow: 0 0 40px rgba(76, 175, 80, 0.8); }}
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            margin-bottom: 25px;
            animation: fadeInUp 0.6s ease-out;
            animation-fill-mode: both;
        }}
        
        @keyframes fadeInUp {{
            from {{
                transform: translateY(20px);
                opacity: 0;
            }}
            to {{
                transform: translateY(0);
                opacity: 1;
            }}
        }}
        
        .section:nth-child(1) {{ animation-delay: 0.1s; }}
        .section:nth-child(2) {{ animation-delay: 0.2s; }}
        .section:nth-child(3) {{ animation-delay: 0.3s; }}
        .section:nth-child(4) {{ animation-delay: 0.4s; }}
        .section:nth-child(5) {{ animation-delay: 0.5s; }}
        .section:nth-child(6) {{ animation-delay: 0.6s; }}
        
        .section-title {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            position: relative;
        }}
        
        .section-title::after {{
            content: '';
            position: absolute;
            bottom: -3px;
            left: 0;
            width: 50px;
            height: 3px;
            background: #764ba2;
            animation: slideLine 2s ease infinite;
        }}
        
        @keyframes slideLine {{
            0%, 100% {{ width: 50px; }}
            50% {{ width: 100px; }}
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }}
        
        .info-item {{
            padding: 12px;
            background: #f8f9fa;
            border-radius: 10px;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .info-item:hover {{
            background: #e9ecef;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .info-label {{
            font-size: 12px;
            color: #6c757d;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .info-value {{
            font-size: 16px;
            font-weight: bold;
            color: #333;
            word-break: break-word;
        }}
        
        .raw-json {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 10px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            margin-top: 10px;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
        }}
        
        .watermark {{
            position: fixed;
            bottom: 10px;
            right: 10px;
            opacity: 0.3;
            font-size: 12px;
            color: #333;
            z-index: 999;
        }}
        
        @media (max-width: 600px) {{
            .info-grid {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 22px;
            }}
            
            .header .number {{
                font-size: 24px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 SIM DATABASE REPORT</h1>
            <div class="number">{formatted_number}</div>
            <div class="status-badge {'status-success' if data_dict.get('success', True) else 'status-error'}">
                {'✅ SUCCESSFUL' if data_dict.get('success', True) else '❌ FAILED'}
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <div class="section-title">📌 Query Details</div>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Query Time</div>
                        <div class="info-value">{current_time}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Phone Number</div>
                        <div class="info-value">{formatted_number}</div>
                    </div>
                </div>
            </div>
            
            {data_sections}
            
            <div class="section">
                <div class="section-title">🔧 Raw API Response</div>
                <div class="raw-json">{raw_json_pretty}</div>
            </div>
        </div>
        
        <div class="footer">
            <p>Data retrieved from API at {current_time}</p>
            <p>© 2026 ATHEX CYBER INTELLIGENCE - All Rights Reserved</p>
        </div>
    </div>
    
    <div class="watermark">ATHEX CYBER TOOL v5.0</div>
</body>
</html>"""
    
    # Save HTML to temp file
    temp_dir = tempfile.gettempdir()
    html_file = os.path.join(temp_dir, f"sim_report_{number}_{int(time.time())}.html")
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return html_file

def display_result_in_browser(raw_data, number):
    """Generate HTML report with raw data and open in browser"""
    print(f"\n{Colors.BRIGHT_CYAN}📊 Generating HTML Report...{Colors.END}")
    loading_animation("CREATING REPORT", 2)
    
    # Generate HTML report with raw data
    html_file = generate_html_report(raw_data, number)
    
    print(f"{Colors.BRIGHT_GREEN}✅ Report generated successfully!{Colors.END}")
    print(f"{Colors.WHITE}📁 File: {html_file}{Colors.END}")
    print(f"{Colors.BRIGHT_YELLOW}🌐 Opening in browser...{Colors.END}")
    
    # Open in browser
    time.sleep(1)
    webbrowser.open(f'file://{html_file}')
    
    print(f"{Colors.BRIGHT_GREEN}✅ Report opened in browser!{Colors.END}")
    print(f"{Colors.GRAY}💡 Report contains exact API response data{Colors.END}")

def get_user_input():
    print(f"\n{Colors.CYAN}{'─' * 60}{Colors.END}")
    print(f"{Colors.WHITE}{Colors.BOLD}📱 ENTER SIM NUMBER{Colors.END}")
    print(f"{Colors.GRAY}Format: 3001234567 (10-11 digits){Colors.END}")
    print(f"{Colors.GRAY}Commands: q=quit | b=banner | c=clear | m=matrix{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 60}{Colors.END}")
    
    frames = ["➤", "➜", "➤", "➜", "➤", "➜"]
    for frame in frames:
        sys.stdout.write(f"\r{Colors.BRIGHT_GREEN}{frame} {Colors.END}")
        sys.stdout.flush()
        time.sleep(0.1)
    
    user_input = input().strip()
    return user_input

def main():
    display_ascii_banner()
    
    while True:
        user_input = get_user_input()
        
        if user_input.lower() == 'q':
            print("\n")
            animated_text("Exiting SIM Database Tool...", 0.02, Colors.BRIGHT_YELLOW)
            animated_text("Thank you for using ATHEX Cyber Tool!", 0.03, Colors.BRIGHT_GREEN, Colors.BOLD)
            animated_text("Stay Legal. Stay Safe. 🔒", 0.04, Colors.BRIGHT_CYAN)
            break
        
        elif user_input.lower() == 'b':
            display_ascii_banner()
            continue
        
        elif user_input.lower() == 'c':
            clear_screen()
            continue
        
        elif not user_input:
            print(f"{Colors.YELLOW}⚠️ Please enter a SIM number{Colors.END}")
            continue
        
        elif not user_input.isdigit() or len(user_input) < 10:
            print(f"{Colors.RED}❌ Invalid format! Use 10-11 digits only.{Colors.END}")
            continue
        
        print(f"\n{Colors.BRIGHT_CYAN}🔍 Searching SIM Database...{Colors.END}")
        loading_animation(f"QUERYING {user_input}", 3)
        
        # Get both parsed data and raw response
        result, raw_response = lookup_sim(user_input)
        
        # Display raw response in browser
        display_result_in_browser(raw_response, user_input)
        
        print(f"\n{Colors.GRAY}Press Enter to continue...{Colors.END}", end='')
        input()
        clear_screen()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️ Program interrupted by user{Colors.END}")
        print(f"{Colors.GREEN}👋 Goodbye!{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}💥 An error occurred: {str(e)}{Colors.END}")
