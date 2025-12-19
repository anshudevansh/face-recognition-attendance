import mysql.connector
from mysql.connector import Error
from config import Config

class DatabaseHelper:
    """Helper class for database operations"""
    
    @staticmethod
    def get_connection():
        """Get database connection"""
        try:
            connection = mysql.connector.connect(**Config.get_db_config())
            return connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None
    
    @staticmethod
    def execute_query(query, values=None, fetch=False):
        """
        Execute a database query
        
        Args:
            query: SQL query string
            values: Tuple of values for parameterized query
            fetch: Boolean, if True returns fetched results
        
        Returns:
            For SELECT: List of tuples or None
            For INSERT/UPDATE/DELETE: Boolean (success/failure)
        """
        connection = DatabaseHelper.get_connection()
        if not connection:
            return None if fetch else False
        
        try:
            cursor = connection.cursor()
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            
            if fetch:
                result = cursor.fetchall()
                cursor.close()
                connection.close()
                return result
            else:
                connection.commit()
                cursor.close()
                connection.close()
                return True
        except Error as e:
            print(f"Database error: {e}")
            if connection:
                connection.close()
            return None if fetch else False
    
    @staticmethod
    def insert_student(roll_no, name, image_data=None):
        """Insert a new student"""
        query = "INSERT INTO students (roll_no, name, image) VALUES (%s, %s, %s)"
        return DatabaseHelper.execute_query(query, (roll_no, name, image_data))
    
    @staticmethod
    def get_student_by_roll_no(roll_no):
        """Get student by roll number"""
        query = "SELECT id, roll_no, name FROM students WHERE roll_no = %s"
        result = DatabaseHelper.execute_query(query, (roll_no,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def insert_user(username, enrollment, password_hash, role='student'):
        """Insert a new user"""
        query = "INSERT INTO users (username, enrollment, password_hash, role) VALUES (%s, %s, %s, %s)"
        return DatabaseHelper.execute_query(query, (username, enrollment, password_hash, role))
    
    @staticmethod
    def verify_user(enrollment, password_hash):
        """Verify user credentials"""
        query = "SELECT id, username, role FROM users WHERE enrollment = %s AND password_hash = %s"
        result = DatabaseHelper.execute_query(query, (enrollment, password_hash), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def mark_attendance(student_id, subject_id, status='present', attendance_type='automatic', marked_by=None):
        """Mark attendance for a student"""
        query = """
            INSERT INTO attendance (student_id, subject_id, attendance_date, status, attendance_type, marked_by)
            VALUES (%s, %s, CURDATE(), %s, %s, %s)
            ON DUPLICATE KEY UPDATE status = %s, marked_at = CURRENT_TIMESTAMP
        """
        return DatabaseHelper.execute_query(
            query, 
            (student_id, subject_id, status, attendance_type, marked_by, status)
        )
    
    @staticmethod
    def get_subject_by_name(subject_name):
        """Get subject by name"""
        query = "SELECT id, subject_code, subject_name FROM subjects WHERE subject_name = %s"
        result = DatabaseHelper.execute_query(query, (subject_name,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def get_all_subjects():
        """Get all subjects"""
        query = "SELECT id, subject_code, subject_name FROM subjects ORDER BY subject_name"
        return DatabaseHelper.execute_query(query, fetch=True)
    
    @staticmethod
    def get_attendance_report(student_id=None, subject_id=None, date_from=None, date_to=None):
        """Get attendance report with optional filters"""
        query = "SELECT * FROM attendance_report WHERE 1=1"
        params = []
        
        if student_id:
            query += " AND roll_no = %s"
            params.append(student_id)
        if subject_id:
            query += " AND subject_name = %s"
            params.append(subject_id)
        if date_from:
            query += " AND attendance_date >= %s"
            params.append(date_from)
        if date_to:
            query += " AND attendance_date <= %s"
            params.append(date_to)
        
        return DatabaseHelper.execute_query(query, tuple(params) if params else None, fetch=True)
