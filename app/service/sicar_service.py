from shapely import wkb

from app.database import get_connection_sicar
from app.service.prodes_service import *

def validate_sicar_data(cod_imovel):
    conn = get_connection_sicar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT 1 FROM public.sicar_geometries WHERE cod_imovel = '{cod_imovel}'")
    is_valid = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return is_valid

def get_sicar_data_by_cod_imovel(cod_imovel):
    conn = get_connection_sicar()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT jsonb_build_object(
            'type', 'Feature',
            'properties', to_jsonb(t) - 'geometry',
            'geometry', ST_AsGeoJSON(t.geometry, 9, 1)::jsonb
        )
        FROM public.sicar_geometries t
        WHERE cod_imovel = '{cod_imovel}'
    """)
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if row:
        sicar_data = {
            "properties": row[0]['properties'],
            "geometry": row[0]['geometry']
        }
    
    return sicar_data if row else None