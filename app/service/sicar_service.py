from shapely import wkb

from app.database import get_connection_sicar
from app.service.prodes_service import is_valid_prodes_data, get_prodes_geometry_by_uuid


def get_sicar_data_by_cod_imovel(cod_imovel):
    conn = get_connection_sicar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM public.sicar_geometries WHERE cod_imovel = '{cod_imovel}'")
    row = cursor.fetchone()

    if row:
        columns = [desc[0] for desc in cursor.description]
        sicar_data = dict(zip(columns, row))

    cursor.close()
    conn.close()

    return sicar_data if row else None

def get_sicar_geometry_by_cod_imovel(cod_imovel):
    conn = get_connection_sicar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT geometry FROM public.sicar_geometries WHERE cod_imovel = '{cod_imovel}'")
    geom = cursor.fetchone()[0] if cursor.rowcount > 0 else None

    cursor.close()
    conn.close()

    return geom

def sicar_intersects_prodes(cod_imovel, uuid):
    
    if not is_valid_prodes_data(uuid):
        return {"error": f"PRODES data not found for uuid: {uuid}"}

    sicar_geom = get_sicar_geometry_by_cod_imovel(cod_imovel)
    prodes_geom = get_prodes_geometry_by_uuid(uuid)

    if not sicar_geom or not prodes_geom:
        return {"error": "Geometry not found"}

    try:
        sicar_shape = wkb.loads(sicar_geom, hex=True)
        prodes_shape = wkb.loads(prodes_geom, hex=True)
    except Exception:
        return {"error": "Invalid geometry format"}
    
    return sicar_shape.intersects(prodes_shape)