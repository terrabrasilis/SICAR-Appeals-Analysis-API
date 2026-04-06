from app.database import get_connection_prodes

from app.database import get_connection_prodes

def is_valid_prodes_data(uuid):
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

                cursor.execute(f"""
                    SELECT geom, class_name, year
                    FROM public.{table_name}
                    WHERE uuid = '{uuid}'
                    LIMIT 1
                """)
                row = cursor.fetchone()

                if row:
                    columns = [desc[0] for desc in cursor.description]
                    prodes_data = dict(zip(columns, row))
                    prodes_data["biome"] = biome
                    prodes_data["layer"] = table_name
                    return prodes_data

        finally:
            cursor.close()
            conn.close()

    return False

def get_table_name_by_uuid(uuid, cursor):
    cursor.execute(f"SELECT tablename FROM public.deforestation WHERE uuid = '{uuid}'")
    result = cursor.fetchone()
    return result[0] if result else None
    
def get_prodes_data_by_uuid(uuid):
    
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
            cursor.execute(f"SELECT * FROM public.{table_name} WHERE uuid = '{uuid}'")
            row = cursor.fetchone()
            
            cursor.close()
            conn.close()

            if row:
                columns = [desc[0] for desc in cursor.description]
                prodes_data = dict(zip(columns, row))
                prodes_data['layer'] = table_name
                
        cursor.close()
        conn.close()
        
    return prodes_data if row else None


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
            result = cursor.fetchone()
        
            cursor.close()
            conn.close()

            if result:
                return result[0]

    return None