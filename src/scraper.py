from bs4 import BeautifulSoup
import requests


def ambil_data_web(url):
  headers = {
      'User-Agent': (
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
          ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
      )
  }

  print(f'\nMenghubungkan ke: {url} ...')
  try:
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f'[ERROR] Gagal mengakses web: {e}')
    return None

  soup = BeautifulSoup(response.text, 'html.parser')
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
    for p in soup.find_all(['p', 'h1', 'h2', 'h3']):
      teks = p.text.strip()
      if teks:
        data_kurs.append([teks])

  if not data_kurs:
    print(
        '[WARNING] Tidak ada data terstruktur yang berhasil ditemukan di'
        ' halaman tersebut.'
    )
    return None

  return data_kurs
