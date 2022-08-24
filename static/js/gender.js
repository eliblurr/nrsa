(async () => {
  //Time Series chart for Historical data
  var casualGenderChart = document.getElementById("gender");

  const getData = async (option) => {
    const formdata = new FormData();
    formdata.append("option", option);

    const response = await fetch("/accidents/gender/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const getAllData = async () => {
    const formdata = new FormData();
    formdata.append("option", "F,K");

    const response = await fetch("accidents/gender/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const allData = await getAllData();
  console.log(allData);

  var genderData = {
    label: "Casualties by Gender (Males)",
    data: allData.K.map((d) => d.Male),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "#853D43",
  };

  var gendaData = {
    label: "Casualties by Gender (females)",
    data: allData["K"].map((d) => d.Female),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "blue",
  };

  var gendarData = {
    labels: [
      1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
      2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
      2015, 2016, 2017, 2018, 2019, 2020,
    ],
    datasets: [genderData, gendaData],
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

  var casGenderChart = new Chart(casualGenderChart, {
    type: "line",
    data: gendarData,
    options: chartOptions,
  });

  //FATALITIES

    var genderFatChart = document.getElementById("gender2");
     var fatMaleData = {
       label: "Fatalities by Gender (Males)",
       data: allData["K"].map((d) => d.Male),
       lineTension: 0.5,
      borderWidth: 2,
       radius: 1,
       fill: false,
      borderColor: "#853D43",
    };

    var fatFemaleData = {
      label: "Fatalities by Gender (Females)",
      data: allData["K"].map((d) => d.Female),
      lineTension: 0.5,
      fill: false,
      borderWidth: 2,
      radius: 1,
      borderColor: "blue",
    };

    var genderFatData = {
      labels: [
        1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
        2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
        2015, 2016, 2017, 2018, 2019, 2020,
      ],
      datasets: [fatMaleData, fatFemaleData],
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

    var fatGenderChart = new Chart(genderFatChart, {
      type: "line",
      lineThickness: -10,
      data: genderFatData,
      options: chartOptions,
    });
})();
