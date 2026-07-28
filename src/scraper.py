# File: src/scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
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
    # PERUBAHAN: Menentukan lokasi ChromeDriver secara manual untuk Raspberry Pi
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(url)
    
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
