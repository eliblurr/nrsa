(async () => {
  //Time Series chart for Historical data
  var fceChart = document.getElementById("FCE");

  const getData = async (option) => {
    const formdata = new FormData();
    formdata.append("option", option);

    const response = await fetch("/accidents/FCE/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const getAllData = async () => {
    const formdata = new FormData();
    formdata.append("option", "B, J");

    const response = await fetch("accidents/FCE/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const allData = await getAllData();
  console.log(allData);

  var fatalFceData = {
    label: "Fatalities by Road Environments",
    data: allData["B"].map((d) => d.Total),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "green",
  };

  var casFceData = {
    label: "Casualties by Road Environments",
    data: allData["J"].map((d) => d.Total),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "blue",
  };

  var fceData = {
    labels: [
      1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
      2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
      2015, 2016, 2017, 2018, 2019, 2020,
    ],
    datasets: [casFceData, fatalFceData],
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

  var fceAllChart = new Chart(fceChart, {
    type: "line",
    data: fceData,
    options: chartOptions,
  });
})();
