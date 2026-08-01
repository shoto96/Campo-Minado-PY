import time
import random
import tkinter as tk
from tkinter import ttk, messagebox


class CampoMinado:

    def __init__(self, root):
        self.root = root
        self.root.title("Campo Minado Pro")
        self.root.configure(bg="#0f172a")  # Dark Slate Background
        self.root.resizable(False, False)

        # Configurações de Dificuldade (linhas, colunas, minas)
        self.dificuldades = {
            "Fácil": (9, 9, 10),
            "Médio": (16, 16, 40),
            "Difícil": (16, 30, 99),
        }
        self.nivel_atual = "Fácil"

        # Variáveis do estado do jogo
        self.botoes = {}
        self.minas = set()
        self.revelados = set()
        self.bandeiras = set()

        self.primeiro_clique = True
        self.tempo_inicio = None
        self.tempo_rodando = False

        self.criar_interface()
        self.novo_jogo()

    def criar_interface(self):
        # Painel Superior (Controles e Métricas)
        self.frame_topo = tk.Frame(self.root, bg="#1e293b", padx=15, pady=10)
        self.frame_topo.pack(fill=tk.X)

        # Contador de Minas
        self.lbl_minas = tk.Label(
            self.frame_topo,
            text="💣 010",
            font=("Consolas", 14, "bold"),
            bg="#0f172a",
            fg="#ef4444",
            padx=8,
            pady=3,
        )
        self.lbl_minas.pack(side=tk.LEFT)

        # Seletor de Dificuldade
        self.combo_diff = ttk.Combobox(
            self.frame_topo,
            values=list(self.dificuldades.keys()),
            state="readonly",
            width=8,
            font=("Arial", 10, "bold"),
        )
        self.combo_diff.set(self.nivel_atual)
        self.combo_diff.bind("<<ComboboxSelected>>", self.mudar_dificuldade)
        self.combo_diff.pack(side=tk.LEFT, padx=15)

        # Botão de Reiniciar (Emoji)
        self.btn_reset = tk.Button(
            self.frame_topo,
            text="🙂",
            font=("Segoe UI Emoji", 14),
            bg="#334155",
            fg="#ffffff",
            activebackground="#475569",
            relief=tk.FLAT,
            bd=0,
            command=self.novo_jogo,
            width=3,
        )
        self.btn_reset.pack(side=tk.LEFT)

        # Cronômetro
        self.lbl_tempo = tk.Label(
            self.frame_topo,
            text="⏱️ 000",
            font=("Consolas", 14, "bold"),
            bg="#0f172a",
            fg="#38bdf8",
            padx=8,
            pady=3,
        )
        self.lbl_tempo.pack(side=tk.RIGHT)

        # Frame do Tabuleiro
        self.frame_tabuleiro = tk.Frame(
            self.root, bg="#0f172a", padx=10, pady=10
        )
        self.frame_tabuleiro.pack()

    def mudar_dificuldade(self, event=None):
        self.nivel_atual = self.combo_diff.get()
        self.novo_jogo()

    def novo_jogo(self):
        self.linhas, self.colunas, self.qtd_minas = self.dificuldades[
            self.nivel_atual
        ]

        # Reset dos estados
        self.primeiro_clique = True
        self.tempo_rodando = False
        self.btn_reset.config(text="🙂")
        self.lbl_tempo.config(text="⏱️ 000")
        self.atualizar_contador_bandeiras()

        # Limpeza do Tabuleiro
        for widget in self.frame_tabuleiro.winfo_children():
            widget.destroy()

        self.botoes.clear()
        self.minas.clear()
        self.revelados.clear()
        self.bandeiras.clear()

        # Construção da Grade
        for r in range(self.linhas):
            for c in range(self.colunas):
                btn = tk.Button(
                    self.frame_tabuleiro,
                    width=2,
                    height=1,
                    font=("Arial", 11, "bold"),
                    bg="#334155",
                    fg="#f8fafc",
                    activebackground="#475569",
                    relief=tk.RAISED,
                    bd=2,
                )
                btn.grid(row=r, column=c, padx=1, pady=1)

                # Eventos do Mouse
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.clicar_esq(r, c))
                btn.bind(
                    "<Button-3>", lambda e, r=r, c=c: self.clicar_dir(r, c)
                )
                btn.bind(
                    "<Button-2>", lambda e, r=r, c=c: self.clicar_meio(r, c)
                )

                self.botoes[(r, c)] = btn

        # Centralizar Janela
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def gerar_minas(self, r_inicial, c_inicial):
        """Garante que o primeiro clique NUNCA seja uma mina."""
        posicoes_possiveis = [
            (r, c)
            for r in range(self.linhas)
            for c in range(self.colunas)
            if (r, c) != (r_inicial, c_inicial)
        ]
        self.minas = set(random.sample(posicoes_possiveis, self.qtd_minas))

    def iniciar_cronometro(self):
        self.tempo_inicio = time.time()
        self.tempo_rodando = True
        self.atualizar_cronometro()

    def atualizar_cronometro(self):
        if self.tempo_rodando:
            passados = int(time.time() - self.tempo_inicio)
            if passados <= 999:
                self.lbl_tempo.config(text=f"⏱️ {passados:03d}")
                self.root.after(1000, self.atualizar_cronometro)

    def atualizar_contador_bandeiras(self):
        restantes = self.qtd_minas - len(self.bandeiras)
        self.lbl_minas.config(text=f"💣 {max(0, restantes):03d}")

    def obter_vizinhos(self, r, c):
        vizinhos = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.linhas and 0 <= nc < self.colunas:
                    vizinhos.append((nr, nc))
        return vizinhos

    def contar_minas_vizinhas(self, r, c):
        return sum(1 for nr, nc in self.obter_vizinhos(r, c) if (nr, nc) in self.minas)

    def clicar_esq(self, r, c):
        if (r, c) in self.bandeiras or (r, c) in self.revelados:
            return

        # Primeiro clique garante segurança e inicia o tempo
        if self.primeiro_clique:
            self.gerar_minas(r, c)
            self.primeiro_clique = False
            self.iniciar_cronometro()

        # Clique numa Mina
        if (r, c) in self.minas:
            self.derrota(r, c)
            return

        # Revela a célula
        self.revelar_celula(r, c)

        # Checa Vitória
        if len(self.revelados) == (self.linhas * self.colunas) - self.qtd_minas:
            self.vitoria()

    def revelar_celula(self, r, c):
        if (r, c) in self.revelados or (r, c) in self.bandeiras:
            return

        self.revelados.add((r, c))
        btn = self.botoes[(r, c)]
        btn.config(relief=tk.SUNKEN, bg="#0f172a", state="disabled")

        qtd = self.contar_minas_vizinhas(r, c)
        if qtd > 0:
            cores = {
                1: "#38bdf8",  # Azul claro
                2: "#4ade80",  # Verde
                3: "#f87171",  # Vermelho
                4: "#c084fc",  # Roxo
                5: "#fb923c",  # Laranja
                6: "#2dd4bf",  # Ciano
                7: "#f43f5e",  # Rosa
                8: "#e2e8f0",  # Branco
            }
            btn.config(
                text=str(qtd),
                disabledforeground=cores.get(qtd, "#ffffff"),
            )
        else:
            for nr, nc in self.obter_vizinhos(r, c):
                self.revelar_celula(nr, nc)

    def clicar_dir(self, r, c):
        if (r, c) in self.revelados:
            return

        btn = self.botoes[(r, c)]
        if (r, c) in self.bandeiras:
            self.bandeiras.remove((r, c))
            btn.config(text="", bg="#334155")
        else:
            if len(self.bandeiras) < self.qtd_minas:
                self.bandeiras.add((r, c))
                btn.config(text="🚩", fg="#ef4444")

        self.atualizar_contador_bandeiras()

    def clicar_meio(self, r, c):
        """Revela vizinhos rapidamente se o número de bandeiras bater com a contagem da célula."""
        if (r, c) not in self.revelados:
            return

        vizinhos = self.obter_vizinhos(r, c)
        bandeiras_vizinhas = sum(1 for nr, nc in vizinhos if (nr, nc) in self.bandeiras)

        if bandeiras_vizinhas == self.contar_minas_vizinhas(r, c):
            for nr, nc in vizinhos:
                if (nr, nc) not in self.bandeiras and (
                    nr,
                    nc,
                ) not in self.revelados:
                    self.clicar_esq(nr, nc)

    def derrota(self, r_bomba, c_bomba):
        self.tempo_rodando = False
        self.btn_reset.config(text="😵")

        # Revela todas as bombas
        for r, c in self.minas:
            btn = self.botoes[(r, c)]
            if (r, c) == (r_bomba, c_bomba):
                btn.config(text="💥", bg="#ef4444")
            else:
                btn.config(text="💣", bg="#94a3b8")

        # Aponta bandeiras erradas
        for r, c in self.bandeiras:
            if (r, c) not in self.minas:
                self.botoes[(r, c)].config(text="❌", bg="#fca5a5")

        messagebox.showerror("Fim de Jogo", "Você acertou uma mina! 💣")

    def vitoria(self):
        self.tempo_rodando = False
        self.btn_reset.config(text="😎")

        # Marca com bandeira as minas restantes
        for r, c in self.minas:
            if (r, c) not in self.bandeiras:
                self.botoes[(r, c)].config(text="🚩", fg="#ef4444")

        self.lbl_minas.config(text="💣 000")
        tempo_total = int(time.time() - self.tempo_inicio)
        messagebox.showinfo(
            "Vitória!", f"Parabéns! Você venceu em {tempo_total} segundos! 🎉"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = CampoMinado(root)
    root.mainloop()
