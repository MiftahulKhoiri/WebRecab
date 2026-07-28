# File: src/scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time


def ambil_data_web(url):
  # Pengaturan Selenium untuk berjalan di latar belakang (Headless)
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  
  # Khusus Raspberry Pi/Linux: mematikan notifikasi error GPU yang mengganggu log
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--log-level=3")

  print(f"[{datetime.now().strftime('%H:%M:%S')}] Membuka browser virtual...")
  
  try:
    # Membuka Chrome secara otomatis (Selenium 4 menangani driver secara internal)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    
    # Tunggu 5 detik agar JavaScript di web game selesai merender data
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Menunggu JavaScript merender halaman...")
    time.sleep(5) 
    
    # Mengambil semua HTML yang SUDAH dirender oleh JavaScript
    html_render = driver.page_source
    
    # Menutup browser agar RAM tidak penuh
    driver.quit()
    
  except Exception as e:
    print(f'[ERROR] Gagal menjalankan Selenium: {e}')
    return None

  # Parsing HTML dengan BeautifulSoup
  soup = BeautifulSoup(html_render, 'html.parser')
  data_kurs = []
  
  tabel = soup.find('table')

  if tabel:
    baris = tabel.find_all('tr')
    for row in baris:
      kolom = row.find_all(['td', 'th'])
      data_baris = [k.text.strip() for k in kolom]
      if data_baris:
        data_kurs.append(data_baris)
  else:
    # Tambahan: Mencari tag <div> dan <span> karena web game biasanya menggunakan ini
    for elemen in soup.find_all(['p', 'h1', 'h2', 'h3', 'div', 'span']):
      teks = elemen.text.strip()
      # Filter agar hanya mengambil teks yang tidak kosong dan cukup relevan
      if teks and len(teks) > 0 and "\n" not in teks:
        data_kurs.append([teks])

  if not data_kurs:
    return None

  # Menambahkan stempel waktu (timestamp)
  waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  data_dengan_waktu = []
  for baris in data_kurs:
    # Menghapus duplikasi baris jika ada (opsional untuk web dinamis)
    if [waktu_sekarang] + baris not in data_dengan_waktu:
      data_dengan_waktu.append([waktu_sekarang] + baris)

  return data_dengan_waktu
