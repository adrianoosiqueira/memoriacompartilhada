import multiprocessing
from multiprocessing import shared_memory, Semaphore, Process, Value
import tkinter as tk
from tkinter import ttk
import time
import random
import json

# ---------- Função do PRODUTOR ----------
def produtor(shared_name, semaforo, contador, lock):
    existing_shm = shared_memory.SharedMemory(name=shared_name)
    while True:
        with lock:
            semaforo.acquire()
            data = existing_shm.buf[:contador.value].tobytes().decode().strip()
            pedidos = json.loads(data) if data else []

            novo_pedido = {"id": len(pedidos) + 1, "status": "Em preparo"}
            pedidos.append(novo_pedido)

            serialized = json.dumps(pedidos).ljust(existing_shm.size)
            existing_shm.buf[:len(serialized)] = bytes(serialized, 'utf-8')
            contador.value = len(serialized)
            semaforo.release()
        time.sleep(random.randint(2, 5))

# ---------- Função do CONSUMIDOR ----------
def consumidor(shared_name, semaforo, contador, lock):
    existing_shm = shared_memory.SharedMemory(name=shared_name)
    while True:
        with lock:
            semaforo.acquire()
            data = existing_shm.buf[:contador.value].tobytes().decode().strip()
            pedidos = json.loads(data) if data else []

            pendentes = [p for p in pedidos if p["status"] == "Em preparo"]
            if pendentes:
                pedido = random.choice(pendentes)
                pedido["status"] = "Pronto"
                serialized = json.dumps(pedidos).ljust(existing_shm.size)
                existing_shm.buf[:len(serialized)] = bytes(serialized, 'utf-8')
                contador.value = len(serialized)
            semaforo.release()
        time.sleep(random.randint(4, 8))

# ---------- Interface Gráfica Simples ----------
class PainelPedidos(tk.Tk):
    def __init__(self, shared_name, semaforo, contador, lock):
        super().__init__()
        self.title("Painel de Pedidos")
        self.geometry("500x450")
        self.configure(bg="#f7f7f7")

        self.shared_name = shared_name
        self.semaforo = semaforo
        self.contador = contador
        self.lock = lock

        # Contadores no topo
        frame_top = tk.Frame(self, bg="#f7f7f7")
        frame_top.pack(pady=5)
        self.label_total = tk.Label(frame_top, text="Criados: 0", font=("Arial", 12))
        self.label_total.grid(row=0, column=0, padx=10)
        self.label_prontos = tk.Label(frame_top, text="Prontos: 0", font=("Arial", 12))
        self.label_prontos.grid(row=0, column=1, padx=10)

        # Lista de pedidos com coluna de ID e Status
        self.tree = ttk.Treeview(self, columns=("id", "status"), show="headings", height=15)
        self.tree.heading("id", text="ID do Pedido")
        self.tree.heading("status", text="Status")
        self.tree.column("id", width=100, anchor="center")
        self.tree.column("status", width=200, anchor="center")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.tree.tag_configure("Em preparo", background="khaki")
        self.tree.tag_configure("Pronto", background="palegreen")

        self.after(1000, self.atualizar_lista)

    def atualizar_lista(self):
        existing_shm = shared_memory.SharedMemory(name=self.shared_name)
        self.semaforo.acquire()
        data = existing_shm.buf[:self.contador.value].tobytes().decode().strip()
        self.semaforo.release()

        pedidos = json.loads(data) if data else []

        self.tree.delete(*self.tree.get_children())
        total = len(pedidos)
        prontos = sum(1 for p in pedidos if p["status"] == "Pronto")
        self.label_total.config(text=f"Criados: {total}")
        self.label_prontos.config(text=f"Prontos: {prontos}")

        for p in pedidos:
            self.tree.insert("", "end", values=(p["id"], p["status"]), tags=(p["status"],))

        self.after(1000, self.atualizar_lista)

# ---------- Execução Principal ----------
if __name__ == "__main__":
    tamanho_memoria = 4096
    shm = shared_memory.SharedMemory(create=True, size=tamanho_memoria)
    shm.buf[:] = bytes("".ljust(tamanho_memoria), 'utf-8')

    semaforo = Semaphore(1)
    contador = Value('i', 0)
    lock = multiprocessing.Lock()

    p_prod = Process(target=produtor, args=(shm.name, semaforo, contador, lock))
    p_cons = Process(target=consumidor, args=(shm.name, semaforo, contador, lock))
    p_prod.start()
    p_cons.start()

    app = PainelPedidos(shm.name, semaforo, contador, lock)
    app.mainloop()

    p_prod.terminate()
    p_cons.terminate()
    shm.close()
    shm.unlink()
