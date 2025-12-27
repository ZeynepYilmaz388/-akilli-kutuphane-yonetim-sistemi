import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

class Database:
    @staticmethod
    def get_connection():
        """PostgreSQL bağlantısı oluşturur"""
        try:
            conn = psycopg2.connect(Config.DB_CONNECTION_STRING)
            return conn
        except psycopg2.Error as e:
            print(f"Veritabanı bağlantı hatası: {e}")
            raise
    
    @staticmethod
    def execute_query(query, params=None, fetch=False, fetch_one=False):
        """SQL sorgusu çalıştırır"""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch_one:
                result = cursor.fetchone()
                conn.commit()
                return result
            elif fetch:
                result = cursor.fetchall()
                conn.commit()
                return result
            else:
                conn.commit()
                return cursor.rowcount
                
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Sorgu hatası: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def execute_stored_procedure(proc_name, params=None):
        """Stored Function çalıştırır"""
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            if params:
                placeholders = ','.join(['%s' for _ in params])
                cursor.execute(f"SELECT {proc_name}({placeholders})", params)
            else:
                cursor.execute(f"SELECT {proc_name}()")
            
            conn.commit()
            
            try:
                return cursor.fetchall()
            except:
                return None
                
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Function hatası: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()