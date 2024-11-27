import shutil
import os
import customtkinter
from screeninfo import get_monitors


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Obter informações sobre os monitores conectados
monitors = get_monitors()

# Se houver múltiplos monitores, escolher o monitor principal ou um específico
monitor = monitors[0]  # Seleciona o monitor primário (primeiro monitor na lista)

screen_width = monitor.width
screen_height = monitor.height

# Definir largura e altura da janela
largura = monitor.width
altura = monitor.height

# Calcula a posição para centralizar a janela no monitor selecionado
x = (screen_width // 2) - (largura // 2)
y = (screen_height // 2) - (altura // 2)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f'{largura}x{altura}+{x}+{y}')

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Definig the frames
        self.lista_de_frames = [
            customtkinter.CTkFrame(self),
            customtkinter.CTkFrame(self),
            customtkinter.CTkFrame(self),
            customtkinter.CTkFrame(self),
        ]

        self.frame_atual = 0

        # Função para esconder todos os frames
        def hide_all_frames():
            for frame in self.lista_de_frames:
                frame.pack_forget()

        # Função para exibir o próximo frame
        def show_next_frame():
            hide_all_frames()  # Esconde todos os frames
            self.frame_atual = (self.frame_atual + 1) % len(self.lista_de_frames)  # Avança para o próximo frame (circular)
            self.lista_de_frames[self.frame_atual].pack(fill="both", expand=True)  # Exibe o próximo frame
            if self.frame_atual <= 2:
                forward_button = customtkinter.CTkButton(self.lista_de_frames[self.frame_atual], text="Next page", command=show_next_frame)# Cria o botão "Next Page" para o novo frame
            else:
                forward_button = customtkinter.CTkButton(self.lista_de_frames[self.frame_atual], text="Processar arquivo", command=close_window)# Cria o botão "Next Page" para o novo frame
            forward_button.pack(pady=20)


        def close_window():
            self.destroy()  # This closes the window

        # Função para desenhar as barrinhas no topo (cabeçalho)
        def draw_header(frame):
            canvas = customtkinter.CTkCanvas(frame, width=screen_width, height=75)
            canvas.pack()
            canvas.create_rectangle(0, 0, screen_width, 25, fill="#e4ebf1")  # Retângulo azul
            canvas.create_rectangle(0, 25, screen_width, 50, fill="#11115c")  # Retângulo vermelho
            canvas.create_rectangle(0, 50, screen_width, 75, fill="#95a6ba")  # Retângulo preto


        # Show the first frame initially
        self.lista_de_frames[0].pack(fill="both", expand=True)

        # --- Frame 1: Home Page ---
        draw_header(self.lista_de_frames[0])  # Desenha o cabeçalho no primeiro frame
        label_1 = customtkinter.CTkLabel(self.lista_de_frames[0], text="Home Page", font=("Arial", 20))
        label_1.pack(pady=20)

        # --- Frame 2: Identificação do cliente ---
        draw_header(self.lista_de_frames[1])  # Desenha o cabeçalho no segundo frame
        label_2 = customtkinter.CTkLabel(self.lista_de_frames[1], text="Digitar CPF", font=("Arial", 20))
        label_2.pack(pady=20)

        # --- Frame 3: Selecionar arquivo ---
        draw_header(self.lista_de_frames[2])  # Desenha o cabeçalho no terceiro frame
        label_3 = customtkinter.CTkLabel(self.lista_de_frames[2], text="Anexar PDF", font=("Arial", 20))
        label_3.pack(pady=20)

        # --- Frame 4: Processar arquivo ---
        draw_header(self.lista_de_frames[3])  # Desenha o cabeçalho no quarto frame
        label_4 = customtkinter.CTkLabel(self.lista_de_frames[3], text="Processar arquivo", font=("Arial", 20))
        label_4.pack(pady=20)

        # Cria o botão "Next Page" para o primeiro frame
        forward_button = customtkinter.CTkButton(self.lista_de_frames[self.frame_atual], text="Next page", command=show_next_frame)
        forward_button.pack(pady=20)

if __name__ == "__main__":
    app = App()
    app.mainloop()
