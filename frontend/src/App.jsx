
import { useState, useEffect } from "react";
import "./App.css";

const skillNames = [
  "Python",
  "SQL",
  "Machine_Learning",
  "React",
  "Node",
  "MongoDB",
  "Excel",
];

const careerOptions = [
  "ML Engineer",
  "Data Analyst",
  "Full Stack Developer",
];

function App() {
  const studentId = "student_001";

  const [skills, setSkills] = useState({
    Python: 5,
    SQL: 5,
    Machine_Learning: 5,
    React: 5,
    Node: 5,
    MongoDB: 5,
    Excel: 5,
  });

  const [targetCareer, setTargetCareer] = useState("ML Engineer");

  const [result, setResult] = useState(null);
  const [gapResult, setGapResult] = useState(null);
  const [roadmapResult, setRoadmapResult] = useState(null);
  const [completedWeeks, setCompletedWeeks] = useState({});

  const [loading, setLoading] = useState(false);
  const [gapLoading, setGapLoading] = useState(false);
  const [roadmapLoading, setRoadmapLoading] = useState(false);
  const [agenticLearningError, setAgenticLearningError] = useState("");

  const [error, setError] = useState("");
  const [gapError, setGapError] = useState("");
  const [roadmapError, setRoadmapError] = useState("");

  const totalWeeks = roadmapResult?.roadmap?.length || 0;

  const completedCount = roadmapResult?.roadmap
    ? roadmapResult.roadmap.filter(
        (item) => Boolean(completedWeeks[item.week])
      ).length
    : 0;

  const progressPercentage = totalWeeks > 0
    ? Math.round((completedCount / totalWeeks) * 100)
    : 0;


  const [question, setQuestion] = useState("");
  const [chatMessages, setChatMessages] = useState([]);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");


  const [ragQuestion, setRagQuestion] = useState("");
  const [ragAnswer, setRagAnswer] = useState("");
  const [ragLoading, setRagLoading] = useState(false);
  const [ragError, setRagError] = useState("");
  const [ragCategory, setRagCategory] = useState("");
  const [ragSources, setRagSources] = useState([]);
  const [ragTotalChunks, setRagTotalChunks] = useState(0);

  // Interview Agent states
const [interviewDifficulty, setInterviewDifficulty] = useState("medium");
const [interviewCount, setInterviewCount] = useState(3);
const [interviewQuestions, setInterviewQuestions] = useState([]);
const [interviewAnswers, setInterviewAnswers] = useState({});
const [interviewReport, setInterviewReport] = useState(null);
const [interviewLoading, setInterviewLoading] = useState(false);
const [interviewSubmitLoading, setInterviewSubmitLoading] = useState(false);
const [interviewError, setInterviewError] = useState("");
  

    useEffect(() => {
      loadSavedProgress();
    }, [targetCareer]);

  // Update skill levels
  const handleChange = (e) => {
    const { name, value } = e.target;

    setSkills((previousSkills) => ({
      ...previousSkills,
      [name]: Number(value),
    }));

    setGapResult(null);
    setResult(null);
    setRoadmapResult(null);
    setRoadmapError("");
  };

  // Career prediction
  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/predict-career",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(skills),
        }
      );

      if (!response.ok) {
        throw new Error("Career prediction failed.");
      }

      const data = await response.json();
      setResult(data);

    } catch (err) {
      setError("Could not connect to the career prediction API.");
    } finally {
      setLoading(false);
    }
  };

  // Skill gap analysis
  const handleGapSubmit = async (e) => {
    e.preventDefault();

    setGapLoading(true);
    setGapError("");
    setGapResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/skill-gap",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ...skills,
            target_career: targetCareer,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Skill gap analysis failed.");
      }

      const data = await response.json();
      setGapResult(data);

    } catch (err) {
      setGapError("Could not connect to the skill gap API.");
    } finally {
      setGapLoading(false);
    }
  };

  
// Generate AI-powered personalized learning plan
const handleRoadmapSubmit = async () => {
    setRoadmapLoading(true);
    setRoadmapError("");
    setRoadmapResult(null);

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/agentic-learning-plan",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    ...skills,
                    target_career: targetCareer,
                }),
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "AI learning plan generation failed."
            );
        }

        // Combine the Learning Agent response
        // with the existing roadmap UI structure.
        const learningPlan = {
            ...data.learning_plan,
            target_career: data.target_career,
            coverage_score: data.coverage_score,
            skill_gaps: data.skill_gaps,
        };

        setRoadmapResult(learningPlan);

        await loadSavedProgress();

    } catch (err) {
        console.error("Learning Agent Error:", err);

        setRoadmapError(
            err.message || "Could not generate the AI learning plan."
        );
    } finally {
        setRoadmapLoading(false);
    }
};


const handleWeekToggle = (week) => {
  setCompletedWeeks((previous) => {
    const updated = {
      ...previous,
      [week]: !previous[week],
    };

    saveProgressToDatabase(updated);

    return updated;
  });
};


  
const loadSavedProgress = async () => {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/get-progress/${studentId}/${encodeURIComponent(targetCareer)}`
    );

    if (!response.ok) {
      throw new Error("Could not retrieve progress");
    }

    const data = await response.json();

    const savedWeeks = {};

    data.completed_weeks.forEach((week) => {
      savedWeeks[week] = true;
    });

    setCompletedWeeks(savedWeeks);

  } catch (err) {
    console.error("Progress loading error:", err);
  }
};



const saveProgressToDatabase = async (updatedWeeks) => {
  try {
    const completed = Object.keys(updatedWeeks)
      .filter((week) => updatedWeeks[week])
      .map(Number);

    const response = await fetch(
      "http://127.0.0.1:8000/save-progress",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          student_id: studentId,
          target_career: targetCareer,
          completed_weeks: completed,
        }),
      }
    );

    if (!response.ok) {
      throw new Error("Could not save progress");
    }

    console.log("Progress saved successfully!");

  } catch (err) {
    console.error("Progress saving error:", err);
  }
};


const handleAIAdvice = async () => {
    if (!question.trim()) {
        setAiError("Please enter a question.");
        return;
    }

    const updatedMessages = [
        ...chatMessages,
        {
            role: "user",
            content: question.trim()
        }
    ].slice(-10);

    setChatMessages(updatedMessages);
    setQuestion("");
    setAiLoading(true);
    setAiError("");

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/personalized-ai-chat",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    ...skills,
                    messages: updatedMessages
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "AI request failed");
        }

        setChatMessages(prev => [
            ...prev,
            {
                role: "assistant",
                content: data.ai_response
            }
        ].slice(-10));

    } catch (error) {
        setAiError(error.message);
    } finally {
        setAiLoading(false);
    }
};


const handleRAGAdvice = async () => {
    if (!ragQuestion.trim()) {
        setRagError("Please enter a question.");
        return;
    }

    setRagLoading(true);
    setRagError("");
    setRagAnswer("");
    setRagSources([]);
    setRagTotalChunks(0);

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/rag-career-advice",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: ragQuestion,
                    category: ragCategory || null
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "RAG request failed");
        }

        setRagAnswer(data.answer);
        setRagSources(data.sources || []);
        setRagTotalChunks(data.total_chunks_used || 0);

    } catch (error) {
        setRagError(error.message);
    } finally {
        setRagLoading(false);
    }
};


// Generate career-specific interview questions
const handleGenerateInterview = async () => {
    setInterviewLoading(true);
    setInterviewError("");
    setInterviewQuestions([]);
    setInterviewAnswers({});
    setInterviewReport(null);

    try {
        const selectedSkills = skillNames
            .filter((skill) => skills[skill] >= 5)
            .map((skill) => skill.replace("_", " "));

        const response = await fetch(
            "http://127.0.0.1:8000/interview/questions",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    target_career: targetCareer,
                    skills: selectedSkills,
                    difficulty: interviewDifficulty,
                    num_questions: Number(interviewCount),
                }),
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Question generation failed.");
        }

        // Extract individual questions from the generated text
        const questionMatches = [
            ...data.questions.matchAll(
                /Q\d+\.\s*([\s\S]*?)(?=\nQ\d+\.|$)/g
            ),
        ];

        const parsedQuestions = questionMatches
            .map((match) => match[1].trim())
            .filter(Boolean);

        if (parsedQuestions.length === 0) {
            throw new Error("Could not extract questions. Please try again.");
        }

        setInterviewQuestions(parsedQuestions);

    } catch (err) {
        setInterviewError(err.message);
    } finally {
        setInterviewLoading(false);
    }
};


// Submit answers for AI evaluation
const handleSubmitInterview = async () => {
    const unanswered = interviewQuestions.some(
        (_, index) => !interviewAnswers[index]?.trim()
    );

    if (unanswered) {
        setInterviewError("Please answer all interview questions before submitting.");
        return;
    }

    setInterviewSubmitLoading(true);
    setInterviewError("");
    setInterviewReport(null);

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/interview/mock",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    questions: interviewQuestions,
                    answers: interviewQuestions.map(
                        (_, index) => interviewAnswers[index]
                    ),
                    target_career: targetCareer,
                }),
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Interview evaluation failed.");
        }

        setInterviewReport(data);

    } catch (err) {
        setInterviewError(err.message);
    } finally {
        setInterviewSubmitLoading(false);
    }
};


  
  return (
    <div className="app dashboard-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">AI</div>
          <div>
            <h2>CareerPilot</h2>
            <span>Intelligent Career Platform</span>
          </div>
        </div>

        <div className="sidebar-label">WORKSPACE</div>

        <nav className="sidebar-nav">
          <a href="#dashboard" className="nav-link active">
            <span>◫</span> Dashboard
          </a>
          <a href="#skills" className="nav-link">
            <span>⌘</span> My Skills
          </a>
          <a href="#career" className="nav-link">
            <span>◎</span> Career Analysis
          </a>
          <a href="#roadmap" className="nav-link">
            <span>↗</span> Learning Roadmap
          </a>
          <a href="#interview" className="nav-link">
            <span>▤</span> Mock Interview
          </a>
          <a href="#assistant" className="nav-link">
            <span>✳</span> AI Assistant
          </a>
          <a href="#knowledge" className="nav-link">
            <span>◈</span> Knowledge Base
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-status">
            <span className="status-dot"></span>
            AI Services
            <strong>Connected</strong>
          </div>
          <div className="sidebar-profile">
            <div className="profile-avatar">PK</div>
            <div>
              <strong>Student Workspace</strong>
              <span>Career Development</span>
            </div>
          </div>
        </div>
      </aside>

      {/* Main dashboard */}
      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="breadcrumb">Workspace / Dashboard</span>
            <h1>Career Dashboard</h1>
          </div>
          <div className="topbar-right">
            <span className="system-status">
              <span className="status-dot"></span>
              System operational
            </span>
            <div className="topbar-avatar">PK</div>
          </div>
        </header>

        <div className="dashboard-content">
          {/* Dashboard overview */}
          <section id="dashboard" className="welcome-section">
            <div>
              <span className="eyebrow">YOUR CAREER JOURNEY</span>
              <h2>Build your future with AI.</h2>
              <p>
                Analyze your skills, discover career opportunities, and
                follow a personalized learning path.
              </p>
            </div>
            <div className="welcome-decoration">
              <div className="decoration-orbit orbit-one"></div>
              <div className="decoration-orbit orbit-two"></div>
              <div className="decoration-core">AI</div>
            </div>
          </section>

          <section className="overview-grid">
            <div className="overview-card">
              <div className="overview-card-top">
                <span>Technical Skills</span>
                <span className="overview-icon">⌘</span>
              </div>
              <strong>{skillNames.length}</strong>
              <p>Skills being tracked</p>
            </div>

            <div className="overview-card">
              <div className="overview-card-top">
                <span>Target Career</span>
                <span className="overview-icon">◎</span>
              </div>
              <strong className="overview-career">{targetCareer}</strong>
              <p>Your selected career path</p>
            </div>

            <div className="overview-card">
              <div className="overview-card-top">
                <span>Learning Progress</span>
                <span className="overview-icon">↗</span>
              </div>
              <strong>{progressPercentage}%</strong>
              <p>
                {completedCount} of {totalWeeks} weeks completed
              </p>
            </div>

            <div className="overview-card">
              <div className="overview-card-top">
                <span>Interview Questions</span>
                <span className="overview-icon">▤</span>
              </div>
              <strong>
                {interviewReport?.interview_summary?.questions_evaluated ?? 0}
              </strong>
              <p>Questions evaluated in latest report</p>
            </div>
          </section>

          {/* Skills */}
          <section id="skills" className="dashboard-section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">SKILL PROFILE</span>
                <h2>Your Technical Skills</h2>
                <p>
                  Rate your current proficiency to personalize your career
                  recommendations.
                </p>
              </div>
              <span className="section-tag">7 tracked skills</span>
            </div>

            <div className="panel skill-panel">
              <div className="skill-grid">
                {skillNames.map((skill) => (
                  <div className="skill-item" key={skill}>
                    <div className="skill-label-row">
                      <label htmlFor={skill}>
                        {skill.replace("_", " ")}
                      </label>
                      <strong>{skills[skill]}/10</strong>
                    </div>
                    <input
                      id={skill}
                      type="range"
                      name={skill}
                      min="1"
                      max="10"
                      value={skills[skill]}
                      onChange={handleChange}
                    />
                    <div className="skill-scale">
                      <span>Beginner</span>
                      <span>Advanced</span>
                    </div>
                  </div>
                ))}
              </div>
              <p className="panel-note">
                Your skill ratings are used by the career prediction,
                skill-gap analysis, and AI learning modules.
              </p>
            </div>
          </section>

          {/* Career analysis */}
          <section id="career" className="dashboard-section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">MACHINE LEARNING</span>
                <h2>Career Analysis</h2>
                <p>
                  Discover a potential career match and understand the skills
                  required for your chosen direction.
                </p>
              </div>
            </div>

            <div className="two-column-grid">
              <div className="panel">
                <div className="panel-heading">
                  <div>
                    <h3>Career Recommendation</h3>
                    <p>ML-powered career prediction</p>
                  </div>
                  <span className="panel-icon">◎</span>
                </div>

                <p className="panel-description">
                  Analyze your current technical skills to identify the
                  career category that best matches your profile.
                </p>

                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={loading}
                  className="primary-button"
                >
                  {loading ? "Analyzing profile..." : "Predict My Career"}
                  <span>→</span>
                </button>

                {error && <div className="error">{error}</div>}

                {result && (
                  <div className="result career-result">
                    <span className="result-label">RECOMMENDED CAREER</span>
                    <h3>{result.recommended_career}</h3>

                    <h4>Career Model Scores</h4>
                    {Object.entries(result.career_scores).map(
                      ([career, score]) => (
                        <div className="score-item" key={career}>
                          <div className="score-heading">
                            <span>{career}</span>
                            <strong>{score}%</strong>
                          </div>
                          <div className="score-track">
                            <div
                              className="score-fill"
                              style={{ width: `${score}%` }}
                            />
                          </div>
                        </div>
                      )
                    )}

                    <p className="disclaimer">
                      Experimental scores based on synthetic training data.
                      They are not real-world career success probabilities.
                    </p>
                  </div>
                )}
              </div>

              <div className="panel">
                <div className="panel-heading">
                  <div>
                    <h3>Skill Gap Analysis</h3>
                    <p>Compare your skills with career requirements</p>
                  </div>
                  <span className="panel-icon">⌁</span>
                </div>

                <form onSubmit={handleGapSubmit} className="analysis-form">
                  <label htmlFor="targetCareer">Target career</label>
                  <select
                    id="targetCareer"
                    value={targetCareer}
                    onChange={(e) => {
                      setTargetCareer(e.target.value);
                      setGapResult(null);
                      setRoadmapResult(null);
                      setRoadmapError("");
                    }}
                  >
                    {careerOptions.map((career) => (
                      <option key={career} value={career}>
                        {career}
                      </option>
                    ))}
                  </select>

                  <button
                    type="submit"
                    disabled={gapLoading}
                    className="primary-button"
                  >
                    {gapLoading ? "Analyzing gaps..." : "Analyze Skill Gaps"}
                    <span>→</span>
                  </button>
                </form>

                {gapError && <div className="error">{gapError}</div>}

                {gapResult && (
                  <div className="gap-result">
                    <div className="coverage">
                      <span>Requirement coverage</span>
                      <strong>{gapResult.coverage_score}%</strong>
                    </div>
                    <div className="score-track">
                      <div
                        className="score-fill"
                        style={{ width: `${gapResult.coverage_score}%` }}
                      />
                    </div>

                    <h3>Skill-by-Skill Analysis</h3>
                    {Object.entries(gapResult.skill_gaps).map(
                      ([skill, details]) => (
                        <div className="gap-item" key={skill}>
                          <div className="gap-heading">
                            <strong>{skill.replace("_", " ")}</strong>
                            <span
                              className={
                                details.gap > 0
                                  ? "needs-improvement"
                                  : "requirement-met"
                              }
                            >
                              {details.status}
                            </span>
                          </div>
                          <p>
                            Current: {details.current_level}/10
                            {" · "}
                            Required: {details.required_level}/10
                          </p>
                          <div className="score-track">
                            <div
                              className="score-fill"
                              style={{
                                width: `${
                                  (details.current_level / 10) * 100
                                }%`,
                              }}
                            />
                          </div>
                          {details.gap > 0 && (
                            <p className="gap-text">
                              Improve by {details.gap} level(s)
                            </p>
                          )}
                        </div>
                      )
                    )}

                    <p className="disclaimer">
                      Benchmarks are illustrative, not validated industry
                      requirements.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </section>

          {/* Learning roadmap */}
          <section id="roadmap" className="dashboard-section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">PERSONALIZED DEVELOPMENT</span>
                <h2>Learning Roadmap</h2>
                <p>
                  Turn your skill gaps into a structured, week-by-week
                  learning journey.
                </p>
              </div>
            </div>

            <div className="panel">
              <div className="panel-heading">
                <div>
                  <h3>Your AI Learning Plan</h3>
                  <p>
                    Generated for your selected career: {targetCareer}
                  </p>
                </div>
                <span className="panel-icon">↗</span>
              </div>

              <button
                type="button"
                onClick={handleRoadmapSubmit}
                disabled={roadmapLoading}
                className="primary-button"
              >
                {roadmapLoading
                  ? "AI Agent is creating your plan..."
                  : "Generate AI Learning Plan"}
                <span>→</span>
              </button>

              {roadmapError && <div className="error">{roadmapError}</div>}

              {roadmapResult && (
                <div className="roadmap-result">
                  <div className="roadmap-overview">
                    <div>
                      <span className="result-label">TARGET CAREER</span>
                      <h3>{roadmapResult.target_career}</h3>
                    </div>
                    <div className="roadmap-summary">
                      <strong>{roadmapResult.total_weeks}</strong>
                      <span>Weeks</span>
                    </div>
                    <div className="roadmap-summary">
                      <strong>{roadmapResult.coverage_score}%</strong>
                      <span>Skill coverage</span>
                    </div>
                  </div>

                  {roadmapResult.explanation && (
                    <div className="ai-learning-guidance">
                      <h3>AI Learning Guidance</h3>
                      <div className="ai-guidance-content">
                        <p style={{ whiteSpace: "pre-wrap" }}>
                          {roadmapResult.explanation}
                        </p>
                      </div>
                    </div>
                  )}

                  <div className="progress-section">
                    <div className="progress-heading">
                      <strong>Overall Learning Progress</strong>
                      <strong>{progressPercentage}%</strong>
                    </div>
                    <div className="score-track">
                      <div
                        className="score-fill"
                        style={{ width: `${progressPercentage}%` }}
                      />
                    </div>
                    <p>
                      {completedCount} of {totalWeeks} weeks completed
                    </p>
                  </div>

                  <div className="roadmap-timeline">
                    {roadmapResult.roadmap.map((item, index) => (
                      <div
                        className="roadmap-week"
                        key={`${item.week}-${item.skill}-${index}`}
                      >
                        <div className="roadmap-week-heading">
                          <span>WEEK {item.week}</span>
                          <label className="week-checkbox">
                            <input
                              type="checkbox"
                              checked={Boolean(completedWeeks[item.week])}
                              onChange={() => handleWeekToggle(item.week)}
                            />
                            Completed
                          </label>
                        </div>

                        <h3>{item.skill.replace("_", " ")}</h3>
                        <h4>Topics to learn</h4>
                        <ul>
                          {item.topics.map((topic, topicIndex) => (
                            <li key={topicIndex}>{topic}</li>
                          ))}
                        </ul>

                        <div className="roadmap-task">
                          <strong>Practical task</strong>
                          <p>{item.task}</p>
                        </div>
                      </div>
                    ))}
                  </div>

                  <p className="disclaimer">
                    Learning duration is an estimate and may vary with your
                    pace. Weekly scheduling is rule-based.
                  </p>
                </div>
              )}
            </div>
          </section>

          {/* Mock interview */}
          <section id="interview" className="dashboard-section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">INTERVIEW PREPARATION</span>
                <h2>AI Mock Interview</h2>
                <p>
                  Practice technical interviews and receive AI-generated
                  evaluations and adaptive follow-up questions.
                </p>
              </div>
            </div>

            <div className="panel interview-section">
              <div className="panel-heading">
                <div>
                  <h3>Interview Configuration</h3>
                  <p>Customize your practice session</p>
                </div>
                <span className="panel-icon">▤</span>
              </div>

              <div className="interview-settings">
                <label>
                  Interview difficulty
                  <select
                    value={interviewDifficulty}
                    onChange={(e) => setInterviewDifficulty(e.target.value)}
                    disabled={interviewLoading || interviewQuestions.length > 0}
                  >
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                  </select>
                </label>

                <label>
                  Number of questions
                  <select
                    value={interviewCount}
                    onChange={(e) => setInterviewCount(Number(e.target.value))}
                    disabled={interviewLoading || interviewQuestions.length > 0}
                  >
                    <option value={3}>3 Questions</option>
                    <option value={5}>5 Questions</option>
                    <option value={10}>10 Questions</option>
                  </select>
                </label>
              </div>

              <button
                type="button"
                onClick={handleGenerateInterview}
                disabled={interviewLoading || interviewSubmitLoading}
                className="primary-button"
              >
                {interviewLoading
                  ? "Generating questions..."
                  : interviewQuestions.length > 0
                    ? "Generate New Interview"
                    : "Start Mock Interview"}
                <span>→</span>
              </button>

              {interviewError && <div className="error">{interviewError}</div>}

              {interviewQuestions.length > 0 && !interviewReport && (
                <div className="interview-questions">
                  <div className="interview-intro">
                    <h3>{targetCareer} Interview</h3>
                    <p>
                      Difficulty: <strong>{interviewDifficulty}</strong>
                      {" · "}
                      Questions: <strong>{interviewQuestions.length}</strong>
                    </p>
                  </div>

                  {interviewQuestions.map((item, index) => (
                    <div className="interview-question" key={index}>
                      <span className="result-label">
                        QUESTION {index + 1}
                      </span>
                      <h4>{item}</h4>
                      <textarea
                        rows="5"
                        placeholder="Write your answer here..."
                        value={interviewAnswers[index] || ""}
                        onChange={(e) => {
                          const value = e.target.value;
                          setInterviewAnswers((previous) => ({
                            ...previous,
                            [index]: value,
                          }));
                        }}
                      />
                    </div>
                  ))}

                  <button
                    type="button"
                    onClick={handleSubmitInterview}
                    disabled={interviewSubmitLoading}
                    className="primary-button"
                  >
                    {interviewSubmitLoading
                      ? "AI is evaluating your answers..."
                      : "Submit for AI Evaluation"}
                    <span>→</span>
                  </button>
                </div>
              )}

              {interviewReport && (
                <div className="interview-report">
                  <h3>Interview Evaluation Report</h3>
                  <p>
                    Target Career: <strong>{interviewReport.target_career}</strong>
                  </p>
                  <p>
                    Total Questions: <strong>{interviewReport.total_questions}</strong>
                  </p>

                  {interviewReport.interview_summary && (
                    <div className="interview-summary">
                      <h3>Overall Performance</h3>
                      <div className="interview-summary-grid">
                        <div className="interview-summary-card">
                          <span>Average Score</span>
                          <strong>
                            {interviewReport.interview_summary.average_score ?? "N/A"}
                            /10
                          </strong>
                        </div>
                        <div className="interview-summary-card">
                          <span>Performance Level</span>
                          <strong>
                            {interviewReport.interview_summary.performance_level}
                          </strong>
                        </div>
                        <div className="interview-summary-card">
                          <span>Questions Evaluated</span>
                          <strong>
                            {interviewReport.interview_summary.questions_evaluated}
                          </strong>
                        </div>
                      </div>
                    </div>
                  )}

                  {interviewReport.interview_results.map((item) => (
                    <div
                      className="interview-result-item"
                      key={item.question_number}
                    >
                      <h4>Question {item.question_number}</h4>
                      <p><strong>Question:</strong> {item.question}</p>
                      <p><strong>Your Answer:</strong></p>
                      <p className="interview-answer">{item.answer}</p>

                      <h4>AI Evaluation</h4>
                      <div className="interview-feedback">
                        <p style={{ whiteSpace: "pre-wrap" }}>
                          {item.evaluation}
                        </p>
                      </div>

                      <h4>Adaptive Follow-up Question</h4>
                      <div className="interview-feedback">
                        <p style={{ whiteSpace: "pre-wrap" }}>
                          {item.follow_up_question}
                        </p>
                      </div>
                    </div>
                  ))}

                  <button
                    type="button"
                    className="secondary-button"
                    onClick={() => {
                      setInterviewQuestions([]);
                      setInterviewAnswers({});
                      setInterviewReport(null);
                      setInterviewError("");
                    }}
                  >
                    Start Another Interview
                  </button>
                </div>
              )}
            </div>
          </section>

          {/* AI Assistant */}
          <section id="assistant" className="dashboard-section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">GENERATIVE AI</span>
                <h2>AI Career Assistant</h2>
                <p>
                  Get personalized guidance about careers, skills, learning,
                  and interview preparation.
                </p>
              </div>
            </div>

            <div className="panel ai-section">
              <div className="panel-heading">
                <div>
                  <h3>Ask your career assistant</h3>
                  <p>Powered by your local AI model</p>
                </div>
                <span className="panel-icon">✳</span>
              </div>

              <textarea
                placeholder="For example: How should I prepare for an ML Engineer role?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                rows="4"
              />

              <button
                type="button"
                onClick={handleAIAdvice}
                disabled={aiLoading}
                className="primary-button"
              >
                {aiLoading ? "Generating response..." : "Ask AI Assistant"}
                <span>→</span>
              </button>

              {aiError && <p className="error-message">{aiError}</p>}

              <div className="chat-messages">
                {chatMessages.length === 0 && !aiLoading && (
                  <div className="empty-state">
                    <span>✳</span>
                    <strong>Your AI conversation starts here</strong>
                    <p>Ask a question to receive personalized career guidance.</p>
                  </div>
                )}

                {chatMessages.map((message, index) => (
                  <div
                    key={index}
                    className={`chat-message ${message.role}`}
                  >
                    <strong>
                      {message.role === "user" ? "You" : "AI Career Assistant"}
                    </strong>
                    <p>{message.content}</p>
                  </div>
                ))}

                {aiLoading && <p className="loading-message">AI is thinking...</p>}
              </div>
            </div>
          </section>

          {/* RAG Knowledge Assistant */}
          <section id="knowledge" className="dashboard-section">
            <div className="section-heading">
              <div>
                <span className="eyebrow">RETRIEVAL-AUGMENTED GENERATION</span>
                <h2>Career Knowledge Base</h2>
                <p>
                  Ask questions and retrieve relevant information from your
                  career learning knowledge base.
                </p>
              </div>
            </div>

            <div className="panel rag-section">
              <div className="panel-heading">
                <div>
                  <h3>RAG Knowledge Assistant</h3>
                  <p>Semantic search with retrieved source information</p>
                </div>
                <span className="panel-icon">◈</span>
              </div>

              <label>Select knowledge category</label>
              <select
                value={ragCategory}
                onChange={(e) => setRagCategory(e.target.value)}
              >
                <option value="">All Categories</option>
                <option value="Python">Python</option>
                <option value="Machine Learning">Machine Learning</option>
                <option value="Deep Learning">Deep Learning</option>
                <option value="Full Stack">Full Stack</option>
                <option value="Data Analytics">Data Analytics</option>
                <option value="Interview Preparation">Interview Preparation</option>
              </select>

              <textarea
                placeholder="Ask a question about programming, ML, or career preparation..."
                value={ragQuestion}
                onChange={(e) => setRagQuestion(e.target.value)}
                rows="4"
              />

              <button
                type="button"
                onClick={handleRAGAdvice}
                disabled={ragLoading}
                className="primary-button"
              >
                {ragLoading ? "Searching knowledge base..." : "Search Knowledge Base"}
                <span>→</span>
              </button>

              {ragError && <p className="error-message">{ragError}</p>}

              {ragAnswer && (
                <div className="rag-answer">
                  <h3>Knowledge Base Response</h3>
                  <div className="rag-answer-content">
                    <p style={{ whiteSpace: "pre-wrap" }}>{ragAnswer}</p>
                  </div>

                  <div className="rag-sources">
                    <div className="sources-heading">
                      <h3>Retrieved Sources</h3>
                      <span>{ragTotalChunks} chunks retrieved</span>
                    </div>

                    {ragSources.length > 0 ? (
                      ragSources.map((source, index) => (
                        <div className="rag-source-item" key={index}>
                          <h4>{source.source}</h4>
                          <p>Category: {source.category}</p>
                          <p>
                            Chunk: {source.chunk_number ?? "Not available"}
                          </p>
                          <p>Retrieval distance: {source.distance}</p>
                        </div>
                      ))
                    ) : (
                      <p>No relevant source documents were retrieved.</p>
                    )}
                  </div>
                </div>
              )}
            </div>
          </section>

          <footer className="dashboard-footer">
            <span>CareerPilot AI</span>
            <span>Machine Learning · Generative AI · Agentic AI</span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
