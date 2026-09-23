import sys
from pathlib import Path

# Configura caminho da pasta src
RAIZ = Path(__file__).resolve().parent
sys.path.append(str(RAIZ / "src"))

from infra.banco import inicializar_banco
from interface.menu import MenuCLI

def main():
    # Garantir que o banco SQLite e suas tabelas existam
    inicializar_banco()

    # Inicializa e abre o menu no terminal
    app = MenuCLI()
    app.exibir_menu_principal()

if __name__ == "__main__":
    main()