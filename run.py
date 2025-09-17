#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de ejecución simplificado para Mini CRM Personal

Este script facilita la ejecución de la aplicación con diferentes configuraciones.

Uso:
    python run.py [--debug] [--port PORT] [--host HOST]
"""

import argparse
import os
import sys
from app import create_app

def main():
    """Función principal para ejecutar la aplicación"""
    parser = argparse.ArgumentParser(description='Ejecutar Mini CRM Personal')
    parser.add_argument('--debug', action='store_true', 
                       help='Ejecutar en modo debug')
    parser.add_argument('--port', type=int, default=5000,
                       help='Puerto para la aplicación (default: 5000)')
    parser.add_argument('--host', default='127.0.0.1',
                       help='Host para la aplicación (default: 127.0.0.1)')
    parser.add_argument('--config', default='development',
                       choices=['development', 'production'],
                       help='Configuración a usar (default: development)')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Mini CRM Personal - Iniciando Aplicación")
    print("=" * 50)
    
    try:
        # Crear la aplicación
        app = create_app(args.config)
        
        print(f"Configuración: {args.config}")
        print(f"Debug: {'Activado' if args.debug else 'Desactivado'}")
        print(f"Host: {args.host}")
        print(f"Puerto: {args.port}")
        print(f"URL: http://{args.host}:{args.port}")
        print("=" * 50)
        print("Presiona Ctrl+C para detener el servidor")
        print("=" * 50)
        
        # Ejecutar la aplicación
        app.run(
            debug=args.debug,
            host=args.host,
            port=args.port,
            use_reloader=args.debug
        )
        
    except KeyboardInterrupt:
        print("\n\nServidor detenido por el usuario")
    except Exception as e:
        print(f"\nError al iniciar la aplicación: {str(e)}")
        print("\nVerifica que:")
        print("1. PostgreSQL esté ejecutándose")
        print("2. La base de datos 'mini_crm' exista")
        print("3. Las dependencias estén instaladas: pip install -r requirements.txt")
        print("4. La base de datos esté inicializada: python init_db.py")
        sys.exit(1)

if __name__ == '__main__':
    main()