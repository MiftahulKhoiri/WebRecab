import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from database import DatabaseFile
from scraper import ambil_data_web
from logo import bersihkan_layar, tampilkan_logo

db = DatabaseFile()


def submenu_lihat_hasil():
  while True:
    bersihkan_layar()
    tampilkan_logo()
    print('          DAFTAR HASIL DATA TERSIMPAN          ')
    print('=' * 45)
    files = db.daftar_file()

    if not files:
      print('[INFO] Belum ada data yang tersimpan.')
      print('=' * 45)
      input('Tekan Enter untuk kembali...')
      break

    for i, file in enumerate(files, 1):
      print(f'{i}. {file}')
    print('=' * 45)
    print('1. Baca')
    print('2. Hapus')
    print('0. Kembali ke menu utama')
    print('=' * 45)

    pilihan = input('Pilih sub-menu (0-2): ').strip()

    if pilihan == '1':
      try:
        idx = int(input('Masukkan nomor file yang ingin dibaca: ')) - 1
        if 0 <= idx < len(files):
          bersihkan_layar()
          db.baca_file(files[idx])
        else:
          print('[ERROR] Nomor file tidak valid.')
      except ValueError:
        print('[ERROR] Masukkan angka yang valid.')
      input('\nTekan Enter untuk melanjutkan...')

    elif pilihan == '2':
      try:
        idx = int(input('Masukkan nomor file yang ingin dihapus: ')) - 1
        if 0 <= idx < len(files):
          konfirmasi = (
              input(f'Yakin ingin menghapus {files[idx]}? (y/n): ')
              .strip()
              .lower()
          )
          if konfirmasi == 'y':
            db.hapus_file(files[idx])
        else:
          print('[ERROR] Nomor file tidak valid.')
      except ValueError:
        print('[ERROR] Masukkan angka yang valid.')
      input('\nTekan Enter untuk melanjutkan...')

    elif pilihan == '0':
      break
    else:
      print('[ERROR] Pilihan tidak valid.')
      input('\nTekan Enter untuk melanjutkan...')


def submenu_simpan_data():
  while True:
    bersihkan_layar()
    tampilkan_logo()
    print('             MENU SIMPAN DATA             ')
    print('=' * 45)
    print('1. Otomatis (Background / Headless)')
    print('2. Manual (Tampil Browser & Tunggu Input)')
    print('3. Lihat hasil')
    print('0. Kembali')
    print('=' * 45)

    pilihan = input('Pilih menu (0-3): ').strip()

    if pilihan in ('1', '2'):
      url = input('Masukkan alamat web: ').strip()
      if not url:
        print('[PERINGATAN] Alamat web tidak boleh kosong!\n')
        input('Tekan Enter untuk melanjutkan...')
        continue

      if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
      
      mode_manual = True if pilihan == '2' else False
      
      print("") # Memberi jarak sebelum log scraper muncul
      data = ambil_data_web(url, mode_manual=mode_manual)
      if data:
        nama_file = 'hasilrekab.csv'
        db.simpan_csv(nama_file, data)
      input('\nTekan Enter untuk melanjutkan...')

    elif pilihan == '3':
      submenu_lihat_hasil()

    elif pilihan == '0':
      break
    else:
      print('[ERROR] Pilihan tidak valid.')
      input('\nTekan Enter untuk melanjutkan...')


def main():
  while True:
    bersihkan_layar()
    tampilkan_logo()
    print('1. Simpan data')
    print('2. Lihat hasil (list data apa saja yg sudah di dapat)')
    print('0. Exit')
    print('=' * 45)

    pilihan = input('Pilih menu (0-2): ').strip()

    if pilihan == '1':
      submenu_simpan_data()
    elif pilihan == '2':
      submenu_lihat_hasil()
    elif pilihan == '0':
      bersihkan_layar()
      print('\nTerima kasih telah menggunakan program ini. Sampai jumpa!\n')
      break
    else:
      print('[ERROR] Pilihan tidak valid.')
      input('\nTekan Enter untuk melanjutkan...')


if __name__ == '__main__':
  main()
