import os
import sys
import time
import bmi_logic
import database_manager
import matplotlib.pyplot as plt

# ANSI Colors for Terminal Theme (Cyan/Blue/Bold)
# Note: May require typical terminal support.
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    print(f"{Color.CYAN}{Color.BOLD}")
    print("==================================================")
    print("        BMI TERMINAL LINK           ")
    print("==================================================")
    print(f"{Color.ENDC}")

def typing_print(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def visualize_trend(name):
    print(f"\n{Color.BLUE}[INFO] Accessing Neural Archives for {name}...{Color.ENDC}")
    history = database_manager.get_user_history(name)
    
    if not history:
        print(f"{Color.WARNING}>> No existing data found for subject: {name}{Color.ENDC}")
        return

    # Text-based history
    print(f"\n{Color.BOLD}>>> RECORD HISTORY ({name}){Color.ENDC}")
    print(f"{'DATE':<25} | {'BMI':<10}")
    print("-" * 40)
    
    dates = []
    bmis = []
    
    for record in history:
        r_date, r_bmi = record
        print(f"{r_date:<25} | {r_bmi:.2f}")
        dates.append(r_date)
        bmis.append(r_bmi)

    # Matplotlib Graph option
    choice = input(f"\n{Color.CYAN}>> Initialize Visual Projection (Matplotlib Graph)? (y/n): {Color.ENDC}").lower()
    if choice == 'y':
        try:
            plt.figure(figsize=(10, 6))
            plt.style.use('dark_background')
            plt.plot(dates, bmis, marker='o', linestyle='-', color='#00FFDD', label='BMI Trend')
            
            # Reference lines
            plt.axhline(y=18.5, color='#44FF44', linestyle='--', alpha=0.5, label='Normal Min')
            plt.axhline(y=24.9, color='#44FF44', linestyle='--', alpha=0.5, label='Normal Max')
            plt.axhline(y=30, color='#FF4444', linestyle=':', alpha=0.5, label='Obese')
            
            plt.title(f"BIOMETRIC TREND ANALYSIS: {name.upper()}")
            plt.xlabel("Timeline")
            plt.ylabel("BMI Index")
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            
            print(f"{Color.GREEN}>> Displaying visual data stream...{Color.ENDC}")
            plt.show()
        except Exception as e:
            print(f"{Color.FAIL}>> Visualization Subsystem Failed: {e}{Color.ENDC}")

def run_cli():
    database_manager.init_db()
    
    while True:
        clear_screen()
        print_banner()
        
        print(f"1. {Color.BOLD}INITIATE NEW SCAN{Color.ENDC} (Calculate BMI)")
        print(f"2. {Color.BOLD}ACCESS ARCHIVES{Color.ENDC} (View History/Graph)")
        print(f"3. {Color.BOLD}TERMINATE LINK{Color.ENDC} (Exit)")
        
        choice = input(f"\n{Color.CYAN}SELECT COMMAND >> {Color.ENDC}")
        
        if choice == '1':
            print(f"\n{Color.BOLD}--- INPUT PARAMETERS ---{Color.ENDC}")
            name = input(f"IDENTITY (Name): ")
            weight_str = input(f"MASS (kg)      : ")
            height_str = input(f"HEIGHT (m)     : ")
            
            try:
                weight, height = bmi_logic.validate_input(weight_str, height_str)
                bmi = bmi_logic.calculate_bmi(weight, height)
                category = bmi_logic.categorize_bmi(bmi)
                
                # Dynamic Output
                print(f"\n{Color.GREEN}>>> PROCESSING...{Color.ENDC}")
                time.sleep(0.5)
                print(f"CALCULATED BMI : {Color.BOLD}{bmi:.2f}{Color.ENDC}")
                
                cat_color = Color.GREEN if category == "Normal" else Color.WARNING if category == "Overweight" else Color.FAIL
                print(f"STATUS         : {cat_color}{category.upper()}{Color.ENDC}")
                
                # Save
                database_manager.add_record(name, weight, height, bmi, category)
                print(f"\n{Color.BLUE}>> Data saved to secure vault.{Color.ENDC}")
                
            except ValueError as e:
                print(f"\n{Color.FAIL}!! ERROR: {e}{Color.ENDC}")
            
            input(f"\n{Color.CYAN}Press ENTER to return...{Color.ENDC}")
            
        elif choice == '2':
            name = input(f"\n{Color.BOLD}ENTER IDENTITY TO SEARCH: {Color.ENDC}")
            visualize_trend(name)
            input(f"\n{Color.CYAN}Press ENTER to return...{Color.ENDC}")
            
        elif choice == '3':
            print(f"\n{Color.FAIL}>> TERMINATING SESSION...{Color.ENDC}")
            time.sleep(0.5)
            break
        else:
            print("Invalid Command.")
            time.sleep(0.5)

if __name__ == "__main__":
    run_cli()
