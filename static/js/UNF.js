(async () => {
  //Time Series chart for Historical data
  var fatalUrbanChart = document.getElementById("urbanFatalities");

  const getData = async (option) => {
    const formdata = new FormData();
    formdata.append("option", option);

    const response = await fetch("/accidents/UNF/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const getAllData = async () => {
    const formdata = new FormData();
    formdata.append("option", "D,C");

    const response = await fetch("accidents/UNF/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const allData = await getAllData();
  console.log(allData);

  var urbanFatBusData = {
    label: "Bus and mini-Bus",
    data: allData.D.map((d) => d.Bus_and_Bus_Mini),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "#853D43",
  };

  var urbanFatCarData = {
    label: "Accidents by cars",
    data: allData["D"].map((d) => d.Car),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "green",
  };

  var urbanFatCycleData = {
    label: "Accidents by Cycles",
    data: allData["D"].map((d) => d.Cycle),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "red",
  };

  var urbanFatPedData = {
    label: "Pedestrians knockdown",
    data: allData["D"].map((d) => d.Ped),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "blue",
  };

  var urbanFatData = {
    labels: [
      1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
      2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
      2015, 2016, 2017, 2018, 2019, 2020,
    ],
    datasets: [
      urbanFatBusData,
      urbanFatCarData,
      urbanFatCycleData,
      urbanFatPedData,
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

  var casGenderChart = new Chart(fatalUrbanChart, {
    type: "line",
    data: urbanFatData,
    options: chartOptions,
  });

  //FATALITIES

  var nonUrbanFatChart = document.getElementById("nonUrbanFatal");
 var nonUrbanFatBusData = {
   label: "Bus and mini-Bus",
   data: allData.C.map((d) => d.Bus_and_Bus_Mini),
   lineTension: 0.5,
   borderWidth: 2,
   radius: 1,
   fill: false,
   borderColor: "#853D43",
 };

 var nonUrbanFatCarData = {
   label: "Accidents by cars",
   data: allData["C"].map((d) => d.Car),
   lineTension: 0.5,
   borderWidth: 2,
   radius: 1,
   fill: false,
   borderColor: "green",
 };

 var nonUrbanFatCycleData = {
   label: "Accidents by Cycles",
   data: allData["C"].map((d) => d.Cycle),
   lineTension: 0.5,
   borderWidth: 2,
   radius: 1,
   fill: false,
   borderColor: "red",
 };

 var nonUrbanFatPedData = {
   label: "Pedestrians knockdown",
   data: allData["C"].map((d) => d.Ped),
   lineTension: 0.5,
   borderWidth: 2,
   radius: 1,
   fill: false,
   borderColor: "blue",
 };

 var nonUrbanFatData = {
   labels: [
     1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
     2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
     2015, 2016, 2017, 2018, 2019, 2020,
   ],
   datasets: [
     nonUrbanFatBusData,
     nonUrbanFatCarData,
     nonUrbanFatCycleData,
     nonUrbanFatPedData,
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

  var nUrbanFatChart = new Chart(nonUrbanFatChart, {
    type: "line",
    lineThickness: -10,
    data: nonUrbanFatData,
    options: chartOptions,
  });
})();
