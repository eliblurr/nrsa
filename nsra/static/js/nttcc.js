(async () => {
  //Time Series chart for Historical data
  var nttccChart = document.getElementById("nttcc");

  const getData = async (option) => {
    const formdata = new FormData();
    formdata.append("option", option);

    const response = await fetch("/accidents/NTCC/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const getAllData = async () => {
    const formdata = new FormData();
    formdata.append("option", "M, N");

    const response = await fetch("accidents/NTCC/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const allData = await getAllData();
  console.log(allData);


  var damageNttccData = {
    label: "Damaged only",
    data: allData["M"].map((d) => d.damage_only),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "green",
  };

  var fatalNttccData = {
    label: "Fatal Crashes",
    data: allData["M"].map((d) => d.fatal_crashes),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "blue",
  };

  var injuryNttccData = {
    label: "Injury Crashes",
    data: allData["M"].map((d) => d.injury_crashes),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "red",
  };

  var nttccData = {
    labels: [
      1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
      2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
      2015, 2016, 2017, 2018, 2019, 2020,
    ],
    datasets: [damageNttccData, fatalNttccData, injuryNttccData],
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

  var casGenderChart = new Chart(nttccChart, {
    type: "line",
    data: nttccData,
    options: chartOptions,
  });

  //FATALITIES

  var nttcc2Chart = document.getElementById("nttcc2");

 var killedData = {
   label: "Total Killed",
   data: allData["N"].map((d) => d.killed),
   lineTension: 0.5,
   borderWidth: 2,
   radius: 1,
   fill: false,
   borderColor: "green",
 };

 var seriousInjData = {
   label: "Seriously Injured",
   data: allData.N.map((d) => d.seriously_injured),
   lineTension: 0.5,
   borderWidth: 2,
   radius: 1,
   fill: false,
   borderColor: "blue",
 };

 var slightlyInjData = {
   label: "Slightly Injured",
   data: allData["N"].map((d) => d.slightly_injured),
   lineTension: 0.5,
   borderWidth: 2,
   radius: 1,
   fill: false,
   borderColor: "red",
 };

 var nttcc2Data = {
   labels: [
     1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
     2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
     2015, 2016, 2017, 2018, 2019, 2020,
   ],
   datasets: [ killedData, seriousInjData, slightlyInjData],
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

  var nttcc2Chart = new Chart(nttcc2Chart, {
    type: "line",
    lineThickness: -10,
    data: nttcc2Data,
    options: chartOptions,
  });
})();
