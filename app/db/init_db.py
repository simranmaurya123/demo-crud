"""
Database initialization module
Creates all tables on application startup
"""

from app.db.connection import get_connection, return_connection
from app.db.sql_schemas import ALL_TABLES, TABLE_NAMES


def init_db():
    """
    Initialize database by creating all tables
    Called on application startup
    """
    conn = None
    try:
        print("\n🔄 Initializing database tables...")
        conn = get_connection()
        cursor = conn.cursor()
        
        for i, table_sql in enumerate(ALL_TABLES):
            try:
                cursor.execute(table_sql)
                print(f"✓ Table '{TABLE_NAMES[i]}' created/verified")
            except Exception as e:
                print(f"⚠️  Table '{TABLE_NAMES[i]}': {str(e)}")
        
        conn.commit()
        print("✅ Database initialization complete!\n")
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}\n")
        print("⚠️  App will attempt to reconnect when queries are executed.\n")
        if conn:
            try:
                conn.rollback()
            except:
                pass
    finally:
        try:
            if cursor:
                cursor.close()
        except:
            pass
        if conn:
            return_connection(conn)


def check_table_exists(table_name: str) -> bool:
    """
    Check if a table exists in the database
    
    Args:
        table_name: Name of the table to check
    
    Returns:
        True if table exists, False otherwise
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables 
            WHERE table_name = %s
        );
        """
        cursor.execute(query, (table_name,))
        result = cursor.fetchone()
        cursor.close()
        
        return result[0] if result else False
        
    except Exception as e:
        print(f"Error checking table existence: {e}")
        return False
    finally:
        if conn:
            return_connection(conn)


def drop_all_tables():
    """
    Drop all tables from the database
    WARNING: This will delete all data!
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("\n⚠️  WARNING: Dropping all tables...")
        
        # Drop in reverse order to respect foreign key constraints
        for table_name in reversed(TABLE_NAMES):
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
                print(f"✓ Dropped table '{table_name}'")
            except Exception as e:
                print(f"✗ Error dropping table '{table_name}': {e}")
        
        conn.commit()
        print("✅ All tables dropped!\n")
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)
