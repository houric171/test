# IDX Screener — Website (GitHub Pages + GitHub Actions)

Satu website untuk screening saham IDX. Data EOD diperbarui otomatis setiap hari bursa
pukul ±17:35 WIB oleh GitHub Actions. Tidak perlu server, tidak perlu menjalankan Python sendiri.

```
idx-screener/
├── index.html                    ← website (UI + mesin screener, jalan di browser)
├── fetch_data.py                 ← dijalankan GitHub Actions: tarik data Yahoo → data/eod.json
├── tickers.txt                   ← daftar 951 kode emiten
├── data/                         ← eod.json muncul di sini setelah workflow pertama jalan
└── .github/workflows/daily.yml   ← jadwal otomatis Senin–Jumat 17:35 WIB
```

## Setup (±15 menit, sekali saja)

1. **Buat akun GitHub** (kalau belum) di github.com.
2. **Buat repository baru** → klik **New** → nama misalnya `idx-screener` → pilih **Public** → **Create repository**.
   (Public = website bisa dibuka tanpa login & Actions gratis. Kodenya terlihat orang lain, tapi tidak ada data rahasia di sini.)
3. **Upload file**: di halaman repo klik **Add file → Upload files**, lalu drag *isi* folder `idx-screener`
   (index.html, fetch_data.py, tickers.txt, README.md, folder `data`, folder `.github`) → **Commit changes**.
   - Folder `.github` tersembunyi di Windows/Mac. Kalau tidak ikut ter-upload: klik **Add file → Create new file**,
     ketik nama `.github/workflows/daily.yml`, lalu tempel isi file `daily.yml`.
4. **Izinkan Actions menulis ke repo**: **Settings → Actions → General → Workflow permissions** →
   pilih **Read and write permissions** → **Save**.
5. **Jalankan pengambilan data pertama**: tab **Actions** → pilih **Update data EOD IDX** → **Run workflow**.
   Tunggu ±5–10 menit sampai centang hijau. File `data/eod.json` akan muncul di repo.
6. **Aktifkan website**: **Settings → Pages** → *Source*: **Deploy from a branch** → Branch **main**, folder **/ (root)** → **Save**.
   Setelah 1–2 menit website aktif di `https://<username>.github.io/idx-screener/`.

Selesai. Buka link itu dari laptop atau HP. Badge di kiri atas berubah dari **DATA DEMO** menjadi **data EOD**.

## Pemakaian
- Klik screener di kiri → hasil langsung muncul. Ubah parameter → **▶ Jalankan**.
- **+ Kondisi**: buat screener dari gabungan syarat (perubahan harga, Volume÷VMA, Close vs MA, jarak ke High/Low, RSI, nilai transaksi, body candle, harga). Kolom *H-1…H-5* = cek kondisi di hari sebelumnya.
- **+ Spike-Pullback**: buat variasi strategi spike → koreksi volume rendah dengan parameter sendiri.
- **Simpan / Simpan sebagai baru** → masuk ke "Screener saya" (tersimpan di browser tsb).
- **Ekspor/Impor** untuk memindahkan screener ke perangkat lain.
- Klik baris hasil → chart candle 90 hari + volume + garis open spike.

## Perawatan
- **Saham IPO baru**: tambahkan kodenya di `tickers.txt` (edit langsung di GitHub, ikon pensil).
- **Kalau data tidak update**: cek tab **Actions** → buka run yang merah untuk lihat error.
  Biasanya karena Yahoo/yfinance berubah — coba **Run workflow** ulang, atau perbarui versi yfinance.
- GitHub bisa menonaktifkan jadwal otomatis di repo yang lama tidak ada aktivitas. Commit data harian
  seharusnya dihitung sebagai aktivitas, tapi kalau jadwal berhenti, aktifkan lagi dari tab Actions.
