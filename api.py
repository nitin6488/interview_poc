from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
import asyncio
from config import Config
from database import DatabaseManager
from scraper import InterviewScraper
from ai_processor import AIProcessor
import datetime

app = FastAPI(title="Interview Research Assistant API", version="1.0.0")

# Initialize components
config = Config()
db_manager = DatabaseManager(config.MONGODB_URL, config.DATABASE_NAME)
scraper = InterviewScraper(config.USER_AGENT, config.REQUEST_TIMEOUT)
ai_processor = AIProcessor(config.GEMINI_API_KEY)

# Request/Response Models
class ResearchRequest(BaseModel):
    company_name: str
    role: Optional[str] = "Software Engineer"
    experience_level: Optional[str] = "Mid-level"
    days_to_prepare: Optional[int] = 30

class ResearchResponse(BaseModel):
    company_name: str
    role: str
    interview_data: dict
    ai_synthesis: dict
    custom_questions: List[str]
    study_plan: dict
    generated_at: str

@app.on_event("startup")
async def startup_event():
    await db_manager.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await db_manager.disconnect()

@app.get("/")
async def root():
    return {"message": "Interview Research Assistant API", "version": "1.0.0"}

@app.post("/research", response_model=ResearchResponse)
async def research_company(request: ResearchRequest, background_tasks: BackgroundTasks):
    """Main endpoint to research company interview data"""
    try:
        # Check if we have cached data
        cached_data = await db_manager.get_company_data(request.company_name, request.role)
        
        if not cached_data:
            # Scrape fresh data
            interview_data = await scrape_company_data(request.company_name, request.role)
            
            # Save to database
            background_tasks.add_task(
                db_manager.save_company_data, 
                interview_data
            )
        else:
            interview_data = cached_data
        
        # AI processing
        ai_synthesis = ai_processor.synthesize_interview_data(interview_data)
        custom_questions = ai_processor.generate_custom_questions(
            request.company_name, 
            request.role, 
            request.experience_level
        )
        study_plan = ai_processor.create_study_plan(interview_data, request.days_to_prepare)
        
        # Prepare response
        response_data = {
            'company_name': request.company_name,
            'role': request.role,
            'interview_data': interview_data,
            'ai_synthesis': ai_synthesis,
            'custom_questions': custom_questions,
            'study_plan': study_plan,
            'generated_at': str(datetime.datetime.utcnow())
        }
        
        # Save generated report
        background_tasks.add_task(
            db_manager.save_generated_report,
            response_data
        )
        
        return ResearchResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")

@app.get("/companies")
async def get_companies():
    """Get list of all researched companies"""
    try:
        companies = await db_manager.get_all_companies()
        return {"companies": companies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch companies: {str(e)}")

async def scrape_company_data(company_name: str, role: str) -> dict:
    """Scrape company interview data from multiple sources"""
    scraped_data = {
        'company_name': company_name,
        'role': role,
        'sources': {}
    }
    
    # Scrape from different sources
    glassdoor_data = scraper.scrape_glassdoor_interviews(company_name, role)
    if glassdoor_data:
        scraped_data.update(glassdoor_data)
        scraped_data['sources']['glassdoor'] = True
    
    leetcode_data = scraper.scrape_leetcode_company(company_name)
    if leetcode_data:
        scraped_data['leetcode_data'] = leetcode_data
        scraped_data['sources']['leetcode'] = True
    
    general_data = scraper.scrape_general_sources(company_name, role)
    if general_data:
        scraped_data['general_sources'] = general_data
        scraped_data['sources']['general'] = True
    
    return scraped_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
