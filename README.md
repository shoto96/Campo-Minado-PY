# 💣 Campo Minado

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Badge" />
  <img src="https://img.shields.io/badge/GUI-Tkinter-FFD43B?style=for-the-badge&logo=python&logoColor=3776AB" alt="Tkinter Badge" />
  <img src="https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge" alt="License Badge" />
  <img src="https://img.shields.io/badge/Plataforma-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge" alt="Platform Badge" />
</p>

<p align="center">
  Um jogo de Campo Minado clássico com interface gráfica moderna construído em <b>Python</b> e <b>Tkinter</b>.
</p>

---

## 🚀 Funcionalidades

* 🛡️ **Primeiro Clique Seguro:** Garante que você nunca perderá na primeira jogada.
* ⏱️ **Cronômetro & Contador:** Exibição em tempo real do tempo decorrido e das minas restantes.
* 🎚️ **Níveis de Dificuldade:**
  * **Fácil:** Grid `9x9` | 10 Minas
  * **Médio:** Grid `16x16` | 40 Minas
  * **Difícil:** Grid `16x30` | 99 Minas
* 🌊 **Abertura em Cascata:** Revela automaticamente grandes áreas vazias limpas.
* ⚡ **Chording (Clique Duplo/Meio):** Revela rapidamente blocos vizinhos se as bandeiras necessárias já foram marcadas.

---

## 🎮 Controles

| Ação | Comando |
| :--- | :--- |
| **Revelar Bloco** | `Clique Esquerdo` |
| **Marcar/Desmarcar Bandeira** | `Clique Direito` 🚩 |
| **Revelação Rápida (Chord)** | `Clique do Scroll` *(Botão do Meio)* |

---

## 📋 Pré-requisitos

* **Python 3.x** instalado no sistema.
* **Tkinter** (já incluído por padrão no instalador do Python para Windows e macOS).

> **Nota para usuários Linux (Ubuntu/Debian):**
> Caso o Tkinter não esteja instalado, execute no terminal:
> ```bash
> sudo apt-get install python3-tk
> ```

---

## 🏃 Como Executar

1. Extraia o conteúdo deste repositório/arquivo `.zip`.
2. Abra o terminal ou prompt de comando na pasta do projeto.
3. Execute o script principal:

```bash
python campo_minado.py
