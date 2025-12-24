#!/usr/bin/env python3

import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server.grpc_server import serve

def main():
    print("=== MEDITRON SERVICE ===")
    print("Iniciando serviço de análise médica...")
    serve()

if __name__ == '__main__':
    main()