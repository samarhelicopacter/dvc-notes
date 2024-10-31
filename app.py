import requests
import streamlit as st
from PyPDF2 import PdfReader
from typing import Dict

# Set page config must be the first Streamlit command
st.set_page_config(page_title="DVCNotes", page_icon="📝", layout="wide")

# Initialize API key directly from secrets
api_key = st.secrets["ANTHROPIC_API_KEY"]

class NotesProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "x-api-key": self.api_key
        }

    def process_notes(self, text: str) -> Dict:
        """Process text using Anthropic API to generate strategically aligned meeting notes."""
        system_prompt = """You are DVCNotes, a specialized meeting notes assistant for DVC that connects discussions to institutional goals. Create detailed notes that align with DVC's mission to "inspire, educate, and empower students to transform their lives and their communities."

        # [Committee/Department] Meeting Notes: [Date]
        **Respectfully submitted by: [Note taker name]**

        ## Quick Strategic Overview
        Brief summary connecting key meeting points to DVC's strategic goals:
        * Student Learning & Success
        * Equity & Institutional Culture
        * Innovation & Strategic Growth
        * Community Engagement & Partnerships

        ## Attendance
        * Present in person: [Names]
        * Present online: [Names]

        ## Formal Approvals
        1. Agenda Approval
            a. Motion by: [Name]
            b. Second: [Name]
            c. Outcome: [Result]

        2. Previous Meeting Notes
            a. Motion by: [Name]
            b. Second: [Name]
            c. Outcome: [Result]

        ## Key Discussions & Updates
        For each major topic, include:
        * **Topic**: [Clear title]
            - Detailed explanation
            - Strategic alignment (how this supports DVC goals)
            - Impact on student success
            - Requirements/deadlines
            - Resources needed
            - Who is responsible
            - Next steps

        For any programs/initiatives:
        * **Program Name**:
            - Purpose and goals
            - Alignment with college mission
            - Implementation timeline
            - Impact on students/faculty
            - Resource requirements
            - Success metrics
            - Contact person

        For acronyms and technical terms:
        * **[Acronym]** ([Full Name]):
            - Definition
            - Purpose
            - Impact on college goals
            - Requirements
            - Timeline
            - Resources

        ## Action Items & Strategic Initiatives
        For each action item:
        * **Action Required**:
            - Specific task
            - Strategic goal alignment
            - Responsible party
            - Timeline/deadline
            - Resources needed
            - Success measures
            - Follow-up plan

        ## Important Dates & Deadlines
        * **[Date]**: [Event/Deadline]
            - Purpose
            - Strategic importance
            - Who needs to participate
            - Required preparation
            - Resources available
            - Contact person

        ## Committee Updates
        For each committee:
        * **[Committee Name]**:
            - Key updates
            - Strategic initiatives
            - Action items
            - Alignment with college goals
            - Next steps
            - Contact person

        ## Future Planning
        * Topics for next meeting
        * Long-term strategic initiatives
        * Required preparation
        * Resource needs

        ## Resources & Support
        * Contact information
        * Available training
        * Support services
        * Reference materials

        Guidelines:
        - Connect discussions to DVC's mission and goals
        - Highlight equity considerations
        - Note student success impacts
        - Include strategic context
        - Explain all acronyms
        - Provide full context
        - Track all deadlines
        - Note resource needs
        - Specify responsible parties
        - Include success metrics
        - Use clear formatting
        - Bold (**) key items

        Key DVC Strategic Goals to Reference:
        1. Student Learning & Success
        - Increase completion rates
        - Enhance support services
        - Improve student experience
        
        2. Equity & Institutional Culture
        - Promote inclusive practices
        - Address achievement gaps
        - Support diverse needs
        
        3. Innovation & Strategic Growth
        - Implement new technologies
        - Enhance programs
        - Improve processes
        
        4. Community Engagement
        - Build partnerships
        - Serve local needs
        - Enhance outreach

        Format notes to be both comprehensive and strategically aligned with DVC's mission and goals."""

        try:
            data = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 4096,
                "system": system_prompt,
                "messages": [
                    {
                        "role": "user",
                        "content": f"Please analyze this transcript and create detailed, strategically-aligned notes:\n\n{text}"
                    }
                ]
            }

            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data
            )
            
            if response.status_code == 200:
                content = response.json()['content'][0]['text']
                sections = {
                    "summary": content
                }
                return sections
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Error processing notes: {str(e)}")
            return None

def extract_text_from_pdf(file) -> str:
    """Extract text from a PDF file using PyPDF2."""
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting PDF text: {str(e)}")
        return ""

def main():
    processor = NotesProcessor(api_key)

    # Enhanced Custom CSS for DVC branding
    st.markdown("""
        <style>
        /* Main theme colors matching DVC green */
        :root {
            --dvc-green-dark: #006341;
            --dvc-green-light: #A2D5C6;
            --dvc-gray: #666666;
        }
        
        /* Global styles */
        .stApp {
            background-color: #ffffff;
        }
        
        .main .block-container {
            padding-top: 2rem;
        }
        
        /* Headers */
        h1, h2, h3, h4 {
            color: var(--dvc-green-dark);
            font-weight: 600;
        }
        
        /* Title area */
        .app-title {
            background: linear-gradient(90deg, var(--dvc-green-dark), var(--dvc-green-light));
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        /* Buttons */
        .stButton>button {
            background: var(--dvc-green-dark);
            color: white;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background: var(--dvc-green-light);
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        /* Text Areas */
        .stTextArea textarea {
            border: 2px solid var(--dvc-green-dark);
            border-radius: 5px;
        }
        
        .stTextArea textarea:focus {
            border-color: var(--dvc-green-light);
            box-shadow: 0 0 5px rgba(102,192,143,0.2);
        }
        
        /* Success messages */
        .success-box {
            background-color: #E5FFE5;
            border: 1px solid #28a745;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: var(--dvc-green-dark);">DVC Mission Statement</h2>
            <p style="font-size: 1.1rem; color: var(--dvc-green-dark);">
                We inspire, educate, and empower students to transform their lives and their communities.
                We guide students to achieve their goals by awarding degrees and certificates, preparing them
                for transfer to four-year colleges and universities, facilitating entrance to and advancement
                in careers, and fostering personal growth.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Header with gradient background
    st.markdown("""
        <div class="app-title">
            <h1 style="margin:0;">DVCNotes</h1>
            <p style="margin:0;font-size:1.2rem;">An AI-driven tool that transforms meeting transcripts into comprehensive, strategically aligned summaries for DVC.</p>
        </div>
    """, unsafe_allow_html=True)

    # Input section with PDF and text options
    st.markdown("### 📝 Input Text or PDF")
    text_input = st.text_area(
        "Paste your text here:",
        height=200,
        placeholder="Enter meeting transcript, lecture notes, or any text to process..."
    )
    
    uploaded_pdf = st.file_uploader("Or upload a PDF file", type="pdf")

    if uploaded_pdf:
        text_input = extract_text_from_pdf(uploaded_pdf)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ Generate Notes", use_container_width=True):
            if text_input and text_input.strip():
                with st.spinner("🔄 Processing your notes..."):
                    notes_data = processor.process_notes(text_input)
                    if notes_data:
                        st.markdown("### 📋 Summary")
                        if notes_data["summary"]:
                            st.markdown(notes_data["summary"])
            else:
                st.warning("Please enter some text to process.")

if __name__ == "__main__":
    main()
