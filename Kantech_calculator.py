#!/usr/bin/env python3
"""
Kantech Credential Calculator - Kobe's Keys Edition
Cyberpunk GUI Tool for RFID Research

Requirements: pip install customtkinter pyperclip
"""

import customtkinter as ctk
from tkinter import messagebox
import pyperclip

# Set cyberpunk theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Cyberpunk color scheme
COLORS = {
    'bg_dark': '#0a0a0f',
    'bg_medium': '#12121a',
    'bg_light': '#1a1a2e',
    'accent_cyan': '#00fff9',
    'accent_magenta': '#ff00ff',
    'accent_yellow': '#f0ff00',
    'accent_orange': '#ff6b00',
    'text_primary': '#ffffff',
    'text_secondary': '#00fff9',
    'success': '#00ff88',
    'border': '#00fff9'
}


class KantechCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("⚡ KANTECH DECODER - Kobe's Keys ⚡")
        self.geometry("800x900")
        self.configure(fg_color=COLORS['bg_dark'])
        self.resizable(True, True)
        
        # Store results for copying
        self.results = {}
        
        # Build UI
        self.create_header()
        self.create_input_section()
        self.create_results_section()
        self.create_footer()
        
    def create_header(self):
        """Create cyberpunk header"""
        header_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        # Glowing title
        title = ctk.CTkLabel(
            header_frame,
            text="◢◤ KANTECH CREDENTIAL DECODER ◢◤",
            font=("Consolas", 28, "bold"),
            text_color=COLORS['accent_cyan']
        )
        title.pack(pady=(20, 5))
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="[ KOBE'S KEYS - RFID RESEARCH TOOL ]",
            font=("Consolas", 14),
            text_color=COLORS['accent_magenta']
        )
        subtitle.pack(pady=(0, 5))
        
        # Decorative line
        line = ctk.CTkLabel(
            header_frame,
            text="═" * 60,
            font=("Consolas", 12),
            text_color=COLORS['accent_cyan']
        )
        line.pack(pady=(5, 15))
        
    def create_input_section(self):
        """Create input fields"""
        input_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_light'], corner_radius=10)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Section header
        header = ctk.CTkLabel(
            input_frame,
            text="◈ INPUT CREDENTIALS ◈",
            font=("Consolas", 16, "bold"),
            text_color=COLORS['accent_yellow']
        )
        header.pack(pady=(15, 10))
        
        # Input container
        input_container = ctk.CTkFrame(input_frame, fg_color="transparent")
        input_container.pack(fill="x", padx=20, pady=10)
        
        # Site Code
        site_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        site_frame.pack(fill="x", pady=5)
        
        site_label = ctk.CTkLabel(
            site_frame,
            text="SITE CODE:",
            font=("Consolas", 14),
            text_color=COLORS['text_secondary'],
            width=150,
            anchor="w"
        )
        site_label.pack(side="left", padx=(0, 10))
        
        self.site_entry = ctk.CTkEntry(
            site_frame,
            font=("Consolas", 16),
            fg_color=COLORS['bg_dark'],
            border_color=COLORS['accent_cyan'],
            text_color=COLORS['text_primary'],
            placeholder_text="e.g. 8020",
            width=200,
            height=40
        )
        self.site_entry.pack(side="left")
        
        # Card Number
        card_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        card_frame.pack(fill="x", pady=5)
        
        card_label = ctk.CTkLabel(
            card_frame,
            text="CARD NUMBER:",
            font=("Consolas", 14),
            text_color=COLORS['text_secondary'],
            width=150,
            anchor="w"
        )
        card_label.pack(side="left", padx=(0, 10))
        
        self.card_entry = ctk.CTkEntry(
            card_frame,
            font=("Consolas", 16),
            fg_color=COLORS['bg_dark'],
            border_color=COLORS['accent_cyan'],
            text_color=COLORS['text_primary'],
            placeholder_text="e.g. 11485",
            width=200,
            height=40
        )
        self.card_entry.pack(side="left")
        
        # OR divider
        or_label = ctk.CTkLabel(
            input_container,
            text="─── OR ENTER COMBINED ───",
            font=("Consolas", 12),
            text_color=COLORS['accent_magenta']
        )
        or_label.pack(pady=10)
        
        # Combined input
        combined_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        combined_frame.pack(fill="x", pady=5)
        
        combined_label = ctk.CTkLabel(
            combined_frame,
            text="COMBINED:",
            font=("Consolas", 14),
            text_color=COLORS['text_secondary'],
            width=150,
            anchor="w"
        )
        combined_label.pack(side="left", padx=(0, 10))
        
        self.combined_entry = ctk.CTkEntry(
            combined_frame,
            font=("Consolas", 16),
            fg_color=COLORS['bg_dark'],
            border_color=COLORS['accent_magenta'],
            text_color=COLORS['text_primary'],
            placeholder_text="e.g. 8020:11485",
            width=200,
            height=40
        )
        self.combined_entry.pack(side="left")
        
        # Buttons
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=15)
        
        self.calc_button = ctk.CTkButton(
            button_frame,
            text="⚡ DECODE ⚡",
            font=("Consolas", 16, "bold"),
            fg_color=COLORS['accent_cyan'],
            hover_color=COLORS['accent_magenta'],
            text_color=COLORS['bg_dark'],
            width=200,
            height=50,
            command=self.calculate
        )
        self.calc_button.pack(side="left", padx=10)
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="◼ CLEAR",
            font=("Consolas", 14),
            fg_color=COLORS['bg_medium'],
            hover_color=COLORS['accent_orange'],
            text_color=COLORS['text_primary'],
            border_color=COLORS['accent_orange'],
            border_width=2,
            width=120,
            height=50,
            command=self.clear_all
        )
        self.clear_button.pack(side="left", padx=10)
        
    def create_results_section(self):
        """Create results display"""
        self.results_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_light'], corner_radius=10)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Section header
        header = ctk.CTkLabel(
            self.results_frame,
            text="◈ DECODED OUTPUT ◈",
            font=("Consolas", 16, "bold"),
            text_color=COLORS['accent_yellow']
        )
        header.pack(pady=(15, 10))
        
        # Scrollable results
        self.results_scroll = ctk.CTkScrollableFrame(
            self.results_frame,
            fg_color=COLORS['bg_dark'],
            corner_radius=5
        )
        self.results_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Placeholder
        self.placeholder = ctk.CTkLabel(
            self.results_scroll,
            text="[ ENTER CREDENTIALS AND PRESS DECODE ]",
            font=("Consolas", 14),
            text_color=COLORS['accent_cyan']
        )
        self.placeholder.pack(pady=50)
        
    def create_footer(self):
        """Create footer"""
        footer_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], corner_radius=0, height=50)
        footer_frame.pack(fill="x", side="bottom")
        
        footer_text = ctk.CTkLabel(
            footer_frame,
            text="◢ KOBE'S KEYS © 2025 | MAMBA MENTALITY ◤",
            font=("Consolas", 11),
            text_color=COLORS['accent_magenta']
        )
        footer_text.pack(pady=10)
        
    def calculate(self):
        """Calculate and display results"""
        # Get input
        site_str = self.site_entry.get().strip()
        card_str = self.card_entry.get().strip()
        combined_str = self.combined_entry.get().strip()
        
        try:
            # Parse input
            if combined_str:
                if ':' in combined_str:
                    parts = combined_str.split(':')
                    site_code = int(parts[0])
                    card_number = int(parts[1])
                else:
                    raise ValueError("Combined format should be SITE:CARD (e.g., 8020:11485)")
            elif site_str and card_str:
                site_code = int(site_str)
                card_number = int(card_str)
            else:
                raise ValueError("Enter Site Code + Card Number, or Combined format")
                
            # Calculate results
            self.results = self.compute_values(site_code, card_number)
            
            # Display results
            self.display_results(site_code, card_number)
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            
    def compute_values(self, site_code, card_number):
        """Compute all credential representations"""
        results = {}
        
        # Basic hex
        results['site_hex'] = format(site_code, '04X')
        results['card_hex'] = format(card_number, '04X')
        results['card_hex_32'] = format(card_number, '08X')
        
        # Binary
        results['site_bin'] = format(site_code, '016b')
        results['card_bin'] = format(card_number, '016b')
        
        # Combined formats
        results['combined_32'] = format((site_code << 16) | card_number, '08X')
        results['combined_48'] = format((site_code << 32) | card_number, '012X')
        
        # Byte patterns
        results['site_be'] = f"{format((site_code >> 8) & 0xFF, '02X')} {format(site_code & 0xFF, '02X')}"
        results['site_le'] = f"{format(site_code & 0xFF, '02X')} {format((site_code >> 8) & 0xFF, '02X')}"
        results['card_be'] = f"{format((card_number >> 8) & 0xFF, '02X')} {format(card_number & 0xFF, '02X')}"
        results['card_le'] = f"{format(card_number & 0xFF, '02X')} {format((card_number >> 8) & 0xFF, '02X')}"
        
        # Full sequences
        results['full_be'] = f"{format((site_code >> 8) & 0xFF, '02X')} {format(site_code & 0xFF, '02X')} {format((card_number >> 8) & 0xFF, '02X')} {format(card_number & 0xFF, '02X')}"
        results['full_le'] = f"{format(card_number & 0xFF, '02X')} {format((card_number >> 8) & 0xFF, '02X')} {format(site_code & 0xFF, '02X')} {format((site_code >> 8) & 0xFF, '02X')}"
        
        # Checksums
        results['xor'] = format(site_code ^ card_number, '04X')
        results['sum'] = format((site_code + card_number) & 0xFFFF, '04X')
        
        return results
        
    def display_results(self, site_code, card_number):
        """Display calculated results"""
        # Clear previous results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        r = self.results
        
        # Create sections
        sections = [
            ("INPUT", [
                ("Site Code", str(site_code)),
                ("Card Number", str(card_number)),
                ("Combined", f"{site_code}:{card_number:05d}")
            ]),
            ("HEXADECIMAL", [
                ("Site Code (16-bit)", f"0x{r['site_hex']}"),
                ("Card Number (16-bit)", f"0x{r['card_hex']}"),
                ("Card Number (32-bit)", f"0x{r['card_hex_32']}")
            ]),
            ("BINARY", [
                ("Site Code", r['site_bin']),
                ("Card Number", r['card_bin'])
            ]),
            ("COMBINED FORMATS", [
                ("32-bit (SC|CN)", r['combined_32']),
                ("48-bit (SC|CN)", r['combined_48'])
            ]),
            ("BYTE PATTERNS - Search in dumps", [
                ("Site (Big Endian)", r['site_be']),
                ("Site (Little Endian)", r['site_le']),
                ("Card (Big Endian)", r['card_be']),
                ("Card (Little Endian)", r['card_le'])
            ]),
            ("FULL SEQUENCES", [
                ("Big Endian (SC CN)", r['full_be']),
                ("Little Endian (CN SC)", r['full_le'])
            ]),
            ("CHECKSUMS", [
                ("XOR (site ^ card)", r['xor']),
                ("SUM (site + card)", r['sum'])
            ])
        ]
        
        for section_name, items in sections:
            self.add_section(section_name, items)
            
        # Add copy all button
        copy_frame = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
        copy_frame.pack(fill="x", pady=15)
        
        copy_btn = ctk.CTkButton(
            copy_frame,
            text="📋 COPY ALL TO CLIPBOARD",
            font=("Consolas", 12),
            fg_color=COLORS['accent_magenta'],
            hover_color=COLORS['accent_cyan'],
            text_color=COLORS['bg_dark'],
            width=250,
            height=35,
            command=lambda: self.copy_all(site_code, card_number)
        )
        copy_btn.pack()
        
    def add_section(self, title, items):
        """Add a section to results"""
        # Section header
        header = ctk.CTkLabel(
            self.results_scroll,
            text=f"┌─ {title} ─┐",
            font=("Consolas", 13, "bold"),
            text_color=COLORS['accent_yellow'],
            anchor="w"
        )
        header.pack(fill="x", padx=10, pady=(15, 5))
        
        # Items
        for label, value in items:
            item_frame = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
            item_frame.pack(fill="x", padx=20, pady=2)
            
            lbl = ctk.CTkLabel(
                item_frame,
                text=f"{label}:",
                font=("Consolas", 11),
                text_color=COLORS['text_secondary'],
                width=200,
                anchor="w"
            )
            lbl.pack(side="left")
            
            val = ctk.CTkLabel(
                item_frame,
                text=value,
                font=("Consolas", 12, "bold"),
                text_color=COLORS['success'],
                anchor="w"
            )
            val.pack(side="left", padx=10)
            
            # Copy button for this value
            copy_btn = ctk.CTkButton(
                item_frame,
                text="📋",
                font=("Consolas", 10),
                fg_color="transparent",
                hover_color=COLORS['bg_light'],
                text_color=COLORS['accent_cyan'],
                width=30,
                height=25,
                command=lambda v=value: self.copy_value(v)
            )
            copy_btn.pack(side="right", padx=5)
            
    def copy_value(self, value):
        """Copy single value to clipboard"""
        try:
            pyperclip.copy(value)
        except:
            self.clipboard_clear()
            self.clipboard_append(value)
            
    def copy_all(self, site_code, card_number):
        """Copy all results to clipboard"""
        r = self.results
        text = f"""KANTECH CREDENTIAL - {site_code}:{card_number}
{'='*50}
HEXADECIMAL:
  Site: 0x{r['site_hex']}
  Card: 0x{r['card_hex']}
  
BYTE PATTERNS (search in dumps):
  Big Endian:    {r['full_be']}
  Little Endian: {r['full_le']}
  
COMBINED:
  32-bit: {r['combined_32']}
  48-bit: {r['combined_48']}
  
CHECKSUMS:
  XOR: {r['xor']}
  SUM: {r['sum']}
{'='*50}
Generated by Kobe's Keys RFID Tools
"""
        try:
            pyperclip.copy(text)
            messagebox.showinfo("Copied", "All results copied to clipboard!")
        except:
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("Copied", "All results copied to clipboard!")
            
    def clear_all(self):
        """Clear all inputs and results"""
        self.site_entry.delete(0, 'end')
        self.card_entry.delete(0, 'end')
        self.combined_entry.delete(0, 'end')
        
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        self.placeholder = ctk.CTkLabel(
            self.results_scroll,
            text="[ ENTER CREDENTIALS AND PRESS DECODE ]",
            font=("Consolas", 14),
            text_color=COLORS['accent_cyan']
        )
        self.placeholder.pack(pady=50)


def main():
    app = KantechCalculator()
    app.mainloop()


if __name__ == "__main__":
    main()