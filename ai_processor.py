import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, List
import json
import datetime
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

class AIProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize LangChain model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7
        )
    
    def synthesize_interview_data(self, scraped_data: Dict) -> Dict:
        """Use AI to synthesize and enhance scraped interview data"""

        prompt_template = """
        You are an expert interview preparation consultant. Based on the following scraped interview data, 
        create a comprehensive interview preparation guide.

        Scraped Data:
        {scraped_data}

        Please provide a structured response with:
        1. Interview Process Overview
        2. Key Technical Areas to Focus
        3. Common Questions (Technical & Behavioral)
        4. Preparation Strategy
        5. Timeline Recommendations
        6. Success Tips

        Make it actionable and specific to the company/role.
        """

        try:
            prompt = PromptTemplate(
                input_variables=["scraped_data"],
                template=prompt_template
            )
            # Use the new RunnableSequence API
            chain = prompt | self.llm
            response = chain.invoke({"scraped_data": json.dumps(scraped_data, indent=2)})
            return self._parse_ai_response(response.content if hasattr(response, "content") else str(response))
        except Exception as e:
            print(f"Error in AI processing: {e}")
            return self._fallback_synthesis(scraped_data)
    
    # ...existing code...
    def generate_custom_questions(self, company_name: str, role: str, experience_level: str) -> List[str]:
        """Generate custom interview questions based on company and role"""

        prompt = f"""
        Generate 10 specific interview questions for a {role} position at {company_name} 
        for someone with {experience_level} experience level.

        Include:
        - 3 technical questions specific to the role
        - 3 behavioral questions relevant to company culture
        - 2 system design questions (if applicable)
        - 2 situational questions

        Format as a JSON list of questions.
        """

        try:
            response = self.model.generate_content(prompt)
            try:
                questions = json.loads(response.text)
            except Exception:
                # Fallback: split lines if not valid JSON
                questions = [q.strip("-• ") for q in response.text.splitlines() if q.strip()]
            return questions if isinstance(questions, list) else []
        except Exception as e:
            print(f"Error generating questions: {e}")
            return self._fallback_questions(company_name, role)

    
    def create_study_plan(self, interview_data: Dict, days_to_prepare: int) -> Dict:
        """Create a personalized study plan"""
        
        prompt = f"""
        Create a {days_to_prepare}-day interview preparation plan based on this interview data:
        
        {json.dumps(interview_data, indent=2)}
        
        Structure the plan as:
        - Daily goals and tasks
        - Resource recommendations
        - Practice schedule
        - Mock interview timeline
        
        Return as structured JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Parse and structure the response
            return {"study_plan": response.text, "duration": days_to_prepare}
        except Exception as e:
            print(f"Error creating study plan: {e}")
            return self._fallback_study_plan(days_to_prepare)
    
    def _parse_ai_response(self, response: str) -> Dict:
        """Parse AI response into structured format"""
        # Try JSON first
        try:
            data = json.loads(response)
            return {
                'overview': data.get('overview', ''),
                'technical_areas': data.get('technical_areas', []),
                'questions': data.get('questions', []),
                'strategy': data.get('strategy', ''),
                'timeline': data.get('timeline', ''),
                'tips': data.get('tips', [])
            }
        except Exception:
            pass  # Not JSON, fallback to text parsing

        # Fallback: simple section parsing
        sections = response.split('\n\n')
        parsed = {
            'overview': '',
            'technical_areas': [],
            'questions': [],
            'strategy': '',
            'timeline': '',
            'tips': []
        }
        current_section = 'overview'
        for section in sections:
            lower = section.lower()
            if 'technical areas' in lower:
                current_section = 'technical_areas'
            elif 'questions' in lower:
                current_section = 'questions'
            elif 'strategy' in lower:
                current_section = 'strategy'
            elif 'timeline' in lower:
                current_section = 'timeline'
            elif 'tips' in lower:
                current_section = 'tips'

            if current_section in ['technical_areas', 'questions', 'tips']:
                parsed[current_section].extend([
                    line.strip('-• 1234567890.').strip()
                    for line in section.split('\n')
                    if line.strip() and (line.strip().startswith('-') or line.strip()[0].isdigit())
                ])
            else:
                parsed[current_section] = section.strip()
        return parsed
    
    def _fallback_synthesis(self, scraped_data: Dict) -> Dict:
        """Fallback synthesis when AI fails"""
        return {
            'overview': f"Interview preparation guide for {scraped_data.get('company_name', 'Unknown Company')}",
            'technical_areas': scraped_data.get('technical_topics', []),
            'questions': scraped_data.get('behavioral_questions', []),
            'strategy': "Focus on technical skills and behavioral preparation",
            'timeline': "2-4 weeks recommended preparation time",
            'tips': scraped_data.get('tips', [])
        }
    
    def _fallback_questions(self, company_name: str, role: str) -> List[str]:
        """Fallback questions when AI generation fails"""
        return [
            f"What interests you about working at {company_name}?",
            f"How would you approach a typical {role} challenge?",
            "Describe your experience with relevant technologies",
            "How do you handle working in a team environment?",
            "What's your approach to learning new technologies?"
        ]
    
    def _fallback_study_plan(self, days: int) -> Dict:
        """Fallback study plan when AI generation fails"""
        return {
            'study_plan': f"Structured {days}-day preparation plan with daily goals",
            'duration': days
        }
