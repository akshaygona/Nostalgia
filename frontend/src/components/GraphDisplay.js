import React from "react";
import { Line } from "react-chartjs-2";

function GraphDisplay({ graphData }) {
  if (!graphData) {
    return <div className="graph-placeholder">Graph will appear here</div>;
  }

  const chartData = {
    labels: graphData.dates, // Backend provides date array
    datasets: [
      {
        label: "Close Prices",
        data: graphData.prices, // Backend provides close price array
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: { title: { display: true, text: "Date" } },
      y: { title: { display: true, text: "Price" } },
    },
  };

  return (
    <div className="graph-container">
      <Line data={chartData} options={options} />
    </div>
  );
}

export default GraphDisplay;
