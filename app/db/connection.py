import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

load_dotenv()

# Global connection pool - created on first use
connection_pool = None


def _init_pool():
    """Initialize connection pool (lazy initialization)"""
    global connection_pool
    
    if connection_pool is not None:
        return  # Already initialized
    
    # Get database URL from environment
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/school_db")

    # Parse connection string
    if DATABASE_URL.startswith("postgresql://"):
        # Format: postgresql://user:password@host:port/database
        db_url = DATABASE_URL.replace("postgresql://", "")
        if "@" in db_url:
            auth, host_db = db_url.split("@")
            user, password = auth.split(":")
            host_port, database = host_db.split("/")
            host, port = host_port.split(":")
        else:
            raise ValueError("Invalid DATABASE_URL format")
    else:
        raise ValueError("DATABASE_URL must start with 'postgresql://'")

    # Create connection pool
    try:
        connection_pool = pool.SimpleConnectionPool(
            1,
            10,  # Min 1, Max 10 connections
            user=user,
            password=password,
            host=host,
            port=int(port),
            database=database
        )
        print("✓ Connection pool created successfully")
    except Exception as e:
        print(f"✗ Failed to create connection pool: {e}")
        connection_pool = None


def get_connection():
    """Get a connection from the pool"""
    global connection_pool
    _init_pool()
    if connection_pool is None:
        raise Exception("Connection pool not initialized")
    return connection_pool.getconn()


def return_connection(conn):
    """Return a connection to the pool"""
    global connection_pool
    _init_pool()
    if connection_pool is not None:
        connection_pool.putconn(conn)


def execute_query(query: str, params: tuple = None, fetch_one: bool = False, fetch_all: bool = False):
    """
    Execute a query and optionally fetch results
    
    Args:
        query: SQL query string with %s placeholders
        params: Tuple of parameters to pass to query
        fetch_one: Return first row
        fetch_all: Return all rows
    
    Returns:
        Query result or None
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        else:
            result = None
        
        conn.commit()
        cursor.close()
        return result
        
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            return_connection(conn)


def close_pool():
    """Close all connections in the pool"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        connection_pool = None
