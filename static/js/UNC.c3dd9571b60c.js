(async () => {
  //Time Series chart for Historical data
  var casNonUrbanChart = document.getElementById("unc2");

  const getData = async (option) => {
    const formdata = new FormData();
    formdata.append("option", option);

    const response = await fetch("/accidents/UNC/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const getAllData = async () => {
    const formdata = new FormData();
    formdata.append("option", "H,O");

    const response = await fetch("accidents/UNC/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const allData = await getAllData();
  console.log(allData);

  var urbanCasBusData = {
    label: "Bus and mini-Bus",
    data: allData.H.map((d) => d.Bus_and_Bus_Mini),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "#853D43",
  };

  var urbanCasCarData = {
    label: "Accidents by cars",
    data: allData["H"].map((d) => d.Car),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "green",
  };

  var urbanCasCycleData = {
    label: "Accidents by Cycles",
    data: allData["H"].map((d) => d.Cycle),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "red",
  };

  var urbanCasPedData = {
    label: "Pedestrians knockdown",
    data: allData["H"].map((d) => d.Ped),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "blue",
  };

  var urbanCasData = {
    labels: [
      1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
      2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
      2015, 2016, 2017, 2018, 2019, 2020,
    ],
    datasets: [
      urbanCasBusData,
      urbanCasCarData,
      urbanCasCycleData,
      urbanCasPedData,
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

  var casNonUrChart = new Chart(casNonUrbanChart, {
    type: "line",
    data: urbanCasData,
    options: chartOptions,
  });

  //URBAN CASUALTIES

  var uncChart = document.getElementById("unc");
  var uncBusData = {
    label: "Bus and mini-Bus",
    data: allData.O.map((d) => d.Bus_and_Bus_Mini),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "#853D43",
  };

  var uncCarData = {
    label: "Accidents by cars",
    data: allData["O"].map((d) => d.Car),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "green",
  };

  var uncCycleData = {
    label: "Accidents by Cycles",
    data: allData["O"].map((d) => d.Cycle),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "red",
  };

  var uncOtherData = {
    label: "Pedestrians knockdown",
    data: allData["O"].map((d) => d.Other),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "blue",
  };

  var uncData = {
    labels: [
      1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
      2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
      2015, 2016, 2017, 2018, 2019, 2020,
    ],
    datasets: [
      uncBusData,
      uncCarData,
      uncCycleData,
      uncOtherData,
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

  var uncCasChart = new Chart(uncChart, {
    type: "line",
    lineThickness: -10,
    data: uncData,
    options: chartOptions,
  });
})();
