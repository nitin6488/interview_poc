import streamlit as st
import requests
import json
from datetime import datetime
import plotly.express as px
import pandas as pd

# Configure Streamlit page
st.set_page_config(
    page_title="Interview Research Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .company-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

class InterviewResearchApp:
    def __init__(self):
        self.api_base_url = "http://localhost:8000"
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'research_results' not in st.session_state:
            st.session_state.research_results = None
        if 'companies_researched' not in st.session_state:
            st.session_state.companies_researched = []
    
    def main(self):
        """Main application interface"""
        st.markdown('<h1 class="main-header">🎯 Interview Research Assistant</h1>', unsafe_allow_html=True)
        
        # Sidebar
        self.render_sidebar()
        
        # Main content area
        tab1, tab2, tab3, tab4 = st.tabs(["🔍 Research", "📊 Results", "📚 Study Plan", "📈 Analytics"])
        
        with tab1:
            self.render_research_tab()
        
        with tab2:
            self.render_results_tab()
        
        with tab3:
            self.render_study_plan_tab()
        
        with tab4:
            self.render_analytics_tab()
    
    def render_sidebar(self):
        """Render sidebar with options"""
        st.sidebar.title("🎯 Navigation")
        
        # Quick company selection
        st.sidebar.subheader("Quick Start")
        popular_companies = ["Google", "Amazon", "Microsoft", "Apple", "Meta", "Netflix", "Tesla", "Uber"]
        selected_company = st.sidebar.selectbox("Select Popular Company", [""] + popular_companies)
        
        if selected_company and st.sidebar.button("Quick Research"):
            self.perform_research(selected_company, "Software Engineer", "Mid-level", 30)
        
        # Settings
        st.sidebar.subheader("⚙️ Settings")
        self.api_status = self.check_api_status()
        status_color = "🟢" if self.api_status else "🔴"
        st.sidebar.write(f"API Status: {status_color}")
        
        # Recent searches
        if st.session_state.companies_researched:
            st.sidebar.subheader("📚 Recent Searches")
            for company in st.session_state.companies_researched[-5:]:
                st.sidebar.write(f"• {company}")
    
    def render_research_tab(self):
        """Render the main research interface"""
        st.subheader("🔍 Company Interview Research")
        
        # Research form
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("Company Name", placeholder="e.g., Google, Amazon, Microsoft")
            role = st.text_input("Role", value="Software Engineer", placeholder="e.g., Software Engineer, Data Scientist")
        
        with col2:
            experience_level = st.selectbox("Experience Level", ["Entry-level", "Mid-level", "Senior-level", "Lead/Principal"])
            days_to_prepare = st.slider("Days to Prepare", min_value=7, max_value=90, value=30)
        
        # Research button
        if st.button("🚀 Start Research", type="primary"):
            if company_name:
                self.perform_research(company_name, role, experience_level, days_to_prepare)
            else:
                st.error("Please enter a company name")
        
        # Display recent API activity
        if st.session_state.research_results:
            st.success("✅ Latest research completed successfully!")
            st.info(f"Last researched: {st.session_state.research_results.get('company_name')} - {st.session_state.research_results.get('role')}")
    
    def render_results_tab(self):
        """Render research results"""
        if not st.session_state.research_results:
            st.info("🔍 No research results yet. Please conduct a research first.")
            return
        
        results = st.session_state.research_results
        
        # Company overview
        st.markdown(f"""
        <div class="company-card">
            <h2>{results['company_name']} - {results['role']}</h2>
            <p>Generated: {results.get('generated_at', 'Unknown')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Interview process
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Interview Process")
            interview_data = results.get('interview_data', {})
            process_steps = interview_data.get('process_steps', [])
            
            for i, step in enumerate(process_steps, 1):
                st.write(f"{i}. {step}")
        
        with col2:
            st.subheader("🎯 Technical Focus Areas")
            technical_topics = interview_data.get('technical_topics', [])
            
            for topic in technical_topics:
                st.write(f"• {topic}")
        
        # AI Synthesis
        st.subheader("🤖 AI-Generated Insights")
        ai_synthesis = results.get('ai_synthesis', {})
        
        if ai_synthesis:
            # Display AI insights in expandable sections
            with st.expander("📖 Interview Overview"):
                st.write(ai_synthesis.get('overview', 'No overview available'))
            
            with st.expander("💡 Preparation Strategy"):
                st.write(ai_synthesis.get('strategy', 'No strategy available'))
            
            with st.expander("⏰ Timeline Recommendations"):
                st.write(ai_synthesis.get('timeline', 'No timeline available'))
        
        # Custom Questions
        st.subheader("❓ Custom Interview Questions")
        custom_questions = results.get('custom_questions', [])
        
        if custom_questions:
            for i, question in enumerate(custom_questions, 1):
                if isinstance(question, dict) and "question" in question:
                    st.write(f"{i}. {question['question']}")
                else:
                    st.write(f"{i}. {question}")
        else:
            st.info("No custom questions generated")
        
        # Behavioral Questions
        behavioral_questions = interview_data.get('behavioral_questions', [])
        if behavioral_questions:
            st.subheader("🗣️ Common Behavioral Questions")
            for question in behavioral_questions:
                st.write(f"• {question}")
        
        # Tips and Advice
        tips = interview_data.get('tips', [])
        if tips:
            st.subheader("💡 Success Tips")
            for tip in tips:
                st.write(f"• {tip}")
    
    def render_study_plan_tab(self):
        """Render study plan interface"""
        if not st.session_state.research_results:
            st.info("🔍 No research results yet. Please conduct a research first.")
            return
        
        results = st.session_state.research_results
        study_plan = results.get('study_plan', {})
        
        st.subheader("📚 Personalized Study Plan")
        
        # Study plan overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>Duration</h4>
                <h2>{} days</h2>
            </div>
            """.format(study_plan.get('duration', 'N/A')), unsafe_allow_html=True)
        
        with col2:
            difficulty = results.get('interview_data', {}).get('difficulty_level', 'Medium')
            st.markdown(f"""
            <div class="metric-card">
                <h4>Difficulty</h4>
                <h2>{difficulty}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            topics_count = len(results.get('interview_data', {}).get('technical_topics', []))
            st.markdown(f"""
            <div class="metric-card">
                <h4>Focus Areas</h4>
                <h2>{topics_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Study plan details
        st.subheader("📅 Detailed Study Plan")
        study_plan_text = study_plan.get('study_plan', 'No detailed study plan available')
        try:
            plan_json = json.loads(study_plan_text)
            st.json(plan_json)
        except Exception:
            st.text_area("Study Plan Details", study_plan_text, height=300)
        
        # Progress tracking
        st.subheader("📊 Progress Tracking")
        
        # Create sample progress data
        days_completed = st.slider("Days Completed", 0, study_plan.get('duration', 30), 0)
        progress_percentage = (days_completed / study_plan.get('duration', 30)) * 100
        
        # Progress bar
        st.progress(progress_percentage / 100)
        st.write(f"Progress: {progress_percentage:.1f}% ({days_completed}/{study_plan.get('duration', 30)} days)")
        
        # Daily checklist (mock)
        st.subheader("✅ Today's Tasks")
        tasks = [
            "Review data structures (Arrays, Linked Lists)",
            "Practice 3 coding problems",
            "Read about company culture",
            "Practice behavioral questions (STAR method)",
            "System design study (30 minutes)"
        ]
        
        for task in tasks:
            completed = st.checkbox(task, key=f"task_{hash(task)}")
    
    def render_analytics_tab(self):
        """Render analytics and insights"""
        st.subheader("📈 Research Analytics")
        
        # Mock analytics data for demonstration
        if not st.session_state.companies_researched:
            st.info("No analytics data available yet. Complete some research first.")
            return
        
        # Companies researched over time
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏢 Companies Researched")
            companies_df = pd.DataFrame({
                'Company': st.session_state.companies_researched[-10:],
                'Research_Date': pd.date_range(end=datetime.now(), periods=len(st.session_state.companies_researched[-10:]))
            })
            
            if not companies_df.empty:
                fig = px.bar(companies_df, x='Company', y=[1]*len(companies_df), 
                           title="Recent Company Research")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 Difficulty Distribution")
            # Mock difficulty data
            difficulty_data = {
                'Difficulty': ['Easy', 'Medium', 'Hard', 'Very Hard'],
                'Count': [2, 5, 8, 3]
            }
            difficulty_df = pd.DataFrame(difficulty_data)
            
            fig = px.pie(difficulty_df, values='Count', names='Difficulty', 
                        title="Interview Difficulty Levels")
            st.plotly_chart(fig, use_container_width=True)
        
        # Success metrics
        st.subheader("🎯 Success Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Research", len(st.session_state.companies_researched), "+2")
        
        with col2:
            st.metric("Avg Prep Time", "25 days", "-3 days")
        
        with col3:
            st.metric("Success Rate", "78%", "+5%")
        
        with col4:
            st.metric("Questions Generated", "150+", "+25")
    
    def perform_research(self, company_name: str, role: str, experience_level: str, days_to_prepare: int):
        """Perform research API call"""
        with st.spinner(f"🔍 Researching {company_name} interview process..."):
            try:
                # Prepare request data
                request_data = {
                    "company_name": company_name,
                    "role": role,
                    "experience_level": experience_level,
                    "days_to_prepare": days_to_prepare
                }
                
                # Make API call
                response = requests.post(
                    f"{self.api_base_url}/research",
                    json=request_data,
                    timeout=60
                )
                
                if response.status_code == 200:
                    results = response.json()
                    st.session_state.research_results = results
                    
                    # Update companies researched
                    if company_name not in st.session_state.companies_researched:
                        st.session_state.companies_researched.append(company_name)
                    
                    st.success(f"✅ Research completed for {company_name}!")
                    st.balloons()
                    
                else:
                    st.error(f"❌ Research failed: {response.status_code}")
                    st.error(response.text)
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Please ensure the FastAPI server is running on localhost:8000")
                self.show_mock_results(company_name, role, experience_level, days_to_prepare)
                
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                self.show_mock_results(company_name, role, experience_level, days_to_prepare)
    
    def show_mock_results(self, company_name: str, role: str, experience_level: str, days_to_prepare: int):
        """Show mock results when API is not available"""
        st.info("🔧 API not available. Showing mock results for demonstration.")
        
        mock_results = {
            'company_name': company_name,
            'role': role,
            'interview_data': {
                'company_name': company_name,
                'role': role,
                'process_steps': [
                    "Initial Screening Call",
                    "Technical Phone Interview",
                    "Onsite/Virtual Interviews (3-4 rounds)",
                    "Final Decision"
                ],
                'technical_topics': [
                    "Data Structures and Algorithms",
                    "System Design",
                    "Problem Solving",
                    "Coding Best Practices",
                    "Company-specific Technologies"
                ],
                'behavioral_questions': [
                    f"Why do you want to work at {company_name}?",
                    "Tell me about a challenging project you worked on",
                    "How do you handle tight deadlines?",
                    "Describe a time you had to work with a difficult team member",
                    "Where do you see yourself in 5 years?"
                ],
                'tips': [
                    f"Research {company_name}'s mission and values",
                    "Practice coding on a whiteboard or shared screen",
                    "Prepare STAR method examples for behavioral questions",
                    "Ask insightful questions about the role and team",
                    "Be ready to discuss your past projects in detail"
                ],
                'difficulty_level': 'Hard'
            },
            'ai_synthesis': {
                'overview': f"Interview process at {company_name} is comprehensive and challenging, focusing on both technical skills and cultural fit.",
                'strategy': "Focus on algorithm practice, system design fundamentals, and behavioral question preparation using the STAR method.",
                'timeline': f"With {days_to_prepare} days to prepare, allocate 60% time to technical preparation and 40% to behavioral/company research."
            },
            'custom_questions': [
                f"How would you scale a system at {company_name}?",
                f"Describe your experience with technologies used at {company_name}",
                "Walk me through your approach to debugging a complex issue",
                f"How do you stay updated with technology trends relevant to {company_name}?",
                "Explain a technical decision you made and its impact"
            ],
            'study_plan': {
                'duration': days_to_prepare,
                'study_plan': f"""
{days_to_prepare}-Day Interview Preparation Plan for {company_name} - {role}

Week 1: Foundation Building
- Days 1-3: Data Structures Review (Arrays, LinkedLists, Trees, Graphs)
- Days 4-7: Algorithm Fundamentals (Sorting, Searching, Dynamic Programming)

Week 2: Advanced Topics
- Days 8-10: System Design Basics
- Days 11-14: Company-specific Technology Research

Week 3: Practice & Mock Interviews
- Days 15-18: Coding Practice (LeetCode, HackerRank)
- Days 19-21: Behavioral Question Practice

Week 4: Final Preparation
- Days 22-25: Mock Interviews
- Days 26-28: Company Culture & Values Research
- Days 29-{days_to_prepare}: Final Review & Relaxation
                """
            },
            'generated_at': datetime.now().isoformat()
        }
        
        st.session_state.research_results = mock_results
        if company_name not in st.session_state.companies_researched:
            st.session_state.companies_researched.append(company_name)
    
    def check_api_status(self):
        """Check if API is running"""
        try:
            response = requests.get(f"{self.api_base_url}/", timeout=5)
            print("API status code:", response.status_code)
            return response.status_code == 200
        except Exception as e:
            print("API status check failed:", e)
            return False

# Run the application
if __name__ == "__main__":
    app = InterviewResearchApp()
    app.main()