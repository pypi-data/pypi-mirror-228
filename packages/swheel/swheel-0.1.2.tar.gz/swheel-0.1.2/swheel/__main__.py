import os
import subprocess

def verifica_projeto_com_src():
    diretorio_atual = os.getcwd()
    caminho_src = os.path.join(diretorio_atual, 'src')
    return os.path.exists(caminho_src) and os.path.isdir(caminho_src)

def main():
    if verifica_projeto_com_src():
        print("Projeto Python encontrado com a pasta 'src'.")
        subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'])
        print("Projeto construído usando swheel.")
    else:
        print("Este não parece ser um projeto Python com a pasta 'src'.")

if __name__ == "__main__":
    main()

