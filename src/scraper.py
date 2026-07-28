# File: src/scraper.py
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Memeriksa pop-up peringatan...")
    try:
      wait = WebDriverWait(driver, 10)
      # Memperluas pencarian tombol (bisa jadi teksnya "Enter", "Agree", dll)
      tombol_umur = wait.until(
          EC.presence_of_element_located((
              By.XPATH, 
              "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'over 18') "
              "or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree') "
              "or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'enter')]"
          ))
      )
      driver.execute_script("arguments[0].click();", tombol_umur)
      print(f"[{datetime.now().strftime('%H:%M:%S')}] Berhasil melewati konfirmasi usia!")
      time.sleep(3)
    except Exception:
      print(f"[{datetime.now().strftime('%H:%M:%S')}] Pop-up usia tidak ditemukan atau sudah dilewati.")

    # Diperlama karena game biasanya membutuhkan waktu loading yang cukup berat
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Menunggu JavaScript merender halaman utama (10 detik)...")
    time.sleep(10) 
    
    # --- LOGIKA BARU UNTUK IFRAME ---
    # Banyak web game memasukkan gamenya di dalam elemen "iframe" (bingkai dalam bingkai)
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
      print(f"[{datetime.now().strftime('%H:%M:%S')}] Ditemukan {len(iframes)} iframe game. Mencoba masuk ke dalam iframe...")
      driver.switch_to.frame(iframes[0])
      time.sleep(5) # Tunggu lagi agar isi iframe termuat penuh
    # --------------------------------
    
    html_render = driver.page_source
    driver.quit()
    
  except Exception as e:
    print(f'[ERROR] Gagal menjalankan Selenium: {e}')
    try:
      driver.quit()
    except:
      pass
    return None

  print(f"[{datetime.now().strftime('%H:%M:%S')}] Mengekstrak data dari halaman...")
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
    for elemen in soup.find_all(['p', 'h1', 'h2', 'h3', 'div', 'span', 'li']):
      teks = elemen.text.strip()
      # Filter: Ambil teks yang punya isi, hindari baris baru ganda
      if teks and len(teks) > 1 and "\n" not in teks:
        data_kurs.append([teks])

  if not data_kurs:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [WARNING] Data teks kosong! Game mungkin menggunakan elemen <canvas>.")
    return None

  waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  data_dengan_waktu = []
  for baris in data_kurs:
    if [waktu_sekarang] + baris not in data_dengan_waktu:
      data_dengan_waktu.append([waktu_sekarang] + baris)

  print(f"[{datetime.now().strftime('%H:%M:%S')}] Berhasil menemukan {len(data_dengan_waktu)} baris teks data.")
  return data_dengan_waktu
