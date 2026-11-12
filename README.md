# AI Career & Placement Preparation Agent

An intelligent career preparation platform built using Machine Learning, Generative AI, RAG, and Agentic AI.

The platform analyzes resumes, recommends suitable career paths, identifies skill gaps, generates personalized learning roadmaps, and helps students prepare for placements through AI-powered mock interviews and performance evaluation.

## Main Modules

1. Resume Analysis and Document Upload
2. Career Recommendation
3. Skill Gap Analysis
4. Personalized Learning Roadmap
5. AI Mock Interview
6. Interview Performance Evaluation
7. Performance Tracking
8. Multi-Agent Career Workflow Orchestration

## Technology Stack

- **Frontend:** React.js, Vite
- **Backend:** Python, FastAPI
- **Machine Learning:** Scikit-learn, Pandas, NumPy
- **Generative AI:** Ollama, Qwen 2.5 3B
- **Embeddings:** Sentence Transformers
- **Vector Database:** ChromaDB
- **Database:** MongoDB Atlas
- **Model Storage:** Joblib
- **Resume Processing:** PyMuPDF, python-docx, python-multipart
- **Version Control:** Git and GitHub

## Project Status

### Phase 1: Development Environment Setup

- [x] Python virtual environment setup
- [x] Required libraries installed
- [x] Project folder structure created
- [x] Ollama setup with Qwen 2.5 3B

### Phase 2: Machine Learning Development

- [x] Career recommendation dataset creation
- [x] Data preprocessing and feature engineering
- [x] Career prediction model training
- [x] Model evaluation and accuracy analysis
- [x] Feature importance analysis
- [x] Model saved using Joblib
- [x] Career prediction using saved model

### Phase 3: Backend Development

- [x] FastAPI backend setup
- [x] Career prediction API
- [x] Skill gap analysis API
- [x] Personalized learning roadmap API
- [x] MongoDB Atlas integration
- [x] Learning progress tracking API
- [x] Ollama integration
- [x] AI career advice and chat APIs
- [x] RAG career advice API
- [x] Agentic Learning Plan API
- [x] Interview question generation API
- [x] Interview answer evaluation API
- [x] Adaptive follow-up question API
- [x] Complete mock interview API
- [x] Interview performance summary generation
- [x] Resume upload and document processing API
- [x] PDF text extraction using PyMuPDF
- [x] DOCX text extraction using python-docx
- [x] Resume file validation and error handling
- [x] Full multi-agent career workflow API
- [x] Career workflow continuation API

### Phase 4: Frontend Development

- [x] React + Vite setup
- [x] Skill assessment interface
- [x] Career recommendation dashboard
- [x] Skill gap analysis interface
- [x] Personalized learning roadmap display
- [x] Progress tracking with MongoDB persistence
- [x] AI Career Assistant chat interface
- [x] RAG knowledge assistant interface
- [x] Agentic Learning Agent integration
- [x] AI Mock Interview interface
- [x] Interview difficulty and question-count selection
- [x] Interview answer submission
- [x] AI evaluation and feedback display
- [x] Adaptive follow-up question display
- [x] Overall interview performance report
- [x] Resume upload interface
- [x] Automatic extraction of uploaded resume text
- [x] Extracted resume preview and manual editing
- [x] Full Career Workflow frontend integration

### Phase 5: Generative AI and RAG

- [x] Local LLM integration using Ollama
- [x] Sentence Transformers embeddings
- [x] ChromaDB vector database setup
- [x] Knowledge base creation
- [x] Document loading and chunking
- [x] Embedding generation and storage
- [x] Semantic document retrieval
- [x] Category-based retrieval
- [x] Source-aware RAG responses
- [x] RAG API integration
- [x] RAG frontend integration with source details

### Phase 6: Agentic AI Development

- [x] Resume Agent development
- [x] Resume analysis tools
- [x] LLM-based tool selection
- [x] Structured resume information extraction
- [x] Contact information extraction
- [x] Education and academic score extraction
- [x] Technical skill and proficiency extraction
- [x] Project name, description, and technology extraction
- [x] Work experience and internship extraction
- [x] Certification extraction
- [x] Achievement and award extraction
- [x] Resume statistics calculation
- [x] Deterministic factual resume report generation
- [x] Separate AI-generated resume improvement suggestions
- [x] Grounded suggestions designed to avoid fabricated achievements and metrics
- [x] Career Agent development
- [x] ML model integration with Career Agent
- [x] Learning Agent development
- [x] Structured learning plan generation
- [x] AI-generated learning guidance
- [x] Resume and Career workflow integration
- [x] Learning workflow integration
- [x] Agentic Learning Plan API
- [x] React dashboard integration with Learning Agent
- [x] Interview Agent development
- [x] AI-generated interview questions
- [x] AI-based interview answer evaluation
- [x] Adaptive follow-up question generation
- [x] Optimized evaluation and follow-up generation
- [x] Interview scoring and performance summary
- [x] React Mock Interview integration
- [x] Complete multi-agent career workflow orchestration
- [x] Career discovery and user-selected career goal modes
- [x] Resume-to-career-to-learning-to-interview integration
- [x] Career-specific skill gap analysis
- [x] Career-specific learning roadmap generation
- [x] Full Career Workflow frontend integration
- [x] PDF and DOCX resume upload integration
- [x] Automatic resume text extraction and frontend integration

### Phase 7: Testing and Deployment

- [x] PDF resume upload testing
- [x] DOCX resume upload testing
- [x] Unsupported file format validation testing
- [x] Resume Agent basic extraction and report generation testing
- [x] Resume Agent improvement suggestion testing
- [x] Career discovery workflow testing
- [x] Career goal selection workflow testing
- [x] Learning roadmap workflow testing
- [x] Interview question generation workflow testing
- [ ] Real-world resume structured extraction validation
- [ ] Complete end-to-end testing
- [ ] Complete multi-agent workflow testing
- [ ] Frontend and backend deployment
- [ ] Final documentation

## Current Agent Architecture

The project currently includes four developed agents:

1. **Resume Agent:** Extracts structured information from resumes, including contact details, education, technical skills, proficiency levels, projects, work experience, certifications, achievements, and resume statistics. Generates a factual resume report and separate improvement suggestions.

2. **Career Agent:** Uses the trained Machine Learning model to recommend suitable careers based on extracted resume skills.

3. **Learning Agent:** Generates personalized learning roadmaps using skill gap analysis and provides AI-powered learning guidance.

4. **Interview Agent:** Generates career-specific interview questions, evaluates candidate answers, generates adaptive follow-up questions, and provides performance reports.

The four agents are connected through a central orchestrator that coordinates the complete career preparation workflow.

## Current Agent Workflows

- **Resume + Career Workflow:** Connects resume analysis with ML-based career recommendation.
- **Learning Workflow:** Connects skill gap analysis with structured roadmap generation and AI learning guidance.
- **Interview Workflow:** Generates mock interviews, evaluates candidate answers, provides adaptive follow-up questions, and calculates overall interview performance.
- **Complete Career Workflow:** Coordinates Resume, Career, Learning, and Interview Agents to provide an integrated career preparation experience.
- **Career Discovery Mode:** Analyzes a resume and recommends suitable career options.
- **Career Goal Mode:** Allows users to select a target career and receive career-specific skill gap analysis, learning roadmaps, and interview preparation.
- **Resume Upload Workflow:** Accepts PDF and DOCX files, extracts their text, and places the extracted content in the editable resume input area.
- **Structured Resume Analysis:** Identifies important resume sections and generates a factual report separately from AI improvement suggestions.
- **Frontend Integration:** Provides interactive interfaces for resume upload, career workflows, learning plans, progress tracking, and AI-powered mock interviews.

## Current Backend APIs

| Endpoint | Purpose |
|---|---|
| `/predict-career` | Predicts a suitable career |
| `/skill-gap` | Analyzes skill gaps |
| `/learning-roadmap` | Generates a structured roadmap |
| `/agentic-learning-plan` | Generates an AI-powered learning plan |
| `/ai-career-advice` | Provides AI career advice |
| `/personalized-ai-advice` | Generates personalized advice |
| `/personalized-ai-chat` | Supports AI career conversations |
| `/rag-career-advice` | Answers questions using the knowledge base |
| `/save-progress` | Saves completed learning weeks |
| `/get-progress/{student_id}/{target_career}` | Retrieves learning progress |
| `/interview/questions` | Generates AI-powered interview questions |
| `/interview/evaluate` | Evaluates an interview answer |
| `/interview/follow-up` | Generates adaptive follow-up questions |
| `/interview/mock` | Runs a complete mock interview and generates a performance report |
| `/upload-resume` | Uploads PDF/DOCX resumes and extracts text |
| `/agents/full-career-workflow` | Executes the complete multi-agent career workflow |
| `/agents/continue-career-workflow` | Continues the workflow using a selected career goal |

## Important Project Notes

- The initial career recommendation model uses a synthetic dataset. Its predictions are experimental and are not validated real-world career suitability probabilities.
- Career skill requirements are illustrative benchmarks.
- Resume-based skill scores currently use skill presence as a proxy, not verified proficiency.
- The Resume Agent extracts explicitly stated proficiency levels; unspecified levels are not automatically classified as beginner.
- Resume facts are presented separately from AI-generated improvement suggestions.
- AI improvement suggestions are intended to avoid inventing qualifications, achievements, project features, or numerical results.
- The learning roadmap uses rule-based scheduling, with an LLM providing additional learning guidance.
- Interview evaluation scores are AI-generated assessments and should be treated as indicative feedback rather than objective measurements.
- The local Qwen 2.5 3B model is used for AI-powered features through Ollama.
- Resume uploads currently support text-based PDF and DOCX files, with a maximum file size of 10 MB.
- Scanned or image-based PDFs requiring OCR are not currently supported.
- Uploaded resume content is processed for text extraction and is not intentionally stored as a permanent uploaded file by the resume upload endpoint.

## Future Enhancements

- Integrate LangGraph for advanced agent workflows and state management.
- Improve career recommendations using real-world datasets.
- Add OCR support for scanned and image-based resumes.
- Improve resume parsing accuracy for complex resume layouts and tables.
- Validate structured resume extraction using diverse real-world resumes.
- Add advanced interview performance analytics.
- Introduce persistent interview history and progress tracking.
- Add more comprehensive automated testing.
- Deploy the complete application.

## Project Repository

GitHub: [AI Career Agent](https://github.com/PankajKumar2075/AI-Career-Agent)

---

**Project Status:** Phase 6 – Agentic AI Development (In Progress)

**Completed:** Machine Learning career prediction, RAG integration, four AI agents, complete multi-agent career workflow orchestration, resume PDF/DOCX upload and extraction, structured resume analysis implementation, and frontend/backend integration.
