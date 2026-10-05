const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const api = {
  // Graph endpoints
  getGraph: async () => {
    const res = await fetch(`${API_BASE_URL}/network/graph`);
    if (!res.ok) throw new Error('Failed to fetch graph');
    return res.json();
  },

  getNodeDetails: async (nodeId) => {
    const res = await fetch(`${API_BASE_URL}/network/node/${encodeURIComponent(nodeId)}`);
    if (!res.ok) throw new Error('Failed to fetch node details');
    return res.json();
  },

  getShortestPath: async (source, target) => {
    const res = await fetch(`${API_BASE_URL}/network/shortest-path?source=${encodeURIComponent(source)}&target=${encodeURIComponent(target)}`);
    if (!res.ok) throw new Error('Failed to compute shortest path');
    return res.json();
  },

  // Intelligence endpoints
  getPredictedLinks: async () => {
    const res = await fetch(`${API_BASE_URL}/intelligence/predict-links`);
    if (!res.ok) throw new Error('Failed to fetch predicted links');
    return res.json();
  },

  getCrossCase: async () => {
    const res = await fetch(`${API_BASE_URL}/intelligence/cross-case`);
    if (!res.ok) throw new Error('Failed to fetch cross case correlations');
    return res.json();
  },

  getMemory: async () => {
    const res = await fetch(`${API_BASE_URL}/intelligence/memory`);
    if (!res.ok) throw new Error('Failed to fetch memory');
    return res.json();
  },

  // Copilot RAG
  queryCopilot: async (question, context = '') => {
    const res = await fetch(`${API_BASE_URL}/copilot/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, case_context: context })
    });
    if (!res.ok) throw new Error('Failed to query Copilot');
    return res.json();
  },

  // Surveillance feeds
  getSurveillanceFeeds: async () => {
    const res = await fetch(`${API_BASE_URL}/surveillance/feeds`);
    if (!res.ok) throw new Error('Failed to fetch surveillance feeds');
    return res.json();
  },

  getAudioIntercepts: async () => {
    const res = await fetch(`${API_BASE_URL}/surveillance/audio-intercepts`);
    if (!res.ok) throw new Error('Failed to fetch audio intercepts');
    return res.json();
  },

  // Cases
  getCases: async () => {
    const res = await fetch(`${API_BASE_URL}/cases`);
    if (!res.ok) throw new Error('Failed to fetch cases');
    return res.json();
  },

  // Ingestion
  ingestData: async (payload) => {
    const res = await fetch(`${API_BASE_URL}/ingestion/process`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to ingest data');
    return res.json();
  },

  // Validate Link
  validateLink: async (payload) => {
    const res = await fetch(`${API_BASE_URL}/investigation/validate-link`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error('Failed to validate link');
    return res.json();
  }
};
