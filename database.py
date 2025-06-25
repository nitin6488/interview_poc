from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from datetime import datetime
import asyncio
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, connection_string: str, database_name: str):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.db = None
        self.connected = False
    
    async def connect(self):
        """Initialize async MongoDB connection with error handling"""
        try:
            self.client = AsyncIOMotorClient(self.connection_string)
            self.db = self.client[self.database_name]
            
            # Test the connection
            await self.client.admin.command('ping')
            self.connected = True
            logger.info(f"✅ Connected to MongoDB: {self.database_name}")
            
            # Create indexes for better performance
            await self.create_indexes()
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            self.connected = False
            raise
    
    async def create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Index for company searches
            await self.db.company_interviews.create_index([
                ("company_name", 1),
                ("role", 1)
            ])
            
            # Index for reports
            await self.db.reports.create_index([
                ("created_at", -1)
            ])
            
            logger.info("✅ Database indexes created")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not create indexes: {e}")
    
    async def disconnect(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info("🔌 Disconnected from MongoDB")
    
    async def health_check(self) -> bool:
        """Check if database connection is healthy"""
        try:
            if not self.connected:
                return False
            
            await self.client.admin.command('ping')
            return True
        except:
            return False
    
    async def save_company_data(self, company_data: Dict):
        """Save scraped company interview data"""
        if not self.connected:
            raise Exception("Database not connected")
        
        try:
            company_data['created_at'] = datetime.utcnow()
            company_data['updated_at'] = datetime.utcnow()
            
            # Upsert based on company name and role
            query = {
                'company_name': company_data['company_name'].lower(),
                'role': company_data.get('role', 'general').lower()
            }
            
            result = await self.db.company_interviews.update_one(
                query,
                {'$set': company_data},
                upsert=True
            )
            
            logger.info(f"💾 Saved data for {company_data['company_name']} - {company_data.get('role', 'general')}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error saving company data: {e}")
            raise
    
    async def get_company_data(self, company_name: str, role: str = None) -> Optional[Dict]:
        """Retrieve company interview data"""
        if not self.connected:
            raise Exception("Database not connected")
        
        try:
            query = {'company_name': company_name.lower()}
            if role:
                query['role'] = role.lower()
            
            result = await self.db.company_interviews.find_one(query)
            
            if result:
                logger.info(f"📖 Retrieved data for {company_name}")
                # Remove MongoDB _id field for JSON serialization
                result.pop('_id', None)
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Error retrieving company data: {e}")
            return None
    
    async def save_generated_report(self, report_data: Dict):
        """Save generated interview preparation report"""
        if not self.connected:
            raise Exception("Database not connected")
        
        try:
            report_data['created_at'] = datetime.utcnow()
            result = await self.db.reports.insert_one(report_data)
            
            logger.info(f"📊 Saved report for {report_data.get('company_name', 'Unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error saving report: {e}")
            raise
    
    async def get_all_companies(self) -> List[str]:
        """Get list of all companies in database"""
        if not self.connected:
            return []
        
        try:
            companies = await self.db.company_interviews.distinct('company_name')
            logger.info(f"📋 Retrieved {len(companies)} companies from database")
            return companies
            
        except Exception as e:
            logger.error(f"❌ Error retrieving companies: {e}")
            return []
    
    async def get_database_stats(self) -> Dict:
        """Get database statistics"""
        if not self.connected:
            return {}
        
        try:
            stats = {
                'companies_count': await self.db.company_interviews.count_documents({}),
                'reports_count': await self.db.reports.count_documents({}),
                'connection_status': 'connected'
            }
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting database stats: {e}")
            return {'connection_status': 'error'}