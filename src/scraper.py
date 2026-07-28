# File: src/scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time


def ambil_data_web(url):
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--log-level=3")

  print(f"[{datetime.now().strftime('%H:%M:%S')}] Membuka browser virtual...")
  
  try:
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    
    # --- LOGIKA BARU UNTUK MELEWATI POP-UP UMUR ---
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Memeriksa pop-up peringatan...")
    try:
      # Tunggu maksimal 10 detik sampai elemen yang mengandung kata "over 18" muncul
      wait = WebDriverWait(driver, 10)
      tombol_umur = wait.until(
          EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'over 18') or contains(text(), 'Over 18')]"))
      )
      
      # Gunakan JavaScript click untuk menghindari masalah elemen yang tertimpa visual lain
      driver.execute_script("arguments[0].click();", tombol_umur)
      print(f"[{datetime.now().strftime('%H:%M:%S')}] Berhasil melewati konfirmasi usia!")
      
      # Tunggu 3 detik agar halaman utama termuat setelah klik
      time.sleep(3)
    except Exception:
      print(f"[{datetime.now().strftime('%H:%M:%S')}] Pop-up usia tidak ditemukan, melanjutkan proses...")
    # ----------------------------------------------
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Menunggu JavaScript merender halaman...")
    time.sleep(5) 
    
    html_render = driver.page_source
    driver.quit()
    
  except Exception as e:
    print(f'[ERROR] Gagal menjalankan Selenium: {e}')
    return None

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
    for elemen in soup.find_all(['p', 'h1', 'h2', 'h3', 'div', 'span']):
      teks = elemen.text.strip()
      if teks and len(teks) > 0 and "\n" not in teks:
        data_kurs.append([teks])

  if not data_kurs:
    return None

  waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  data_dengan_waktu = []
  for baris in data_kurs:
    if [waktu_sekarang] + baris not in data_dengan_waktu:
      data_dengan_waktu.append([waktu_sekarang] + baris)

  return data_dengan_waktu
