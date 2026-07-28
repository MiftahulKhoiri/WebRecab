# File: src/scraper.py
import time
import io
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import pytesseract


def ambil_data_web(url, mode_manual=False):
  chrome_options = Options()
  
  # Hanya gunakan mode headless jika mode_manual adalah False
  if not mode_manual:
    chrome_options.add_argument("--headless")
    
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--disable-gpu")
  chrome_options.add_argument("--log-level=3")
  # Mengatur ukuran layar virtual agar screenshot tidak terpotong
  chrome_options.add_argument("--window-size=1920,1080")

  print(f"[{datetime.now().strftime('%H:%M:%S')}] Membuka browser virtual...")
  
  try:
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    
    if mode_manual:
      print(f"[{datetime.now().strftime('%H:%M:%S')}] [MODE MANUAL AKTIF] Jendela browser telah dibuka.")
      input(">>> Lakukan interaksi di browser, lalu tekan ENTER di sini untuk melanjutkan proses OCR...")
    else:
      print(f"[{datetime.now().strftime('%H:%M:%S')}] Memeriksa pop-up peringatan...")
      try:
        wait = WebDriverWait(driver, 10)
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

      print(f"[{datetime.now().strftime('%H:%M:%S')}] Menunggu JavaScript & Game merender halaman (10 detik)...")
      time.sleep(10) 
    
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if iframes:
      print(f"[{datetime.now().strftime('%H:%M:%S')}] Masuk ke dalam iframe game...")
      driver.switch_to.frame(iframes[0])
      time.sleep(5) 
    
    # --- LOGIKA BARU OCR (SCREENSHOT) ---
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Mengambil screenshot dari game (Canvas)...")
    screenshot = driver.get_screenshot_as_png()
    driver.quit()
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Memproses gambar menggunakan AI OCR (Membaca teks dari gambar)...")
    image = Image.open(io.BytesIO(screenshot))
    
    # Ekstrak teks dari gambar menggunakan Tesseract OCR
    teks_hasil_ocr = pytesseract.image_to_string(image)
    # -------------------------------------
    
  except Exception as e:
    print(f'[ERROR] Gagal menjalankan operasi Selenium/OCR: {e}')
    try:
      driver.quit()
    except:
      pass
    return None

  print(f"[{datetime.now().strftime('%H:%M:%S')}] Mengekstrak data teks...")
  data_kurs = []
  
  # Memproses hasil teks dari OCR
  if teks_hasil_ocr:
    baris_teks = teks_hasil_ocr.split('\n')
    for teks in baris_teks:
      teks_bersih = teks.strip()
      # Simpan jika teks memiliki isi
      if teks_bersih and len(teks_bersih) > 1:
        data_kurs.append([teks_bersih])

  if not data_kurs:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [WARNING] OCR gagal menemukan teks yang jelas pada layar game.")
    return None

  waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  data_dengan_waktu = []
  for baris in data_kurs:
    if [waktu_sekarang] + baris not in data_dengan_waktu:
      data_dengan_waktu.append([waktu_sekarang] + baris)

  print(f"[{datetime.now().strftime('%H:%M:%S')}] Berhasil merekam {len(data_dengan_waktu)} baris teks data dari gambar.")
  return data_dengan_waktu
