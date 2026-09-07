import { useState } from "react";
import "./App.css";

const API_URL = "https://waypoint-rag.onrender.com";

const suggestions = [
  "Customer charged twice",
  "Customer doesn't recognize a transaction",
  "Customer never received the merchandise",
  "Customer wants to cancel a transaction",
];

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async (q = question) => {
    if (!q.trim()) return;

    setQuestion(q);
    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: q }),
      });

      if (!response.ok) {
        throw new Error("Unable to retrieve policy guidance.");
      }

      const data = await response.json();

      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="terminal">
      {/* TOP BAR */}
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">W</div>

          <div>
            <div className="brand-name">WAYPOINT</div>
            <div className="brand-subtitle">
              DISPUTE INTELLIGENCE TERMINAL
            </div>
          </div>
        </div>

        <div className="system-info">
          <span>RAG v1.0</span>
          <span>VISA KNOWLEDGE BASE</span>
          <span className="online">
            <i />
            ONLINE
          </span>
        </div>
      </header>

      {/* MAIN */}
      <main>
        <section className="command-header">
          <div className="eyebrow">
            POLICY QUERY / <span>LIVE</span>
          </div>

          <h1>
            Dispute policy,
            <br />
            <strong>at your command.</strong>
          </h1>

          <p>
            Search the Visa dispute knowledge base. Get policy-grounded
            answers with traceable sources.
          </p>
        </section>

        {/* QUERY */}
        <section className="query-section">
          <div className="query-label">
            <span>QUERY</span>
            <span className="mono">POST /ask</span>
          </div>

          <div className="query-box">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  askQuestion();
                }
              }}
              placeholder="Describe the transaction or dispute scenario..."
              rows={2}
            />

            <button
              onClick={() => askQuestion()}
              disabled={loading || !question.trim()}
            >
              {loading ? "..." : "RUN"}
            </button>
          </div>

          <div className="suggestions">
            <span className="suggestion-label">SCENARIOS</span>

            {suggestions.map((item) => (
              <button key={item} onClick={() => askQuestion(item)}>
                {item}
              </button>
            ))}
          </div>
        </section>

        {/* RESULTS */}
        {(answer || loading || error) && (
          <section className="results">
            <div className="result-header">
              <span>ANALYSIS RESULT</span>
              <span className="mono">WAYPOINT / RAG</span>
            </div>

            {/* STATUS STRIP */}
            <div className="status-strip">
              <div>
                <span>STATUS</span>
                <strong className="green">
                  {loading ? "PROCESSING" : "COMPLETE"}
                </strong>
              </div>

              <div>
                <span>SOURCES</span>
                <strong>{sources.length || "—"}</strong>
              </div>

              <div>
                <span>ENGINE</span>
                <strong>RETRIEVAL + LLM</strong>
              </div>
            </div>

            {/* ANSWER */}
            <div className="answer-panel">
              <div className="panel-heading">
                <span className="number">01</span>
                <span>POLICY ANALYSIS</span>
              </div>

              {loading && (
                <div className="loading">
                  <span className="loader" />
                  SEARCHING KNOWLEDGE BASE...
                </div>
              )}

              {error && <div className="error">{error}</div>}

              {answer && <div className="answer">{answer}</div>}
            </div>

            {/* SOURCES */}
            {sources.length > 0 && (
              <div className="sources-panel">
                <div className="panel-heading">
                  <span className="number">02</span>
                  <span>SOURCE RECORDS</span>
                </div>

                {sources.map((source, index) => (
                  <div className="source-row" key={index}>
                    <div className="source-number">
                      {String(index + 1).padStart(2, "0")}
                    </div>

                    <div className="source-content">
                      <strong>
                        {source.title || "Visa Dispute Guidelines"}
                      </strong>

                      <span>
                        {source.page
                          ? `PAGE ${source.page}`
                          : "POLICY KNOWLEDGE BASE"}
                      </span>
                    </div>

                    <div className="source-arrow">↗</div>
                  </div>
                ))}
              </div>
            )}
          </section>
        )}
      </main>

      <footer>
        <span>WAYPOINT</span>
        <span>POLICY INTELLIGENCE / AUDIT-FIRST RAG</span>
        <span>LOCAL SESSION</span>
      </footer>
    </div>
  );
}

export default App;