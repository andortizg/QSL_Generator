# QSL Card LaTeX Generator

A Python application for generating customized amateur radio QSL cards with LaTeX. Features an intuitive GUI, automatic PDF generation, and persistent settings management.
Based on QSL Card design by Ian Renton M0TRT (Public Domain), which was based on an example by Fabian Kurz, DJ5CW.

![Version](https://img.shields.io/badge/version-1.3-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![License](https://img.shields.io/badge/license-Public_Domain-lightgrey)

## Features

### Core Capabilities
- ** Visual GUI Interface** - Easy-to-use tabbed interface with organized sections
- ** Direct PDF Generation** - Create print-ready PDFs with one click
- ** Automatic Settings** - Save and load your station configuration automatically
- ** Customizable Design** - Adjust logo sizes, images, and layout
- ** Fast Workflow** - Generate multiple QSL cards quickly
- ** Real-time Status** - Status bar shows progress and confirmations

### Station Management
- Complete station information storage
- Equipment configuration (transceiver, power, antenna)
- Custom image and logo support
- Persistent settings across sessions

### Smart Features
- **Clear All Button** - Clears only contact fields, preserves station data
- **Scrollable Interface** - Comfortable viewing of all fields
- **Logo Scale Control** - Adjust size of each logo independently
- **Default Values** - Pre-filled with sensible defaults

## Requirements

### Essential
- **Python 3.6+** (usually pre-installed on Linux/macOS)
- **tkinter** (included with Python)
- **LaTeX with pdflatex** (for PDF generation)

### Installing LaTeX

**Ubuntu/Debian:**
```bash
sudo apt-get install texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

**Fedora:**
```bash
sudo dnf install texlive-scheme-basic
```

**macOS:**
```bash
brew install mactex
```

**Windows:**
Download and install [MiKTeX](https://miktex.org/)

## Quick Start

### 1. Download
```bash
# Download the script
wget https://your-url/qsl_card_generator_final.py

# Or clone the repository
git clone https://your-repo/qsl-generator
cd qsl-generator
```

### 2. Prepare Image Files
Place these files in the same directory as the script:
```
qsl_generator/
├── qsl_card_generator_final.py
├── foto_antenas.jpg          # Your background image
├── logo_ure_negro.png         # URE logo
├── qrz_com.png                # QRZ.com logo
└── lotw.png                   # LoTW logo
```

### 3. Run the Application
```bash
python3 qsl_card_generator_final.py
```

### 4. First-Time Setup
1. **Station Info Tab**:
   - Fill in your callsign, name, QTH, grid locator
   - Add your equipment (transceiver, power, antenna)
   - Configure image files and logo scales
   - Click **"Save Defaults"** 

2. **You're Ready!** Your configuration is saved permanently

### 5. Generate a QSL Card
1. Open the application (your data loads automatically)
2. Go to **Contact Details** tab
3. Fill in: Their callsign, date, time, band, mode, report
4. Go to **LaTeX Output** tab
5. Click **"Generate PDF"** 
6. Save your PDF
7. Click **"Clear All"** for the next QSO

## Detailed Usage

### Interface Overview

The application has 3 tabs:

#### 1. Station Info Tab
**Station Details:**
- Callsign, Operator Name
- QTH (City, State/Province, Country)
- Grid Locator, CQ Zone, ITU Zone
- Email, QRZ URL

**Equipment:**
- Transceiver model
- Power (Watts)
- Antenna type
- Via Satellite (if applicable)

**Image Files:**
- Background image filename
- Logo 1 (URE) with scale control
- Logo 2 (QRZ.com) with scale control
- Logo 3 (LoTW) with scale control

**Buttons:**
- **Save Defaults** - Saves all station and equipment data
- **Load Defaults** - Reloads saved configuration
- **Clear All** - Clears only contact fields

#### 2. Contact Details Tab
- VIA (QSL bureau or manager)
- TO STATION (their callsign)
- Their callsign, date, time, band, mode, report
- QTH type (Home/Portable)
- QSL type (QSO/SWL report)
- QSL request (PSE/TNX)

#### 3. LaTeX Output Tab
- **Generate LaTeX** - Creates LaTeX code
- **Generate PDF** - Creates PDF directly
- **Save LaTeX** - Exports .tex file
- **Copy to Clipboard** - Copies code
- Code preview area

### Logo Scale Guide

Logo scales are decimal values representing the width relative to text width:

**Default Values:**
```
Logo 1 (URE):   0.07  →  Small, detailed logo
Logo 2 (QRZ):   0.2   →  Large, prominent logo
Logo 3 (LoTW):  0.1   →  Medium-sized logo
```

**Examples:**
```
Bigger logos:     0.10, 0.25, 0.15
Smaller logos:    0.05, 0.15, 0.08
Balanced logos:   0.1,  0.1,  0.1
```

**Tips:**
- Leave empty to use defaults
- Use period (not comma): 0.07 ✓ not 0,07 ✗
- Test with sample data
- Adjust and save new defaults

## Configuration

### Settings File Location
**Linux/macOS:** `~/.qsl_generator_settings.json`  
**Windows:** `C:\Users\YourUsername\.qsl_generator_settings.json`

### Saved Settings Include:
- All station information
- Equipment configuration
- Image filenames
- Logo scales
- Automatically loaded on startup

### Settings File Format
```json
{
  "callsign": "EA7HQL",
  "operator_name": "Your Name",
  "transceiver": "Yaesu FT-991A",
  "logo1_scale": "0.07",
  ...
}
```

### Changing Equipment
```
1. Go to Station Info tab
2. Update transceiver/antenna/power
3. Click "Save Defaults"
4. Done - all future cards use new equipment
```

## Customization

### Custom Background Image
1. Replace `foto_antenas.jpg` with your image
2. Or change filename in Station Info tab
3. Recommended size: 14cm × 9cm at 300 DPI

### Custom Logos
1. Replace logo files with your images
2. Adjust scales as needed
3. Supported formats: PNG, JPG

### LaTeX Code Customization
1. Generate LaTeX code
2. Save to .tex file
3. Edit with any text editor
4. Compile with `pdflatex yourfile.tex`

## Troubleshooting

### "tkinter not found"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS - reinstall Python from python.org
```

### "pdflatex not found"
- Install LaTeX as shown in Requirements section
- Verify installation: `pdflatex --version`
- Restart terminal after installation

### "Image file not found"
- Ensure image files are in same directory as script
- Check filenames match exactly (case-sensitive on Linux/Mac)
- Verify file permissions

### PDF Generation Fails
1. Check LaTeX installation: `pdflatex --version`
2. Verify all image files exist
3. Review error messages for missing packages
4. Try generating LaTeX only, then compile manually

### Settings Not Loading
- Check file permissions on settings file
- Delete `~/.qsl_generator_settings.json` to reset
- Fill in data and "Save Defaults" again

### Empty Fields After Opening
- Click "Load Defaults" button
- Or fill in data and "Save Defaults"

## Recommended Directory Structure

```
qsl_cards/
├── qsl_card_generator_final.py
├── foto_antenas.jpg
├── logo_ure_negro.png
├── qrz_com.png
├── lotw.png
└── generated/
    ├── 2024-11-28_EA7XXX.pdf
    ├── 2024-11-28_EA7ZZZ.pdf
    └── ...
```

## Data Privacy

- All data stored locally only
- Settings file on your computer
- No internet connection required (except for optional updates)
- No telemetry or tracking

## Contributing

Contributions welcome! Areas for improvement:
- Additional card templates
- ADIF file import
- Database integration for logging
- Batch processing
- Multi-language support

## License

Based on QSL Card design by Ian Renton M0TRT (Public Domain), which was based on an example by Fabian Kurz, DJ5CW.

Generator application provided as-is for amateur radio use.

## Technical Details

### Generated LaTeX
- Uses standard LaTeX packages
- 14cm × 9cm card size
- Professional typography
- High-quality output at 300+ DPI

### Python Dependencies
- tkinter (GUI)
- json (settings)
- subprocess (PDF generation)
- tempfile (temporary files)
- Standard library only - no pip packages needed

### Cross-Platform
- Linux (tested on Ubuntu, Debian, Fedora)
- macOS (tested on 10.14+)
- Windows (tested on Windows 10, 11)

## Version History

- **v1.0** - Current version


## Learning Resources

### LaTeX Basics
- [LaTeX Project](https://www.latex-project.org/)
- [Overleaf Documentation](https://www.overleaf.com/learn)

### QSL Card Design
- [ARRL QSL Information](http://www.arrl.org/qsl)
- Amateur radio club resources
- QSL card design guides




