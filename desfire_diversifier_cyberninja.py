#!/usr/bin/env python3
"""
DESFire Key Diversification Calculator - CyberNinja Edition
Kobe's Keys - RFID Research Tool

Requirements: pip install customtkinter pyperclip pycryptodome
"""

import customtkinter as ctk
from tkinter import messagebox
import pyperclip
from Crypto.Cipher import AES
from binascii import unhexlify, hexlify

# CyberNinja Color Scheme (matching your Kantech tool)
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

class DesfireDiversifier(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("⚡ DESFIRE DIVERSIFIER - CyberNinja ⚡")
        self.geometry("850x950")
        self.configure(fg_color=COLORS['bg_dark'])
        self.resizable(True, True)
        
        self.results = {}
        self.create_header()
        self.create_input_section()
        self.create_results_section()
        self.create_footer()
        
    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        title = ctk.CTkLabel(
            header_frame,
            text="◢◤ DESFIRE KEY DIVERSIFIER ◢◤",
            font=("Consolas", 28, "bold"),
            text_color=COLORS['accent_cyan']
        )
        title.pack(pady=(20, 5))
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="[ CYBERNINJA EDITION - KOBE'S KEYS ]",
            font=("Consolas", 14),
            text_color=COLORS['accent_magenta']
        )
        subtitle.pack(pady=(0, 5))
        
        line = ctk.CTkLabel(
            header_frame,
            text="═" * 65,
            font=("Consolas", 12),
            text_color=COLORS['accent_cyan']
        )
        line.pack(pady=(5, 15))
        
    def create_input_section(self):
        input_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_light'], corner_radius=10)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        header = ctk.CTkLabel(
            input_frame,
            text="◈ INPUT MASTER KEY & CARD UID ◈",
            font=("Consolas", 16, "bold"),
            text_color=COLORS['accent_yellow']
        )
        header.pack(pady=(15, 10))
        
        container = ctk.CTkFrame(input_frame, fg_color="transparent")
        container.pack(fill="x", padx=20, pady=10)
        
        # Master Key Input
        master_frame = ctk.CTkFrame(container, fg_color="transparent")
        master_frame.pack(fill="x", pady=8)
        
        master_label = ctk.CTkLabel(
            master_frame,
            text="MASTER KEY (32 hex chars):",
            font=("Consolas", 14),
            text_color=COLORS['text_secondary'],
            width=220,
            anchor="w"
        )
        master_label.pack(side="left", padx=(0, 10))
        
        self.master_entry = ctk.CTkEntry(
            master_frame,
            font=("Consolas", 16),
            fg_color=COLORS['bg_dark'],
            border_color=COLORS['accent_cyan'],
            text_color=COLORS['text_primary'],
            placeholder_text="e.g. 0102030405060708090A0B0C0D0E0F10",
            width=400,
            height=40
        )
        self.master_entry.pack(side="left")
        
        # UID Input
        uid_frame = ctk.CTkFrame(container, fg_color="transparent")
        uid_frame.pack(fill="x", pady=8)
        
        uid_label = ctk.CTkLabel(
            uid_frame,
            text="CARD UID (hex, spaces optional):",
            font=("Consolas", 14),
            text_color=COLORS['text_secondary'],
            width=220,
            anchor="w"
        )
        uid_label.pack(side="left", padx=(0, 10))
        
        self.uid_entry = ctk.CTkEntry(
            uid_frame,
            font=("Consolas", 16),
            fg_color=COLORS['bg_dark'],
            border_color=COLORS['accent_magenta'],
            text_color=COLORS['text_primary'],
            placeholder_text="e.g. 040C6FFA1D2090",
            width=400,
            height=40
        )
        self.uid_entry.pack(side="left")
        
        # Buttons
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        self.calc_button = ctk.CTkButton(
            button_frame,
            text="⚡ DIVERSIFY KEY ⚡",
            font=("Consolas", 16, "bold"),
            fg_color=COLORS['accent_cyan'],
            hover_color=COLORS['accent_magenta'],
            text_color=COLORS['bg_dark'],
            width=220,
            height=50,
            command=self.calculate
        )
        self.calc_button.pack(side="left", padx=15)
        
        self.clear_button = ctk.CTkButton(
            button_frame,
            text="◼ CLEAR ALL",
            font=("Consolas", 14),
            fg_color=COLORS['bg_medium'],
            hover_color=COLORS['accent_orange'],
            text_color=COLORS['text_primary'],
            border_color=COLORS['accent_orange'],
            border_width=2,
            width=140,
            height=50,
            command=self.clear_all
        )
        self.clear_button.pack(side="left", padx=15)
        
    def create_results_section(self):
        self.results_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_light'], corner_radius=10)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        header = ctk.CTkLabel(
            self.results_frame,
            text="◈ DERIVED CARD KEY ◈",
            font=("Consolas", 16, "bold"),
            text_color=COLORS['accent_yellow']
        )
        header.pack(pady=(15, 10))
        
        self.results_scroll = ctk.CTkScrollableFrame(
            self.results_frame,
            fg_color=COLORS['bg_dark'],
            corner_radius=5
        )
        self.results_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.placeholder = ctk.CTkLabel(
            self.results_scroll,
            text="[ ENTER MASTER KEY AND UID → PRESS DIVERSIFY ]",
            font=("Consolas", 14),
            text_color=COLORS['accent_cyan']
        )
        self.placeholder.pack(pady=60)
        
    def create_footer(self):
        footer_frame = ctk.CTkFrame(self, fg_color=COLORS['bg_medium'], corner_radius=0, height=50)
        footer_frame.pack(fill="x", side="bottom")
        
        footer_text = ctk.CTkLabel(
            footer_frame,
            text="◢ CYBERNINJA © 2026 | KOBE'S KEYS - MAMBA FOREVER ◤",
            font=("Consolas", 11),
            text_color=COLORS['accent_magenta']
        )
        footer_text.pack(pady=10)
        
    def calculate(self):
        master_hex = self.master_entry.get().strip().replace(" ", "").upper()
        uid_hex = self.uid_entry.get().strip().replace(" ", "").upper()
        
        try:
            if len(master_hex) != 32:
                raise ValueError("Master key must be 32 hex characters (16 bytes AES)")
            if not uid_hex:
                raise ValueError("UID cannot be empty")
                
            derived_key = self.diversify_key(master_hex, uid_hex)
            self.results = {
                "master": master_hex,
                "uid": uid_hex,
                "derived": derived_key
            }
            self.display_results()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def diversify_key(self, master_hex: str, uid_hex: str) -> str:
        """Simple AES-ECB diversification: K_card = AES_ECB(K_master, UID || 00...)"""
        uid_bytes = unhexlify(uid_hex)
        if len(uid_bytes) > 16:
            raise ValueError("UID too long (>16 bytes)")
            
        # Pad UID with zeros to 16 bytes
        data = uid_bytes + b'\x00' * (16 - len(uid_bytes))
        
        master_key = unhexlify(master_hex)
        cipher = AES.new(master_key, AES.MODE_ECB)
        derived = cipher.encrypt(data)
        
        return hexlify(derived).decode().upper()
        
    def display_results(self):
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        r = self.results
        
        sections = [
            ("INPUT", [
                ("Master Key", r['master']),
                ("Card UID", r['uid'])
            ]),
            ("DERIVED CARD KEY", [
                ("AES Key (32 hex)", r['derived'])
            ]),
            ("PROXMARK3 COMMAND READY", [
                ("Change Master Key (example)", 
                 f"hf mfdes changekey --aid 010203 --keyno 0 --oldkey 00000000000000000000000000000000 --newkey {r['derived']}"),
                ("Auth with derived key (example)", 
                 f"hf mfdes auth --aid 010203 -n 0 -t aes -k {r['derived']}")
            ])
        ]
        
        for section_name, items in sections:
            self.add_section(section_name, items)
            
        # Copy all button
        copy_frame = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
        copy_frame.pack(fill="x", pady=20)
        
        copy_btn = ctk.CTkButton(
            copy_frame,
            text="📋 COPY DERIVED KEY + COMMANDS",
            font=("Consolas", 12),
            fg_color=COLORS['accent_magenta'],
            hover_color=COLORS['accent_cyan'],
            text_color=COLORS['bg_dark'],
            width=300,
            height=40,
            command=self.copy_all
        )
        copy_btn.pack()
        
    def add_section(self, title, items):
        header = ctk.CTkLabel(
            self.results_scroll,
            text=f"┌─ {title} ─┐",
            font=("Consolas", 13, "bold"),
            text_color=COLORS['accent_yellow'],
            anchor="w"
        )
        header.pack(fill="x", padx=10, pady=(15, 5))
        
        for label, value in items:
            item_frame = ctk.CTkFrame(self.results_scroll, fg_color="transparent")
            item_frame.pack(fill="x", padx=20, pady=3)
            
            lbl = ctk.CTkLabel(
                item_frame,
                text=f"{label}:",
                font=("Consolas", 11),
                text_color=COLORS['text_secondary'],
                width=260,
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
            
            copy_btn = ctk.CTkButton(
                item_frame,
                text="📋",
                font=("Consolas", 10),
                fg_color="transparent",
                hover_color=COLORS['bg_light'],
                text_color=COLORS['accent_cyan'],
                width=30,
                height=25,
                command=lambda v=value: pyperclip.copy(v)
            )
            copy_btn.pack(side="right", padx=5)
            
    def copy_all(self):
        r = self.results
        text = f"""DESFIRE DERIVED KEY - CyberNinja Tool
{'='*60}
Master Key : {r['master']}
Card UID   : {r['uid']}
Derived Key: {r['derived']}

Proxmark3 Commands:
hf mfdes changekey --aid 010203 --keyno 0 --oldkey 00000000000000000000000000000000 --newkey {r['derived']}
hf mfdes auth --aid 010203 -n 0 -t aes -k {r['derived']}

{'='*60}
Generated by Kobe's Keys - Mamba Mentality
"""
        pyperclip.copy(text)
        messagebox.showinfo("Copied!", "Derived key + PM3 commands copied to clipboard!")
        
    def clear_all(self):
        self.master_entry.delete(0, 'end')
        self.uid_entry.delete(0, 'end')
        
        for widget in self.results_scroll.winfo_children():
            widget.destroy()
            
        self.placeholder = ctk.CTkLabel(
            self.results_scroll,
            text="[ ENTER MASTER KEY AND UID → PRESS DIVERSIFY ]",
            font=("Consolas", 14),
            text_color=COLORS['accent_cyan']
        )
        self.placeholder.pack(pady=60)


def main():
    app = DesfireDiversifier()
    app.mainloop()


if __name__ == "__main__":
    main()