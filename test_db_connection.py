#!/usr/bin/env python
import psycopg2

try:
    conn = psycopg2.connect(
        user='postgres',
        password='postgres',
        host='127.0.0.1',
        port=5432,
        database='user_data'
    )
    print('✓ Connection successful!')
    cursor = conn.cursor()
    
    # Test query
    cursor.execute('SELECT 1')
    result = cursor.fetchone()
    print(f'✓ Query executed: {result}')
    
    # Check if tables exist
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()
    print(f'✓ Tables in database: {len(tables)}')
    for t in tables:
        print(f'  - {t[0]}')
    
    cursor.close()
    conn.close()
except Exception as e:
    import traceback
    print(f'✗ Failed: {e}')
    traceback.print_exc()
