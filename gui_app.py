import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import bmi_logic
import database_manager

# --- Theme Configuration ---
THEME = {
    "bg_color": "#050510",        # Deep Space Black
    "fg_color": "#E0E0E0",        # Star White
    "accent_color": "#00FFDD",    # Neon Cyan/Antigravity Glow
    "accent_dim": "#008F7A",      # Dimmer Cyan
    "panel_bg": "#121225",        # Panel color
    "danger": "#FF4444",          # Error/Overweight
    "success": "#44FF44",         # Normal
    "font_main": ("Courier New", 12),
    "font_header": ("Courier New", 24, "bold"),
    "font_button": ("Courier New", 14, "bold")
}

class AntigravityBMIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ANTIGRAVITY // BMI Calculator")
        self.root.geometry("800x800")
        self.root.configure(bg=THEME["bg_color"])
        
        # Initialize Database
        database_manager.init_db()
        
        # Style Configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("TFrame", background=THEME["bg_color"])
        style.configure("Panel.TFrame", background=THEME["panel_bg"], relief="flat")
        
        style.configure("TLabel", background=THEME["bg_color"], foreground=THEME["fg_color"], font=THEME["font_main"])
        style.configure("Panel.TLabel", background=THEME["panel_bg"], foreground=THEME["fg_color"], font=THEME["font_main"])
        
        style.configure("Header.TLabel", background=THEME["bg_color"], foreground=THEME["accent_color"], font=THEME["font_header"])
        
        style.configure("TEntry", fieldbackground="#202030", foreground=THEME["accent_color"], insertcolor="white", font=THEME["font_main"])
        
        style.configure("TButton", 
                        background=THEME["accent_dim"], 
                        foreground=THEME["bg_color"], 
                        font=THEME["font_button"], 
                        borderwidth=0, 
                        focuscolor=THEME["accent_color"])
        style.map("TButton", background=[("active", THEME["accent_color"])])

        self.setup_ui()

    def setup_ui(self):
        """Sets up the entire user interface hierarchy."""
        
        # --- Header ---
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=30, fill="x")
        
        header_label = ttk.Label(header_frame, text=" SYSTEMS", style="Header.TLabel")
        header_label.pack()
        
        sub_header = ttk.Label(header_frame, text="BIOMETRIC ANALYSIS INTERFACE", font=("Courier New", 10))
        sub_header.pack()

        # --- Main Container ---
        self.main_container = ttk.Frame(self.root, style="Panel.TFrame")
        self.main_container.pack(expand=True, fill="both", padx=40, pady=20)
        
        # --- Input Section ---
        input_frame = ttk.Frame(self.main_container, style="Panel.TFrame")
        input_frame.pack(pady=20, fill="x", padx=20)
        
        # Name
        self.create_input_field(input_frame, "CODENAME:", 0)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(input_frame, textvariable=self.name_var)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Weight
        self.create_input_field(input_frame, "WEIGHT (KG):", 1)
        self.weight_var = tk.StringVar()
        self.weight_entry = ttk.Entry(input_frame, textvariable=self.weight_var)
        self.weight_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Height
        self.create_input_field(input_frame, "HEIGHT (M):", 2)
        self.height_var = tk.StringVar()
        self.height_entry = ttk.Entry(input_frame, textvariable=self.height_var)
        self.height_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        
        input_frame.columnconfigure(1, weight=1)

        # --- Controls ---
        btn_frame = ttk.Frame(self.main_container, style="Panel.TFrame")
        btn_frame.pack(pady=20)
        
        calc_btn = ttk.Button(btn_frame, text="[ INITIATE CALCULATION ]", command=self.calculate_and_save)
        calc_btn.pack(side="left", padx=10)
        
        clear_btn = tk.Button(btn_frame, text="RESET", bg=THEME["panel_bg"], fg="#FF6666", 
                              font=("Courier New", 10), command=self.clear_fields, bd=0, activebackground=THEME["bg_color"], activeforeground="#FF0000")
        clear_btn.pack(side="left", padx=10)

        # --- Output Section ---
        self.result_label = ttk.Label(self.main_container, text="WAITING FOR INPUT...", 
                                      font=("Courier New", 16, "bold"), style="Panel.TLabel", foreground="#555")
        self.result_label.pack(pady=10)
        
        self.category_label = ttk.Label(self.main_container, text="", font=("Courier New", 14), style="Panel.TLabel")
        self.category_label.pack(pady=5)

        # --- Visualization Section ---
        self.graph_frame = ttk.Frame(self.main_container, style="Panel.TFrame")
        self.graph_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Placeholder for graph
        self.figure, self.ax = plt.subplots(figsize=(5, 3), dpi=100)
        self.figure.patch.set_facecolor(THEME["panel_bg"])
        self.ax.set_facecolor(THEME["panel_bg"])
        self.setup_empty_chart()
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def create_input_field(self, parent, label_text, row):
        """Helper to create standardized input labels."""
        lbl = ttk.Label(parent, text=label_text, style="Panel.TLabel")
        lbl.grid(row=row, column=0, padx=10, pady=10, sticky="w")

    def setup_empty_chart(self):
        """Sets up the initial empty chart appearance."""
        self.ax.clear()
        self.ax.set_facecolor(THEME["panel_bg"])
        self.ax.tick_params(colors=THEME["fg_color"], labelcolor=THEME["fg_color"])
        for spine in self.ax.spines.values():
            spine.set_edgecolor(THEME["accent_dim"])
        self.ax.set_title("TEMPORAL DATA STREAM", color=THEME["accent_color"], fontname="Courier New")
        self.ax.grid(color="#333", linestyle="--", linewidth=0.5)

    def calculate_and_save(self):
        """Handles the calculation, saving, and updating of the UI."""
        name = self.name_var.get().strip()
        weight_str = self.weight_var.get().strip()
        height_str = self.height_var.get().strip()

        if not name:
            messagebox.showerror("Input Error", "Codename is required.")
            return

        try:
            # 1. Validation & Calculation
            weight, height = bmi_logic.validate_input(weight_str, height_str)
            bmi = bmi_logic.calculate_bmi(weight, height)
            category = bmi_logic.categorize_bmi(bmi)

            # 2. Update Display
            self.result_label.config(text=f"CALCULATED BMI: {bmi:.2f}", foreground=THEME["accent_color"])
            
            # Color code category
            cat_color = THEME["success"] if category == "Normal" else THEME["danger"]
            self.category_label.config(text=f"STATUS: {category.upper()}", foreground=cat_color)

            # 3. Save to Database
            database_manager.add_record(name, weight, height, bmi, category)

            # 4. Update Graph
            self.update_graph(name)

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("System Error", f"An unexpected error occurred: {e}")

    def update_graph(self, name):
        """Fetches history and updates the trend line."""
        history = database_manager.get_user_history(name)
        
        if not history:
            return
            
        dates = [rec[0] for rec in history]
        bmis = [rec[1] for rec in history]
        
        # Simplified date for display (just time if same day, or date if different)
        # For this prototype, we'll just index them 1, 2, 3... or use raw strings if few
        x_indices = range(len(dates))

        self.ax.clear()
        self.ax.set_facecolor(THEME["panel_bg"])
        
        # Plot Line
        self.ax.plot(x_indices, bmis, color=THEME["accent_color"], marker="o", linestyle="-", linewidth=2, markersize=6)
        
        # Fill under line for "cyber" effect
        self.ax.fill_between(x_indices, bmis, alpha=0.1, color=THEME["accent_color"])
        
        # Reference Lines (Normal Range)
        self.ax.axhline(y=18.5, color=THEME["accent_dim"], linestyle="--", alpha=0.5, linewidth=1)
        self.ax.axhline(y=24.9, color=THEME["accent_dim"], linestyle="--", alpha=0.5, linewidth=1)
        
        # Styling
        self.ax.set_title(f"BMI TREND: {name.upper()}", color=THEME["accent_color"], fontname="Courier New", pad=10)
        self.ax.tick_params(colors=THEME["fg_color"])
        for spine in self.ax.spines.values():
            spine.set_edgecolor(THEME["accent_dim"])
        self.ax.grid(color="#222", linestyle=":", linewidth=0.5)
        
        # Redraw
        self.canvas.draw()

    def clear_fields(self):
        """Resets the input fields and result labels."""
        self.name_var.set("")
        self.weight_var.set("")
        self.height_var.set("")
        self.result_label.config(text="WAITING FOR INPUT...", foreground="#555")
        self.category_label.config(text="")
        self.setup_empty_chart()
        self.canvas.draw()
