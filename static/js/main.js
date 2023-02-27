const MAX_SERIES_SIZE = 10;

// Fetch new data from the server and update the chart
function _fetchChartData(chart, chartUrl) {
  fetch(chartUrl)
    .then((response) => response.json())
    .then((data) => _update_chart(chart, data));
}

// Update a Chart.js chart with new data and labels removing the oldest data to
// keep the chart size constant
function _update_chart(chart, data) {
  if (chart.data.labels.length > MAX_SERIES_SIZE) {
    chart.data.labels.shift();
  }

  chart.data.labels.push(data.label);

  chart.data.datasets.forEach((dataset) => {
    datasetData = data.datasets[dataset.label];

    if (dataset.data.length > MAX_SERIES_SIZE) {
      dataset.data.shift();
    }

    dataset.data.push(datasetData);
  });

  chart.update();
}

document.addEventListener("DOMContentLoaded", () => {
  const chartCanvas = document.getElementById("chart");
  const chartUrl = chartCanvas.dataset.chartUrl;

  Chart.defaults.color = "#EDEDED";
  Chart.defaults.borderColor = "#171717";

  // Initialize our chart object with empty data to be updated dynamically
  const chart = new Chart(chartCanvas, {
    type: "line",
    data: {
      labels: [],
      datasets: [
        {
          label: "Memory",
          data: [],
          borderColor: "#DA0037",
        },

        {
          label: "CPU",
          data: [],
          borderColor: "#2cda00",
        },
      ],
    },

    options: {
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  });

  _fetchChartData(chart, chartUrl);
  setInterval(() => _fetchChartData(chart, chartUrl), 1000);
});
