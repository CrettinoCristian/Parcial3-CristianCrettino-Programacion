#!/usr/bin/env python3
"""
Script para migrar las etiquetas de contactos al nuevo formato JSON
"""

from app import create_app
from models import db, Contacto
import json

def migrate_tags():
    """Migra las etiquetas existentes al formato JSON"""
    app = create_app()
    
    with app.app_context():
        contactos = Contacto.query.all()
        print(f'Migrando {len(contactos)} contactos...')
        
        migrated_count = 0
        
        for contacto in contactos:
            if contacto.etiquetas and contacto.etiquetas.strip():
                try:
                    # Verificar si ya es JSON válido
                    json.loads(contacto.etiquetas)
                    print(f'Contacto {contacto.id} ({contacto.nombre}) ya tiene formato JSON')
                except (json.JSONDecodeError, TypeError):
                    # Convertir string separado por comas a JSON
                    if ',' in contacto.etiquetas or contacto.etiquetas.strip():
                        etiquetas_list = [tag.strip() for tag in contacto.etiquetas.split(',') if tag.strip()]
                        contacto.etiquetas = json.dumps(etiquetas_list)
                        print(f'Contacto {contacto.id} ({contacto.nombre}): {etiquetas_list}')
                        migrated_count += 1
                    else:
                        etiquetas_list = [contacto.etiquetas.strip()]
                        contacto.etiquetas = json.dumps(etiquetas_list)
                        print(f'Contacto {contacto.id} ({contacto.nombre}): {etiquetas_list}')
                        migrated_count += 1
            else:
                contacto.etiquetas = json.dumps([])
                print(f'Contacto {contacto.id} ({contacto.nombre}): sin etiquetas')
        
        try:
            db.session.commit()
            print(f'¡Migración completada! {migrated_count} contactos migrados.')
        except Exception as e:
            db.session.rollback()
            print(f'Error durante la migración: {e}')
            return False
        
        return True

if __name__ == '__main__':
    migrate_tags()