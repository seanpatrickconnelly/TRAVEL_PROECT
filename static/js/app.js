function buildBubble(sample) {

      var url =  `/samples/${sample}`
  
      d3.json(url).then(function(data) {
    
        var Time2 = []
        var scale = 400
          if (sample === "securityDelay") {scale = 10}
            else if (sample === "weatherDelay") {scale = 50}
            else if (sample === "TotDelayArrFlight") {scale = 500}
        for (var i = 0, length = data.Time.length; i < length; i ++){
         Time2[i] = data.Time[i]/scale;
        }

        console.log(data)
        var xValues = data.AirportCode;
        var yValues = data.Count;
        var mSize = Time2;
        var mClrs = data.AirportCode;

        var trace_bubble = {
          x: xValues,
          y: yValues,
          mode: 'markers',
          marker: {
            size: mSize,
            colorscale: "YIGnBu"
          }
        };
     
        var data = [trace_bubble];
     
        var layout = {
          title: "Total Airport Delays (Circle Size Represents Minutes Delayed)",
          xaxis: {title: "Airport"},
          yaxis: {title: "Total Delays"}
        };

        Plotly.newPlot('bubble', data, layout);
  
      }
    )}

  function buildBar1(sample1) {

      var url = `/samples1/${sample1}`

      d3.json(url).then(function(data) {

      var trace1 = {
        x: data.AirportCode,
        y: data.Time,
        mode:"markers",
        type:"bar"
      };

      var data_1 = [trace1];

      var layout = {
      title:"Airport Delays By Minutes",
      xaxis: {title: "Airport"},
      yaxis: {title: "Total Minutes Delayed"}
      };

      Plotly.newPlot('bar1', data_1, layout);
        })
  };

  function buildBar2(sample2) {

    var url = `/samples2/${sample2}`

    d3.json(url).then(function(data) {

    var trace2 = {
    x: data.AirlineName,
    y: data.Time,
    mode:"markers",
    type:"bar"
  };

    var data_2 = [trace2];

    var layout = {
    title:"Total Airline Delays By Minutes",
    xaxis: {title: "Airline"},
    yaxis: {title: "Total Minutes Delayed"}
    };

  Plotly.newPlot('bar2', data_2, layout);
    })
  };

  function buildLine(sample3) {
    var url =  `/samples3/${sample3}`
    d3.json(url).then(function(data) {
  var trace3 = {
   x: data.Date,
   y: data.Time,
   type:"line"
  };
  var data_3 = [trace3];
  var layout = {
  title:"Average Minutes of Delay By Month",
  xaxis: {title: "Month"},
  yaxis: {title: "Total Minutes Delayed"}
  };
  Plotly.newPlot('line', data_3, layout);
  })
  };

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");
  // Use the list of reasons to populate the select options
  d3.json("/reasons").then((cleanNames) => {

    console.log(cleanNames)
    cleanNames.forEach((flight) => {
      selector
        .append("option")
        .text(flight)
        .property("value", flight);
    });

    // Use all reasons to build the initial plots
    //const allReasons = cleanNames[0];
    buildBubble('TotDelayArrFlight');
    buildBar1('TotDelayArrFlight');
    buildBar2('TotDelayArrFlight');
    buildLine('TotDelayArrFlight');
  });
}

  function optionChanged(newReason) {
    // Fetch new data each time a new reason is selected
    if (newReason == "All Delays"){
      newReason = "TotDelayArrFlight"
      }
      else if (newReason == "Airline"){
        newReason = "airlineDelay"
      }
      else if (newReason == "Late-Aircraft"){
        newReason = "lateAircraftDelay"
      }
      else if (newReason == "NAS"){
        newReason = "nasDelay"
      }
      else if (newReason == "Security"){
        newReason = "securityDelay"
      }
      else if (newReason == "Weather"){
        newReason = "weatherDelay"
      }

      buildBubble(newReason);
      buildBar1(newReason);
      buildBar2(newReason);
      buildLine(newReason)
  }

// Initialize the dashboard
init();

// Animation library
anime.timeline({loop: true})
  .add({
    targets: '.ml5 .line',
    opacity: [0.5,1],
    scaleX: [0, 1],
    easing: "easeInOutExpo",
    duration: 700
  }).add({
    targets: '.ml5 .line',
    duration: 600,
    easing: "easeOutExpo",
    translateY: function(e, i, l) {
      var offset = -0.625 + 0.625*2*i;
      return offset + "em";
    }
  }).add({
    targets: '.ml5 .letters-center',
    opacity: [0,1],
    scaleY: [0.5, 1],
    easing: "easeOutExpo",
    duration: 600,
    offset: '-=600'
  }).add({
    targets: '.ml5 .letters-left',
    opacity: [0,1],
    translateX: ["0.5em", 0],
    easing: "easeOutExpo",
    duration: 600,
    offset: '-=300'
  }).add({
    targets: '.ml5 .letters-right',
    opacity: [0,1],
    translateX: ["-0.5em", 0],
    easing: "easeOutExpo",
    duration: 600,
    offset: '-=600'
  }).add({
    targets: '.ml5',
    opacity: 0,
    duration: 1000,
    easing: "easeOutExpo",
    delay: 5000
  });