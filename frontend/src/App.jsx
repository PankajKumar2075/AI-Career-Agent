
import { useState } from "react";
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

  const [loading, setLoading] = useState(false);
  const [gapLoading, setGapLoading] = useState(false);
  const [roadmapLoading, setRoadmapLoading] = useState(false);

  const [error, setError] = useState("");
  const [gapError, setGapError] = useState("");
  const [roadmapError, setRoadmapError] = useState("");

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

  
  // Generate personalized learning roadmap
  const handleRoadmapSubmit = async () => {
    setRoadmapLoading(true);
    setRoadmapError("");
    setRoadmapResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/learning-roadmap",
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
        throw new Error("Learning roadmap generation failed.");
      }

      const data = await response.json();
      setRoadmapResult(data);

    } catch (err) {
      console.error(err);
      setRoadmapError(
        "Could not connect to the learning roadmap API."
      );
    } finally {
      setRoadmapLoading(false);
    }
  };


  return (
    <div className="app">

      <header className="header">
        <h1>AI Career Agent</h1>
        <p>
          Discover your career path and identify
          the skills you need to improve.
        </p>
      </header>

      <main className="container">

        {/* Shared skill inputs */}

        <section className="skill-form">
          <h2>Your Technical Skills</h2>

          <p>Rate your current skills from 1 to 10.</p>

          <div className="skill-grid">

            {skillNames.map((skill) => (
              <div className="skill-item" key={skill}>

                <label htmlFor={skill}>
                  {skill.replace("_", " ")}
                </label>

                <div className="skill-input">

                  <input
                    id={skill}
                    type="range"
                    name={skill}
                    min="1"
                    max="10"
                    value={skills[skill]}
                    onChange={handleChange}
                  />

                  <span>{skills[skill]}/10</span>

                </div>

              </div>
            ))}

          </div>
        </section>

        {/* Career recommendation */}

        <section className="skill-form">
          <h2>Career Recommendation</h2>

          <p>
            Find the career category that best matches
            your current skills.
          </p>

          <form onSubmit={handleSubmit}>

            <button type="submit" disabled={loading}>
              {loading ? "Analyzing..." : "Predict My Career"}
            </button>

          </form>

          {error && <div className="error">{error}</div>}

          {result && (
            <div className="result">

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
        </section>

        {/* Skill gap analysis */}

        <section className="skill-form">

          <h2>Skill Gap Analysis</h2>

          <p>
            Select your target career to discover
            which skills you need to improve.
          </p>

          <form onSubmit={handleGapSubmit}>

            <label htmlFor="targetCareer">
              Select Your Target Career
            </label>

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

            <button type="submit" disabled={gapLoading}>
              {gapLoading
                ? "Analyzing Skill Gaps..."
                : "Analyze My Skill Gaps"}
            </button>

          </form>

          {gapError && (
            <div className="error">{gapError}</div>
          )}

          {gapResult && (
            <div className="gap-result">

              <h3>{gapResult.target_career}</h3>

              <div className="coverage">
                <span>Skill Requirement Coverage</span>

                <strong>
                  {gapResult.coverage_score}%
                </strong>
              </div>

              <div className="score-track">
                <div
                  className="score-fill"
                  style={{
                    width: `${gapResult.coverage_score}%`,
                  }}
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
                      {" | "}
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
                Benchmarks are illustrative and should not be
                interpreted as validated industry requirements.
              </p>

            </div>
          )}

        </section>

        
        {/* Personalized Learning Roadmap */}

        <section className="skill-form">

          <h2>Personalized Learning Roadmap</h2>

          <p>
            Generate a week-by-week learning plan based on
            your current skills and target career.
          </p>

          <button
            type="button"
            onClick={handleRoadmapSubmit}
            disabled={roadmapLoading}
          >
            {roadmapLoading
              ? "Generating Roadmap..."
              : "Generate Learning Roadmap"}
          </button>

          {roadmapError && (
            <div className="error">{roadmapError}</div>
          )}

          {roadmapResult && (
            <div className="roadmap-result">

              <h3>{roadmapResult.target_career}</h3>

              <div className="roadmap-summary">
                <strong>
                  {roadmapResult.total_weeks} Weeks
                </strong>
                <span>Total Learning Duration</span>
              </div>

              <p>
                Skill Requirement Coverage:{" "}
                <strong>{roadmapResult.coverage_score}%</strong>
              </p>

              <h3>Your Weekly Plan</h3>

              {roadmapResult.roadmap.map((item, index) => (
                <div
                  className="roadmap-week"
                  key={`${item.week}-${item.skill}-${index}`}
                >

                  <div className="roadmap-week-heading">
                    <span>Week {item.week}</span>
                    <strong>
                      {item.skill.replace("_", " ")}
                    </strong>
                  </div>

                  <h4>Topics to Learn</h4>

                  <ul>
                    {item.topics.map((topic, topicIndex) => (
                      <li key={topicIndex}>{topic}</li>
                    ))}
                  </ul>

                  <div className="roadmap-task">
                    <strong>Practical Task:</strong>
                    <p>{item.task}</p>
                  </div>

                </div>
              ))}

              <p className="disclaimer">
                This roadmap is generated using rule-based
                scheduling. Learning duration is an estimate
                and can vary with your pace.
              </p>

            </div>
          )}

        </section>


      </main>

      <footer>
        AI Career Agent | Powered by Machine Learning
      </footer>

    </div>
  );
}

export default App;
