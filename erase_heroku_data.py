import os
import psycopg2

# Get DATABASE_URL from environment or replace with actual URL string
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://udc0qhdnupk8rp:p79f4d89e4a09b61c1b73e1dc1bfb441868056c58cf6ddad3fa747953e7a827c9@cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d8t4mijc9j0uti")

def wipe_all_data(database_url):
    conn = psycopg2.connect(database_url)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        # Get all table names
        cur.execute("""
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public';
        """)
        tables = cur.fetchall()

        if not tables:
            print("No tables found.")
            return

        # Build TRUNCATE CASCADE statement
        table_names = ', '.join(f'public."{table[0]}"' for table in tables)
        truncate_sql = f'TRUNCATE {table_names} CASCADE;'
        cur.execute(truncate_sql)

        print("✅ All data wiped using TRUNCATE CASCADE.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    wipe_all_data(DATABASE_URL)
