#!/usr/bin/env python3
"""
Database Migration Script for AI Study Buddy
Run this script to set up the MySQL database and create all required tables.
"""

import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DB = os.environ.get('MYSQL_DB', 'ai_study_buddy')

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect without specifying database
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Database '{MYSQL_DB}' created successfully")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create all required tables"""
    try:
        # Connect to the specific database
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    is_premium BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_username (username),
                    INDEX idx_email (email)
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """)
            print("✅ Users table created")
            
            # Flashcards table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS flashcards (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    title VARCHAR(200) NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
                    times_studied INT DEFAULT 0,
                    correct_answers INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """)
            print("✅ Flashcards table created")
            
            # Suggestions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suggestions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    content TEXT NOT NULL,
                    email_sent BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_email_sent (email_sent)
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """)
            print("✅ Suggestions table created")
            
            # Payments table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    intasend_invoice_id VARCHAR(100) UNIQUE NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    currency VARCHAR(3) DEFAULT 'KES',
                    status ENUM('pending', 'completed', 'failed', 'cancelled') DEFAULT 'pending',
                    payment_method VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    paid_at TIMESTAMP NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_status (status),
                    INDEX idx_invoice_id (intasend_invoice_id)
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """)
            print("✅ Payments table created")
            
            # Study sessions table (for analytics)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS study_sessions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    flashcard_id INT NOT NULL,
                    is_correct BOOLEAN,
                    time_spent INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE,
                    INDEX idx_user_id (user_id),
                    INDEX idx_flashcard_id (flashcard_id)
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """)
            print("✅ Study sessions table created")
        
        connection.commit()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def insert_sample_data():
    """Insert sample data for testing"""
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Check if sample data already exists
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                print("📝 Inserting sample data...")
                
                # Insert sample user (password: 'password123')
                cursor.execute("""
                    INSERT INTO users (username, email, password_hash, is_premium) VALUES 
                    ('demo_student', 'demo@aistudybuddy.com', 'scrypt:32768:8:1$salt$hash', FALSE)
                """)
                
                print("✅ Sample data inserted")
            else:
                print("ℹ️ Sample data already exists")
        
        connection.commit()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")
        return False

def main():
    """Main migration function"""
    print("🚀 Starting AI Study Buddy Database Migration...")
    print("=" * 50)
    
    # Step 1: Create database
    print("1. Creating database...")
    if not create_database():
        print("❌ Migration failed at database creation")
        return
    
    # Step 2: Create tables
    print("\n2. Creating tables...")
    if not create_tables():
        print("❌ Migration failed at table creation")
        return
    
    # Step 3: Insert sample data
    print("\n3. Setting up sample data...")
    insert_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 Database migration completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy .env.example to .env and update your credentials")
    print("2. Get your Hugging Face API key from: https://huggingface.co/settings/tokens")
    print("3. Set up IntaSend account at: https://intasend.com")
    print("4. Configure email settings for bulk email feature")
    print("5. Run: python app.py")
    print("\n🌍 Ready to serve African students with AI-powered education!")

if __name__ == "__main__":
    main()