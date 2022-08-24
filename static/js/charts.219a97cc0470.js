(async () => {
  const monthsLabels = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  const regionsLabel = [
    "Accra",
    "Tema",
    "Eastern",
    "Central",
    "Western",
    "Ashanti",
    "Volta",
    "Northern",
    "Upper West",
    "Upper East",
    "Bono",
    "Bono East",
    "Ahafo",
    "Oti",
    "Savanna",
    "Western North",
    "North East",
  ];
  //collapsible div
  var coll = document.getElementsByClassName("collapsible");
  var i;

  for (i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
      // this.classList.toggle("active");
      var content = this.nextElementSibling;
      if (content.style.display === "block") {
        content.style.display = "none";
      } else {
        content.style.display = "block";
      }
    });
  }

    const getData = async (category, region, date_from, date_to, specific = "") => {
    const formData = new FormData();
    formData.append("date_from", date_from);
    formData.append("date_to", date_to);
    formData.append("category", category); // RC, Priv, com, inj, totkilled, gov
    formData.append("region", region);
    formData.append("submit", "submit");
    formData.append("specific", specific)

    const res = await fetch("accidents/chart/", {
      method: "post",
      body: formData,
    });
    const data = await res.json();

    return data;
  };

  const plotTotalCases = async () => {
    const init_data = await getData("RC", "ghana", "2020-01-01", "2020-12-31", "all");
    //Total cases reported in 2021
    data = {};
    init_data.forEach((d) => {
      if (data[d.month]) {
        data[d.month]["fatal"] += d.fatal;
        data[d.month]["serious"] += d.serious;
        data[d.month]["minor"] += d.minor;
      } else {
        data[d.month] = {};
        data[d.month]["fatal"] = d.fatal;
        data[d.month]["serious"] = d.serious;
        data[d.month]["minor"] = d.minor;
      }
    });

    const displayCases = document.getElementById("Year");

    let Year21 = new Chart(displayCases, {
      type: "bar",
      data: {
        labels: monthsLabels,

        datasets: [
          {
            label: "Fatal",
            fill: false,
            data: monthsLabels.map((d) => data[d].fatal),
            backgroundColor: "#E91E63",
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
            ],
            borderWidth: 1,
          },

          {
            label: "Serious",
            fill: false,
            data: monthsLabels.map((d) => data[d].serious),
            backgroundColor: "#3F51B5",
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
            ],
            borderWidth: 1,
          },
          {
            label: "Minor",
            data: monthsLabels.map((d) => data[d].minor),
            fill: false,
            backgroundColor: "#004D40",
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        title: {
          display: true,
        },
        responsive: true,

        tooltips: {
          callbacks: {
            labelColor: function (tooltipItem, chart) {
              return {
                borderColor: "rgb(255, 0, 20)",
                backgroundColor: "rgb(255,20, 0)",
              };
            },
          },
        },
        legend: {
          labels: {
            // This more specific font property overrides the global property
            fontColor: "red",
          },
        },
      },
    });
  }

  const plotRegionalCases = async () => {
    const init_data = await getData("all", "ghana", "2020-01-01", "2020-12-31", "RC");
    //Total cases reported in 2021
    data = {};
    init_data.forEach((d) => {
      if (data[d.region]) {
        data[d.region] += d.RC_total;
      } else {
        data[d.region] = d.RC_total;
      }
    });

    //Regions that cases were recorded
    const dataReg = {
      labels: regionsLabel,
      datasets: [
        {
          label: "Recorded cases Regional",
          data: regionsLabel.map(p => data[p]),
          backgroundColor: "rgb(255, 99, 132)",
          borderColor: "rgb(255, 99, 132)",
        },
      ],
    };

    const configRegionN = {
      type: "bar",
      data: dataReg,
    };

    const Regions = new Chart(document.getElementById("RegionsN"), configRegionN);
  }

  const plotVehiclesCases = async () => {
    const init_data = await getData("all", "ghana", "2020-01-01", "2020-12-31", "all");
    //Total cases reported in 2021
    data = {};
    init_data[1].forEach((d) => {
      if (data[d.month] && data[d.month]["Com_total"]) {
        data[d.month]["Com_total"] += d.Com_total;
      } else {
        data[d.month] = {};
        data[d.month]["Com_total"] = d.Com_total;
      }
    });
    init_data[2].forEach((d) => {
      if (data[d.month] && data[d.month]["Priv_total"]) {
        data[d.month]["Priv_total"] += d.Priv_total;
      } else {
        data[d.month]["Priv_total"] = d.Priv_total;
      }
    });
    init_data[3].forEach((d) => {
      if (data[d.month] && data[d.month]["Cyc_total"]) {
        data[d.month]["Cyc_total"] += d.Cyc_total;
      } else {
        data[d.month]["Cyc_total"] = d.Cyc_total;
      }
    });

    //Vehicles involved in 2021 accidents
    const showVehicles = document.getElementById("vehiclesN");
    const VYear = new Chart(showVehicles, {
      type: "bar",
      data: {
        labels: monthsLabels,

        datasets: [
          {
            label: "Commercial",
            fill: false,
            data: monthsLabels.map(p => data[p]["Com_total"]),
            backgroundColor: "#E91E63",
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
            ],
            borderWidth: 1,
          },

          {
            label: "Private",
            fill: false,
            data: monthsLabels.map(p => data[p]["Priv_total"]),
            backgroundColor: "#3F51B5",
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
            ],
            borderWidth: 1,
          },
          {
            label: ["Motorcycles"],
            data: monthsLabels.map(p => data[p]["Cyc_total"]),
            fill: false,
            backgroundColor: "#004D40",
            borderColor: [
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
              "rgba(255,99,132,1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        title: {
          display: true,
        },
        responsive: true,

        tooltips: {
          callbacks: {
            labelColor: function (tooltipItem, chart) {
              return {
                borderColor: "rgb(255, 0, 20)",
                backgroundColor: "rgb(255,20, 0)",
              };
            },
          },
        },
        legend: {
          labels: {
            // This more specific font property overrides the global property
            fontColor: "red",
          },
        },
      },
    });
  }

  const plotPedistrianCases = async () => {
    const init_data = await getData("all", "ghana", "2020-01-01", "2020-12-31", "all");
    data = {};
    init_data[4].forEach((d) => {
      if (data[d.region]) {
        data[d.region] += d.Ped_total;
      } else {
        data[d.region] = d.Ped_total;
      }
    });

    //Pedestrian cases recorded in 2021
    const dataPedestrians = {
      labels: regionsLabel,
      datasets: [
        {
          label: "Pedestrians cases (Regional)",
          data: regionsLabel.map(p => data[p]),
          backgroundColor: "rgb(255, 99, 132)",
          borderColor: "rgb(255, 99, 132)",
        },
      ],
    };

    const configPedestrians = {
      type: "bar",
      data: dataPedestrians,
    };

    const Pedestrians = new Chart(
      document.getElementById("pedestrian"),
      configPedestrians
    );
  }

  plotTotalCases()
  plotRegionalCases()
  plotVehiclesCases()
  plotPedistrianCases()
})();
