const BASE = "http://localhost:8000";

export async function getCompanies() {
  const res = await fetch(`${BASE}/companies`);
  return res.json();
}

export async function getHistorical(symbol) {
  const res = await fetch(`${BASE}/historical/${encodeURIComponent(symbol)}`);
  return res.json();
}

export async function getPrediction(symbol) {
  const res = await fetch(`${BASE}/predict`, {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({symbol})
  });
  return res.json();
}
