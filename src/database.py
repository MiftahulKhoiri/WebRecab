csv
import os


class DatabaseFile:

  def __init__(self, folder_name='dataweb'):
    self.folder_name = folder_name
    if not os.path.exists(self.folder_name):
      os.makedirs(self.folder_name)

  def simpan_csv(self, nama_file, data):
    path_file = os.path.join(self.folder_name, nama_file)
    try:
      with open(path_file, mode='w', newline='', encoding='utf-8') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerows(data)
      print(f'[SUKSES] Data berhasil disimpan ke: {path_file}')
      return True
    except Exception as e:
      print(f'[ERROR] Gagal menyimpan file CSV: {e}')
      return False

  def daftar_file(self):
    if not os.path.exists(self.folder_name):
      return []
    return [
        f
        for f in os.listdir(self.folder_name)
        if f.endswith('.csv') or f.endswith('.txt')
    ]

  def baca_file(self, nama_file):
    path_file = os.path.join(self.folder_name, nama_file)
    if not os.path.exists(path_file):
      print(f'[ERROR] File {nama_file} tidak ditemukan.')
      return

    print(f'\n--- ISI FILE: {nama_file} ---')
    try:
      with open(path_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for baris in reader:
          print(', '.join(baris))
    except Exception as e:
      print(f'[ERROR] Gagal membaca file: {e}')
    print('-' * 30)

  def hapus_file(self, nama_file):
    path_file = os.path.join(self.folder_name, nama_file)
    if not os.path.exists(path_file):
      print(f'[ERROR] File {nama_file} tidak ditemukan.')
      return False

    try:
      os.remove(path_file)
      print(f'[SUKSES] File {nama_file} berhasil dihapus.')
      return True
    except Exception as e:
      print(f'[ERROR] Gagal menghapus file: {e}')
      return False
