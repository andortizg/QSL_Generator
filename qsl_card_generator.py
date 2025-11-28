#!/usr/bin/env python3
"""
QSL Card LaTeX Generator with PDF Generation and Settings Management
A visual application to generate LaTeX code for amateur radio QSL cards
"""

import sys
import os
import json
import subprocess
import tempfile
import shutil

# Try to import tkinter for GUI mode
try:
    import tkinter as tk
    from tkinter import ttk, scrolledtext, messagebox, filedialog
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("Warning: tkinter not available. Running in command-line mode.")

class QSLCardGenerator:
    def __init__(self, root=None):
        if root is not None:
            self.root = root
            self.root.title("QSL Card LaTeX Generator")
            self.root.geometry("950x850")
            
            # Settings file path
            self.settings_file = os.path.expanduser("~/.qsl_generator_settings.json")
            
            # Create notebook for tabs
            self.notebook = ttk.Notebook(root)
            self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Create tabs
            self.station_tab = ttk.Frame(self.notebook)
            self.contact_tab = ttk.Frame(self.notebook)
            self.output_tab = ttk.Frame(self.notebook)
            self.about_tab = ttk.Frame(self.notebook)
            
            self.notebook.add(self.station_tab, text="Station Info")
            self.notebook.add(self.contact_tab, text="Contact Details")
            self.notebook.add(self.output_tab, text="LaTeX Output")
            self.notebook.add(self.about_tab, text="About")
            
            # Initialize fields
            self.fields = {}
            
            # Add status bar first (before loading settings)
            self.setup_status_bar()
            
            # Setup all tabs
            self.setup_station_tab()
            self.setup_contact_tab()
            self.setup_output_tab()
            self.setup_about_tab()
            
            # Load saved settings
            self.load_settings()
        else:
            # Command-line mode
            self.fields = {}
            self.init_cli_defaults()
    
    def setup_status_bar(self):
        """Setup status bar at the bottom"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side='bottom', fill='x', padx=5, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready", relief=tk.SUNKEN, anchor='w')
        self.status_label.pack(side='left', fill='x', expand=True)
    
    def update_status(self, message):
        """Update status bar message"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
            self.root.update_idletasks()
    
    def init_cli_defaults(self):
        """Initialize default values for CLI mode"""
        self.data = {
            'callsign': "EA7HQL",
            'operator_name': "Andrés Ortiz",
            'qth_city': "Torremolinos",
            'qth_state': "Málaga",
            'country': "SPAIN",
            'grid': "IM76SP",
            'cq_zone': "14",
            'itu_zone': "37",
            'email': "ea7hql@gmail.com",
            'qrz_url': "https://www.qrz.com",
            'via': "",
            'to_station': "",
            'their_call': "",
            'date': "",
            'time': "",
            'band': "",
            'mode': "",
            'report': "",
            'qth_type': "home",
            'portable_location': "",
            'qsl_type': "qso",
            'qsl_request': "tnx",
            'transceiver': "",
            'power': "",
            'antenna': "",
            'satellite': "",
            'background_image': "foto_antenas.jpg",
            'logo1': "logo_ure_negro.png",
            'logo1_scale': "0.07",
            'logo2': "qrz_com.png",
            'logo2_scale': "0.2",
            'logo3': "lotw.png",
            'logo3_scale': "0.1"
        }
    
    def setup_station_tab(self):
        """Setup the station information tab"""
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(self.station_tab)
        scrollbar = ttk.Scrollbar(self.station_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Use scrollable_frame instead of frame
        frame = ttk.Frame(scrollable_frame, padding="20")
        frame.pack(fill='both', expand=True)
        
        # Header with save/load buttons
        header_frame = ttk.Frame(frame)
        header_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky='ew')
        
        ttk.Label(header_frame, text="Station Information & Equipment", font=('Arial', 14, 'bold')).pack(side='left')
        
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side='right')
        ttk.Button(button_frame, text="Save Defaults", command=self.save_settings, 
                  width=15).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Load Defaults", command=self.load_settings, 
                  width=15).pack(side='left', padx=2)
        ttk.Button(button_frame, text="Clear All", command=self.clear_contact_fields, 
                  width=15).pack(side='left', padx=2)
        
        # Station details
        labels = [
            ("Callsign:", "callsign"),
            ("Operator Name:", "operator_name"),
            ("QTH (City):", "qth_city"),
            ("QTH (State/Province):", "qth_state"),
            ("Country:", "country"),
            ("Grid Locator:", "grid"),
            ("CQ Zone:", "cq_zone"),
            ("ITU Zone:", "itu_zone"),
            ("Email:", "email"),
            ("QRZ URL:", "qrz_url"),
        ]
        
        row = 1
        for label_text, field_name in labels:
            ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)
            self.fields[field_name] = entry
            row += 1
        
        # Equipment section
        ttk.Label(frame, text="Equipment:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, columnspan=2, sticky='w', padx=5, pady=(15, 5))
        row += 1
        
        equipment_labels = [
            ("Transceiver:", "transceiver"),
            ("Power (Watts):", "power"),
            ("Antenna:", "antenna"),
            ("Via Satellite:", "satellite"),
        ]
        
        for label_text, field_name in equipment_labels:
            ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)
            self.fields[field_name] = entry
            row += 1
        
        # Image files section
        ttk.Label(frame, text="Image Files:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, columnspan=3, sticky='w', padx=5, pady=(15, 5))
        row += 1
        
        # Background image (no scale)
        ttk.Label(frame, text="Background Image:").grid(row=row, column=0, sticky='e', padx=5, pady=5)
        entry = ttk.Entry(frame, width=40)
        entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        self.fields['background_image'] = entry
        row += 1
        
        # Logo files with scales on the right
        logo_configs = [
            ("Logo 1 (URE):", "logo1", "logo1_scale"),
            ("Logo 2 (QRZ):", "logo2", "logo2_scale"),
            ("Logo 3 (LoTW):", "logo3", "logo3_scale"),
        ]
        
        for label_text, file_field, scale_field in logo_configs:
            # Label
            ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky='e', padx=5, pady=5)
            
            # Filename entry
            file_entry = ttk.Entry(frame, width=30)
            file_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)
            self.fields[file_field] = file_entry
            
            # Scale label and entry on the right
            scale_label = ttk.Label(frame, text="Scale:")
            scale_label.grid(row=row, column=2, sticky='e', padx=(10, 5), pady=5)
            
            scale_entry = ttk.Entry(frame, width=8)
            scale_entry.grid(row=row, column=3, sticky='w', padx=5, pady=5)
            self.fields[scale_field] = scale_entry
            
            row += 1
        
        # Help text for scales
        help_text = ttk.Label(frame, text="Logo scales: decimal values (e.g., 0.07, 0.2, 0.1) - Leave empty for defaults", 
                             font=('Arial', 8, 'italic'), foreground='gray')
        help_text.grid(row=row, column=0, columnspan=4, pady=(5, 0), sticky='w', padx=5)
    
    def setup_contact_tab(self):
        """Setup the contact details tab"""
        frame = ttk.Frame(self.contact_tab, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Contact Details", font=('Arial', 14, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Via and To Station
        ttk.Label(frame, text="VIA (Bureau/Manager):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.fields['via'] = ttk.Entry(frame, width=40)
        self.fields['via'].grid(row=1, column=1, sticky='w', padx=5, pady=5)
        
        ttk.Label(frame, text="TO STATION (Their Call):").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.fields['to_station'] = ttk.Entry(frame, width=40)
        self.fields['to_station'].grid(row=2, column=1, sticky='w', padx=5, pady=5)
        
        # QSO Details
        ttk.Label(frame, text="QSO Information", font=('Arial', 12, 'bold')).grid(
            row=3, column=0, columnspan=2, pady=(15, 10))
        
        labels = [
            ("Their Callsign:", "their_call"),
            ("Date (DD/MM/YYYY):", "date"),
            ("Time (UTC):", "time"),
            ("Band:", "band"),
            ("Mode:", "mode"),
            ("Signal Report:", "report"),
        ]
        
        row = 4
        for label_text, field_name in labels:
            ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky='e', padx=5, pady=5)
            entry = ttk.Entry(frame, width=40)
            entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)
            self.fields[field_name] = entry
            row += 1
        
        # QTH Type
        ttk.Label(frame, text="My QTH Type:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky='e', padx=5, pady=(15, 5))
        qth_frame = ttk.Frame(frame)
        qth_frame.grid(row=row, column=1, sticky='w', padx=5, pady=(15, 5))
        
        self.fields['qth_type'] = tk.StringVar(value="home")
        ttk.Radiobutton(qth_frame, text="Home", variable=self.fields['qth_type'], 
                       value="home").pack(side='left', padx=5)
        ttk.Radiobutton(qth_frame, text="Portable", variable=self.fields['qth_type'], 
                       value="portable").pack(side='left', padx=5)
        row += 1
        
        ttk.Label(frame, text="Portable Location:").grid(row=row, column=0, sticky='e', padx=5, pady=5)
        self.fields['portable_location'] = ttk.Entry(frame, width=40)
        self.fields['portable_location'].grid(row=row, column=1, sticky='w', padx=5, pady=5)
        row += 1
        
        # QSL Type
        ttk.Label(frame, text="QSL Type:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky='e', padx=5, pady=(15, 5))
        qsl_frame = ttk.Frame(frame)
        qsl_frame.grid(row=row, column=1, sticky='w', padx=5, pady=(15, 5))
        
        self.fields['qsl_type'] = tk.StringVar(value="qso")
        ttk.Radiobutton(qsl_frame, text="QSO", variable=self.fields['qsl_type'], 
                       value="qso").pack(side='left', padx=5)
        ttk.Radiobutton(qsl_frame, text="SWL Report", variable=self.fields['qsl_type'], 
                       value="swl").pack(side='left', padx=5)
        row += 1
        
        # PSE/TNX
        ttk.Label(frame, text="QSL Request:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky='e', padx=5, pady=(15, 5))
        qsl_request_frame = ttk.Frame(frame)
        qsl_request_frame.grid(row=row, column=1, sticky='w', padx=5, pady=(15, 5))
        
        self.fields['qsl_request'] = tk.StringVar(value="tnx")
        ttk.Radiobutton(qsl_request_frame, text="PSE (Please send)", 
                       variable=self.fields['qsl_request'], value="pse").pack(side='left', padx=5)
        ttk.Radiobutton(qsl_request_frame, text="TNX (Thanks)", 
                       variable=self.fields['qsl_request'], value="tnx").pack(side='left', padx=5)
    
    def setup_output_tab(self):
        """Setup the output tab"""
        frame = ttk.Frame(self.output_tab, padding="20")
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Generated LaTeX Code", font=('Arial', 14, 'bold')).pack(pady=(0, 10))
        
        # Button frame
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(button_frame, text="Generate LaTeX", 
                  command=self.generate_latex, width=15).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Generate PDF", 
                  command=self.generate_pdf, width=15).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Save LaTeX", 
                  command=self.save_to_file, width=15).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard, width=18).pack(side='left', padx=5)
        
        # Text area for output
        self.output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=30)
        self.output_text.pack(fill='both', expand=True)
    
    def setup_about_tab(self):
        """Setup the about tab"""
        frame = ttk.Frame(self.about_tab, padding="20")
        frame.pack(fill='both', expand=True)
        
        # Create a centered frame
        center_frame = ttk.Frame(frame)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title_label = ttk.Label(center_frame, 
                                text="QSL Card Generator",
                                font=('Arial', 20, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Version
        version_label = ttk.Label(center_frame,
                                  text="Version 1.3",
                                  font=('Arial', 12))
        version_label.pack(pady=(0, 20))
        
        # Author info
        author_label = ttk.Label(center_frame,
                                text="Andrés Ortiz, EA7HQL",
                                font=('Arial', 14, 'bold'))
        author_label.pack(pady=(0, 30))
        
        # Credits
        credits_frame = ttk.Frame(center_frame)
        credits_frame.pack(pady=(0, 20))
        
        credits_title = ttk.Label(credits_frame,
                                 text="Credits:",
                                 font=('Arial', 11, 'bold'))
        credits_title.pack(pady=(0, 10))
        
        credits_text = ttk.Label(credits_frame,
                                text="Based on QSL Card design by Ian Renton M0TRT (Public Domain),\n"
                                     "which was based on an example by Fabian Kurz, DJ5CW.",
                                font=('Arial', 12),
                                justify='center')
        credits_text.pack()
        
        # Additional info
        info_frame = ttk.Frame(center_frame)
        info_frame.pack(pady=(30, 0))
        
        info_label = ttk.Label(info_frame,
                              text="Amateur Radio QSL Card Generator\n"
                                   "with LaTeX and PDF support",
                              font=('Arial', 10, 'italic'),
                              justify='center',
                              foreground='gray')
        info_label.pack(pady=(0, 20))
        
        # 73 message
        sign_off = ttk.Label(center_frame,
                            text="73 and Good DX!",
                            font=('Arial', 12, 'bold'))
        sign_off.pack()
    
    def clear_contact_fields(self):
        """Clear only contact-specific fields, keeping station info and equipment"""
        if messagebox.askyesno("Clear Fields", "Clear all contact details fields?"):
            contact_fields = ['via', 'to_station', 'their_call', 'date', 'time', 
                            'band', 'mode', 'report', 'portable_location']
            
            for field_name in contact_fields:
                if field_name in self.fields:
                    field = self.fields[field_name]
                    if isinstance(field, tk.StringVar):
                        pass  # Don't clear radio buttons
                    else:
                        field.delete(0, tk.END)
            
            # Reset radio buttons to defaults
            self.fields['qth_type'].set("home")
            self.fields['qsl_type'].set("qso")
            self.fields['qsl_request'].set("tnx")
            
            self.update_status("Contact fields cleared (equipment preserved)")
    
    def save_settings(self):
        """Save station information and equipment as defaults"""
        settings = {}
        
        # Fields to save
        save_fields = ['callsign', 'operator_name', 'qth_city', 'qth_state', 'country',
                      'grid', 'cq_zone', 'itu_zone', 'email', 'qrz_url',
                      'transceiver', 'power', 'antenna', 'satellite',
                      'background_image', 'logo1', 'logo2', 'logo3',
                      'logo1_scale', 'logo2_scale', 'logo3_scale']
        
        for field_name in save_fields:
            if field_name in self.fields:
                field = self.fields[field_name]
                if isinstance(field, tk.StringVar):
                    settings[field_name] = field.get()
                else:
                    settings[field_name] = field.get()
        
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Success", f"Default settings saved to:\n{self.settings_file}")
            self.update_status("Settings saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
            self.update_status(f"Error saving settings: {str(e)}")
    
    def load_settings(self):
        """Load saved station information and equipment"""
        if not os.path.exists(self.settings_file):
            # Set default values if no settings file exists
            defaults = {
                'callsign': "EA7HQL",
                'operator_name': "Andrés Ortiz",
                'qth_city': "Torremolinos",
                'qth_state': "Málaga",
                'country': "SPAIN",
                'grid': "IM76SP",
                'cq_zone': "14",
                'itu_zone': "37",
                'email': "ea7hql@gmail.com",
                'qrz_url': "https://www.qrz.com",
                'transceiver': "",
                'power': "",
                'antenna': "",
                'satellite': "",
                'background_image': "foto_antenas.jpg",
                'logo1': "logo_ure_negro.png",
                'logo1_scale': "0.07",
                'logo2': "qrz_com.png",
                'logo2_scale': "0.2",
                'logo3': "lotw.png",
                'logo3_scale': "0.1"
            }
            
            for field_name, value in defaults.items():
                if field_name in self.fields:
                    field = self.fields[field_name]
                    if not isinstance(field, tk.StringVar):
                        field.insert(0, value)
            
            self.update_status("Default values loaded (no saved settings found)")
            return
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            for field_name, value in settings.items():
                if field_name in self.fields:
                    field = self.fields[field_name]
                    if isinstance(field, tk.StringVar):
                        field.set(value)
                    else:
                        field.delete(0, tk.END)
                        field.insert(0, value)
            
            self.update_status(f"Settings loaded from {self.settings_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")
            self.update_status(f"Error loading settings: {str(e)}")
    
    def get_field_value(self, field_name):
        """Get field value from GUI or CLI data"""
        if hasattr(self, 'root') and self.root is not None:
            # GUI mode
            if field_name not in self.fields:
                return ""
            field = self.fields[field_name]
            if isinstance(field, tk.StringVar):
                return field.get()
            else:
                return field.get()
        else:
            # CLI mode
            return self.data.get(field_name, "")
    
    def generate_latex_code(self):
        """Generate the LaTeX code from the form data"""
        # Get all values
        callsign = self.get_field_value('callsign')
        operator_name = self.get_field_value('operator_name')
        qth_city = self.get_field_value('qth_city')
        qth_state = self.get_field_value('qth_state')
        country = self.get_field_value('country')
        grid = self.get_field_value('grid')
        cq_zone = self.get_field_value('cq_zone')
        itu_zone = self.get_field_value('itu_zone')
        email = self.get_field_value('email')
        qrz_url = self.get_field_value('qrz_url')
        
        via = self.get_field_value('via')
        to_station = self.get_field_value('to_station')
        their_call = self.get_field_value('their_call')
        date = self.get_field_value('date')
        time = self.get_field_value('time')
        band = self.get_field_value('band')
        mode = self.get_field_value('mode')
        report = self.get_field_value('report')
        
        qth_type = self.get_field_value('qth_type')
        portable_location = self.get_field_value('portable_location')
        qsl_type = self.get_field_value('qsl_type')
        qsl_request = self.get_field_value('qsl_request')
        
        transceiver = self.get_field_value('transceiver')
        power = self.get_field_value('power')
        antenna = self.get_field_value('antenna')
        satellite = self.get_field_value('satellite')
        
        # Image files
        background_image = self.get_field_value('background_image') or "foto_antenas.jpg"
        logo1 = self.get_field_value('logo1') or "logo_ure_negro.png"
        logo1_scale = self.get_field_value('logo1_scale') or "0.07"
        logo2 = self.get_field_value('logo2') or "qrz_com.png"
        logo2_scale = self.get_field_value('logo2_scale') or "0.2"
        logo3 = self.get_field_value('logo3') or "lotw.png"
        logo3_scale = self.get_field_value('logo3_scale') or "0.1"
        
        # Generate checkboxes
        home_check = "$\\boxtimes$" if qth_type == "home" else "$\\square$"
        portable_check = "$\\boxtimes$" if qth_type == "portable" else "$\\square$"
        qso_check = "$\\boxtimes$" if qsl_type == "qso" else "$\\square$"
        swl_check = "$\\boxtimes$" if qsl_type == "swl" else "$\\square$"
        pse_check = "$\\boxtimes$" if qsl_request == "pse" else "$\\square$"
        tnx_check = "$\\boxtimes$" if qsl_request == "tnx" else "$\\square$"
        
        # Build the LaTeX document
        latex_code = f"""% QSL Card design by Ian Renton M0TRT. Public domain. Based on an example by Fabian Kurz, DJ5CW.

\\documentclass[10pt]{{article}}
\\pagestyle{{empty}}
\\usepackage{{array}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{tgschola}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usepackage{{latexsym}}
\\usepackage{{graphicx}}
\\usepackage[export]{{adjustbox}}
\\usepackage{{eso-pic}}
\\usepackage{{xcolor}}
\\usepackage{{anyfontsize}}
\\usepackage[outline]{{contour}}
\\usepackage[papersize={{14cm,9cm}}, margin=0.5cm, marginratio=1:1]{{geometry}}
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\parskip}}{{0pt}}
\\AddToShipoutPictureBG{{
    \\ifodd\\value{{page}}
      \\AtPageCenter{{
        \\includegraphics[width=\\paperwidth,height=\\paperheight,valign=M,center=-0.55em]{{{background_image}}}%
        }}
    \\fi
}}

\\begin{{document}}
\\vspace{{0.5cm}}
\\begin{{center}}
\\fontfamily{{phv}}\\selectfont \\fontsize{{60}}{{72}}\\selectfont \\textcolor{{white}}{{\\contour{{black}}{{\\textbf{{{callsign}}}}}}}
\\end{{center}}
\\vspace{{4.5cm}}
\\hfill
\\begin{{minipage}}{{0.5\\textwidth}}
\\begin{{center}}
{{\\huge {{\\fontfamily{{phv}}\\selectfont \\textcolor{{white}}{{\\contour{{black}}{{\\textbf{{{operator_name}}}}}}}}}}}

\\vspace{{6pt}}
{{\\Large {{\\fontfamily{{phv}}\\selectfont \\textcolor{{white}}{{\\contour{{black}}{{\\textbf{{{qth_city}, {country}}}}}}}}}}}
\\end{{center}}
\\end{{minipage}}
\\newpage
\\begin{{minipage}}{{0.6\\textwidth}}
{{\\Large \\textbf{{{callsign}}}}} \\quad {{\\textbf{{{operator_name}}}}}

{{\\small {qth_city}, {qth_state}, {country}}}

{{\\small Grid: {grid} \\quad CQ: {cq_zone} \\quad ITU: {itu_zone}}}

{{\\small {email} \\quad {qrz_url}}}

\\end{{minipage}}
\\hfill
\\begin{{minipage}}{{0.35\\textwidth}}
\\begin{{tabular}}{{ | m{{11.7em}} | }}
\\hline
{{\\scriptsize VIA \\vphantom{{$\\int\\limits_{{\\dfrac aa}}$}} {via}}}\\\\
\\hline
{{\\scriptsize TO STATION \\vphantom{{$\\int\\limits_{{\\dfrac aa}}$}} {to_station}}}\\\\
\\hline
\\end{{tabular}}
\\end{{minipage}}

\\smallskip

\\begin{{center}}
\\begin{{tabular}}{{|w{{c}}{{5em}}|w{{c}}{{6.5em}}|w{{c}}{{6em}}|w{{c}}{{4em}}|w{{c}}{{4em}}|w{{c}}{{4em}}|}}
\\hline
{{\\footnotesize Your Call}}&{{\\footnotesize Date (D/M/Y)}}&{{\\footnotesize Time (UTC)}}&{{\\footnotesize Band}}&{{\\footnotesize Mode}}&{{\\footnotesize Report}}\\\\
\\hline
\\vphantom{{$\\dfrac b b$}} {their_call} & {date} & {time} & {band} & {mode} & {report} \\\\
\\hline
\\end{{tabular}}

\\bigskip

\\begin{{tabular}}{{|w{{c}}{{4em}}|w{{c}}{{20em}}|w{{c}}{{4em}}|w{{c}}{{3.9em}}|}}
\\hline
{{\\footnotesize My QTH}} & \\multicolumn{{3}}{{l|}}{{{{\\footnotesize \\vphantom{{$\\dfrac b b$}} {home_check} Home \\enspace {portable_check} Portable: {portable_location}}}}} \\\\
\\hline
{{\\footnotesize Transceiver}} & {{\\footnotesize \\vphantom{{$\\dfrac b b$}} {transceiver}}} & {{\\footnotesize Power}} & {{\\footnotesize \\vphantom{{$\\dfrac b b$}} {power} W}} \\\\
\\hline
{{\\footnotesize Antenna}} & {{\\footnotesize \\vphantom{{$\\dfrac b b$}} {antenna}}} & {{\\footnotesize Via Sat.}} & {{\\footnotesize \\vphantom{{$\\dfrac b b$}} {satellite}}} \\\\
\\hline
\\end{{tabular}}
\\end{{center}}
\\vspace{{3pt}}
\\begin{{minipage}}{{0.65\\textwidth}}
{{\\footnotesize Thanking you for: \\quad {qso_check} our QSO \\quad {swl_check} your SWL report}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}{{0.3\\textwidth}}
{{\\footnotesize QSL \\quad \\quad {pse_check} PSE \\quad {tnx_check} TNX}}
\\end{{minipage}}

\\begin{{minipage}}{{0.65\\textwidth}}
\\vspace{{2em}}
\\includegraphics[width={logo1_scale}\\textwidth,valign=m]{{{logo1}}}
\\includegraphics[width={logo2_scale}\\textwidth,valign=m]{{{logo2}}}
\\includegraphics[width={logo3_scale}\\textwidth,valign=m]{{{logo3}}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}{{0.3\\textwidth}}
\\vspace{{0.5em}}
{{\\footnotesize VY 73,}}

\\vspace{{1.5em}}
\\makebox{{\\rule[-0.5em]{{11em}}{{0.4pt}}}}
\\end{{minipage}}

\\end{{document}}
"""
        return latex_code
    
    def generate_latex(self):
        """Generate and display LaTeX in GUI"""
        latex_code = self.generate_latex_code()
        
        # Display in output
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(1.0, latex_code)
        
        self.update_status("LaTeX code generated successfully")
        messagebox.showinfo("Success", "LaTeX code generated successfully!")
    
    def generate_pdf(self):
        """Generate PDF from the LaTeX code"""
        # Check if pdflatex is available
        if not shutil.which('pdflatex'):
            messagebox.showerror("Error", 
                "pdflatex is not installed or not in PATH.\n\n"
                "Please install LaTeX:\n"
                "  Ubuntu/Debian: sudo apt-get install texlive-latex-base texlive-fonts-recommended\n"
                "  Fedora: sudo dnf install texlive-scheme-basic\n"
                "  macOS: brew install mactex")
            return
        
        self.update_status("Generating PDF...")
        
        try:
            # Generate LaTeX code
            latex_code = self.generate_latex_code()
            
            # Create temporary directory
            temp_dir = tempfile.mkdtemp()
            tex_file = os.path.join(temp_dir, "qsl_card.tex")
            
            # Write LaTeX to temporary file
            with open(tex_file, 'w', encoding='utf-8') as f:
                f.write(latex_code)
            
            # Copy image files to temp directory if they exist
            image_files = [
                self.get_field_value('background_image') or "foto_antenas.jpg",
                self.get_field_value('logo1') or "logo_ure_negro.png",
                self.get_field_value('logo2') or "qrz_com.png",
                self.get_field_value('logo3') or "lotw.png"
            ]
            
            missing_images = []
            for img in image_files:
                if os.path.exists(img):
                    shutil.copy(img, temp_dir)
                else:
                    missing_images.append(img)
            
            if missing_images:
                response = messagebox.askyesno("Missing Images",
                    f"The following image files were not found:\n" +
                    "\n".join(f"  • {img}" for img in missing_images) +
                    "\n\nDo you want to continue anyway?\n" +
                    "(PDF generation may fail)")
                if not response:
                    shutil.rmtree(temp_dir)
                    self.update_status("PDF generation cancelled")
                    return
            
            # Run pdflatex
            self.update_status("Running pdflatex (this may take a moment)...")
            process = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'qsl_card.tex'],
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            pdf_file = os.path.join(temp_dir, "qsl_card.pdf")
            
            if os.path.exists(pdf_file):
                # Ask user where to save the PDF
                save_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                    initialfile="qsl_card.pdf"
                )
                
                if save_path:
                    shutil.copy(pdf_file, save_path)
                    self.update_status(f"PDF saved successfully to {save_path}")
                    messagebox.showinfo("Success", 
                        f"PDF generated successfully!\n\nSaved to:\n{save_path}\n\n"
                        "You can now print your QSL card.")
                else:
                    self.update_status("PDF generation cancelled by user")
            else:
                # Show error log
                log_file = os.path.join(temp_dir, "qsl_card.log")
                error_msg = "PDF generation failed.\n\n"
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        log_content = f.read()
                    # Extract relevant errors
                    lines = log_content.split('\n')
                    error_lines = [l for l in lines if '!' in l or 'Error' in l or 'error' in l]
                    if error_lines:
                        error_msg += "Errors found:\n" + "\n".join(error_lines[:10])
                else:
                    error_msg += process.stderr
                
                messagebox.showerror("Error", error_msg)
                self.update_status("PDF generation failed")
            
            # Clean up
            shutil.rmtree(temp_dir)
            
        except subprocess.TimeoutExpired:
            messagebox.showerror("Error", "PDF generation timed out. Check your LaTeX installation.")
            self.update_status("PDF generation timed out")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")
            self.update_status(f"Error: {str(e)}")
    
    def save_to_file(self):
        """Save the generated LaTeX to a file"""
        content = self.output_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "Please generate LaTeX code first!")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".tex",
            filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")],
            initialfile="qsl_card.tex"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.update_status(f"LaTeX file saved to {filename}")
                messagebox.showinfo("Success", f"File saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                self.update_status(f"Error saving file: {str(e)}")
    
    def copy_to_clipboard(self):
        """Copy the generated LaTeX to clipboard"""
        content = self.output_text.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "Please generate LaTeX code first!")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.update_status("LaTeX code copied to clipboard")
        messagebox.showinfo("Success", "LaTeX code copied to clipboard!")

def main():
    if not GUI_AVAILABLE:
        print("GUI mode not available. Please install tkinter.")
        return
    
    root = tk.Tk()
    app = QSLCardGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
