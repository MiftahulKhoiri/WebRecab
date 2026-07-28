import os

def bersihkan_layar():
  """Membersihkan layar terminal sesuai dengan OS (Windows/Linux/Mac)."""
  os.system('cls' if os.name == 'nt' else 'clear')

def tampilkan_logo():
  """Menampilkan logo ASCII art berwarna pada header."""
  # ANSI Escape Codes untuk pewarnaan terminal
  C = '\033[96m'  # Cyan
  G = '\033[92m'  # Green
  Y = '\033[93m'  # Yellow
  R = '\033[0m'   # Reset format/warna
  B = '\033[1m'   # Teks tebal (Bold)
  
  logo = f"""
{C}╔═══════════════════════════════════════════════════╗{R}
{G}{B}   ╦ ╦┌─┐┌┐   ╔═╗┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐ {R}
{G}{B}   ║║║├┤ ├┴┐  ╚═╗│  ├┬┘├─┤├─┘├┤ ├┬┘ {R}
{G}{B}   ╚╩╝└─┘└─┘  ╚═╝└─┘┴└─┴ ┴┴  └─┘┴└─ {R}
{Y}{B}           DATA REKAP GENERATOR             {R}
{C}╚═══════════════════════════════════════════════════╝{R}
"""
  print(logo, end="")
