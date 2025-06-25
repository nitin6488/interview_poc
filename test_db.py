import asyncio
import os
from dotenv import load_dotenv
from database import DatabaseManager

async def test_database_connection():
    """Test MongoDB connection and basic operations"""
    load_dotenv()
    
    # Get connection details from environment
    mongodb_url = os.getenv("MONGODB_URL")
    database_name = os.getenv("DATABASE_NAME", "interview_research")
    
    if not mongodb_url:
        print("❌ MONGODB_URL not found in environment variables")
        return
    
    print("🔄 Testing MongoDB connection...")
    
    # Initialize database manager
    db_manager = DatabaseManager(mongodb_url, database_name)
    
    try:
        # Test connection
        await db_manager.connect()
        
        if db_manager.connected:
            print("✅ Database connection successful!")
            
            # Test health check
            health = await db_manager.health_check()
            print(f"💓 Health check: {'✅ Healthy' if health else '❌ Unhealthy'}")
            
            # Test saving data
            test_data = {
                'company_name': 'TestCompany',
                'role': 'Software Engineer',
                'process_steps': ['Phone Screen', 'Technical Interview'],
                'technical_topics': ['Algorithms', 'System Design'],
                'difficulty_level': 'Medium'
            }
            
            await db_manager.save_company_data(test_data)
            print("✅ Test data saved successfully!")
            
            # Test retrieving data
            retrieved_data = await db_manager.get_company_data('TestCompany', 'Software Engineer')
            if retrieved_data:
                print("✅ Test data retrieved successfully!")
                print(f"📄 Retrieved: {retrieved_data['company_name']} - {retrieved_data['role']}")
            
            # Get database stats
            stats = await db_manager.get_database_stats()
            print(f"📊 Database stats: {stats}")
            
            # Get all companies
            companies = await db_manager.get_all_companies()
            print(f"🏢 Companies in database: {companies}")
            
        else:
            print("❌ Database connection failed!")
            
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        
    finally:
        await db_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(test_database_connection())