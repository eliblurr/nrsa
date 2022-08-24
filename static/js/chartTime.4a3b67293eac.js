(async () => {
  //Time Series chart for Historical data
  var trafficChart = document.getElementById("byRoad");

  const getData = async (option) => {
    const formdata = new FormData();
    formdata.append("option", option);

    const response = await fetch("accidents/NTF/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const getAllData = async () => {
    const formdata = new FormData();
    formdata.append("option", "A,B,C,D,E,F,G,H,I,J,K,L,M,N");

    const response = await fetch("accidents/NTF/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const allData = await getAllData();
  console.log(allData);

  var allCrashesData = {
    label: "All crashes",
    data: allData.A.map((d) => d.all_crashes),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "#853D43",
  };

  var allCasData = {
    label: "Casualties",
    data: allData["A"].map((d) => d.all_casualties),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "blue",
  };

   var fatalitiesData = {
     label: "Fatalities",
     data: allData["A"].map((d) => d.fatalities),
     lineTension: 0.5,
     borderWidth: 2,
     radius: 1,
     fill: false,
     borderColor: "blue",
   };

  var trafficData = {
    labels: [
      1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
      2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
      2015, 2016, 2017, 2018, 2019, 2020,
    ],
    datasets: [allCrashesData, allCasData, fatalitiesData],
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

  var roadChart = new Chart(trafficChart, {
    type: "line",
    data: trafficData,
    options: chartOptions,
  });
})();
  //casualties
//   var casualtiesChart = document.getElementById("Casaulties");

//   var environsData = {
//     label: "Distribution of casualties by road environments",
//     data: allData["J"].map((d) => d.Total),
//     lineTension: 0.5,
//     fill: false,
//     borderWidth: 2,
//     radius: 1,
//     borderColor: "green",
//   };
//   var roadsUserData = {
//     label: "Distribution of casualties by road",
//     data: allData["G"].map((d) => d.Total),
//     lineTension: 0.5,
//     borderWidth: 2,
//     radius: 1,
//     fill: false,
//     borderColor: "#853D43",
//   };

//   var sexData = {
//     label: "distribution of  casualties by  sexs",
//     data: allData["K"].map((d) => d.Total),
//     lineTension: 0.5,
//     fill: false,
//     borderWidth: 2,
//     radius: 1,
//     borderColor: "blue",
//   };

//   var casualtiesData = {
//     labels: [
//       1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
//       2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
//       2015, 2016, 2017, 2018, 2019, 2020,
//     ],
//     datasets: [environsData, roadsUserData, sexData],
//   };

//   var chartOptions = {
//     legend: {
//       display: true,
//       position: "top",
//       labels: {
//         boxWidth: 80,
//         fontColor: "black",
//       },
//     },
//   };

//   var lineChart = new Chart(casualtiesChart, {
//     type: "line",
//     lineThickness: -10,
//     data: casualtiesData,
//     options: chartOptions,
//   });

//   //Total Fatalities
//   var fatalitiesChart = document.getElementById("Fatalities");

//   var fatalityAgeData = {
//     label: "Distribution of fatalities by age groups",
//     data: allData["E"].map((d) => d.Total),
//     lineTension: 0.5,
//     borderWidth: 2,
//     radius: 1,
//     fill: false,
//     borderColor: "green",
//   };
//   var fatalitySexData = {
//     label: "Distribution of fatalities by sex",
//     data: allData["F"].map((d) => d.Total),
//     lineTension: 0.5,
//     borderWidth: 2,
//     radius: 1,
//     fill: false,
//     borderColor: "#853D43",
//   };

//   var fatalityRoadData = {
//     label: "Distribution of fatalities by road environments",
//     data: allData["B"].map((d) => d.Total),
//     lineTension: 0.5,
//     borderWidth: 2,
//     radius: 1,
//     fill: false,
//     borderColor: "blue",
//   };

//   var fatalitiesData = {
//     labels: [
//       1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
//       2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
//       2015, 2016, 2017, 2018, 2019, 2020,
//     ],
//     datasets: [fatalityAgeData, fatalitySexData, fatalityRoadData],
//   };

//   var chartOptions = {
//     legend: {
//       display: true,
//       position: "top",
//       labels: {
//         boxWidth: 80,
//         fontColor: "black",
//       },
//     },
//   };

//   var fatalityChart = new Chart(fatalitiesChart, {
//     type: "line",
//     lineThickness: -10,
//     data: fatalitiesData,
//     options: chartOptions,
//   });

//   //traffic fatalities

//   var trafficChart = document.getElementById("Traffic");

//   var nationalTrafficData = {
//     label: "Changes in national traffic fatality",
//     // data: ,
//     data: allData["A"].map((d) => d.all_casualties),
//     lineTension: 0.5,
//     borderWidth: 2,
//     radius: 1,
//     fill: false,
//     borderColor: "black",
//   };
//   var vehiclesData = {
//     label: "Vehicle types involved in crashes",
//     data: allData["L"].map((d) => d.Total),
//     lineTension: 0.5,
//     borderWidth: 2,
//     radius: 1,
//     fill: false,
//     borderColor: "blue",
//   };

//   var trafficData = {
//     labels: [
//       1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
//       2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
//       2015, 2016, 2017, 2018, 2019, 2020,
//     ],
//     datasets: [nationalTrafficData, vehiclesData],
//   };

//   var chartOptions = {
//     legend: {
//       display: true,
//       position: "top",
//       labels: {
//         boxWidth: 80,
//         fontColor: "black",
//       },
//     },
//   };

//   var fatalityChart = new Chart(trafficChart, {
//     type: "line",
//     data: trafficData,
//     options: chartOptions,
//   });
