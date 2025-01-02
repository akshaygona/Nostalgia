import React, { useState } from "react";
import axios from "axios";

function InputForm({ setGraphData }) {
  const [symbol, setSymbol] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(
        `http://localhost:8000/stock/full-history/${symbol}`,
        { params: { start_date: startDate, end_date: endDate } }
      );
      setGraphData(response.data); // Backend sends processed data for graphing
    } catch (error) {
      console.error("Error fetching stock data:", error);
    }
  };

  return (
    <div className="input-form">
      <form onSubmit={handleSubmit}>
        <div>
          <label>Stock Symbol:</label>
          <input
            type="text"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value)}
          />
        </div>
        <div>
          <label>Start Date (YYYY-MM):</label>
          <input
            type="text"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </div>
        <div>
          <label>End Date (YYYY-MM):</label>
          <input
            type="text"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>
        <button type="submit">Fetch Data</button>
      </form>
    </div>
  );
}

export default InputForm;
