import os

def bersihkan_layar():
  """Membersihkan layar terminal sesuai dengan OS (Windows/Linux/Mac)."""
  os.system('cls' if os.name == 'nt' else 'clear')

def tampilkan_logo():
  """Menampilkan logo ASCII art pada header."""
  logo = """
=============================================
 ╦ ╦┌─┐┌┐   ╔═╗┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
 ║║║├┤ ├┴┐  ╚═╗│  ├┬┘├─┤├─┘├┤ ├┬┘
 ╚╩╝└─┘└─┘  ╚═╝└─┘┴└─┴ ┴┴  └─┘┴└─
        DATA REKAP GENERATOR
=============================================
"""
  print(logo, end="")
