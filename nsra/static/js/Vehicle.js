(async () => {
  //Time Series chart for Historical data
  var vehiclesChart = document.getElementById("Vehicles");

  const getData = async (option) => {
    const formdata = new FormData();
    formdata.append("option", option);

    const response = await fetch("/accidents/vehicles/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const getAllData = async () => {
    const formdata = new FormData();
    formdata.append("option", "L");

    const response = await fetch("accidents/vehicles/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();
    return data;
  };

  const allData = await getAllData();
  console.log(allData);

  var BusData = {
    label: "Bus and mini-Bus",
    data: allData.L.map((d) => d.Bus_and_Bus_Mini),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "#853D43",
  };

  var CarData = {
    label: "Cars",
    data: allData["L"].map((d) => d.Car),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "green",
  };

  var CycleData = {
    label: "Cycles",
    data: allData.L.map((d) => d.Cycle),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "red",
  };

  var otherData = {
    label: "Other",
    data: allData["L"].map((d) => d.Other),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "blue",
  };

  var vehiclesData = {
    labels: [
      1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
      2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
      2015, 2016, 2017, 2018, 2019, 2020,
    ],
    datasets: [
      BusData,
      CarData,
      CycleData,
      otherData,
    ],
  };

  var chartOptions = {
    legend: {
      display: true,
      position: "top",
      labels: {
        boxWidth: 80,
        fontColor: "black",
      },
    },
  };

  var vehicleChart = new Chart(vehiclesChart, {
    type: "line",
    data: vehiclesData,
    options: chartOptions,
  });
})();
