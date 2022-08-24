(async () => {
  //Time Series chart for Historical data
  var ageChart = document.getElementById("ageGroup");

  const getData = async (option) => {
    const formdata = new FormData();
    formdata.append("option", option);

    const response = await fetch("accidents/age_group/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const getAllData = async () => {
    const formdata = new FormData();
    formdata.append("option", "E, I");

    const response = await fetch("accidents/age_group/", {
      method: "post",
      body: formdata,
    });
    const data = await response.json();

    return data;
  };

  const allData = await getAllData();
  console.log(allData);

  var agekidsData = {
    label: "0-5",
    data: allData.E.map((d) => d.Ages_0_to_5),
    lineTension: 0.5,
    borderWidth: 2,
    radius: 1,
    fill: false,
    borderColor: "black",
  };

    var ageTeenData = {
      label: "6-15",
      data: allData.E.map((d) => d.Ages_6_to_15),
      lineTension: 0.5,
      borderWidth: 2,
      radius: 1,
      fill: false,
      borderColor: "#853D43",
    };

   var ageMidData = {
     label: "16-25",
     data: allData.E.map((d) => d.Ages_16_to_25),
     lineTension: 0.5,
     borderWidth: 2,
     radius: 1,
     fill: false,
     borderColor: "purple",
   };

    var ageYouthData = {
      label: "28-35",
      data: allData.E.map((d) => d.Ages_28_to_35),
      lineTension: 0.5,
      borderWidth: 2,
      radius: 1,
      fill: false,
      borderColor: "red",
    };

     var ageAdultData = {
       label: "36-40",
       data: allData.E.map((d) => d.Ages_36_to_45),
       lineTension: 0.5,
       borderWidth: 2,
       radius: 1,
       fill: false,
       borderColor: "green",
     };

      var ageGrownData = {
        label: "46-55",
        data: allData.E.map((d) => d.Ages_46_to_55),
        lineTension: 0.5,
        borderWidth: 2,
        radius: 1,
        fill: false,
        borderColor: "yellow",
      };

       var ageData = {
         label: "58-65",
         data: allData.E.map((d) => d.Ages_58_to_65),
         lineTension: 0.5,
         borderWidth: 2,
         radius: 1,
         fill: false,
         borderColor: "darkgreen",
       };

        var agedData = {
          label: "Above 65",
          data: allData.E.map((d) => d.Ages_Over_65),
          lineTension: 0.5,
          borderWidth: 2,
          radius: 1,
          fill: false,
          borderColor: "darkblue",
        };

  var agesData = {
    labels: [
      1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002,
      2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
      2015, 2016, 2017, 2018, 2019, 2020,
    ],
    datasets: [agekidsData, ageTeenData, ageMidData, ageYouthData, ageAdultData, ageGrownData, ageData, agedData],
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

  var ageGroup = new Chart(ageChart, {
    type: "line",
    data: agesData,
    options: chartOptions,
  });
})();
