# AI Career & Placement Preparation Agent

An intelligent career preparation platform built using Machine Learning, Generative AI, RAG, and Agentic AI.

The platform analyzes resumes, recommends suitable career paths, identifies skill gaps, generates personalized learning roadmaps, and helps students prepare for placements.

## Main Modules

1. Resume Analysis
2. Career Recommendation
3. Skill Gap Analysis
4. Personalized Learning Roadmap
5. AI Mock Interview
6. Performance Tracking

## Technology Stack

- **Frontend:** React.js, Vite
- **Backend:** Python, FastAPI
- **Machine Learning:** Scikit-learn, Pandas, NumPy
- **Generative AI:** Ollama, Qwen 2.5 3B
- **Embeddings:** Sentence Transformers
- **Vector Database:** ChromaDB
- **Database:** MongoDB Atlas
- **Model Storage:** Joblib
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
- [x] Career Agent development
- [x] ML model integration with Career Agent
- [x] Learning Agent development
- [x] Structured learning plan generation
- [x] AI-generated learning guidance
- [x] Resume and Career workflow integration
- [x] Learning workflow integration
- [x] Agentic Learning Plan API
- [x] React dashboard integration with Learning Agent
- [ ] Interview Agent development
- [ ] Complete multi-agent orchestration
- [ ] Advanced agent tool integration

### Phase 7: Testing and Deployment

- [ ] End-to-end testing
- [ ] Agent workflow testing
- [ ] Frontend and backend deployment
- [ ] Final documentation

## Current Agent Architecture

The project currently includes three developed agents:

1. **Resume Agent:** Extracts skills, projects, and resume statistics using resume analysis tools.
2. **Career Agent:** Uses the trained Machine Learning model to recommend a career based on extracted resume skills.
3. **Learning Agent:** Generates personalized learning roadmaps using skill gap analysis and provides AI-powered learning guidance.

**Upcoming Agent:**

4. **Interview Agent:** Will generate interview questions, evaluate candidate answers, and provide personalized feedback.

## Current Agent Workflows

- **Resume + Career Workflow:** Connects resume analysis with ML-based career recommendation.
- **Learning Workflow:** Connects skill gap analysis with structured roadmap generation and AI learning guidance.
- **Frontend Integration:** Displays personalized learning plans and supports learning progress tracking.

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

## Important Project Notes

- The initial career recommendation model uses a synthetic dataset. Its predictions are experimental and are not validated real-world career suitability probabilities.
- Career skill requirements are illustrative benchmarks.
- Resume-based skill scores currently use skill presence as a proxy, not verified proficiency.
- The learning roadmap uses rule-based scheduling, with an LLM providing additional learning guidance.

## Future Enhancements

- Develop the Interview Agent.
- Build complete multi-agent orchestration.
- Integrate LangGraph for advanced agent workflows.
- Add resume upload and document processing through the frontend.
- Improve career recommendations using real-world datasets.
- Add interview performance analytics.
- Deploy the complete application.

## Project Repository

GitHub: https://github.com/PankajKumar2075/AI-Career-Agent

---

**Project Status:** Phase 6 – Agentic AI Development (In Progress)