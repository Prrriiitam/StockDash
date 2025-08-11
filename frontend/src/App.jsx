import React, {useState, useEffect} from "react";
import { getCompanies, getHistorical, getPrediction } from "./api";
import CompanyList from "./components/CompanyList";
import StockChart from "./components/StockChart";

function App(){
  const [companies, setCompanies] = useState([]);
  const [selected, setSelected] = useState(null);
  const [historical, setHistorical] = useState([]);
  const [prediction, setPrediction] = useState(null);

  useEffect(()=> {
    getCompanies().then(setCompanies);
  },[]);

  useEffect(()=> {
    if(!selected) return;
    setHistorical([]);
    getHistorical(selected).then(res => {
      // res.data is array of objects
      setHistorical(res.data);
    });
    getPrediction(selected).then(res => {
      setPrediction(res.prediction);
    }).catch(err => console.error(err));
  }, [selected]);

  return (
    <div style={{display:"flex"}}>
      <CompanyList companies={companies} onSelect={setSelected} selected={selected}/>
      <div style={{flex:1}}>
        <StockChart data={historical} symbol={selected} prediction={prediction}/>
      </div>
    </div>
  )
}

export default App;
