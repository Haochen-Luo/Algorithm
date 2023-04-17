worldmapSymbol.js code:
export const worldFlightMap = (parent, props, factor,projectionSelect) => {
  let {
    countries,   
    airportsData,
    flightRoutesData, selectedContinents
  } = props;
  // console.log(props)
  // height+=100;
  const width = 1080;
  const height = 650;
  // console.log(parent.width,width,height)
  // Create an airport lookup object
  const airportLookup = {};
  airportsData.forEach(airport => {
    airportLookup[airport.Airport] = airport;
  });


  const projectionType = "natural";
  let projection = d3.geoOrthographic();
  if(projectionSelect==="globe"){
    projection = d3.geoOrthographic();
  }else{
    projection = d3.geoMercator();
  }
   
  let pathGenerator = d3.geoPath().projection(projection);

  // Group for map elements
  const g = parent.append('g');
  // Tool tip to provide more information
  const tooltip = parent.append("g")
  .attr("class", "tooltip")
  .style("display", "none");
  tooltip.append("rect")
  .attr("width", 150) 
  .attr("height", 50)
  .attr("fill", "white")
  .style("opacity", 0.8)
  .style("stroke", "black")

  tooltip.append("text")
    .attr("class", "country-name")
    .attr("x", 10)
    .attr("y", 20)
    .style("font-size", "12px");
  tooltip.append("text")
      .attr("class", "airport-count")
      .attr("x", 10)
      .attr("y", 40)
      .style("font-size", "12px");
  
  // Utility Function to Adjust the tool tip position
  function getElementPosition(element) {
    const rect = element.getBoundingClientRect();
    return {
      top: rect.top + window.pageYOffset,
      left: rect.left + window.pageXOffset,
    };
  }

  // Create the globe
  g.append("path")
    .attr("class", "sphere")
    .attr("d", pathGenerator({ type: "Sphere" }));

  const countryGroup = g.append("g");

  
    
  // Compute the number of airports for each country
  const airportsByCountry = {};
  airportsData.forEach(airport => {
    const country = airport.Country;
    airportsByCountry[country] = (airportsByCountry[country] || 0) + 1;
  });
  
  // Create a color scale based on the number of airports
  const colorScale = d3.scaleThreshold()
  .domain([5, 20, 50, 100, 200, 300, 400, 800, 1200])
  .range([
    '#B8DDB3',     '#92C38A',     '#69AD66',     '#469947',     '#2C8C3B',     '#237D36',     '#19682F',     '#00411D',     '#002D11',   ]);
 
  // Add a new group to hold the legend elements
  const colorBarWidth = 20;
const colorBarHeight = 100;
const legendGroup = parent.append('g')
.attr('transform', `translate(50, ${height - colorBarHeight - 100})`); // Move the color bar to the lower-left corner of the SVG

// Draw the segmented color bar

const segmentHeight = colorBarHeight / colorScale.range().length;
const colors = ['#B8DDB3', '#92C38A', '#69AD66', '#469947', '#2C8C3B', '#237D36', '#19682F', '#00411D', '#002D11'];
const tickValues = [5, 20, 50, 100, 200, 300, 400, 800, 1200];

colors.forEach((color, i) => {
legendGroup.append('rect')
  .attr('x', 0)
  .attr('y', i * segmentHeight)
  .attr('width', colorBarWidth)
  .attr('height', segmentHeight)
  .attr('fill', color);
});

// Add the text labels adjacent to the color bar
tickValues.forEach((value, i) => {
legendGroup.append('text')
  .attr('x', colorBarWidth + 5)
  .attr('y', i * segmentHeight + segmentHeight / 2)
  .attr('font-size', '10px')
  .attr('alignment-baseline', 'middle')
  .text(value);
});

// Add a title to the color bar
legendGroup.append('text')
.attr('x', -colorBarHeight / 2)
.attr('y', -10)
.attr('transform', 'rotate(-90)')
.attr('text-anchor', 'middle')

.text('Number of Airports');



  countryGroup.selectAll('path').data(countries.features)
    .enter().append('path')
      .attr('class', 'country')
      .attr('d', pathGenerator)
      .attr('fill', d => {
        const countryName = d.properties.name;
        const numAirports = airportsByCountry[countryName] || 0;      
        return colorScale(numAirports);
      })
      .text(d => `${d.properties.name}: ${airportsByCountry[d.properties.name] || 0} airports`)
      .on("mouseover", (event, d) => {
        const offsetX = 10;
        const offsetY = 80; // Adjust this value as needed
        const containerPos = getElementPosition(parent.node());
        tooltip.attr("transform", `translate(${event.clientX + offsetX - containerPos.left},${event.clientY - offsetY - containerPos.top})`);
        tooltip.style("display", "inline");
      
        const countryName = d.properties.name;
        const numAirports = airportsByCountry[countryName] || 0;
        tooltip.select(".country-name")
          .text(countryName);
        tooltip.select(".airport-count")
          .text(`${numAirports} airports`);
      })
      .on('mousemove', (event) => {
        const offsetX = 10;
        const offsetY = 80; // Adjust this value as needed
        const containerPos = getElementPosition(parent.node());
        tooltip.attr("transform", `translate(${event.clientX + offsetX - containerPos.left},${event.clientY - offsetY - containerPos.top})`);
      }).on("mouseout", () => {
        tooltip.style("display", "none");
      })
      .on("mouseleave", () => {
        tooltip.style("display", "none");
      });
  // Draw airports
  const airportMarkers = g.selectAll('.airport')
  .data(airportsData)
  .enter().append('circle')
    .attr('class', 'airport')
    .attr('cx', d => {
      const coords = projection([d.longitude, d.latitude]);
      return isFinite(coords[0]) ? coords[0] : null;
    })
    .attr('cy', d => {
      const coords = projection([d.longitude, d.latitude]);
      return isFinite(coords[1]) ? coords[1] : null;
    })
    .attr('r', 1)
    .filter(d => {
      const coords = projection([d.longitude, d.latitude]);
      return isFinite(coords[0]) && isFinite(coords[1]);
    });

        // Filter the flight routes based on the selected continents
  const selectedFlightRoutesData = flightRoutesData.filter((route) => {
    if (!selectedContinents || selectedContinents.length === 0) {
      return false;
    }
    // console.log(route.Source_airport_ID,airportLookup[route.Source_airport_ID])
    // console.log(route.Destination_airport_ID,airportLookup[route.Destination_airport_ID])
    const source = airportLookup[route.Source_airport_ID];
    const dest = airportLookup[route.Destination_airport_ID];
    // console.log(source,dest)
    if(source!=undefined&&dest!=undefined){
      const sourceContinent = airportLookup[route.Source_airport_ID].Continent;
      const destContinent = airportLookup[route.Destination_airport_ID].Continent;
      // console.log('good')
      return (
        selectedContinents.includes(sourceContinent) ||
        selectedContinents.includes(destContinent)
      );
    }else{
      return false;
    }
 
  });

  // Update the route lines
  // const  filteredRoutes  = g.selectAll('.flight-route')
    // .data(filteredFlightRoutesData.slice(0, limit), d => d.ID);
    
    function filterRoutes(percentage, routes) {
      // const sortedRoutes = [...routes].sort((a, b) => b.Stops - a.Stops);
      const numRoutes = Math.ceil(percentage * routes.length);
      return routes.slice(0, numRoutes);
    }
  

      
  const filteredRoutes = filterRoutes(factor, selectedFlightRoutesData);
  // Draw flight routes
  const flightRoutes = g.selectAll('.flight-route')
    .data(filteredRoutes)
    .enter().append('path')
      .attr('class', 'flight-route')
      .attr('d', d => {
        const source = airportLookup[d.Source_airport_ID];
        const destination = airportLookup[d.Destination_airport_ID];

        if (source && destination) {
          const coordinates = [
            // console.log(source.longitude,source.Longitude)
            [source.longitude, source.latitude],
            [destination.longitude, destination.latitude]
          ];
          return pathGenerator({ type: "LineString", coordinates: coordinates });
        }
        return null;
      });

  // Update positions of airports and flight routes during rotation
  function updatePositions() {
    airportMarkers
      .attr('cx', d => projection([d.longitude, d.latitude])[0])
      .attr('cy', d => projection([d.longitude, d.latitude])[1]);

    flightRoutes.attr('d', d => {
      const source = airportLookup[d.Source_airport_ID];
      const destination = airportLookup[d.Destination_airport_ID];

      if (source && destination) {
        const coordinates = [
          [source.longitude, source.latitude],
          [destination.longitude, destination.latitude]
        ];
        return pathGenerator({ type: "LineString", coordinates: coordinates });
      }
      return null;
    });
  }

  // Zoom and rotation interactivity
  const sensitivity = 70;
  if(projectionSelect!=="globe"){
    // console.log(projection.type())
    parent.call(d3.zoom()
      .scaleExtent([1, 8])
      .translateExtent([[0, 0], [width, height]])
      .on('zoom', event => {
        g.attr('transform', event.transform);
      }));
  
  }else{

  
  parent.call(d3.drag().on("drag", (event) => {
    const rotate = projection.rotate();
    const k = sensitivity / projection.scale();
    projection.rotate([
      rotate[0] + event.dx * k,
      rotate[1] - event.dy * k
    ]);
    pathGenerator = d3.geoPath().projection(projection);
    g.selectAll(".country").attr("d", pathGenerator);
    updatePositions();
  }))
  .call(d3.zoom()
    .scaleExtent([1, 8])
    .translateExtent([[0, 0], [width, height]])
    .on('zoom', event => {
      g.attr('transform', event.transform);
    }));}

};

Above is all the worldmapSymbol.js code

Now is packedcircle.js code:
import { countryToContinentData } from "./createChordData.js";

export const airportsByCountryData = () => {
  return new Promise((resolve) => {
    d3.csv("./data/airports.csv").then((airportsData) => {
      const airportsByCountry = {};
      airportsData.forEach((airport) => {
        const country = airport.Country;
        airportsByCountry[country] = (airportsByCountry[country] || 0) + 1;
      });
      resolve(airportsByCountry);
    });
  });
};

let x, y, width,height,xAxis, yAxis, histogram;

let continentData = [  {
      "name": "Oceania","value": 620},  {"name": "North America","value": 2322},  {"name": "Europe",   "value": 1848},  
      {"name": "Africa","value": 757  },  {"name": "South America","value": 705  },  {"name": "Asia","value": 1439}];
export const coordinateView = (svgPackedCircle,svgHistogram) => {
  const countryToContinent = countryToContinentData();
  airportsByCountryData().then((airportsByCountry) => {
    const continentsData = {};

    // Iterate through the airportsByCountry object
    for (const country in airportsByCountry) {
      const continent = countryToContinent[country];
      if (continent === "Antarctica") continue;
      const airportCount = airportsByCountry[country];

      // If the continent is not in the continentsData object, add it with an empty children array
      if (!continentsData[continent]) {
        continentsData[continent] = { name: continent, children: [] };
      }

      // Add the country with its airport count to the children array of the corresponding continent
      continentsData[continent].children.push({ name: country, value: airportCount });
      
    }
    

    // Create the final data structure needed for the packed circles
    const packedCirclesData = {
      name: "Continents",
      children: Object.values(continentsData),
    };
    // console.log(packedCirclesData)
    
    continentData = packedCirclesData.children.map(continent => ({
      name: continent.name,
      value: continent.children.reduce((acc, country) => acc + country.value, 0)
    })).sort((a, b) => b.value - a.value);
    const initialHistogramData = continentData;
    // console.log(continentData);
    
    createHistogram(svgHistogram, initialHistogramData);
    renderZoomablePackedCircles(svgPackedCircle, packedCirclesData);
    // Extract continent data from the packed circles data and sum up the values per continent
    // console.log(continentData);
    
});

function renderZoomablePackedCircles(svg, data) {
    const width = +svg.attr('width');
    const height = +svg.attr('height');
    
    const color = d3.scaleOrdinal(d3.schemeTableau10);
  
    const pack = data => d3.pack()
      .size([width, height])
      .padding(6)
    (d3.hierarchy(data)
      .sum(d => d.value)
      .sort((a, b) => b.value - a.value))
  
    const root = pack(data);
    let focus = root;
    let view;


    
  
svg.attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
    .style("display", "block")
    .style("margin", "0 -14px")
    .style("background", "#c2dbef")
    // #fcd671;#b7a2e2;#9de0b5;#9ac3e5;
    .style("cursor", "pointer")
    .style("border", "1px solid rgba(0, 0, 0, 0.2)") // Add a border
    .style("border-radius", "30px") // Add border radius
    // .style("box-shadow", "0 4px 6px rgba(0, 0, 0, 0.1)") // Add a box shadow
    .on("click", (event) => zoom(event, root));
  
    const node = svg.append("g")
      .selectAll("circle")
      .data(root.descendants().slice(1))
      .join("circle")
        .attr("fill", d => d.children ? color(d.data.name) : "white")
        .attr("pointer-events", d => !d.children ? "none" : null)
        .on("mouseover", function() { d3.select(this).attr("stroke", "#000"); })
        .on("mouseout", function() { d3.select(this).attr("stroke", null); })
        .on("click", (event, d) => focus !== d && (zoom(event, d), event.stopPropagation()));
        const label = svg.append("g")
        .style("font", "10px sans-serif")
        .attr("pointer-events", "none")
        .attr("text-anchor", "middle")
      .selectAll("text")
      .data(root.descendants())
      .join("text")
        .style("fill-opacity", d => d.parent === root ? 1 : 0)
        .style("display", d => d.parent === root ? "inline" : "none")
        .style("font-size", d => d.depth === 1 ? "18px" : "10px") // Increase font size for continents
        .text(d => d.data.name);
  
    zoomTo([root.x, root.y, root.r * 2]);
  
    function zoomTo(v) {
      const k = width / v[2];
  
      view = v;
  
      label.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
      node.attr("transform", d => `translate(${(d.x - v[0]) * k},${(d.y - v[1]) * k})`);
      node.attr("r", d => d.r * k);
    }
  
    function zoom(event, d) {
      const focus0 = focus;
      focus = d;
  
      const transition = svg.transition()
          .duration(event.altKey ? 7500 : 750)
          .tween("zoom", d => {
            const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2]);
            return t => zoomTo(i(t));
          });
  
      label
        .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
        .transition(transition)
          .style("fill-opacity", d => d.parent === focus ? 1 : 0)
          .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
          .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
      
           // Update histogram data based on zoom level
      if (focus === root) {
        console.log(focus)
        updateHistogram(continentData);
      } else if (focus.depth === 1) { // Continent level
        console.log('anothe level')
        const topCountries = focus.data.children.slice(0).sort((a, b) => b.value - a.value).slice(0, 10);
        updateHistogram(topCountries);
      }
    }
  

    return svg.node();
  }
}
const margin = { top: -40, right: 40, bottom: 45, left: 20 };
function createHistogram(svgHistogram, data) {
  width = +svgHistogram.attr('width');
  height = +svgHistogram.attr('height');
  
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // X and Y scales
  x = d3.scaleBand().range([0, innerWidth]).padding(0.1);
  y = d3.scaleLinear().range([innerHeight, 0]);

  // X and Y axis
  xAxis = d3.axisBottom(x).tickSizeOuter(0);;
  yAxis = d3.axisLeft(y);

  // Create histogram group and apply margins
  histogram = svgHistogram.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);
  histogram.append('text')
    .attr('class', 'histogram-title')
    .attr('x', width / 2)
    .attr('y', margin.top / 2+80)
    .attr('text-anchor', 'middle')
    .style('font-size', '16px')
    .style('font-weight', 'bold')
    .text('Airport Number Ranking by Continent/Country');
  // Initialize the histogram
  updateHistogram(data);
}

function updateHistogram(data) {
  // Set the new domains for the scales
  x = d3.scaleBand()
    .domain(data.map(d => d.name))
    .range([margin.left, width - margin.right])
    .padding(0.3)

  y = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)]).nice()
    .range([height - margin.bottom, margin.top])

  // Update the X axis
  histogram.selectAll('.x-axis').remove();
  // histogram.append('g')
  //   .attr('class', 'x-axis')
  //   .attr('transform', `translate(0,${innerHeight})`)
  //   .call(xAxis);
  
  xAxis = g => g
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x).tickSizeOuter(0))

  yAxis = g => g
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y))
    .call(g => g.select(".domain").remove())


  // Update the Y axis
  histogram.selectAll('.y-axis').remove();


  // Update the bars
  const bars = histogram.selectAll('.bar')
    .data(data, d => d.name);

  bars.enter().append('rect')
    .attr('class', 'bar')
    .attr('x', d => x(d.name))
    .attr('width', x.bandwidth())
    .attr('fill', (d, i) => d3.schemeCategory10[0])
    .attr('opacity',0.6)
    .merge(bars)
      .transition()
      .duration(750)
      .attr('y', d => y(d.value))
      .attr('height', d => y(0) - y(d.value));
  
    

  bars.exit().remove();
  
  histogram.append("g")
    .attr("class", "x-axis")
    .call(xAxis)    
  histogram.append("g")
    .attr("class", "y-axis")
    .call(yAxis);
}

