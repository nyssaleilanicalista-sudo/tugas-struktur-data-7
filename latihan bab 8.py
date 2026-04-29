# ============================================================
# LATIHAN BAB 8 - STRUKTUR DATA (QUEUE)
# ============================================================

# ── Implementasi Queue sederhana ──────────────────────────────
class Queue:
    def __init__(self):
        self._data = []

    def enqueue(self, item):
        self._data.append(item)          # O(1) amortised

    def dequeue(self):
        if self.isEmpty():
            raise IndexError("dequeue from empty queue")
        return self._data.pop(0)         # O(n)

    def peek(self):
        if self.isEmpty():
            raise IndexError("peek from empty queue")
        return self._data[0]

    def isEmpty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return "Queue(" + str(self._data) + ")"


# ── Implementasi Array sederhana ──────────────────────────────
class Array:
    def __init__(self, size):
        self._data = [None] * size

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __len__(self):
        return len(self._data)


# ============================================================
# SOAL 1 – Kompleksitas Waktu TicketCounterSimulation
# ============================================================
print("=" * 60)
print("SOAL 1 – KOMPLEKSITAS WAKTU")
print("=" * 60)

kompleksitas = """
Metode / Operasi                      | Worst-Case
--------------------------------------|------------
__init__(numAgents, numMinutes, ...)  | O(n)  -- mengisi Array numAgents agen
run()                                 | O(m*n) -- m menit × n agen per menit
  _handleArrival(curTime)             | O(1)  -- satu enqueue
  _handleBeginService(curTime)        | O(n)  -- iterasi semua agen
  _handleEndService(curTime)          | O(n)  -- iterasi semua agen
printResults()                        | O(1)  -- hanya aritmatika & print

Catatan:
  m = numMinutes,  n = numAgents
  Queue.enqueue  → O(1) amortised
  Queue.dequeue  → O(n) (list.pop(0))
"""
print(kompleksitas)


# ============================================================
# SOAL 2 – Eksekusi Manual Queue (hanya enqueue)
# ============================================================
print("=" * 60)
print("SOAL 2 – EKSEKUSI MANUAL (enqueue saja)")
print("=" * 60)

values = Queue()
for i in range(16):
    if i % 3 == 0:
        values.enqueue(i)

print("Nilai yang di-enqueue (i % 3 == 0):", [i for i in range(16) if i % 3 == 0])
print("Isi queue akhir:", values)
print()


# ============================================================
# SOAL 3 – Eksekusi Manual Queue (enqueue + dequeue)
# ============================================================
print("=" * 60)
print("SOAL 3 – EKSEKUSI MANUAL (enqueue + dequeue)")
print("=" * 60)

values = Queue()
trace = []
for i in range(16):
    if i % 3 == 0:
        values.enqueue(i)
        trace.append(f"i={i:2d} → enqueue({i})  | queue={list(values._data)}")
    elif i % 4 == 0:
        if not values.isEmpty():
            removed = values.dequeue()
            trace.append(f"i={i:2d} → dequeue()={removed} | queue={list(values._data)}")
        else:
            trace.append(f"i={i:2d} → dequeue() SKIP (kosong)")

for line in trace:
    print(line)
print("\nIsi queue akhir:", values)
print()


# ============================================================
# SOAL 4 – Implementasi Metode yang Tersisa
# ============================================================
print("=" * 60)
print("SOAL 4 – IMPLEMENTASI TicketCounterSimulation")
print("=" * 60)

import random

class TicketAgent:
    _idCounter = 0

    def __init__(self, agentId):
        self._agentId   = agentId
        self._passenger = None
        self._stopTime  = 0

    def isFree(self):
        return self._passenger is None

    def isFinished(self, curTime):
        return self._passenger is not None and curTime >= self._stopTime

    def startService(self, passenger, stopTime):
        self._passenger = passenger
        self._stopTime  = stopTime

    def stopService(self):
        passenger = self._passenger
        self._passenger = None
        return passenger

    def __str__(self):
        return f"Agent({self._agentId})"


class Passenger:
    def __init__(self, passId, arrivalTime):
        self._passId      = passId
        self._arrivalTime = arrivalTime

    def timeArrived(self):
        return self._arrivalTime

    def __str__(self):
        return f"Passenger({self._passId})"


class TicketCounterSimulation:
    def __init__(self, numAgents, numMinutes, betweenTime, serviceTime):
        self._arriveProb    = 1.0 / betweenTime
        self._serviceTime   = serviceTime
        self._numMinutes    = numMinutes

        self._passengerQ    = Queue()
        self._theAgents     = Array(numAgents)
        for i in range(numAgents):
            self._theAgents[i] = TicketAgent(i + 1)

        self._totalWaitTime = 0
        self._numPassengers = 0

    def run(self):
        for curTime in range(self._numMinutes + 1):
            self._handleArrival(curTime)
            self._handleBeginService(curTime)
            self._handleEndService(curTime)

    def printResults(self):
        numServed = self._numPassengers - len(self._passengerQ)
        if numServed == 0:
            avgWait = 0.0
        else:
            avgWait = float(self._totalWaitTime) / numServed
        print()
        print(f"  Jumlah penumpang dilayani        = {numServed}")
        print(f"  Jumlah penumpang tersisa di antrean = {len(self._passengerQ)}")
        print(f"  Rata-rata waktu tunggu           = {avgWait:.2f} menit")

    # Rule #1 – kedatangan penumpang
    def _handleArrival(self, curTime):
        if random.random() <= self._arriveProb:
            self._numPassengers += 1
            passenger = Passenger(self._numPassengers, curTime)
            self._passengerQ.enqueue(passenger)

    # Rule #2 – mulai pelayanan
    def _handleBeginService(self, curTime):
        for i in range(len(self._theAgents)):
            agent = self._theAgents[i]
            if agent.isFree() and not self._passengerQ.isEmpty():
                passenger = self._passengerQ.dequeue()
                waitTime  = curTime - passenger.timeArrived()
                self._totalWaitTime += waitTime
                agent.startService(passenger, curTime + self._serviceTime)

    # Rule #3 – selesai pelayanan
    def _handleEndService(self, curTime):
        for i in range(len(self._theAgents)):
            agent = self._theAgents[i]
            if agent.isFinished(curTime):
                agent.stopService()


print("Menjalankan simulasi (2 agen, 25 menit, antara=2, servis=3)...")
random.seed(42)
sim = TicketCounterSimulation(numAgents=2, numMinutes=25,
                               betweenTime=2, serviceTime=3)
sim.run()
sim.printResults()
print()


# ============================================================
# SOAL 5 – Modifikasi ke Satuan Detik + Tabel Eksperimen
# ============================================================
print("=" * 60)
print("SOAL 5 – SIMULASI DALAM DETIK + TABEL HASIL")
print("=" * 60)

class TicketCounterSimulationSeconds(TicketCounterSimulation):
    """Sama persis, hanya label satuan diganti 'detik'."""
    def printResults(self):
        numServed = self._numPassengers - len(self._passengerQ)
        if numServed == 0:
            avgWait = 0.0
        else:
            avgWait = float(self._totalWaitTime) / numServed
        return numServed, len(self._passengerQ), round(avgWait, 2)


experiments = [
    # (numSeconds, numAgents, serviceTime, betweenTime)
    (100,   2, 3, 2),
    (500,   2, 3, 2),
    (1000,  2, 3, 2),
    (5000,  2, 3, 2),
    (10000, 2, 3, 2),
    (100,   2, 4, 2),
    (500,   2, 4, 2),
    (1000,  2, 4, 2),
    (5000,  2, 4, 2),
    (10000, 2, 4, 2),
    (100,   3, 4, 2),
    (500,   3, 4, 2),
    (1000,  3, 4, 2),
    (5000,  3, 4, 2),
    (10000, 3, 4, 2),
]

header = (f"{'Detik':>7} {'Agen':>5} {'Servis':>7} {'Antara':>7} "
          f"{'Avg Wait':>10} {'Served':>8} {'Remaining':>10}")
print(header)
print("-" * len(header))

random.seed(0)
for (sec, agents, svc, btw) in experiments:
    sim = TicketCounterSimulationSeconds(
        numAgents=agents, numMinutes=sec,
        betweenTime=btw, serviceTime=svc)
    sim.run()
    served, remaining, avg = sim.printResults()
    print(f"{sec:>7} {agents:>5} {svc:>7} {btw:>7} "
          f"{avg:>10.2f} {served:>8} {remaining:>10}")
print()


# ============================================================
# SOAL 6 – Fungsi Membalik Urutan Queue
# ============================================================
print("=" * 60)
print("SOAL 6 – FUNGSI REVERSE QUEUE")
print("=" * 60)

def reverseQueue(q):
    """
    Membalik urutan item dalam queue.
    Hanya menggunakan operasi Queue ADT + satu stack (list Python).
    """
    stack = []
    # Keluarkan semua item dari queue ke stack
    while not q.isEmpty():
        stack.append(q.dequeue())
    # Masukkan kembali dari stack ke queue (urutan terbalik)
    while stack:
        q.enqueue(stack.pop())


# Uji coba
q = Queue()
for v in [10, 20, 30, 40, 50]:
    q.enqueue(v)

print("Queue sebelum reverse:", q)
reverseQueue(q)
print("Queue sesudah  reverse:", q)

# Verifikasi isi
hasil = []
while not q.isEmpty():
    hasil.append(q.dequeue())
print("Urutan akhir           :", hasil)
print()
print("Selesai – semua soal dikerjakan.")