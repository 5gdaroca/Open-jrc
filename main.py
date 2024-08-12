import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps
import numpy as np
import os

# Função para realizar posterização customizada com qualquer número de bits
def custom_posterize(image, bits):
    num_colors = 2 ** bits  # Calcula o número de cores
    img_array = np.array(image)  # Converte a imagem para um array numpy
    img_array = img_array / 255.0  # Normaliza o array para o intervalo [0, 1]
    img_array = np.floor(img_array * (num_colors - 1))  # Escala os valores para [0, num_colors - 1]
    img_array = (img_array / (num_colors - 1)) * 255  # Escala de volta para [0, 255]
    return Image.fromarray(img_array.astype('uint8'))  # Converte de volta para imagem PIL

# Função principal para converter a imagem para o estilo NES
def convert_to_nes_style(input_image_path, output_image_path, bits):
    # Abre a imagem
    img = Image.open(input_image_path)
    
    # Converte para RGB se não estiver nesse formato
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Redimensiona a imagem para uma resolução semelhante à do NES (por exemplo, 256x240)
    img_resized = img.resize((256, 240), Image.NEAREST)
    
    # Posteriza a imagem com base nos bits especificados
    if bits <= 8:
        img_posterized = ImageOps.posterize(img_resized, bits)
    else:
        img_posterized = custom_posterize(img_resized, bits)
    
    # Define uma paleta para imitar as cores do NES
    palette = [
        0, 0, 0,        # Preto
        29, 43, 83,     # Azul Escuro
        126, 37, 83,    # Roxo Escuro
        0, 135, 81,     # Verde Escuro
        171, 82, 54,    # Marrom
        95, 87, 79,     # Cinza Escuro
        194, 195, 199,  # Cinza Claro
        255, 241, 232,  # Branco
        255, 0, 77,     # Vermelho Vivo
        255, 163, 0,    # Laranja
        255, 236, 39,   # Amarelo
        0, 228, 54,     # Verde
        41, 173, 255,   # Azul Claro
        131, 118, 156,  # Roxo Claro
        255, 119, 168,  # Rosa
        255, 204, 170   # Pêssego
    ]
    
    # Cria uma imagem de paleta
    palette_img = Image.new('P', (1, 1))
    palette_img.putpalette(palette * 16)  # A paleta precisa ter 768 (256*3) cores
    
    # Converte a imagem posterizada para usar a paleta do NES
    img_nes = img_posterized.convert('RGB').quantize(palette=palette_img)
    
    # Salva a nova imagem
    img_nes.save(output_image_path)

# Função para lidar com a conversão da imagem através da interface gráfica
def convert_image():
    try:
        input_image_path = filedialog.askopenfilename(title="Selecionar Imagem de Entrada")
        if not input_image_path:
            return  # Se o usuário cancelar a seleção
        
        output_image_path = filedialog.asksaveasfilename(title="Salvar Imagem de Saída", defaultextension=".png")
        if not output_image_path:
            return  # Se o usuário cancelar a seleção
        
        bits = int(entry_bits.get())
        if bits <= 0 or bits > 64:
            messagebox.showerror("Erro", "O número de bits deve estar entre 1 e 64.")
            return
        
        convert_to_nes_style(input_image_path, output_image_path, bits)
        messagebox.showinfo("Conversão Concluída", f"Imagem convertida com sucesso e salva em '{output_image_path}'.")
    
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter a imagem: {str(e)}")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Jasper Retro Converter")

# Define o ícone da janela (usando o arquivo icon.png)
script_dir = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório do script
icon_path = os.path.join(script_dir, 'icon.png')  # Caminho completo para icon.png
icon = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon)

# Textos de boas-vindas e direitos autorais
welcome_text = "Jasper Retro Converter"
copyright_text = "© 2023-2024 Leopardus Equipe Indie. Todos os direitos reservados."

# Labels para os textos
label_welcome = tk.Label(root, text=welcome_text)
label_welcome.pack()

# Labels e Entry para os bits
label_bits = tk.Label(root, text="Número de Bits:")
label_bits.pack()
entry_bits = tk.Entry(root)
entry_bits.pack()

# Botão para iniciar a conversão
button_convert = tk.Button(root, text="Converter Imagem", command=convert_image)
button_convert.pack()

# Label para os direitos autorais
label_copyright = tk.Label(root, text=copyright_text)
label_copyright.pack()

# Inicia o loop principal da interface gráfica
root.mainloop()
