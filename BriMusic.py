import tkinter as tk
from tkinter import filedialog
import customtkinter as custk
import os
from PIL import Image
import pygame

# Establece el modo de apariencia
custk.set_appearance_mode("dark")
#custk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(custk.CTk):
    def __init__(self):
        super().__init__()

        #--------------------------------------------------------------------------------------------------------------------------------

        # Configuración de la ventana
        self.title("BriMusic.py")
        self.geometry(f"{500}x{350}")
        self.minsize(500, 350)

        # Inicializar pygame mixer solo para audio
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Configurar el evento de finalización de la canción
        pygame.mixer.music.set_volume(0.1)

        # Variables para el índice de la canción actual
        self.current_index = 0
        self.song_paths = []
        self.flagButtonPlay = True
        self.current_pos = 0.0
        #--------------------------------------------------------------------------------------------------------------------------------
        
        def select_folder():
            folder_path = filedialog.askdirectory()  # Abrir diálogo de selección de carpetas
            if folder_path:  # Verificar que se haya seleccionado una carpeta
                self.songlist.delete(0, tk.END)  # Limpiar el Listbox
                self.song_paths = []  # Lista para almacenar rutas de archivos
                for file in os.listdir(folder_path):  # Listar archivos en la carpeta
                    if file.endswith(".mp3"):  # Filtrar solo archivos .mp4
                        self.songlist.insert(tk.END, file)  # Agregar archivos al Listbox
                        self.song_paths.append(os.path.join(folder_path, file))  # Almacenar la ruta completa

        #--------------------------------------------------------------------------------------------------------------------------------

        def change_tab():
            if self.frameListBox.winfo_manager():
                self.frameListBox.pack_forget()
                self.nameMusic.pack(anchor="center", expand=True, pady=0, padx=10)
                self.frameMusic.pack(anchor="center", expand=True, pady=0, padx=10)
                self.frameButtons.pack_forget()
                self.volume.pack(anchor="center", expand=True, pady=0, padx=0)
                self.frameButtons.pack(anchor="center", expand=True, pady=0, padx=10)
            else:
                self.frameButtons.pack_forget()
                self.frameMusic.pack_forget()
                self.nameMusic.pack_forget()
                self.volume.pack_forget()
                self.frameListBox.pack(anchor="s", fill=tk.BOTH, expand=True, pady=10, padx=10)
                self.frameButtons.pack(anchor="center", expand=True, pady=0, padx=10)

        #--------------------------------------------------------------------------------------------------------------------------------

        def play_song():
            if self.songlist.size() > 0:
                if self.current_pos == 0:
                    selected_song = self.song_paths[self.current_index]
                    pygame.mixer.music.load(selected_song)
                    pygame.mixer.music.play()

                    # Obtener el nombre del archivo con la extensión
                    file_name_with_extension = os.path.basename(selected_song)
                    # Separar el nombre del archivo de su extensión
                    file_name, file_extension = os.path.splitext(file_name_with_extension)
                    self.nameMusic.configure(text=file_name)
                    
                    # Se convierte el boton para pausar
                    self.imagePlay.configure(light_image=Image.open('C:/Users/BRYAN/Desktop/BriMusic/Pause.png'), size=(160,160))
                    self.buttonPlay.configure(command=stop_song)
                    self.flagButtonPlay = False
                    check_events()
                else:
                    pygame.mixer.music.play(start=self.current_pos)
                    # Se convierte el boton para pausar
                    self.imagePlay.configure(light_image=Image.open('C:/Users/BRYAN/Desktop/BriMusic/Pause.png'), size=(160,160))
                    self.buttonPlay.configure(command=stop_song)
                    self.flagButtonPlay = False
                    check_events()
               
        def play_next():
            self.current_pos = 0.0
            if self.songlist.size() > 0:
                self.current_index = (self.current_index + 1) % self.songlist.size()
                play_song()

        def play_previous():
            self.current_pos = 0.0
            if self.songlist.size() > 0:
                self.current_index = (self.current_index - 1) % self.songlist.size()
                play_song()

        def set_volume(value):
            volume = int(value) / 100  # Convertir el valor del slider a un rango de 0 a 1
            pygame.mixer.music.set_volume(volume)

        def stop_song():
            get_pos = pygame.mixer.music.get_pos() / 1000  # Obtener posición actual en segundos
            self.current_pos = self.current_pos + get_pos
            print(self.current_pos)

            pygame.mixer.music.stop()
            
            # Se convierte el boton para pausar
            self.imagePlay.configure(light_image=Image.open('C:/Users/BRYAN/Desktop/BriMusic/Play.png'), size=(160,160))
            self.buttonPlay.configure(command=play_song)
            self.flagButtonPlay = True
        
        def check_events():
            if self.flagButtonPlay:
                pass
            else:
                if pygame.mixer.music.get_busy():
                    pass
                else:
                    play_next()  # Llamar a play_next() cuando la canción actual haya terminado
                self.after(1000, check_events)  # Verificar cada 100 ms

        #--------------------------------------------------------------------------------------------------------------------------------
        #Frame principal y entrada de nombre y link

        self.frame = custk.CTkFrame(master=self, fg_color="#6D2C2C", border_color="#EF7373", border_width=2)
        self.frame.pack(anchor="center", fill=tk.BOTH, expand=True, padx=20, pady=20)

        #Frame para la listbox
        self.frameListBox = custk.CTkFrame(master=self.frame, fg_color="transparent", border_color="#EF7373", border_width=2)
        self.frameListBox.pack(anchor="s", fill=tk.BOTH, expand=True, pady=10, padx=10)

        self.songlist = tk.Listbox(master=self.frameListBox, bg="#944343", fg="white", borderwidth=0, highlightthickness=0)
        self.songlist.pack(side="left", anchor="s",fill=tk.BOTH, expand=True, pady=3, padx=3)

        #--------------------------------------------------------------------------------------------------------------------------------
        #Frame para los botones de abajo
        self.frameButtons = custk.CTkFrame(master=self.frame, fg_color="transparent", border_width=0)
        self.frameButtons.pack(anchor="center", expand=True, pady=0, padx=10)

        #--------------------------------------------------------------------------------------------------------------------------------
        
        self.selectFile = custk.CTkButton(master=self.frameButtons, text="Seleccionar carpeta", fg_color="#944343", hover_color="#EF7373", border_color="#EF7373", border_width=2, corner_radius=36, command=select_folder)
        self.selectFile.pack(side="left", anchor="s", expand=True, pady=5, padx=10)

        self.selectMusic = custk.CTkButton(master=self.frameButtons, text="Seleccionar musica", fg_color="#944343", hover_color="#EF7373", border_color="#EF7373", border_width=2, corner_radius=36, command=change_tab)
        self.selectMusic.pack(side="left", anchor="s", expand=True, pady=5, padx=10)
        
        #--------------------------------------------------------------------------------------------------------------------------------
        
        self.frameMusic = custk.CTkFrame(master=self.frame, fg_color="transparent", border_width=0)

        self.imageBack = custk.CTkImage(light_image=Image.open('C:/Users/BRYAN/Desktop/BriMusic/Back.png'), size=(80,80))
        self.buttonBack = custk.CTkButton(master=self.frameMusic, image=self.imageBack, fg_color="transparent", text="", hover_color="#EF7373", command=play_previous)
        self.buttonBack.pack(side="left", anchor="e", expand=True, pady=0, padx=0)
        
        self.imagePlay = custk.CTkImage(light_image=Image.open('C:/Users/BRYAN/Desktop/BriMusic/Play.png'), size=(160,160))
        self.buttonPlay = custk.CTkButton(master=self.frameMusic, image=self.imagePlay, fg_color="transparent", text="", hover_color="#EF7373", command=play_song)
        self.buttonPlay.pack(side="left", anchor="center", expand=True, pady=0, padx=0)

        self.imageNext = custk.CTkImage(light_image=Image.open('C:/Users/BRYAN/Desktop/BriMusic/Next.png'), size=(80,80))
        self.buttonNext = custk.CTkButton(master=self.frameMusic, image=self.imageNext, fg_color="transparent", text="", hover_color="#EF7373", command=play_next)
        self.buttonNext.pack(side="left", anchor="w", expand=True, pady=0, padx=0)

        #--------------------------------------------------------------------------------------------------------------------------------

        self.nameMusic = custk.CTkLabel(master=self.frame, text="Nombre Cancion", font=("Arial", 20), anchor=custk.W, text_color="white")

        #--------------------------------------------------------------------------------------------------------------------------------

        self.volume = custk.CTkSlider(master=self.frame, from_=0, to=20, number_of_steps=100, button_color="#EF7373", progress_color="#EF7373", button_hover_color="#EF7373", command=set_volume)
        self.volume.set(10)

        

if __name__ == "__main__":
    app = App()
    app.mainloop()