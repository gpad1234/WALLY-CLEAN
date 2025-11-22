import React, { useState } from 'react';

import api from '../../services/api';

const HINTS = [
  "How many nodes and edges are there?",
  "Show me the full graph.",
  "List all node IDs.",
  "List all edges.",
  "Who are Alice's neighbors?",
  "Find the shortest path from Alice to Frank."
];

const NLP = () => {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  const handleSearch = async (e, q) => {
    e && e.preventDefault();
    const searchQuery = q || query;
    if (!searchQuery) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await api.post('/api/nlp_query', { query: searchQuery });
      setResult(response.data);
      setHistory((prev) => [searchQuery, ...prev.filter(h => h !== searchQuery)].slice(0, 8));
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to search.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="nlp-tab">
      <h2>Search & NLP</h2>
      <form className="nlp-form" onSubmit={handleSearch}>
        <textarea
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Ask a question or type a graph search..."
          rows={3}
          className="nlp-input"
        />
        <button type="submit" disabled={loading || !query}>Search</button>
      </form>
      <div className="nlp-hints">
        <b>Hints:</b>
        {HINTS.map((hint, i) => (
          <span key={i} className="nlp-hint" onClick={() => { setQuery(hint); handleSearch(null, hint); }}>{hint}</span>
        ))}
      </div>
      {history.length > 0 && (
        <div className="nlp-history">
          <b>Recent queries:</b>
          {history.map((h, i) => (
            <span key={i} className="nlp-history-item" onClick={() => { setQuery(h); handleSearch(null, h); }}>{h}</span>
          ))}
        </div>
      )}
      {loading && <div>Loading...</div>}
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="result">
          {result.explanation && <div className="nlp-explanation">{result.explanation}</div>}
          {result.action && <div className="nlp-action"><b>Action:</b> {result.action}</div>}
          {result.nodes && (
            <div className="nlp-nodes">
              <b>Nodes:</b> {Array.isArray(result.nodes) ? result.nodes.join(', ') : result.nodes}
            </div>
          )}
          {result.edges && (
            <div className="nlp-edges">
              <b>Edges:</b>
              <pre>{Array.isArray(result.edges) ? JSON.stringify(result.edges, null, 2) : result.edges}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NLP;
