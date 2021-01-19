
////////////////////////////////funciones para mostrar graficas///////////////////////////////

function graficPrincipal(){

    var $graficPrin = $("#grafic-prin");
    $.ajax({
        url: $graficPrin.data("url"),
      success: function (data) {

        var ctx = $graficPrin[0].getContext("2d");

        var cont = data.contador;
        document.getElementById('estudiantes').innerHTML= cont;
        var inst = data.instituciones;
        document.getElementById('instituciones').innerHTML= inst;
        var muni = data.municipios;
        document.getElementById('municipios').innerHTML= muni;

        var puntaje = {
          label: 'Puntaje',
              backgroundColor: 'blue',
              data:data.data
        };

        var estudiantes = {
          label: 'Estudiantes',
          backgroundColor: 'red',
          data:data.conta
        };

        var genero = {
          label: 'Genero',
          backgroundColor: 'dark'
        };

        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [puntaje,estudiantes]
          },
          options: {
            responsive: true,
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Puntaje Promedio global y numero de estudiantes por municipio'
            }
          }
        });

      }
    });
}

function punt_anio(){
  var $punt_anio = $("#punt-anio");
  $.ajax({
    url: $punt_anio.data("url"),
    success: function (data) {
      var ctx = $punt_anio[0].getContext("2d");
      var puntaje = {
        label: 'Puntaje',
        borderColor: 'blue',
        data:data.puntajes
      };
      new Chart(ctx, {
          type: 'line',
          data: {
            labels: data.labels,
            datasets: [puntaje]
          },
          options: {
            responsive: false,
            legend: {
              position: 'top',
            },
            title: {
              display: false,
              // text: 'Puntaje global por año'
            }
          }
        });
    }
  });
}

function tot_est(){
  var $tot_est = $("#tot-est");

  $.ajax({
    url: $tot_est.data("url"),
    success: function (data) {
      var ctx = $tot_est[0].getContext("2d");
      function getRandomColor() {
        var letters = "0123456789ABCDEF".split("");
        var color = "#";
        for (var i = 0; i < 6; i++ ) {
          color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
      }
      var estudiantes = {
          label: 'Estudiantes',
          backgroundColor: [
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),
                getRandomColor(),

            ],
          data:data.conta

        };
      new Chart(ctx, {
          type: 'pie',
          data: {
            labels: data.labels,
            datasets: [estudiantes]
          },
          options: {
            responsive: false,
            legend: {
              position: 'right',
            },
            title: {
              display: false,
              // text: 'Puntaje global y numero de estudiantes por municipio'
            }
          }
        });

    }
  });
}

function lectura_critic_ciudad(){

  var $graf = $("#graf");
  $.ajax({
      url: $graf.data("url"),
      success: function (data) {

        var ctx = $graf[0].getContext("2d");

        var punt2012 = {
          label: '2012',
          backgroundColor: 'gray',
          data:data.punt2012,
          borderColor: 'gray',
          lineTension: 0,
          fill: false,
        }

        var punt2013 = {
          label: '2013',
          backgroundColor: 'black',
          data:data.punt2013,
          borderColor: 'black',
          lineTension: 0,
          fill: false,
        }

        var punt2014 = {
          label: '2014',
          backgroundColor: 'orange',
          data:data.punt2014,
          borderColor: 'orange',
          lineTension: 0,
          fill: false,
        }

        var punt2015 = {
          label: '2015',
          backgroundColor: 'purple',
          data:data.punt2015,
          borderColor: 'purple',
          lineTension: 0,
          fill: false,
        }

        var punt2016 = {
          label: '2016',
          backgroundColor: 'green',
          data:data.punt2016,
          borderColor: 'green',
          lineTension: 0,
          fill: false,
        }

        var punt2017 = {
          label: '2017',
          backgroundColor: 'violet',
          data:data.punt2017,
          borderColor: 'violet',
          lineTension: 0,
          fill: false,
        }

        var punt2018 = {
          label: '2018',
          backgroundColor: 'brown',
          data:data.punt2018,
          borderColor: 'brown',
          lineTension: 0,
          fill: false,
        }

        var punt2019 = {
          label: '2019',
          backgroundColor: 'red',
          data:data.punt2019,
          borderColor: 'red',
          lineTension: 0,
          fill: false,
        };

        var punt2020 = {
          label: '2020',
          backgroundColor: 'yellow',
          data:data.punt2020,
          borderColor: 'yellow',
          lineTension: 0,
          fill: false,
        };

        var punt2021 = {
          label: '2021',
          backgroundColor: 'blue',
          data:data.punt2021,
          borderColor: 'blue',
          lineTension: 0,
          fill: false,
        }

        var punt2022 = {
          label: '2022',
          backgroundColor: 'gray',
          data:data.punt2022,
          borderColor: 'gray',
          lineTension: 0,
          fill: false,
        }

        var punt2023 = {
          label: '2023',
          backgroundColor: 'violet',
          data:data.punt2023,
          borderColor: 'violet',
          lineTension: 0,
          fill: false,
        }

        let dato;
        if (data.punt2017[0] != null || data.punt2018[0] != null || data.punt2019[0] != null || data.punt2020[0] != null || data.punt2021[0] != null || data.punt2022[0] != null || data.punt2023[0] != null){
            dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017]
            }
          if (data.punt2018[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018]
            }
          }
          if (data.punt2019[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018,punt2019]
            }
          }
          if (data.punt2020[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018,punt2019,punt2020]
            }
          }
          if (data.punt2021[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018,punt2019,punt2020,punt2021]
            }
          }
          if (data.punt2022[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018,punt2019,punt2020,punt2021,punt2022]
            }
          }
          if (data.punt2023[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018,punt2019,punt2020,punt2021,punt2022,punt2023]
            }
          }
        }


        else
          dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016]
          }

        window.grafica = new Chart(ctx, {
          type: 'line',
          data: dato,
          options: {
            responsive: true,
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Puntaje lectura critica por municipio y año'
            },
              pan: {
                  enabled: true,
                  mode: "xy",
                  speed: 10,
                  threshold: 10
              },
              zoom: {
                enabled: true,
                drag: false,
                mode: "xy",
                speed: 0.01,
                // sensitivity: 0.1,
                limits: {
                  max: 10,
                  min: 0.5
                }
              }
          }
        });
      }
    });
}
function op(){
  var graph=document.getElementById("graf");
  var btn=document.getElementById("btn_resetZoom");
  var tb=document.getElementById("container");
  var select = document.getElementById("op");
  if (select.value == "tabla"){
    graph.style.display='none';
    btn.style.display='block';
    tb.style.display='block';
    const tableContainer = document.getElementById('container');
    const xAxis = grafica.data.labels;
    const yAxis = grafica.data.datasets;

    const tableHeader = `<tr>${
        xAxis.reduce((memo, entry) => {
            memo += `<th>${entry}</th>`;
            return memo;
        }, '<th>AÑO:</th>')
    }</tr>`;

    const tableBody = yAxis.reduce((memo, entry) => {
        const rows = entry.data.reduce((memo, entry) => {
            memo += `<td>${entry}</td>`
            return memo;
        }, '');

        memo += `<tr><td>${entry.label}</td>${rows}</tr>`;

        return memo;
    }, '');

    const table = ` 
                    <div id="tabla" class="container-fluid">
                        <div class="card shadow mb-4">
                                <div class="card-body">
                                    <div class="table-responsive">
                                        <table class="table table-striped table-bordered" id="dataTable" width="100%" cellspacing="0">
                                            <thead>
                                                ${tableHeader}
                                            </thead>
                                            <tbody>
                                                ${tableBody}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        <script>
                            $('#dataTable').DataTable({
                                "pagingType": "full_numbers"
                            });
                        </script>
                    </div>`;


    tableContainer.innerHTML = table;
    ban=0;
  }else{
    graph.style.display='block';
    btn.style.display='block';
    tb.style.display='none';
  }

}

function estu_anio(){

  var $estuanio = $("#estu-anio");
  $.ajax({
    url: $estuanio.data("url"),
    success: function(data){
      var ctx = $estuanio[0].getContext("2d");
      var cantidad = {
        label: 'Cantidad',
            backgroundColor: 'red',
            data:data.data,
            borderColor: 'red',
            lineTension: 0,
            fill: false,
      };
      var porcentaje = {

        data:data.porcen,
      };

      window.estuanio = new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [cantidad]
        },
        options: {
          scales: {
            yAxes: [{
              scaleLabel: {
                labelString: "Cantidad",
                display: true
              }
            }]
          },

          // tooltips: {
          //     callbacks: {
          //       title: function(tooltipItem, data) {
          //         return 'Porcentaje';
          //       },
          //       label: function(tooltipItem, data) {
          //         return data['datasets'][1]['data'][tooltipItem['index']] + '%';
          //       }
          //     },
          //
          //
          //
          // },
          responsive: true,
          legend: {
            display: false,
            position: 'top',
          },
          title: {
            display: false,
            text: 'Numero de estudiantes que presentaron la Prueba por año'
          },
          pan: {
              enabled: true,
              mode: "xy",
              speed: 10,
              threshold: 10
          },
          zoom: {
            enabled: true,
            drag: false,
            mode: "xy",
            speed: 0.01,
            // sensitivity: 0.1,
            limits: {
              max: 10,
              min: 0.5
            }
          }
        }
      });
    }
  });
}
function opestu_anio(){
  var graph=document.getElementById("estu-anio");
  var btn=document.getElementById("btn_resetZoom");
  var tb=document.getElementById("containerestu_anio");
  var select = document.getElementById("opestu_anio");
  if (select.value == "tabla"){
    graph.style.display='none';
    btn.style.display='none';
    tb.style.display='block';
    const tableContainer = document.getElementById('containerestu_anio');
    const xAxis = estuanio.data.labels;
    const yAxis = estuanio.data.datasets;

    const tableHeader = `<tr>${
        xAxis.reduce((memo, entry) => {
            memo += `<th>${entry}</th>`;
            return memo;
        }, '<th>AÑOS:</th>')
    }</tr>`;

    const tableBody = yAxis.reduce((memo, entry) => {
        const rows = entry.data.reduce((memo, entry) => {
            memo += `<td>${entry}</td>`
            return memo;
        }, '');

        memo += `<tr><td>${entry.label}</td>${rows}</tr>`;

        return memo;
    }, '');

    const table = ` 
                    <div id="tabla" class="container-fluid">
                        <div class="card shadow mb-4">
                                <div class="card-body">
                                    <div class="table-responsive">
                                        <table class="table table-striped table-bordered" id="dataTable" width="100%" cellspacing="0">
                                            <thead>
                                                ${tableHeader}
                                            </thead>
                                            <tbody>
                                                ${tableBody}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        <script>
                            $('#dataTable').DataTable({
                                "pagingType": "full_numbers"
                            });
                        </script>
                    </div>`;


    tableContainer.innerHTML = table;
    ban=0;
  }else{
    graph.style.display='block';
    btn.style.display='block';
    tb.style.display='none';
  }

}

function estu_Edad() {
  var $estuEdad = $("#estu-edad");
  $.ajax({
    url: $estuEdad.data("url"),
    success: function(data) {
      var ctx = $estuEdad[0].getContext("2d");
      var cantidad = {
        label: 'Cantidad',
        backgroundColor: [
                "#FF6384",
                "#63FF84",
                "#84FF63",
                "#8463FF",
                "#6384FF"
            ],
        data:data.data
      }

      window.estu_edad = new Chart(ctx, {
        type: 'pie',
        data: {
          labels:data.labels,
          datasets: [cantidad]
        },
        options: {
          tooltips: {
            callbacks: {
              title: function (tooltipItem, data) {
                return data['labels'][tooltipItem[0]['index']];
              },

              label: function (tooltipItem, data) {
                var dataset = data['datasets'][0];
                total = dataset['data'][0]+dataset['data'][1]+dataset['data'][2]+dataset['data'][3]+dataset['data'][4];
                var percent = Math.round((dataset['data'][tooltipItem['index']] / total * 100))
                //var percent = 'hola'//Math.round((dataset['data'][tooltipItem['index']] / dataset["_meta"][0]['total']) * 100)
                return '(' + percent + '%)';
              }
            },
          },
          title: {
            display: false,
            text: 'Porcentaje de estudiantes por rangos de edades'
          },
          pan: {
              enabled: true,
              mode: "xy",
              speed: 10,
              threshold: 10
          },
          zoom: {
            enabled: true,
            drag: false,
            mode: "xy",
            speed: 0.01,
            // sensitivity: 0.1,
            limits: {
              max: 10,
              min: 0.5
            }
          }
        }
      });
    }
  });
}
function opestu_edad(){
  var graph=document.getElementById("estu-edad");
  var btn=document.getElementById("btn_resetZoom");
  var tb=document.getElementById("containerestu_edad");
  var select = document.getElementById("opestu_edad");
  if (select.value == "tabla"){
    graph.style.display='none';
    btn.style.display='none';
    tb.style.display='block';
    const tableContainer = document.getElementById('containerestu_edad');
    const xAxis = estu_edad.data.labels;
    const yAxis = estu_edad.data.datasets;

    const tableHeader = `<tr>${
        xAxis.reduce((memo, entry) => {
            memo += `<th>${entry}</th>`;
            return memo;
        }, '<th>EDAD:</th>')
    }</tr>`;

    const tableBody = yAxis.reduce((memo, entry) => {
        const rows = entry.data.reduce((memo, entry) => {
            memo += `<td>${entry}</td>`
            return memo;
        }, '');

        memo += `<tr><td>${entry.label}</td>${rows}</tr>`;

        return memo;
    }, '');

    const table = ` 
                    <div id="tabla" class="container-fluid">
                        <div class="card shadow mb-4">
                                <div class="card-body">
                                    <div class="table-responsive">
                                        <table class="table table-striped table-bordered" id="dataTable" width="100%" cellspacing="0">
                                            <thead>
                                                ${tableHeader}
                                            </thead>
                                            <tbody>
                                                ${tableBody}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        <script>
                            $('#dataTable').DataTable({
                                "pagingType": "full_numbers"
                            });
                        </script>
                    </div>`;


    tableContainer.innerHTML = table;
    ban=0;
  }else{
    graph.style.display='block';
    btn.style.display='block';
    tb.style.display='none';
  }

}

function desemp_ciu_edad() {
  var $desemCiuEdad = $("#desemp-ciu-edad");
    $.ajax({
        url: $desemCiuEdad.data("url"),
      success: function (data) {

        var ctx = $desemCiuEdad[0].getContext("2d");

        var puntaje = {
          label: 'Puntaje',
              backgroundColor: 'blue',
              data:data.data
        };

        var estudiantes = {
          label: 'Estudiantes',
          backgroundColor: 'red',
          data:data.conta
        };

        var genero = {
          label: 'Genero',
          backgroundColor: 'dark'
        };

        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [puntaje,estudiantes]
          },
          options: {
            responsive: true,
            legend: {
              position: 'top',
            },
            title: {
              display: false,
              text: 'Puntaje global y numero de estudiantes por municipio'
            }
          }
        });
      }
    });
}

function desemp_ciu_edad() {
  var $desemCiuEdad = $("#desemp-ciu-edad");
    $.ajax({
        url: $desemCiuEdad.data("url"),
      success: function (data) {

        var ctx = $desemCiuEdad[0].getContext("2d");

        var avanzado = {
          label: 'Avanzado',
          backgroundColor: 'green',
          data:data.avanzado
        };

        var satisfactorio = {
          label: 'Satisfactorio',
          backgroundColor: 'blue',
          data:data.satisfactorio
        };

        var minimo = {
          label: 'Minimo',
          backgroundColor: 'yellow',
          data:data.minimo
        };

        var insuficiente = {
          label: 'Insuficiente',
          backgroundColor: 'red',
          data:data.insuficiente
        };

        window.ciu_edad = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [avanzado,satisfactorio,minimo,insuficiente]
          },
          options: {
            responsive: true,
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Número   de   estudiantes que presentaron la prueba de sociales y ciudadanas, por rango de edad y desempeño'
            },
              pan: {
                  enabled: true,
                  mode: "xy",
                  speed: 10,
                  threshold: 10
              },
              zoom: {
                enabled: true,
                drag: false,
                mode: "xy",
                speed: 0.01,
                // sensitivity: 0.1,
                limits: {
                  max: 10,
                  min: 0.5
                }
              }
          }
        });
      }
    });
}
function opciu_edad(){
  var graph=document.getElementById("desemp-ciu-edad");
  var btn=document.getElementById("btn_resetZoom");
  var tb=document.getElementById("containerciu_edad");
  var select = document.getElementById("opciu_edad");
  if (select.value == "tabla"){
    graph.style.display='none';
    btn.style.display='none';
    tb.style.display='block';
    const tableContainer = document.getElementById('containerciu_edad');
    const xAxis = ciu_edad.data.labels;
    const yAxis = ciu_edad.data.datasets;

    const tableHeader = `<tr>${
        xAxis.reduce((memo, entry) => {
            memo += `<th>${entry}</th>`;
            return memo;
        }, '<th>EDAD:</th>')
    }</tr>`;

    const tableBody = yAxis.reduce((memo, entry) => {
        const rows = entry.data.reduce((memo, entry) => {
            memo += `<td>${entry}</td>`
            return memo;
        }, '');

        memo += `<tr><td>${entry.label}</td>${rows}</tr>`;

        return memo;
    }, '');

    const table = ` 
                    <div id="tabla" class="container-fluid">
                        <div class="card shadow mb-4">
                                <div class="card-body">
                                    <div class="table-responsive">
                                        <table class="table table-striped table-bordered" id="dataTable" width="100%" cellspacing="0">
                                            <thead>
                                                ${tableHeader}
                                            </thead>
                                            <tbody>
                                                ${tableBody}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        <script>
                            $('#dataTable').DataTable({
                                "pagingType": "full_numbers"
                            });
                        </script>
                    </div>`;


    tableContainer.innerHTML = table;
    ban=0;
  }else{
    graph.style.display='block';
    btn.style.display='block';
    tb.style.display='none';
  }

}

function global_mun_ano() {
  var $globalmunano = $("#global-mun-ano");
    $.ajax({
        url: $globalmunano.data("url"),
      success: function (data) {

        var ctx = $globalmunano[0].getContext("2d");

        var punt2012 = {
          label: '2012',
          backgroundColor: 'gray',
          data:data.punt2012,
          borderColor: 'gray',
          lineTension: 0,
          fill: false,
        }

        var punt2013 = {
          label: '2013',
          backgroundColor: 'black',
          data:data.punt2013,
          borderColor: 'black',
          lineTension: 0,
          fill: false,
        }

        var punt2014 = {
          label: '2014',
          backgroundColor: 'orange',
          data:data.punt2014,
          borderColor: 'orange',
          lineTension: 0,
          fill: false,
        }

        var punt2015 = {
          label: '2015',
          backgroundColor: 'purple',
          data:data.punt2015,
          borderColor: 'purple',
          lineTension: 0,
          fill: false,
        }

        var punt2016 = {
          label: '2016',
          backgroundColor: 'green',
          data:data.punt2016,
          borderColor: 'green',
          lineTension: 0,
          fill: false,
        }

        var punt2017 = {
          label: '2017',
          backgroundColor: 'violet',
          data:data.punt2017,
          borderColor: 'violet',
          lineTension: 0,
          fill: false,
        }

        var punt2018 = {
          label: '2018',
          backgroundColor: 'brown',
          data:data.punt2018,
          borderColor: 'brown',
          lineTension: 0,
          fill: false,
        }

        var punt2019 = {
          label: '2019',
          backgroundColor: 'red',
          data:data.punt2019,
          borderColor: 'red',
          lineTension: 0,
          fill: false,
        };

        var punt2020 = {
          label: '2020',
          backgroundColor: 'yellow',
          data:data.punt2020,
          borderColor: 'yellow',
          lineTension: 0,
          fill: false,
        };

        var punt2021 = {
          label: '2021',
          backgroundColor: 'blue',
          data:data.punt2021,
          borderColor: 'blue',
          lineTension: 0,
          fill: false,
        }

        var punt2022 = {
          label: '2022',
          backgroundColor: 'gray',
          data:data.punt2022,
          borderColor: 'gray',
          lineTension: 0,
          fill: false,
        }

        var punt2023 = {
          label: '2023',
          backgroundColor: 'violet',
          data:data.punt2023,
          borderColor: 'violet',
          lineTension: 0,
          fill: false,
        }

        let dato;
        if (data.punt2017[0] != null || data.punt2018[0] != null || data.punt2019[0] != null || data.punt2020[0] != null || data.punt2021[0] != null || data.punt2022[0] != null || data.punt2023[0] != null){
            dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017]
            }
          if (data.punt2018[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018]
            }
          }
          if (data.punt2019[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018,punt2019]
            }
          }
          if (data.punt2020[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018,punt2019,punt2020]
            }
          }
          if (data.punt2021[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018,punt2019,punt2020,punt2021]
            }
          }
          if (data.punt2022[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018,punt2019,punt2020,punt2021,punt2022]
            }
          }
          if (data.punt2023[0] != null){
              dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016,punt2017,punt2018,punt2019,punt2020,punt2021,punt2022,punt2023]
            }
          }
        }
        else
          dato = {
              labels: data.labels,
              datasets: [punt2012,punt2013,punt2014,punt2015,punt2016]
          }

        window.mun_ano = new Chart(ctx, {
          type: 'line',
          data: dato,
          options: {
            responsive: true,
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Puntaje Global por Municipio y Año'
            },
              pan: {
                  enabled: true,
                  mode: "xy",
                  speed: 10,
                  threshold: 10
              },
              zoom: {
                enabled: true,
                drag: false,
                mode: "xy",
                speed: 0.01,
                // sensitivity: 0.1,
                limits: {
                  max: 10,
                  min: 0.5
                }
              }
          }
        });
      }
    });
}
function opmun_ano(){
  var graph=document.getElementById("global-mun-ano");
  var btn=document.getElementById("btn_resetZoom");
  var tb=document.getElementById("containermun_ano");
  var select = document.getElementById("opmun_ano");
  if (select.value == "tabla"){
    graph.style.display='none';
    btn.style.display='none';
    tb.style.display='block';
    const tableContainer = document.getElementById('containermun_ano');
    const xAxis = mun_ano.data.labels;
    const yAxis = mun_ano.data.datasets;

    const tableHeader = `<tr>${
        xAxis.reduce((memo, entry) => {
            memo += `<th>${entry}</th>`;
            return memo;
        }, '<th>AÑO:</th>')
    }</tr>`;

    const tableBody = yAxis.reduce((memo, entry) => {
        const rows = entry.data.reduce((memo, entry) => {
            memo += `<td>${entry}</td>`
            return memo;
        }, '');

        memo += `<tr><td>${entry.label}</td>${rows}</tr>`;

        return memo;
    }, '');

    const table = ` 
                    <div id="tabla" class="container-fluid">
                        <div class="card shadow mb-6">
                                <div class="card-body">
                                    <div class="table-responsive">
                                        <table class="table table-striped table-bordered" id="dataTable" width="100%" cellspacing="0">
                                            <thead>
                                                ${tableHeader}
                                            </thead>
                                            <tbody>
                                                ${tableBody}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        <script>
                            $('#dataTable').DataTable({
                                "pagingType": "full_numbers"
                            });
                        </script>
                    </div>`;

    // removeAttr('style');
    tableContainer.innerHTML = table;
    ban=0;
  }else{
    graph.style.display='block';
    btn.style.display='block';
    tb.style.display='none';
  }

}

function gen_ano() {
  var $genano = $("#global-gen-ano");
    $.ajax({
        url: $genano.data("url"),
      success: function (data) {

        var ctx = $genano[0].getContext("2d");

        var masculino = {
          label: 'Masculino',
          backgroundColor: 'red',
          data:data.masculino,
          borderColor: 'red',
          lineTension: 0,
          fill: false,
        }

        var femenino = {
          label: 'Femenino',
          backgroundColor: 'blue',
          data:data.femenino,
          borderColor: 'blue',
          lineTension: 0,
          fill: false,
        }

        window.gen_ano = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.labels,
            datasets: [masculino,femenino]
          },
          options: {
            tooltips: {
                callbacks: {
                    title: function (tooltipItem, data) {
                        return data['labels'][tooltipItem[0]['index']];
                    },

                    label: function (tooltipItems, data) {
                        // var dataset = data.datasets[tooltipItem.datasetIndex];
                        // var dataset = data['datasets'][0];
                        // total = data['masculino'][tooltipItem[0]['index']] + data['femenino'][tooltipItem[0]['index']];
                        // var percent = Math.round((dataset['data'][tooltipItem['index']] / total * 100))
                        //var percent = 'hola'//Math.round((dataset['data'][tooltipItem['index']] / dataset["_meta"][0]['total']) * 100)
                        return tooltipItems.yLabel+ '%';
                    }
                },
            },
            responsive: true,
            legend: {
              position: 'top',
            },
            title: {
              display: true,
              text: 'Porcentaje de Estudiantes por Genero y Año'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        min: 0,
                        max: 100,
                        callback: function (value) {
                            return value + "%"
                        }
                    },
                    scaleLabel: {
                        display: true,
                        labelString: "Percentage"
                    }
                }]
            },

              pan: {
                  enabled: true,
                  mode: "xy",
                  speed: 10,
                  threshold: 10
              },
              zoom: {
                enabled: true,
                drag: false,
                mode: "xy",
                speed: 0.01,
                // sensitivity: 0.1,
                limits: {
                  max: 10,
                  min: 0.5
                }
              }
          }
        });
      }
    });
}
function opgen_ano(){
  var graph=document.getElementById("global-gen-ano");
  var btn=document.getElementById("btn_resetZoom");
  var tb=document.getElementById("containergen_ano");
  var select = document.getElementById("opgen_ano");
  if (select.value == "tabla"){
    graph.style.display='none';
    btn.style.display='none';
    tb.style.display='block';
    const tableContainer = document.getElementById('containergen_ano');
    const xAxis = gen_ano.data.labels;
    const yAxis = gen_ano.data.datasets;

    const tableHeader = `<tr>${
        xAxis.reduce((memo, entry) => {
            memo += `<th>${entry}</th>`;
            return memo;
        }, '<th>AÑO:</th>')
    }</tr>`;

    const tableBody = yAxis.reduce((memo, entry) => {
        const rows = entry.data.reduce((memo, entry) => {
            memo += `<td>${entry}</td>`
            return memo;
        }, '');

        memo += `<tr><td>${entry.label}</td>${rows}</tr>`;

        return memo;
    }, '');

    const table = ` 
                    <div id="tabla" class="container-fluid">
                        <div class="card shadow mb-6">
                                <div class="card-body">
                                    <div class="table-responsive">
                                        <table class="table table-striped table-bordered" id="dataTable" width="100%" cellspacing="0">
                                            <thead>
                                                ${tableHeader}
                                            </thead>
                                            <tbody>
                                                ${tableBody}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        <script>
                            $('#dataTable').DataTable({
                                "pagingType": "full_numbers"
                            });
                        </script>
                    </div>`;

    // removeAttr('style');
    tableContainer.innerHTML = table;
    ban=0;
  }else{
    graph.style.display='block';
    btn.style.display='block';
    tb.style.display='none';
  }

}

function cargarFunciones(){
   lectura_critic_ciudad();
   estu_anio();
   estu_Edad();
   desemp_ciu_edad();
   global_mun_ano();
   gen_ano();
}

function cargaFuncionesPrincipal(){
  graficPrincipal();
  punt_anio();
  tot_est();
}

///////////////////funciones para crear graficas//////////////////////////
function evdragstart(ev) {
    ev.dataTransfer.setData("text",ev.target.id);
}

function evdragover (ev) {
    ev.preventDefault();
}

function evdrop(ev,el) {
    ev.stopPropagation();
    ev.preventDefault();
    data=ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}

function resetzoom() {
  window.grafica.resetZoom();
}

