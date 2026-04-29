# 📦 Latihan Bab 8 – Struktur Data: Queue

Implementasi latihan soal Bab 8 tentang **Queue (Antrian)** menggunakan Python sederhana, mencakup simulasi loket tiket, analisis kompleksitas, dan manipulasi queue.

---

## 📁 Struktur File

```
latihan bab 8.py   # Semua implementasi & jawaban soal 1–6
README.md                       # Dokumentasi proyek ini
```

---

## 🧩 Daftar Soal & Penjelasan

### Soal 1 – Analisis Kompleksitas Waktu

Analisis *worst-case* setiap operasi pada class `TicketCounterSimulation`:

| Metode / Operasi | Kompleksitas |
|---|---|
| `__init__(numAgents, ...)` | O(n) |
| `run()` | O(m × n) |
| `_handleArrival(curTime)` | O(1) |
| `_handleBeginService(curTime)` | O(n) |
| `_handleEndService(curTime)` | O(n) |
| `printResults()` | O(1) |

> `m` = numMinutes, `n` = numAgents

---

### Soal 2 – Eksekusi Manual Queue (enqueue saja)

```python
values = Queue()
for i in range(16):
    if i % 3 == 0:
        values.enqueue(i)
```

**Hasil akhir queue:** `[0, 3, 6, 9, 12, 15]`

Semua bilangan antara 0–15 yang habis dibagi 3 dimasukkan ke queue.

---

### Soal 3 – Eksekusi Manual Queue (enqueue + dequeue)

```python
values = Queue()
for i in range(16):
    if i % 3 == 0:
        values.enqueue(i)
    elif i % 4 == 0:
        values.dequeue()
```

**Trace eksekusi:**

| i | Operasi | Isi Queue |
|---|---|---|
| 0 | enqueue(0) | [0] |
| 3 | enqueue(3) | [0, 3] |
| 4 | dequeue()=0 | [3] |
| 6 | enqueue(6) | [3, 6] |
| 8 | dequeue()=3 | [6] |
| 9 | enqueue(9) | [6, 9] |
| 12 | enqueue(12) | [6, 9, 12] |
| 15 | enqueue(15) | [6, 9, 12, 15] |

**Hasil akhir queue:** `[6, 9, 12, 15]`

> Catatan: `i=4` dan `i=8` memenuhi `i % 4 == 0` tapi **bukan** `i % 3 == 0`, sehingga masuk ke `elif` dan melakukan dequeue.

---

### Soal 4 – Implementasi Metode TicketCounterSimulation

Tiga metode yang diimplementasikan:

#### `_handleArrival(curTime)` — Rule #1
Penumpang baru tiba berdasarkan probabilitas kedatangan (`arriveProb`). Jika random number ≤ `arriveProb`, penumpang baru di-enqueue.

```python
def _handleArrival(self, curTime):
    if random.random() <= self._arriveProb:
        self._numPassengers += 1
        passenger = Passenger(self._numPassengers, curTime)
        self._passengerQ.enqueue(passenger)
```

#### `_handleBeginService(curTime)` — Rule #2
Cari agen yang sedang bebas. Jika ada penumpang di antrian, ambil dan mulai pelayanan. Catat waktu tunggu.

```python
def _handleBeginService(self, curTime):
    for i in range(len(self._theAgents)):
        agent = self._theAgents[i]
        if agent.isFree() and not self._passengerQ.isEmpty():
            passenger = self._passengerQ.dequeue()
            waitTime  = curTime - passenger.timeArrived()
            self._totalWaitTime += waitTime
            agent.startService(passenger, curTime + self._serviceTime)
```

#### `_handleEndService(curTime)` — Rule #3
Cek semua agen. Jika sudah selesai melayani, bebaskan agen tersebut.

```python
def _handleEndService(self, curTime):
    for i in range(len(self._theAgents)):
        agent = self._theAgents[i]
        if agent.isFinished(curTime):
            agent.stopService()
```

**Contoh output** (2 agen, 25 menit, antara=2, servis=3):
```
Jumlah penumpang dilayani           = 13
Jumlah penumpang tersisa di antrian = 1
Rata-rata waktu tunggu              = 1.77 menit
```

---

### Soal 5 – Simulasi dalam Satuan Detik + Tabel Hasil

Modifikasi `TicketCounterSimulation` menggunakan satuan **detik** (bukan menit). Hasil eksperimen:

| Detik | Agen | Servis | Antara | Avg Wait | Served | Remaining |
|------:|-----:|-------:|-------:|---------:|-------:|----------:|
| 100 | 2 | 3 | 2 | 0.59 | 37 | 0 |
| 500 | 2 | 3 | 2 | 16.14 | 249 | 15 |
| 1000 | 2 | 3 | 2 | 10.96 | 493 | 10 |
| 5000 | 2 | 3 | 2 | 16.10 | 2447 | 15 |
| 10000 | 2 | 3 | 2 | 47.40 | 4977 | 35 |
| 100 | 2 | 4 | 2 | 8.00 | 39 | 8 |
| 500 | 2 | 4 | 2 | 67.73 | 200 | 68 |
| 1000 | 2 | 4 | 2 | 88.38 | 400 | 79 |
| 5000 | 2 | 4 | 2 | 438.85 | 2000 | 472 |
| 10000 | 2 | 4 | 2 | 1008.88 | 3999 | 936 |
| 100 | 3 | 4 | 2 | 2.00 | 55 | 0 |
| 500 | 3 | 4 | 2 | 1.03 | 248 | 0 |
| 1000 | 3 | 4 | 2 | 1.82 | 518 | 1 |
| 5000 | 3 | 4 | 2 | 1.38 | 2548 | 0 |
| 10000 | 3 | 4 | 2 | 1.60 | 5082 | 0 |

> **Kesimpulan:** Menambah agen dari 2 → 3 dengan servis=4 menurunkan waktu tunggu rata-rata secara dramatis (dari >1000 menjadi ~1.6 detik pada 10.000 detik simulasi).

---

### Soal 6 – Fungsi Reverse Queue

Membalik urutan item dalam queue **hanya menggunakan operasi Queue ADT** + satu struktur data bantu (stack/list).

**Algoritma:**
1. Keluarkan semua item dari queue → masukkan ke stack
2. Keluarkan semua item dari stack → masukkan kembali ke queue

```python
def reverseQueue(q):
    stack = []
    while not q.isEmpty():
        stack.append(q.dequeue())
    while stack:
        q.enqueue(stack.pop())
```

**Contoh:**
```
Queue sebelum : [10, 20, 30, 40, 50]
Queue sesudah  : [50, 40, 30, 20, 10]
```

**Kompleksitas:**
- Waktu : O(n) — setiap item diproses 2 kali
- Ruang : O(n) — stack menyimpan seluruh isi queue

---

## ▶️ Cara Menjalankan

Pastikan Python 3 sudah terinstall, lalu jalankan:

```bash
python latihan_bab8_struktur_data.py
```

Tidak ada dependensi eksternal — hanya menggunakan modul bawaan Python (`random`).

---

## 🗂️ Konsep yang Digunakan

| Konsep | Keterangan |
|---|---|
| **Queue ADT** | Struktur data FIFO dengan operasi `enqueue`, `dequeue`, `peek`, `isEmpty` |
| **Array** | Wrapper list Python berukuran tetap |
| **Simulasi berbasis waktu** | Event-driven per satuan waktu (menit/detik) |
| **Probabilitas kedatangan** | `arriveProb = 1 / betweenTime` |
| **Stack sebagai pembantu** | Digunakan pada fungsi `reverseQueue` |

---

## 👤 Informasi

> Latihan Bab 8 — Mata Kuliah Struktur Data  
> Implementasi menggunakan **Python 3** tanpa library eksternal
