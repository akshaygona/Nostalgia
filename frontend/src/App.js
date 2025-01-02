import React from "react";
import InputForm from "./components/InputForm";
import GraphDisplay from "./components/GraphDisplay";
import "./App.css";

function App() {
  const [graphData, setGraphData] = React.useState(null);

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Stock Performance Dashboard</h1>
      </header>
      <div className="main-content">
        <InputForm setGraphData={setGraphData} />
        <GraphDisplay graphData={graphData} />
      </div>
    </div>
  );
}

export default App;
