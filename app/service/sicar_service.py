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

def get_sicar_geometry_by_cod_imovel(cod_imovel):
    conn = get_connection_sicar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT geometry FROM public.sicar_geometries WHERE cod_imovel = '{cod_imovel}'")
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return row[0] if row else None

def sicar_intersects_prodes(cod_imovel, uuid):
    
    prodes_geom = get_prodes_geometry_by_uuid(uuid)
    sicar_geom = get_sicar_geometry_by_cod_imovel(cod_imovel)
    
    if prodes_geom and sicar_geom:
        conn = get_connection_sicar()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT ST_AsGeoJSON(
                ST_Intersection(%s, %s), 9, 1
            )::jsonb
            WHERE ST_Intersects(%s, %s)
        """, (sicar_geom, prodes_geom, sicar_geom, prodes_geom))
        
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return row[0] if row and row[0] else {"message": "As geometrias não intersectam ou a interseção é nula."}