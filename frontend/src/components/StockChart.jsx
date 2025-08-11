import React from "react";
import { Line } from "react-chartjs-2";
import 'chart.js/auto';

export default function StockChart({data, symbol, prediction}) {
  if(!data || data.length===0) return <div style={{padding:20}}>Select a company to view chart</div>
  // data: array of {Date, Open, High, Low, Close, Volume}
  const labels = data.map(r => (new Date(r.Date)).toLocaleDateString());
  const closes = data.map(r => r.Close);
  const chartData = {
    labels,
    datasets: [
      {
        label: `${symbol} Close`,
        data: closes,
        fill: false,
        tension: 0.2,
        pointRadius: 0
      }
    ]
  };
  return (
    <div style={{padding:20, width:"100%"}}>
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
        <h2>{symbol}</h2>
        {prediction && <div>Next-day Predicted Close: <strong>{prediction.toFixed(4)}</strong></div>}
      </div>
      <div style={{height:400}}>
        <Line data={chartData} />
      </div>
    </div>
  );
}
