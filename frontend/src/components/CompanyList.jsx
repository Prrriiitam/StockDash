import React from "react";

export default function CompanyList({companies, onSelect, selected}) {
  return (
    <div style={{width: 260, overflowY: "auto", borderRight: "1px solid #ddd", padding: 12, height: "100vh"}}>
      <h3>Companies</h3>
      {companies.map(c => (
        <div key={c.symbol}
             onClick={() => onSelect(c.symbol)}
             style={{
               padding: 10, marginBottom: 6, cursor: "pointer",
               background: selected === c.symbol ? "#f0f8ff":"transparent",
               borderRadius: 6
             }}>
          <strong style={{fontSize: 14}}>{c.name}</strong>
          <div style={{fontSize: 12, color: "#666"}}>{c.symbol}</div>
        </div>
      ))}
    </div>
  );
}
