
$( window ).ready( async () => {
// window.onload = 
  let startDate = moment().subtract(1, "years");
  let endDate = moment();
  let region = "ghana";
  let data = {};
  const refreshEvent = new Event("refresh");

  const getCookie = (name) => {
    var match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    if (match) return match[2];
  };

  const createPieChart = (data) => {
    const pie = new d3pie("expand-plot", {
      data: {
        content: [...data],
      },
    });
    return pie;
  };

  const selectRegion = (element) => {
    if (element) {
      if (element.classList.contains("selected")) {
        element.classList.remove("selected");
        region = "ghana";
      } else {
        if (document.querySelector(".selected"))
          document.querySelector(".selected").classList.remove("selected");
        element.classList.add("selected");
        region = element.getAttribute("region_name");
      }
      document.dispatchEvent(refreshEvent);
    } else {
      region = "ghana";
      if (document.querySelector(".selected")) {
        document.querySelector(".selected").classList.remove("selected");
        document.dispatchEvent(refreshEvent);
      }
    }
  };

  document.addEventListener("refresh", async (e) => {
    let r = region;
    if (region == "Greater Accra") r = "Accra";

    data = await getData(r);
    document.querySelector(".total-crashes .plot-value").textContent =
      data["RC_total__sum"];
    document.querySelector(".total-fatalities .plot-value").textContent =
      data["Tk_total__sum"];
    document.querySelector(".total-injured .plot-value").textContent =
      data["injured__sum"];
    document.querySelector(".fatal-crashes .plot-value").textContent =
      data["fatal__sum"];
    document.querySelector(".commercial-vehicles .plot-value").textContent =
      data["Com_total__sum"];
    document.querySelector(".private-vehicles .plot-value").textContent =
      data["Priv_total__sum"];
    document.querySelector(".motorcycles .plot-value").textContent =
      data["Cyc_total__sum"];
    document.querySelector(".ped-knocked-down .plot-value").textContent =
      data["Ped_total__sum"];
  });

  const getData = async (region) => {
    // FETCH DATA FROM DJANGO BACKEND
    const formData = new FormData();

    formData.append("csrfmiddlewaretoken", getCookie("csrftoken"));
    formData.append("region", region);
    formData.append("date_from", startDate.format("YYYY-MM-DD"));
    formData.append("date_to", endDate.format("YYYY-MM-DD"));
    formData.append("submit", "submit");

    const r = await fetch("accidents/", {
      method: "post",
      body: formData,
    });
    return await r.json();
  };

  const setupCalendar = () => {
    document.querySelector(
      'input[name="daterange"]'
    ).value = `${startDate.format("MMMM YYYY")} → ${endDate.format(
      "MMMM YYYY"
    )}`;

    $(function () {
      $('input[name="daterange"]').daterangepicker(
        {
          opens: "center",
          autoUpdateInput: false,
          startDate: startDate,
          endDate: endDate,
          maxDate: endDate,
          minDate: "01/01/2020",
        },
        function (start, end, label) {
          document.querySelector(
            'input[name="daterange"]'
          ).value = `${start.format("MMMM YYYY")} → ${end.format("MMMM YYYY")}`;
          startDate = start;
          endDate = end;
          document.dispatchEvent(refreshEvent);
        }
      );
    });
  };

  let scale = 5000;
  let translate = [500, 1000];

  const map_data = await d3.json("/static/json/ghana_regions.json");

  const features = topojson.feature(map_data, map_data.objects.gha).features;

  const svg = d3
    .select("#canvas")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%");

  const renderMap = (f) => {
    const colors = {
      Ahafo: "#325B3A",
      Ashanti: "#7B3F00",
      Bono: "#E09540",
      "Bono East": "#1AAA55",
      Central: "#A56204",
      Eastern: "#FF9000",
      "Greater Accra": "#D26E25",
      Northern: "#02523D",
      "North East": "#00C6FF",
      Oti: "#075B5B",
      Savanna: "#005BFF",
      "Upper East": "#6C9259",
      "Upper West": "#CBCD5F",
      Volta: "#787806",
      Western: "#92762B",
      "Western North": "#EBB51A",
    };
    // Remove g element, if any
    d3.select("#canvas svg g").remove();

    const projection = d3.geoMercator().scale(scale).translate(translate);
    const path = d3.geoPath(projection);

    const g = svg.append("g");

    const handleZoom = (e) => g.attr("transform", e.transform);

    const zoom = d3.zoom().on("zoom", handleZoom);
    d3.select("svg").call(zoom);

    g.selectAll("path")
      .data(f)
      .enter()
      .append("path")
      .attr("class", "country")
      .attr("d", path)
      .attr("region_name", f => f.properties.ADM1_EN)
      .style("fill", f => colors[f.properties.ADM1_EN])

    function generateGetBoundingClientRect(x = 0, y = 0) {
      return () => ({
        width: 0,
        height: 0,
        top: y,
        right: x,
        bottom: y,
        left: x,
      });
    }

    const virtualElement = {
      getBoundingClientRect: generateGetBoundingClientRect(),
    };

    const paths = document.querySelectorAll(".country");

    const tooltip = document.querySelector("#region-tooltip");
    const popperInstance = new Popper(virtualElement, tooltip, {
      placement: "right",
      modifiers: {
        offset: {
          offset: "0,20",
        },
      },
    });

    for (el of paths) {
      const region_name = el.getAttribute("region_name");
      if (region_name === region) el.classList.add("selected");

      el.addEventListener("click", (e) => {
        e.stopImmediatePropagation();
        selectRegion(e.target);
        console.log(colors[region_name])
        document.querySelector("#total-crashes").style.backgroundColor = colors[region_name]
        document.querySelector("#total-injured").style.backgroundColor = colors[region_name]
        document.querySelector("#total-fatalities").style.backgroundColor = colors[region_name]
      });

      el.addEventListener("mouseenter", (e) => {
        tooltip.setAttribute("data-show", "");
        document.querySelector("#region-tooltip span").textContent =
          region_name;
        // // We need to tell Popper to update the tooltip position
        // // after we show the tooltip, otherwise it will be incorrect
        // popperInstance.update();
        // console.log('entering')
      });

      el.addEventListener("mouseleave", () => {
        tooltip.removeAttribute("data-show");
      });

      el.addEventListener("mousemove", ({ clientX: x, clientY: y }) => {
        virtualElement.getBoundingClientRect = generateGetBoundingClientRect(
          x,
          y
        );
        popperInstance.update();
      });
    }

    document
      .querySelector("#canvas")
      .addEventListener("click", () => selectRegion());
  };

  const setupExtraDataTooltips = () => {
    const tooltip = document.querySelector("#more-tooltip");
    const instance = new Popper(
      document.querySelector(".total-crashes"),
      tooltip,
      {
        placement: "right-start",
        modifiers: {
          offset: {
            offset: "0,5",
          },
        },
      }
    );

    // Total crashes
    document
      .querySelector(".total-crashes")
      .addEventListener("mouseenter", (e) => {
        const { fatal__sum, serious__sum, minor__sum } = data;
        const table = `
      <div>
        <table>
          <tr id="fatal__sum">
            <th>Fatal: </th>
            <td>${fatal__sum}</td>
          </tr>
          <tr id="serious__sum">
            <th>Serious injuries: </th>
            <td>${serious__sum}</td>
          </tr>
          <tr id="minor__sum">
            <th>Minor injuries: </th>
            <td>${minor__sum}</td>
          </tr>
        </table>
        <div id="expand-plot"></div>
      </div>
      `;
        tooltip.innerHTML = table;
        createPieChart([
          { label: "Fatal", value: fatal__sum },
          { label: "Serious injuries", value: serious__sum },
          { label: "Minor injuries", value: minor__sum },
        ]);
        instance.reference = e.target;
        instance.update();
        tooltip.setAttribute("data-show", "");
      });
    document
      .querySelector(".total-crashes")
      .addEventListener("mouseleave", (e) => {
        tooltip.removeAttribute("data-show");
      });

    // Total fatalities
    document
      .querySelector(".total-fatalities")
      .addEventListener("mouseenter", (e) => {
        const {
          male_over18__sum,
          male_under18__sum,
          female_over18__sum,
          female_under18__sum,
        } = data;
        const table = `
      <div>
        <table>
          <tr id="male_under18__sum">
            <th>Male under 18: </th>
            <td>${male_under18__sum}</td>
          </tr>
          <tr id="female_under18__sum">
            <th>Female under 18: </th>
            <td>${female_under18__sum}</td>
          </tr>
          <tr id="female_over18__sum">
            <th>Female over 18: </th>
            <td>${female_over18__sum}</td>
          </tr>
          <tr id="male_over18__sum">
            <th>Male over 18: </th>
            <td>${male_over18__sum}</td>
          </tr>
        </table>
        <div id="expand-plot"></div>
      </div>
      `;
        tooltip.innerHTML = table;
        createPieChart([
          { label: "Male under 18", value: male_under18__sum },
          { label: "Female under 18", value: female_under18__sum },
          { label: "Female over 18", value: female_over18__sum },
          { label: "Male over 18", value: male_over18__sum },
        ]);
        instance.reference = e.target;
        instance.update();
        tooltip.setAttribute("data-show", "");
      });
    document
      .querySelector(".total-fatalities")
      .addEventListener("mouseleave", (e) => {
        tooltip.removeAttribute("data-show");
      });
    // Total injured
    document
      .querySelector(".total-injured")
      .addEventListener("mouseenter", (e) => {
        // tooltip.setAttribute('data-show', '')
      });
    document
      .querySelector(".total-injured")
      .addEventListener("mouseleave", (e) => {
        tooltip.removeAttribute("data-show");
      });
    // Fatal crashes
    document
      .querySelector(".fatal-crashes")
      .addEventListener("mouseenter", (e) => {
        // tooltip.setAttribute('data-show', '')
      });
    document
      .querySelector(".fatal-crashes")
      .addEventListener("mouseleave", (e) => {
        // tooltip.removeAttribute('data-show')
      });
    // Commercial vehicles
    document
      .querySelector(".commercial-vehicles")
      .addEventListener("mouseenter", (e) => {
        const { bus__sum, minor_bus__sum, truck__sum, taxi__sum, other__sum } =
          data;
        const table = `
      <div>
        <table>
          <tr id="bus__sum">
            <th>Buses: </th>
            <td>${bus__sum}</td>
          </tr>
          <tr id="minor_bus__sum">
            <th>Minor buses: </th>
            <td>${minor_bus__sum}</td>
          </tr>
          <tr id="truck__sum">
            <th>Trucks: </th>
            <td>${truck__sum}</td>
          </tr>
          <tr id="taxi__sum">
            <th>Taxis: </th>
            <td>${taxi__sum}</td>
          </tr>
          <tr id="other__sum">
            <th>Other vehicles: </th>
            <td>${other__sum}</td>
          </tr>
        </table>
        <div id="expand-plot"></div>
      </div>
      `;
        tooltip.innerHTML = table;
        createPieChart([
          { label: "Buses", value: bus__sum },
          { label: "Minor buses", value: minor_bus__sum },
          { label: "Trucks", value: truck__sum },
          { label: "Taxis", value: taxi__sum },
          { label: "Other vehicles", value: other__sum },
        ]);
        instance.reference = e.target;
        instance.update();
        tooltip.setAttribute("data-show", "");
      });
    document
      .querySelector(".commercial-vehicles")
      .addEventListener("mouseleave", (e) => {
        tooltip.removeAttribute("data-show");
      });
    // Private vehicles
    document
      .querySelector(".private-vehicles")
      .addEventListener("mouseenter", (e) => {
        const { minibus__sum, salon__sum, suv__sum, govt__sum } = data;
        const table = `
      <div>
        <table>
          <tr id="minibus__sum">
            <th>Minibuses: </th>
            <td>${minibus__sum}</td>
          </tr>
          <tr id="salon__sum">
            <th>Salon cars: </th>
            <td>${salon__sum}</td>
          </tr>
          <tr id="suv__sum">
            <th>SUVs: </th>
            <td>${suv__sum}</td>
          </tr>
          <tr id="govt__sum">
            <th>Government vehicles: </th>
            <td>${govt__sum}</td>
          </tr>
        </table>
        <div id="expand-plot"></div>
      </div>
      `;
        tooltip.innerHTML = table;
        createPieChart([
          { label: "Minibuses", value: minibus__sum },
          { label: "Salon cars", value: salon__sum },
          { label: "Suvs", value: suv__sum },
          { label: "Government vehicles", value: govt__sum },
        ]);
        instance.reference = e.target;
        instance.update();
        tooltip.setAttribute("data-show", "");
      });
    document
      .querySelector(".private-vehicles")
      .addEventListener("mouseleave", (e) => {
        tooltip.removeAttribute("data-show");
      });
    // Motorcycles
    document
      .querySelector(".motorcycles")
      .addEventListener("mouseenter", (e) => {
        const { m_cycle__sum, bicycles__sum, handcart__sum, tricycle__sum } =
          data;
        const table = `
      <div>
        <table>
          <tr id="m_cycle__sum">
            <th>Motorcycles: </th>
            <td>${m_cycle__sum}</td>
          </tr>
          <tr id="bicycles__sum">
            <th>Bicycles: </th>
            <td>${bicycles__sum}</td>
          </tr>
          <tr id="handcart__sum">
            <th>Hand carts: </th>
            <td>${handcart__sum}</td>
          </tr>
          <tr id="tricycle__sum">
            <th>Tricycles: </th>
            <td>${tricycle__sum}</td>
          </tr>
        </table>
        <div id="expand-plot"></div>
      </div>
      `;
        tooltip.innerHTML = table;
        createPieChart([
          { label: "Motorcycles", value: m_cycle__sum },
          { label: "Bicycles", value: bicycles__sum },
          { label: "Hand carts", value: handcart__sum },
          { label: "Tricycles", value: tricycle__sum },
        ]);
        instance.reference = e.target;
        instance.update();
        tooltip.setAttribute("data-show", "");
      });
    document
      .querySelector(".motorcycles")
      .addEventListener("mouseleave", (e) => {
        tooltip.removeAttribute("data-show");
      });
    // Pedestrians knocked down
    document
      .querySelector(".ped-knocked-down")
      .addEventListener("mouseenter", (e) => {
        const { fatal__sum, serious__sum, minor__sum } = data;
        const table = `
      <div>
        <table>
          <tr id="fatal__sum">
            <th>Fatal: </th>
            <td>${fatal__sum}</td>
          </tr>
          <tr id="serious__sum">
            <th>Serious injuries: </th>
            <td>${serious__sum}</td>
          </tr>
          <tr id="minor__sum">
            <th>Minor injuries: </th>
            <td>${minor__sum}</td>
          </tr>
        </table>
        <div id="expand-plot"></div>
      </div>
      `;
        tooltip.innerHTML = table;
        createPieChart([
          { label: "Fatal", value: fatal__sum },
          { label: "Serious injuries", value: serious__sum },
          { label: "Minor injuries", value: minor__sum },
        ]);
        instance.reference = e.target;
        instance.update();
        tooltip.setAttribute("data-show", "");
      });
    document
      .querySelector(".ped-knocked-down")
      .addEventListener("mouseleave", (e) => {
        tooltip.removeAttribute("data-show");
      });
  };

  const populatedropdown = () => {
    const element = document.querySelector('.dropdown-menu li:first-child')
    const dropdown = document.querySelector("#year");
    const popper = new Popper(element, dropdown, { placement: 'left' })

    element.addEventListener('mouseenter', () => {
      dropdown.setAttribute('data-show', '')
      popper.update();
    })
    element.addEventListener('mouseleave', () => {
      dropdown.removeAttribute('data-show')
    })
  };

  const eventdropdown = () => {
    const element = document.querySelector(".dropdown-menu li:nth-child(2)");
    const dropdown = document.querySelector("#Quarter");
    const popper = new Popper(element, dropdown, { placement: 'left' })

    element.addEventListener('mouseenter', () => {
      dropdown.setAttribute('data-show', '')
      popper.update();
    })
    element.addEventListener('mouseleave', () => {
      dropdown.removeAttribute('data-show')
    })
  }

  const monthsdropdown = () => {
    const element = document.querySelector(".dropdown-menu li:nth-child(3)");
    const dropdown = document.querySelector("#months");
    const popper = new Popper(element, dropdown, { placement: "left" });

    element.addEventListener("mouseenter", () => {
      dropdown.setAttribute("data-show", "");
      popper.update();
    });
    element.addEventListener("mouseleave", () => {
      dropdown.removeAttribute("data-show");
    });
  };



  // regions is kind of like an array, so we can loop over it
  const regions = document.querySelectorAll("div[region_name]")
  // We use forEach to loop over things that behave like arrays
  regions.forEach(
    e => {
      const region_name = e.getAttribute("region_name");
      e.addEventListener("click", e => {
        region = region_name
        document.dispatchEvent(refreshEvent)
      })
    }
  )

  setupCalendar();
  renderMap(features);
  setupExtraDataTooltips();
  populatedropdown();
  eventdropdown();
  monthsdropdown();
  document.dispatchEvent(refreshEvent);
  
})
