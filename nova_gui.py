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
        frame_1 = customtkinter.CTkFrame(self)
        frame_2 = customtkinter.CTkFrame(self)
        frame_3 = customtkinter.CTkFrame(self)
        frame_4 = customtkinter.CTkFrame(self)

        # Function to hide all frames
        def hide_all_frames():
            frame_1.pack_forget()
            frame_2.pack_forget()
            frame_3.pack_forget()
            frame_4.pack_forget()

        # Function to show frame1
        def show_frame_1():
            hide_all_frames()
            frame_1.pack(fill="both", expand=True)

                # Function to show frame1
        def show_frame_2():
            hide_all_frames()
            frame_2.pack(fill="both", expand=True)

                # Function to show frame1
        def show_frame_3():
            hide_all_frames()
            frame_3.pack(fill="both", expand=True)

        def show_frame_4():
            hide_all_frames()
            frame_4.pack(fill="both", expand=True)

        def close_window():
            self.destroy()  # This closes the window

        # --- Frame 1: Home Page ---
        label_1 = customtkinter.CTkLabel(frame_1, text="Home Page", font=("Arial", 20))
        label_1.pack(pady=20)

        # --- Frame 2: Identificação do cliente ---
        label_2 = customtkinter.CTkLabel(frame_2, text="Digitar CPF", font=("Arial", 20))
        label_2.pack(pady=20)

        # --- Frame 3: Selecionar arquivo ---
        label_3 = customtkinter.CTkLabel(frame_3, text="Anexar PDF", font=("Arial", 20))
        label_3.pack(pady=20)

        # --- Frame 4: Processar arquivo ---
        label_4 = customtkinter.CTkLabel(frame_4, text="Processar arquivo", font=("Arial", 20))
        label_4.pack(pady=20)

        #Pass the frames
        foward_button_1 = customtkinter.CTkButton(frame_1, text="Next page", command=show_frame_2)
        foward_button_1.pack()

        #Pass the frames
        foward_button_2 = customtkinter.CTkButton(frame_2, text="Next page", command=show_frame_3)
        foward_button_2.pack()

        #Pass the frames
        foward_button_3 = customtkinter.CTkButton(frame_3, text="Next page", command=show_frame_4)
        foward_button_3.pack()
        
        #Pass the frames
        foward_button_4 = customtkinter.CTkButton(frame_4, text="Process archive", command=close_window)
        foward_button_4.pack()

        # Show the first frame initially
        show_frame_1()

if __name__ == "__main__":
    app = App()
    app.mainloop()
