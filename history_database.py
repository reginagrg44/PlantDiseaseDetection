import sqlite3
from datetime import datetime
import os

class HistoryDatabase:
    def __init__(self, db_name='prediction_history.db'):
        self.db_name = db_name
        self.create_history_table()
    
    def create_history_table(self):
        """Create the prediction history table if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                image_name TEXT NOT NULL,
                prediction_type TEXT NOT NULL,
                predicted_disease TEXT,
                confidence_score REAL,
                is_leaf BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                cure_info TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_prediction_record(self, username, image_name, prediction_type, 
                            predicted_disease=None, confidence_score=None, 
                            is_leaf=None, cure_info=None):
        """Add a new prediction record to the history"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute('''
            INSERT INTO prediction_history 
            (username, image_name, prediction_type, predicted_disease, 
             confidence_score, is_leaf, timestamp, cure_info)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, image_name, prediction_type, predicted_disease, 
              confidence_score, is_leaf, timestamp, cure_info))
        
        conn.commit()
        conn.close()
    
    def get_user_history(self, username, limit=None):
        """Get prediction history for a specific user"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        if limit:
            c.execute('''
                SELECT * FROM prediction_history 
                WHERE username = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (username, limit))
        else:
            c.execute('''
                SELECT * FROM prediction_history 
                WHERE username = ? 
                ORDER BY timestamp DESC
            ''', (username,))
        
        records = c.fetchall()
        conn.close()
        return records
    
    def get_all_history(self, limit=None):
        """Get all prediction history records"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        if limit:
            c.execute('''
                SELECT * FROM prediction_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
        else:
            c.execute('''
                SELECT * FROM prediction_history 
                ORDER BY timestamp DESC
            ''')
        
        records = c.fetchall()
        conn.close()
        return records
    
    def delete_user_history(self, username):
        """Delete all history records for a specific user"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('DELETE FROM prediction_history WHERE username = ?', (username,))
        conn.commit()
        conn.close()
    
    def delete_record_by_id(self, record_id):
        """Delete a specific record by ID"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('DELETE FROM prediction_history WHERE id = ?', (record_id,))
        conn.commit()
        conn.close()
    
    def get_history_stats(self, username=None):
        """Get statistics about prediction history"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        if username:
            # User-specific stats
            c.execute('''
                SELECT 
                    COUNT(*) as total_predictions,
                    COUNT(CASE WHEN is_leaf = 1 THEN 1 END) as leaf_predictions,
                    COUNT(CASE WHEN is_leaf = 0 THEN 1 END) as non_leaf_predictions,
                    AVG(confidence_score) as avg_confidence
                FROM prediction_history 
                WHERE username = ?
            ''', (username,))
        else:
            # Overall stats
            c.execute('''
                SELECT 
                    COUNT(*) as total_predictions,
                    COUNT(CASE WHEN is_leaf = 1 THEN 1 END) as leaf_predictions,
                    COUNT(CASE WHEN is_leaf = 0 THEN 1 END) as non_leaf_predictions,
                    AVG(confidence_score) as avg_confidence
                FROM prediction_history
            ''')
        
        stats = c.fetchone()
        conn.close()
        return stats
    
    def search_history(self, username, search_term):
        """Search history records by disease name or image name"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''
            SELECT * FROM prediction_history 
            WHERE username = ? AND 
            (predicted_disease LIKE ? OR image_name LIKE ?)
            ORDER BY timestamp DESC
        ''', (username, f'%{search_term}%', f'%{search_term}%'))
        
        records = c.fetchall()
        conn.close()
        return records

# Helper functions for formatting history data
def format_history_record(record):
    """Format a history record for display"""
    return {
        'id': record[0],
        'username': record[1],
        'image_name': record[2],
        'prediction_type': record[3],
        'predicted_disease': record[4],
        'confidence_score': record[5],
        'is_leaf': record[6],
        'timestamp': record[7],
        'cure_info': record[8]
    }

def get_column_names():
    """Get column names for the history table"""
    return ['ID', 'Username', 'Image Name', 'Prediction Type', 'Predicted Disease', 
            'Confidence Score', 'Is Leaf', 'Timestamp', 'Cure Info']