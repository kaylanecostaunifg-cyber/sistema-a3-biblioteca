import sys
from pathlib import Path

# Configura o caminho para o Python encontrar a pasta 'src'
RAIZ = Path(__file__).resolve().parent
sys.path.append(str(RAIZ / "src"))
from src.infra.banco import inicializar_banco

from infra.banco import inicializar_banco
from interface.app_gui import AppBiblioteca

def main():
    # Inicializa o banco de dados SQLite
    inicializar_banco()

    # Inicializa e abre a interface gráfica CustomTkinter
    app = AppBiblioteca()
    app.mainloop()

if __name__ == "__main__":
    main()