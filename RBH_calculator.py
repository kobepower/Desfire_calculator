#!/usr/bin/env python3
"""
RBH 50-Bit Credential Calculator - Kobe's Keys Edition
Cyberpunk GUI Tool for RFID Research

RBH 50-bit Format Structure:
| Parity (1) | Site Code (16-bit) | Card Number (32-bit) | Parity (1) | = 50 bits

Requirements: pip install customtkinter pyperclip
"""

import customtkinter as ctk
from tkinter import messagebox
import pyperclip

# Set cyberpunk theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Cyberpunk color scheme - RBH Orange/Red theme
COLORS = {
    'bg_dark': '#0a0a0f',
    'bg_medium': '#12121a',
    'bg_light': '#1a1a2e',
    'accent_primary': '#ff6b00',  # RBH Orange
    'accent_secondary': '#ff0055',  # Red
    'accent_cyan': '#00fff9',
    'accent_yellow': '#f0ff00',
    'text_primary': '#ffffff',
    'text_secondary': '#ff6b00',
    'success': '#00ff88',
    'border': '#ff6b00'
}


class RBHCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("⚡ RBH 50-BIT DECODER - Kobe's Keys ⚡")
        self.geometry("850x950")
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
            text="◢◤ RBH 50-BIT CREDENTIAL DECODER ◢◤",
            font=("Consolas", 26, "bold"),
            text_color=COLORS['accent_primary']
        )
        title.pack(pady=(20, 5))
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="[ KOBE'S KEYS - RFID RESEARCH TOOL ]",
            font=("Consolas", 14),
            text_color=COLORS['accent_secondary']
        )
        subtitle.pack(pady=(0, 5))
        
        # Format info
        format_info = ctk.CTkLabel(
            header_frame,
            text="Format: [1-bit Parity][16-bit Site][32-bit Card][1-bit Parity] = 50 bits",
            font=("Consolas", 11),
            text_color=COLORS['accent_cyan']
        )
        format_info.pack(pady=(5, 5))
        
        # Decorative line
        line = ctk.CTkLabel(
            header_frame,
            text="═" * 65,
            font=("Consolas", 12),
            text_color=COLORS['accent_primary']
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
            text="SITE CODE (0-65535):",
            font=("Consolas", 14),
            text_color=COLORS['text_secondary'],
            width=200,
            anchor="w"
        )
        site_label.pack(side="left", padx=(0, 10))
        
        self.site_entry = ctk.CTkEntry(
            site_frame,
            font=("Consolas", 16),
            fg_color=COLORS['bg_dark'],
            border_color=COLORS['accent_primary'],
            text_color=COLORS['text_primary'],
            placeholder_text="e.g. 4000",
            width=200,
            height=40
        )
        self.site_entry.pack(side="left")
        
        # Card Number
        card_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        card_frame.pack(fill="x", pady=5)
        
        card_label = ctk.CTkLabel(
            card_frame,
            text="CARD NUMBER (0-4294967295):",
            font=("Consolas", 14),
            text_color=COLORS['text_secondary'],
            width=200,
            anchor="w"
        )
        card_label.pack(side="left", padx=(0, 10))
        
        self.card_entry = ctk.CTkEntry(
            card_frame,
            font=("Consolas", 16),
            fg_color=COLORS['bg_dark'],
            border_color=COLORS['accent_primary'],
            text_color=COLORS['text_primary'],
            placeholder_text="e.g. 12345",
            width=200,
            height=40
        )
        self.card_entry.pack(side="left")
        
        # OR divider
        or_label = ctk.CTkLabel(
            input_container,
            text="─── OR ENTER FROM CARD BACK ───",
            font=("Consolas", 12),
            text_color=COLORS['accent_secondary']
        )
        or_label.pack(pady=10)
        
        # Combined input (format on card back)
        combined_frame = ctk.CTkFrame(input_container, fg_color="transparent")
        combined_frame.pack(fill="x", pady=5)
        
        combined_label = ctk.CTkLabel(
            combined_frame,
            text="CARD BACK FORMAT:",
            font=("Consolas", 14),
            text_color=COLORS['text_secondary'],
            width=200,
            anchor="w"
        )
        combined_label.pack(side="left", padx=(0, 10))
        
        self.combined_entry = ctk.CTkEntry(
            combined_frame,
            font=("Consolas", 16),
            fg_color=COLORS['bg_dark'],
            border_color=COLORS['accent_secondary'],
            text_color=COLORS['text_primary'],
            placeholder_text="e.g. 4000-12345 or 4000:12345",
            width=250,
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
            fg_color=COLORS['accent_primary'],
            hover_color=COLORS['accent_secondary'],
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
            hover_color=COLORS['accent_secondary'],
            text_color=COLORS['text_primary'],
            border_color=COLORS['accent_secondary'],
            border_width=2,
            width=120,
            height=50,
            command=self.clear_all
        )
        self.clear_button.pack(side="left", padx=10)
        
        self.reverse_button = ctk.CTkButton(
            button_frame,
            text="🔄 REVERSE 50-BIT",
            font=("Consolas", 14),
            fg_color=COLORS['bg_medium'],
            hover_color=COLORS['accent_cyan'],
            text_color=COLORS['text_primary'],
            border_color=COLORS['accent_cyan'],
            border_width=2,
            width=150,
            height=50,
            command=self.show_reverse_dialog
        )
        self.reverse_button.pack(side="left", padx=10)
        
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
            text_color=COLORS['accent_primary']
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
            text_color=COLORS['accent_secondary']
        )
        footer_text.pack(pady=10)
        
    def calculate_parity(self, bits, even=True):
        """Calculate parity bit"""
        count = bits.count('1')
        if even:
            return '0' if count % 2 == 0 else '1'
        else:
            return '1' if count % 2 == 0 else '0'
    
    def calculate(self):
        """Calculate and display results"""
        # Get input
        site_str = self.site_entry.get().strip()
        card_str = self.card_entry.get().strip()
        combined_str = self.combined_entry.get().strip()
        
        try:
            # Parse input
            if combined_str:
                # Try different separators
                for sep in [':', '-', ' ']:
                    if sep in combined_str:
                        parts = combined_str.split(sep)
                        site_code = int(parts[0])
                        card_number = int(parts[1])
                        break
                else:
                    raise ValueError("Format should be SITE:CARD or SITE-CARD (e.g., 4000:12345)")
            elif site_str and card_str:
                site_code = int(site_str)
                card_number = int(card_str)
            else:
                raise ValueError("Enter Site Code + Card Number, or Combined format")
            
            # Validate ranges
            if site_code > 65535:
                raise ValueError("Site Code must be 0-65535 (16-bit)")
            if card_number > 4294967295:
                raise ValueError("Card Number must be 0-4294967295 (32-bit)")
                
            # Calculate results
            self.results = self.compute_values(site_code, card_number)
            
            # Display results
            self.display_results(site_code, card_number)
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            
    def compute_values(self, site_code, card_number):
        """Compute all credential representations for RBH 50-bit"""
        results = {}
        
        # Basic values
        results['site_dec'] = site_code
        results['card_dec'] = card_number
        
        # Hexadecimal
        results['site_hex'] = format(site_code, '04X')
        results['card_hex'] = format(card_number, '08X')
        
        # Binary
        results['site_bin'] = format(site_code, '016b')
        results['card_bin'] = format(card_number, '032b')
        
        # Build 50-bit credential
        # Structure: [P1 (1-bit)] [Site (16-bit)] [Card (32-bit)] [P2 (1-bit)]
        
        # First half for parity 1 (site code, first 16 bits)
        site_bits = format(site_code, '016b')
        
        # Second half for parity 2 (card number, 32 bits)
        card_bits = format(card_number, '032b')
        
        # Calculate parities (even parity is common)
        # P1 covers first 24 bits (site + first 8 bits of card typically)
        # P2 covers last 24 bits (last 24 bits of card typically)
        # This varies by implementation - showing common patterns
        
        p1_even = self.calculate_parity(site_bits, even=True)
        p2_even = self.calculate_parity(card_bits, even=True)
        
        # Full 50-bit binary (most common structure)
        full_50bit = p1_even + site_bits + card_bits + p2_even
        results['full_50bit_bin'] = full_50bit
        
        # Convert to hex (50 bits = 13 hex chars, padded)
        full_50bit_int = int(full_50bit, 2)
        results['full_50bit_hex'] = format(full_50bit_int, '013X')
        results['full_50bit_dec'] = str(full_50bit_int)
        
        # Alternative: without parity (48-bit data only)
        data_48bit = site_bits + card_bits
        results['data_48bit_bin'] = data_48bit
        results['data_48bit_hex'] = format(int(data_48bit, 2), '012X')
        
        # Byte patterns for searching dumps
        # Site code bytes
        results['site_be'] = f"{format((site_code >> 8) & 0xFF, '02X')} {format(site_code & 0xFF, '02X')}"
        results['site_le'] = f"{format(site_code & 0xFF, '02X')} {format((site_code >> 8) & 0xFF, '02X')}"
        
        # Card number bytes (32-bit = 4 bytes)
        results['card_be'] = f"{format((card_number >> 24) & 0xFF, '02X')} {format((card_number >> 16) & 0xFF, '02X')} {format((card_number >> 8) & 0xFF, '02X')} {format(card_number & 0xFF, '02X')}"
        results['card_le'] = f"{format(card_number & 0xFF, '02X')} {format((card_number >> 8) & 0xFF, '02X')} {format((card_number >> 16) & 0xFF, '02X')} {format((card_number >> 24) & 0xFF, '02X')}"
        
        # Full sequence (Site + Card)
        results['full_be'] = results['site_be'] + " " + results['card_be']
        results['full_le'] = results['card_le'] + " " + results['site_le']
        
        # Wiegand-style output (what reader sends to controller)
        # 50-bit Wiegand: typically the raw 50-bit value
        results['wiegand_hex'] = results['full_50bit_hex']
        results['wiegand_bin'] = results['full_50bit_bin']
        
        # Checksums
        results['xor'] = format(site_code ^ card_number, '08X')
        results['sum'] = format((site_code + card_number) & 0xFFFFFFFF, '08X')
        
        return results
        
    def display_results(self, site_code, card_number):
        """Display calculated results"""
        # Clear previous results
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        r = self.results
        
        # Create sections
        sections = [
            ("INPUT VALUES", [
                ("Site Code (Decimal)", str(site_code)),
                ("Card Number (Decimal)", str(card_number)),
                ("Combined", f"{site_code}:{card_number}")
            ]),
            ("HEXADECIMAL", [
                ("Site Code (16-bit)", f"0x{r['site_hex']}"),
                ("Card Number (32-bit)", f"0x{r['card_hex']}")
            ]),
            ("BINARY", [
                ("Site Code (16-bit)", r['site_bin']),
                ("Card Number (32-bit)", r['card_bin'])
            ]),
            ("50-BIT CREDENTIAL", [
                ("Full 50-bit (Binary)", r['full_50bit_bin']),
                ("Full 50-bit (Hex)", r['full_50bit_hex']),
                ("Full 50-bit (Decimal)", r['full_50bit_dec'])
            ]),
            ("48-BIT DATA (No Parity)", [
                ("48-bit (Hex)", r['data_48bit_hex']),
                ("48-bit (Binary)", r['data_48bit_bin'])
            ]),
            ("BYTE PATTERNS - Search in dumps", [
                ("Site (Big Endian)", r['site_be']),
                ("Site (Little Endian)", r['site_le']),
                ("Card (Big Endian)", r['card_be']),
                ("Card (Little Endian)", r['card_le'])
            ]),
            ("FULL BYTE SEQUENCES", [
                ("Big Endian (SC + CN)", r['full_be']),
                ("Little Endian (CN + SC)", r['full_le'])
            ]),
            ("WIEGAND OUTPUT", [
                ("50-bit Wiegand (Hex)", r['wiegand_hex']),
                ("50-bit Wiegand (Binary)", r['wiegand_bin'])
            ]),
            ("CHECKSUMS", [
                ("XOR", r['xor']),
                ("SUM", r['sum'])
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
            fg_color=COLORS['accent_secondary'],
            hover_color=COLORS['accent_primary'],
            text_color=COLORS['text_primary'],
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
                width=220,
                anchor="w"
            )
            lbl.pack(side="left")
            
            # Truncate long values for display
            display_value = value if len(value) <= 50 else value[:47] + "..."
            
            val = ctk.CTkLabel(
                item_frame,
                text=display_value,
                font=("Consolas", 11, "bold"),
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
                text_color=COLORS['accent_primary'],
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
        text = f"""RBH 50-BIT CREDENTIAL - {site_code}:{card_number}
{'='*60}
INPUT:
  Site Code:   {site_code}
  Card Number: {card_number}

HEXADECIMAL:
  Site: 0x{r['site_hex']}
  Card: 0x{r['card_hex']}

50-BIT CREDENTIAL:
  Binary: {r['full_50bit_bin']}
  Hex:    {r['full_50bit_hex']}

BYTE PATTERNS (search in dumps):
  Site BE:     {r['site_be']}
  Site LE:     {r['site_le']}
  Card BE:     {r['card_be']}
  Card LE:     {r['card_le']}
  
FULL SEQUENCES:
  Big Endian:    {r['full_be']}
  Little Endian: {r['full_le']}

WIEGAND OUTPUT:
  Hex: {r['wiegand_hex']}
{'='*60}
Generated by Kobe's Keys RFID Tools
"""
        try:
            pyperclip.copy(text)
            messagebox.showinfo("Copied", "All results copied to clipboard!")
        except:
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("Copied", "All results copied to clipboard!")
            
    def show_reverse_dialog(self):
        """Show dialog to reverse 50-bit hex back to site/card"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Reverse 50-bit to Site/Card")
        dialog.geometry("500x300")
        dialog.configure(fg_color=COLORS['bg_dark'])
        dialog.transient(self)
        dialog.grab_set()
        
        # Title
        title = ctk.CTkLabel(
            dialog,
            text="◈ REVERSE 50-BIT DECODER ◈",
            font=("Consolas", 16, "bold"),
            text_color=COLORS['accent_cyan']
        )
        title.pack(pady=(20, 10))
        
        info = ctk.CTkLabel(
            dialog,
            text="Enter 50-bit hex from card dump to extract Site/Card",
            font=("Consolas", 11),
            text_color=COLORS['text_secondary']
        )
        info.pack(pady=(0, 15))
        
        # Input
        input_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        input_frame.pack(fill="x", padx=30, pady=10)
        
        hex_label = ctk.CTkLabel(
            input_frame,
            text="50-bit Hex:",
            font=("Consolas", 12),
            text_color=COLORS['text_secondary']
        )
        hex_label.pack(side="left", padx=(0, 10))
        
        hex_entry = ctk.CTkEntry(
            input_frame,
            font=("Consolas", 14),
            fg_color=COLORS['bg_medium'],
            border_color=COLORS['accent_cyan'],
            text_color=COLORS['text_primary'],
            placeholder_text="e.g. 1F4000003039",
            width=250,
            height=40
        )
        hex_entry.pack(side="left")
        
        # Result display
        result_frame = ctk.CTkFrame(dialog, fg_color=COLORS['bg_medium'], corner_radius=10)
        result_frame.pack(fill="x", padx=30, pady=20)
        
        result_label = ctk.CTkLabel(
            result_frame,
            text="Results will appear here",
            font=("Consolas", 12),
            text_color=COLORS['accent_primary']
        )
        result_label.pack(pady=20)
        
        def do_reverse():
            hex_val = hex_entry.get().strip().replace(" ", "").upper()
            try:
                # Convert hex to binary
                value = int(hex_val, 16)
                
                # Extract based on 50-bit structure
                # [P1][Site 16-bit][Card 32-bit][P2]
                binary = format(value, '050b')
                
                # Skip first parity bit, get site (16 bits)
                site_bits = binary[1:17]
                site_code = int(site_bits, 2)
                
                # Get card number (32 bits)
                card_bits = binary[17:49]
                card_number = int(card_bits, 2)
                
                result_label.configure(
                    text=f"Site Code: {site_code} (0x{format(site_code, '04X')})\n"
                         f"Card Number: {card_number} (0x{format(card_number, '08X')})\n"
                         f"Combined: {site_code}:{card_number}",
                    text_color=COLORS['success']
                )
            except Exception as e:
                result_label.configure(
                    text=f"Error: {str(e)}",
                    text_color=COLORS['accent_secondary']
                )
        
        # Decode button
        decode_btn = ctk.CTkButton(
            dialog,
            text="⚡ REVERSE DECODE ⚡",
            font=("Consolas", 14, "bold"),
            fg_color=COLORS['accent_cyan'],
            hover_color=COLORS['accent_primary'],
            text_color=COLORS['bg_dark'],
            width=200,
            height=40,
            command=do_reverse
        )
        decode_btn.pack(pady=10)
            
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
            text_color=COLORS['accent_primary']
        )
        self.placeholder.pack(pady=50)


def main():
    app = RBHCalculator()
    app.mainloop()


if __name__ == "__main__":
    main()