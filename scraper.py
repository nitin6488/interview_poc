import requests
from bs4 import BeautifulSoup
import time
import json
from typing import Dict, List
from dataclasses import dataclass
import re

@dataclass
class InterviewData:
    company_name: str
    role: str
    process_steps: List[str]
    technical_topics: List[str]
    behavioral_questions: List[str]
    tips: List[str]
    difficulty_level: str
    source_urls: List[str]

class InterviewScraper:
    def __init__(self, user_agent: str, timeout: int = 30):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.timeout = timeout
    
    def scrape_glassdoor_interviews(self, company_name: str, role: str = "") -> Dict:
        """Scrape interview data from Glassdoor (simplified simulation)"""
        # Note: This is a simplified simulation. In production, you'd need:
        # 1. Proper Glassdoor API access or selenium for dynamic content
        # 2. Handle rate limiting and captchas
        # 3. Respect robots.txt
        
        try:
            # Simulate Glassdoor search
            search_url = f"https://www.glassdoor.com/Interview/{company_name.replace(' ', '-')}-interview-questions-SRCH_KE0,{len(company_name)}.htm"
            
            # For POC, return mock data based on common patterns
            mock_data = self._generate_mock_glassdoor_data(company_name, role)
            return mock_data
            
        except Exception as e:
            print(f"Error scraping Glassdoor: {e}")
            return {}
    
    def scrape_leetcode_company(self, company_name: str) -> Dict:
        """Scrape company-specific questions from LeetCode"""
        try:
            # Mock LeetCode company data
            mock_data = {
                'technical_questions': [
                    f"Two Sum - {company_name} favorite",
                    f"System Design - {company_name} specific",
                    f"Dynamic Programming - {company_name} style",
                ],
                'difficulty_distribution': {
                    'easy': 30,
                    'medium': 50,
                    'hard': 20
                },
                'frequency': 'high'
            }
            return mock_data
        except Exception as e:
            print(f"Error scraping LeetCode: {e}")
            return {}
    
    def scrape_general_sources(self, company_name: str, role: str) -> Dict:
        """Scrape from multiple general sources"""
        sources_data = {}
        
        # GeeksforGeeks
        gfg_data = self._scrape_geeksforgeeks(company_name)
        if gfg_data:
            sources_data['geeksforgeeks'] = gfg_data
        
        # InterviewBit
        ib_data = self._scrape_interviewbit(company_name)
        if ib_data:
            sources_data['interviewbit'] = ib_data
        
        return sources_data
    
    def _scrape_geeksforgeeks(self, company_name: str) -> Dict:
        """Scrape GeeksforGeeks interview experiences"""
        try:
            # Mock GeeksforGeeks data
            return {
                'interview_experiences': [
                    f"{company_name} Software Engineer Interview Experience",
                    f"{company_name} Internship Interview Questions",
                ],
                'technical_prep': [
                    "Data Structures and Algorithms",
                    "System Design",
                    "Object-Oriented Programming",
                ],
                'tips': [
                    "Practice coding problems daily",
                    "Understand company culture",
                    "Prepare behavioral questions",
                ]
            }
        except Exception as e:
            print(f"Error scraping GeeksforGeeks: {e}")
            return {}
    
    def _scrape_interviewbit(self, company_name: str) -> Dict:
        """Scrape InterviewBit company data"""
        try:
            return {
                'common_questions': [
                    f"Tell me about yourself - {company_name} version",
                    f"Why {company_name}?",
                    "Technical problem solving approach",
                ],
                'preparation_timeline': "2-3 months",
                'success_rate': "65%"
            }
        except Exception as e:
            print(f"Error scraping InterviewBit: {e}")
            return {}
    
    def _generate_mock_glassdoor_data(self, company_name: str, role: str) -> Dict:
        """Generate realistic mock data for demonstration"""
        company_specific_data = {
            'google': {
                'process_steps': [
                    "Phone/Video Screen with Recruiter",
                    "Technical Phone Interview",
                    "Onsite Interviews (4-5 rounds)",
                    "Hiring Committee Review"
                ],
                'technical_topics': [
                    "Algorithms and Data Structures",
                    "System Design",
                    "Coding in preferred language",
                    "Problem-solving approach"
                ],
                'difficulty_level': "Very Hard"
            },
            'amazon': {
                'process_steps': [
                    "Online Assessment",
                    "Phone Interview",
                    "Virtual Onsite (3-4 rounds)",
                    "Bar Raiser Round"
                ],
                'technical_topics': [
                    "Leadership Principles",
                    "Data Structures",
                    "System Design",
                    "Behavioral Questions"
                ],
                'difficulty_level': "Hard"
            },
            'microsoft': {
                'process_steps': [
                    "Recruiter Screen",
                    "Technical Phone Screen",
                    "Onsite Interviews (4-5 rounds)",
                    "Final Review"
                ],
                'technical_topics': [
                    "Coding Problems",
                    "System Design",
                    "Technical Discussion",
                    "Culture Fit"
                ],
                'difficulty_level': "Hard"
            }
        }
        
        default_data = {
            'process_steps': [
                "Initial Screening",
                "Technical Interview",
                "Final Round",
                "Offer Discussion"
            ],
            'technical_topics': [
                "Programming Fundamentals",
                "Problem Solving",
                "Technical Knowledge",
                "Communication Skills"
            ],
            'difficulty_level': "Medium"
        }
        
        base_data = company_specific_data.get(company_name.lower(), default_data)
        
        return {
            'company_name': company_name,
            'role': role or 'Software Engineer',
            'process_steps': base_data['process_steps'],
            'technical_topics': base_data['technical_topics'],
            'behavioral_questions': [
                "Tell me about yourself",
                f"Why do you want to work at {company_name}?",
                "Describe a challenging project you worked on",
                "How do you handle tight deadlines?",
                "Where do you see yourself in 5 years?"
            ],
            'tips': [
                f"Research {company_name}'s culture and values",
                "Practice coding problems on whiteboard",
                "Prepare STAR method examples",
                "Ask thoughtful questions about the role",
                "Be ready to discuss your projects in detail"
            ],
            'difficulty_level': base_data['difficulty_level'],
            'source_urls': ["https://glassdoor.com", "https://leetcode.com"]
        }