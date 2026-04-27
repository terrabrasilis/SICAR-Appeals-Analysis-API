from app.database import get_connection_prodes

from app.database import get_connection_prodes


def validate_prodes_data(uuid):
    biomes = ["pantanal", "amazonia", "cerrado", "pampa", "caatinga", "mata_atlantica"]
    
    for biome in biomes:
        
        try:
            conn = get_connection_prodes(biome)
            cursor = conn.cursor()
        except Exception:
            continue
        
        if not conn or not cursor:
            continue
        
        try:
            table_name = get_table_name_by_uuid(uuid, cursor)
            if table_name:
                return {"uuid": uuid, "is_valid": True, "biome": biome, "layer": table_name}
        finally:
            cursor.close()
            conn.close()    
    return {"uuid": uuid, "is_valid": False}            
                
                
def get_table_name_by_uuid(uuid, cursor):
    cursor.execute(f"SELECT tablename FROM public.search_deforestation_uuid WHERE uuid = '{uuid}'")
    result = cursor.fetchone()
    return result[0] if result else None
    
def get_prodes_data_by_uuid(uuid):

    biomes = ["pantanal", "amazonia", "cerrado", "pampa", "caatinga", "mata_atlantica"]

    for biome in biomes:

        conn = None
        cursor = None

        try:
            conn = get_connection_prodes(biome)

            if not conn:
                continue

            cursor = conn.cursor()

            table_name = get_table_name_by_uuid(uuid, cursor)

            if not table_name:
                continue

            cursor.execute(f"""
                SELECT jsonb_build_object(
                    'type', 'Feature',
                    'properties', to_jsonb(t) - 'geom',
                    'geometry', ST_AsGeoJSON(t.geom, 9, 4|1)::jsonb
                )
                FROM public.{table_name} t
                WHERE uuid = %s;
            """, (uuid,))

            row = cursor.fetchone()

            if row:
                prodes_data = {
                    "properties": row[0]["properties"],
                    "type": row[0]["type"],
                    "geometry": row[0]["geometry"]
                }

                prodes_data["properties"]["uuid"] = uuid
                prodes_data["properties"]["biome"] = biome
                prodes_data["properties"]["layer"] = table_name

                return prodes_data

        except Exception:
            continue

        finally:
            if cursor:
                cursor.close()

            if conn:
                conn.close()

    return None

def get_prodes_geometry_by_uuid(uuid):
    
    biomes = ["pantanal", "amazonia", "cerrado", "pampa", "caatinga", "mata_atlantica"]
    
    for biome in biomes:
        
        try:
            conn = get_connection_prodes(biome)
            cursor = conn.cursor()
        except Exception:
            continue
        
        if not conn or not cursor:
            continue
        
        table_name = get_table_name_by_uuid(uuid, cursor)
        
        if table_name:
            cursor.execute(f"SELECT geom FROM public.{table_name} WHERE uuid = '{uuid}'")
            row = cursor.fetchone()
            
            cursor.close()
            conn.close()

            if row:
                return row[0]
        
        cursor.close()
        conn.close()
        
    return None