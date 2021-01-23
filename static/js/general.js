$(document).ready(function (){
                $("#formulario").submit(function (e){
                    e.preventDefault();
                    var $graficGest = $("#grafic-gest");

                    var graf = document.getElementById("graf").value;
                    var punt = document.getElementById("puntaje").options[document.getElementById("puntaje").selectedIndex].text;
                    var ano = document.getElementById("ano").options[document.getElementById("ano").selectedIndex].text;
                    var muni = document.getElementById("municipio").options[document.getElementById("municipio").selectedIndex].text;
                    var inst = document.getElementById("inst").options[document.getElementById("inst").selectedIndex].text;
                    let cat = document.getElementById("categoria").options[document.getElementById("categoria").selectedIndex].text;
                    let metrica = document.getElementById("metrica").options[document.getElementById("metrica").selectedIndex].text;
                    let ban=0;
                    $.ajax({
                        url: $(this).attr('action'),
                        type: $(this).attr('method'),
                        data: $(this).serialize(),


                        success: function (data) {
                            var ctx = $graficGest[0].getContext("2d");
                            function getRandomColor() {
                                var letters = "0123456789ABCDEF".split("");
                                var color = "#";
                                for (var i = 0; i < 6; i++ ) {
                                  color += letters[Math.floor(Math.random() * 16)];
                                }
                                return color;
                            }

                              var contador = {
                                label: 'Cantidad',
                                  backgroundColor: [
                                    'blue',
                                    'red',
                                    'green',
                                    'yellow',
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
                                    getRandomColor(),
                                    getRandomColor(),
                                    getRandomColor(),
                                    getRandomColor(),
                                    getRandomColor(),
                                    getRandomColor(),
                                    getRandomColor(),
                                  ],
                                  data:data.contador,
                                yAxisID: 'A'
                              }
                              var promedio = {
                                label: 'Puntaje',
                                  backgroundColor: [
                                    'blue',
                                    'red',
                                    'green',
                                    'yellow',
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
                                    getRandomColor(),
                                    getRandomColor(),
                                    getRandomColor(),
                                    getRandomColor(),
                                    getRandomColor(),
                                    getRandomColor(),
                                    getRandomColor(),
                                  ],
                                  data:data.promedio,
                                yAxisID: 'A'
                            }

                              var masculino = {
                                  label: (metrica == "Puntaje") ? 'Puntaje Promedio Masculino' : 'Número de Estudiantes Masculino',
                                  backgroundColor: 'red',
                                  data: (metrica == "Puntaje") ? data.masculino : data.Cmasculino,
                                  borderColor: graf=="line"||graf=="radar"?'red':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                                  // data:data.masculino
                              }

                              var femenino = {
                                  label: (metrica == "Puntaje") ? 'Puntaje Promedio Femenino' : 'Número de Estudiantes Femenino',
                                  backgroundColor: 'blue',
                                  data: (metrica == "Puntaje") ? data.femenino : data.Cfemenino,
                                  borderColor: graf=="line"||graf=="radar"?'blue':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var ticbuena = {
                                  label: (metrica == "Puntaje") ? 'Puntaje Promedio Buena' : 'Número de Estudiantes Buena',
                                  backgroundColor: 'green',
                                  data: (metrica == "Puntaje") ? data.ticbuena : data.Cticbuena,
                                  borderColor: graf=="line"||graf=="radar"?'green':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var ticregular = {
                                  label: (metrica == "Puntaje") ? 'Puntaje Promedio REGULAR' : 'Número de Estudiantes REGULAR',
                                  backgroundColor: 'yellow',
                                  data: (metrica == "Puntaje") ? data.ticregular : data.Cticregular,
                                  borderColor: graf=="line"||graf=="radar"?'yellow':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var ticmala = {
                                  label: (metrica == "Puntaje") ? 'Puntaje Promedio Mala' : 'Número de Estudiantes Mala',
                                  backgroundColor: 'red',
                                  data: (metrica == "Puntaje") ? data.ticmala : data.Cticmala,
                                  borderColor: graf=="line"||graf=="radar"?'red':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var vivbuena = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio Hacinamiento Medio' : 'Número de Estudiantes en Hacinamiento Medio',
                                  backgroundColor: 'green',
                                  data: (metrica == "Puntaje") ? data.Hmedio : data.CHmedio,
                                  borderColor: graf=="line"||graf=="radar"?'green':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var vivregular = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio Hacinamiento Critico' : 'Número de Estudiantes en Hacinamiento Critico',
                                  backgroundColor: 'red',
                                  data: (metrica == "Puntaje") ? data.Hcritico : data.CHcritico,
                                  borderColor: graf=="line"||graf=="radar"?'red':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var vivmala = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio Sin Hacinamiento' : 'Número de Estudiantes Sin Hacinamiento',
                                  backgroundColor: 'black',
                                  data: (metrica == "Puntaje") ? data.Hsin : data.CHsin,
                                  borderColor: graf=="line"||graf=="radar"?'black':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var e17 = {
                                  label: (metrica == "Puntaje") ? 'Puntaje Promedio de 17' : 'Número de Estudiantes de 17 años',
                                  backgroundColor: 'blue',
                                  data: (metrica == "Puntaje") ? data.e17 : data.Ce17,
                                  borderColor: graf=="line"||graf=="radar"?'blue':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var e18y19 = {
                                  label: (metrica == "Puntaje") ? 'Puntaje Promedio de 18 Y 19' : 'Número de Estudiantes de 18 Y 19 años',
                                  backgroundColor: 'red',
                                  data: (metrica == "Puntaje") ? data.e18y19 : data.Ce18y19,
                                  borderColor: graf=="line"||graf=="radar"?'red':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var e20a28 = {
                                  label: (metrica == "Puntaje") ? 'Puntaje Promedio de 20 A 28' : 'Número de Estudiantes entre 20 Y 28 años',
                                  backgroundColor: 'green',
                                  data: (metrica == "Puntaje") ? data.e20a28 : data.Ce20a28,
                                  borderColor: graf=="line"||graf=="radar"?'green':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var emayoresde28 = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio MAYORES DE 28' : 'Número de Estudiantes MAYORES DE 28 años',
                                  backgroundColor: 'yellow',
                                  data: (metrica == "Puntaje") ? data.emayoresde28 : data.Cemayoresde28,
                                  borderColor: graf=="line"||graf=="radar"?'yellow':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var emenoresde17 = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio MENORES DE 17' : 'Número de Estudiantes MENORES DE 17 años',
                                  backgroundColor: 'brown',
                                  data: (metrica == "Puntaje") ? data.emenoresde17 : data.Cemenoresde17,
                                  borderColor: graf=="line"||graf=="radar"?'brown':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var es1 = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio ESTRATO 1' : 'Número de Estudiantes en ESTRATO 1',
                                  backgroundColor: 'red',
                                  data: (metrica == "Puntaje") ? data.es1 : data.Ces1,
                                  borderColor: graf=="line"||graf=="radar"?'red':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var es2 = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio ESTRATO 2' : 'Número de Estudiantes en ESTRATO 2',
                                  backgroundColor: 'blue',
                                  data: (metrica == "Puntaje") ? data.es2 : data.Ces2,
                                  borderColor: graf=="line"||graf=="radar"?'blue':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var es3 = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio ESTRATO 3' : 'Número de Estudiantes en ESTRATO 3',
                                  backgroundColor: 'yellow',
                                  data: (metrica == "Puntaje") ? data.es3 : data.Ces3,
                                  borderColor: graf=="line"||graf=="radar"?'yellow':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var es4 = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio ESTRATO 4' : 'Número de Estudiantes en ESTRATO 4',
                                  backgroundColor: 'green',
                                  data: (metrica == "Puntaje") ? data.es4 : data.Ces4,
                                  borderColor: graf=="line"||graf=="radar"?'green':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var es5 = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio ESTRATO 5' : 'Número de Estudiantes en ESTRATO 5',
                                  backgroundColor: 'brown',
                                  data: (metrica == "Puntaje") ? data.es5 : data.Ces5,
                                  borderColor: graf=="line"||graf=="radar"?'brown':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var es6 = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio ESTRATO 6' : 'Número de Estudiantes en ESTRATO 6',
                                  backgroundColor: 'black',
                                  data: (metrica == "Puntaje") ? data.es6 : data.Ces6,
                                  borderColor: graf=="line"||graf=="radar"?'black':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var n = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio NINGUNO' : 'Número de NINGUNO',
                                  backgroundColor: 'red',
                                  data: (metrica == "Puntaje") ? data.n : data.Cn,
                                  borderColor: graf=="line"||graf=="radar"?'red':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }
                              var PI = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio PRIMARIA INCOMPLETA' : 'Número de PRIMARIA INCOMPLETA',
                                  backgroundColor: 'blue',
                                  data: (metrica == "Puntaje") ? data.PI : data.CPI,
                                  borderColor: graf=="line"||graf=="radar"?'blue':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var PC = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio PRIMARIA COMPLETA' : 'Número de PRIMARIA COMPLETA',
                                  backgroundColor: 'green',
                                  data: (metrica == "Puntaje") ? data.PC : data.CPC,
                                  borderColor: graf=="line"||graf=="radar"?'green':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var BI = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio SECUNDARIA BACHILLERATO IMCOMPLETO' : 'Número de SECUNDARIA BACHILLERATO IMCOMPLETO',
                                  backgroundColor: 'yellow',
                                  data: (metrica == "Puntaje") ? data.BI : data.CBI,
                                  borderColor: graf=="line"||graf=="radar"?'yellow':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var BC = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio SECUNDARIA BACHILLERATO COMPLETO' : 'Número de SECUNDARIA BACHILLERATO COMPLETO',
                                  backgroundColor: 'brown',
                                  data: (metrica == "Puntaje") ? data.BC : data.CBC,
                                  borderColor: graf=="line"||graf=="radar"?'brown':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var ETI = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio EDUCACION TECNICA O TECNOLOGICA INCOMPLETA' : 'Número de EDUCACION TECNICA O TECNOLOGICA INCOMPLETA',
                                  backgroundColor: 'pink',
                                  data: (metrica == "Puntaje") ? data.ETI : data.CETI,
                                  borderColor: graf=="line"||graf=="radar"?'pink':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var ETC = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio EDUCACION TECNICA O TECNOLOGICA COMPLETA' : 'Número de EDUCACION TECNICA O TECNOLOGICA COMPLETA',
                                  backgroundColor: 'purple',
                                  data: (metrica == "Puntaje") ? data.ETC : data.CETC,
                                  borderColor: graf=="line"||graf=="radar"?'purple':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var EPI = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio EDUCACION PROFECIONAL INCOMPLETA' : 'Número de EDUCACION PROFECIONAL INCOMPLETA',
                                  backgroundColor: 'orange',
                                  data: (metrica == "Puntaje") ? data.EPI : data.CEPI,
                                  borderColor: graf=="line"||graf=="radar"?'orange':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var EPC = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio EDUCACION PROFECIONAL COMPLETA' : 'Número de EDUCACION PROFECIONAL COMPLETA',
                                  backgroundColor: 'violet',
                                  data: (metrica == "Puntaje") ? data.EPC : data.CEPC,
                                  borderColor: graf=="line"||graf=="radar"?'violet':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var postgrado = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio POSTGRADO' : 'Número de POSTGRADO',
                                  backgroundColor: 'gray',
                                  data: (metrica == "Puntaje") ? data.postgrado : data.Cpostgrado,
                                  borderColor: graf=="line"||graf=="radar"?'gray':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }

                              var nosabe = {
                                  label: (metrica == "Puntaje") ? 'Punt.Promedio NO SABE' : 'Número de NO SABE',
                                  backgroundColor: 'black',
                                  data: (metrica == "Puntaje") ? data.nosabe : data.Cnosabe,
                                  borderColor: graf=="line"||graf=="radar"?'black':'white',
                                  lineTension: 0,
                                  fill: false,
                                  yAxisID: 'A'
                              }


                              if (window.grafica) {
                                  window.grafica.clear();
                                  window.grafica.destroy();
                              }
                              let dato = {
                                  labels: data.labels,
                                  datasets: [puntaje]
                              }
                              if (cat == 'Genero') {
                                  dato = {
                                      labels: data.labels,

                                      datasets: [masculino, femenino]
                                  }
                              } else {
                                  if (cat == 'Condicion de las TIC')
                                      dato = {
                                          labels: data.labels,
                                          datasets: [ticbuena, ticregular, ticmala]
                                      }
                                  else {
                                      if (cat == 'Condicion en la que vive')
                                          dato = {
                                              labels: data.labels,
                                              datasets: [vivbuena, vivregular, vivmala]
                                          }
                                      else {
                                          if (cat == 'Rango de Edad')
                                              dato = {
                                                  labels: data.labels,
                                                  datasets: [e17, e18y19, e20a28, emayoresde28, emenoresde17]
                                              }
                                          else {
                                              if (cat == 'Estrato')
                                                  dato = {
                                                      labels: data.labels,
                                                      datasets: [es1, es2, es3, es4, es5, es6]
                                                  }
                                              else {
                                                  if (cat == 'Nivel Educativo Padres')
                                                      dato = {
                                                          labels: data.labels,
                                                          datasets: [n, PI, PC, BI, BC, ETI, ETC, EPI, EPC, postgrado, nosabe]
                                                      }
                                              }
                                          }
                                      }
                                  }
                              }


                              if (metrica != "Puntaje y Número de Estudiantes") {
                                  if(ano!="TODOS" && muni!="TODOS" && inst!="General"){
                                dato = {
                                    labels: data.labels,
                                    // datasets: [promedio]
                                    datasets: (metrica == "Puntaje") ? [promedio]:[contador]
                                }
                              }
                                    if(graf=="tabla"){
                                        graf="bar";
                                        ban=1;
                                    }
                                  window.grafica = new Chart(ctx, {
                                      type: graf,
                                      data: dato,
                                      options: {
                                          tooltips: {
                                            callbacks: {
                                                label: function(item, data) {
                                                    console.log(data.labels, item);
                                                    return graf=="pie"||graf=="polarArea"||graf=="doughnut"?data.datasets[item.datasetIndex].label+ ": "+ data.labels[item.index]+ ": "+ data.datasets[item.datasetIndex].data[item.index]:data.datasets[item.datasetIndex].label+ ": "+ data.datasets[item.datasetIndex].data[item.index];
                                                }
                                            },
                                          },
                                          responsive: true,
                                          legend: {
                                              position: 'top',
                                          },
                                          title: {
                                              display: true,
                                              text: 'METRICA: ' + metrica + '     PUNTAJE: ' + punt + '     Categoria: ' + cat + '      AÑO: ' + ano + '        MUNICIPIO: ' + muni + '     INSTITUCION: ' + inst
                                          },
                                          scales: {
                                              yAxes: [{
                                                  id: 'A',
                                                  position: 'left',
                                                  ticks: {
                                                    min: 0,

                                                    //callback: function(value) { return value + "%" }
                                                  },
                                                  scaleLabel: {
                                                      display: true,
                                                      labelString: (metrica == "Puntaje") ? 'Puntaje Promedio' : 'Número de Estudiantes'
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
                                              sensitivity: 0.1,
                                              limits: {
                                                  max: 10,
                                                  min: 0.5
                                              }
                                          }
                                      }
                                  });
                                    var graph=document.getElementById("grafic-gest");
                                    var btn=document.getElementById("btn_resetZoom");
                                    var tb=document.getElementById("container");
                                  if(ban==1){

                                    graph.style.display='none';
                                    btn.style.display='none';
                                    tb.style.display='block';
                                    const tableContainer = document.getElementById('container');
                                    const xAxis = grafica.data.labels;
                                    const yAxis = grafica.data.datasets;

                                    const tableHeader = `<tr>${
                                        xAxis.reduce((memo, entry) => {
                                            memo += `<th>${entry}</th>`;
                                            return memo;
                                        }, '<th>METRICAS:</th>')
                                    }</tr>`;

                                    const tableBody = yAxis.reduce((memo, entry) => {
                                        const rows = entry.data.reduce((memo, entry) => {
                                            memo += `<td>${entry}</td>`
                                            return memo;
                                        }, '');

                                        memo += `<tr><td>${entry.label}</td>${rows}</tr>`;

                                        return memo;
                                    }, '');
                                    console.log(data);
                                    const table = ` <div class="container-fluid">
                                                        <div class="card shadow mb-6">
                                                        <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                                          <h6 class="m-0 font-weight-bold text-dark">METRICA: ${metrica}&nbsp;&nbsp;&nbsp;PUNTAJE: ${punt}&nbsp;&nbsp;&nbsp;CATEGORIA: ${cat}&nbsp;&nbsp;&nbsp;AÑO: ${ano}&nbsp;&nbsp;&nbsp;<br> <br>MUNICIPIO: ${muni}&nbsp;&nbsp;&nbsp;INSTITUCION: ${inst}</h6>
                                                        </div>
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


                              } else {
                                  var Pmasculino = {
                                      label: 'Puntaje Promedio Masculino',
                                      backgroundColor: 'red',
                                      data: data.masculino,
                                      borderColor: graf=="line"||graf=="radar"?'red':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                      // data:data.masculino
                                  }

                                  var Pfemenino = {
                                      label: 'Puntaje Promedio Femenino',
                                      backgroundColor: 'blue',
                                      data: data.femenino,
                                      borderColor: graf=="line"||graf=="radar"?'blue':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pticbuena = {
                                      label: 'Puntaje Promedio Buena',
                                      backgroundColor: 'green',
                                      data: data.ticbuena,
                                      borderColor: graf=="line"||graf=="radar"?'green':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pticregular = {
                                      label: 'Puntaje Promedio REGULAR',
                                      backgroundColor: 'yellow',
                                      data: data.ticregular,
                                      borderColor: graf=="line"||graf=="radar"?'yellow':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pticmala = {
                                      label: 'Puntaje Promedio Mala',
                                      backgroundColor: 'red',
                                      data: data.ticmala,
                                      borderColor: graf=="line"||graf=="radar"?'red':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pvivbuena = {
                                      label: 'Punt.Promedio Hacinamiento Medio',
                                      backgroundColor: 'green',
                                      data: data.Hmedio,
                                      borderColor: graf=="line"||graf=="radar"?'green':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pvivregular = {
                                      label: 'Punt.Promedio Hacinamiento Critico',
                                      backgroundColor: 'red',
                                      data: data.Hcritico,
                                      borderColor: graf=="line"||graf=="radar"?'red':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pvivmala = {
                                      label: 'Punt.Promedio Sin Hacinamiento',
                                      backgroundColor: 'black',
                                      data: data.Hsin,
                                      borderColor: graf=="line"||graf=="radar"?'black':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pe17 = {
                                      label: 'Puntaje Promedio de 17',
                                      backgroundColor: 'blue',
                                      data: data.e17,
                                      borderColor: graf=="line"||graf=="radar"?'blue':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pe18y19 = {
                                      label: 'Puntaje Promedio de 18 Y 19',
                                      backgroundColor: 'red',
                                      data: data.e18y19,
                                      borderColor: graf=="line"||graf=="radar"?'red':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pe20a28 = {
                                      label: 'Puntaje Promedio de 20 A 28',
                                      backgroundColor: 'green',
                                      data: data.e20a28,
                                      borderColor: graf=="line"||graf=="radar"?'green':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pemayoresde28 = {
                                      label: 'Puntaje Promedio MAYORES DE 28',
                                      backgroundColor: 'yellow',
                                      data: data.emayoresde28,
                                      borderColor: graf=="line"||graf=="radar"?'yellow':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pemenoresde17 = {
                                      label: 'Puntaje Promedio de MENORES DE 17',
                                      backgroundColor: 'brown',
                                      data: data.emenoresde17,
                                      borderColor: graf=="line"||graf=="radar"?'brown':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pes1 = {
                                      label: 'Punt.Promedio ESTRATO 1',
                                      backgroundColor: 'red',
                                      data: data.es1,
                                      borderColor: graf=="line"||graf=="radar"?'red':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pes2 = {
                                      label: 'Punt.Promedio ESTRATO 2',
                                      backgroundColor: 'blue',
                                      data: data.es2,
                                      borderColor: graf=="line"||graf=="radar"?'blue':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pes3 = {
                                      label: 'Punt.Promedio ESTRATO 3',
                                      backgroundColor: 'yellow',
                                      data: data.es3,
                                      borderColor: graf=="line"||graf=="radar"?'yellow':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pes4 = {
                                      label: 'Punt.Promedio ESTRATO 4',
                                      backgroundColor: 'green',
                                      data: data.es4,
                                      borderColor: graf=="line"||graf=="radar"?'green':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pes5 = {
                                      label: 'Punt.Promedio ESTRATO 5',
                                      backgroundColor: 'brown',
                                      data: data.es5,
                                      borderColor: graf=="line"||graf=="radar"?'brown':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pes6 = {
                                      label: 'Punt.Promedio ESTRATO 6',
                                      backgroundColor: 'black',
                                      data: data.es6,
                                      borderColor: graf=="line"||graf=="radar"?'black':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pn = {
                                      label: 'Punt.Promedio NINGUNO',
                                      backgroundColor: 'red',
                                      data: data.n,
                                      borderColor: graf=="line"||graf=="radar"?'red':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }
                                  var PPI = {
                                      label: 'Punt.Promedio PRIMARIA INCOMPLETA',
                                      backgroundColor: 'blue',
                                      data: data.PI,
                                      borderColor: graf=="line"||graf=="radar"?'blue':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var PPC = {
                                      label: 'Punt.Promedio PRIMARIA COMPLETA',
                                      backgroundColor: 'green',
                                      data: data.PC,
                                      borderColor: graf=="line"||graf=="radar"?'green':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var PBI = {
                                      label: 'Punt.Promedio SECUNDARIA BACHILLERATO IMCOMPLETO',
                                      backgroundColor: 'yellow',
                                      data: data.BI,
                                      borderColor: graf=="line"||graf=="radar"?'yellow':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var PBC = {
                                      label: 'Punt.Promedio SECUNDARIA BACHILLERATO COMPLETO',
                                      backgroundColor: 'brown',
                                      data: data.BC,
                                      borderColor: graf=="line"||graf=="radar"?'brown':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var PETI = {
                                      label: 'Punt.Promedio EDUCACION TECNICA O TECNOLOGICA INCOMPLETA',
                                      backgroundColor: 'pink',
                                      data: data.ETI,
                                      borderColor: graf=="line"||graf=="radar"?'pink':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var PETC = {
                                      label: 'Punt.Promedio EDUCACION TECNICA O TECNOLOGICA COMPLETA',
                                      backgroundColor: 'purple',
                                      data: data.ETC,
                                      borderColor: graf=="line"||graf=="radar"?'purple':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var PEPI = {
                                      label: 'Punt.Promedio EDUCACION PROFECIONAL INCOMPLETA',
                                      backgroundColor: 'orange',
                                      data: data.EPI,
                                      borderColor: graf=="line"||graf=="radar"?'orange':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var PEPC = {
                                      label: 'Punt.Promedio EDUCACION PROFECIONAL COMPLETA',
                                      backgroundColor: 'violet',
                                      data: data.EPC,
                                      borderColor: graf=="line"||graf=="radar"?'violet':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Ppostgrado = {
                                      label: 'Punt.Promedio POSTGRADO',
                                      backgroundColor: 'gray',
                                      data: data.postgrado,
                                      borderColor: graf=="line"||graf=="radar"?'gray':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  var Pnosabe = {
                                      label: 'Punt.Promedio NO SABE',
                                      backgroundColor: 'black',
                                      data: data.nosabe,
                                      borderColor: graf=="line"||graf=="radar"?'gray':'white',
                                      lineTension: 0,
                                      fill: false,
                                      yAxisID: 'B'
                                  }

                                  let dato2 = {
                                      labels: data.labels,
                                      datasets: [puntaje]
                                  }
                                  if (cat == 'Genero') {
                                      dato2 = {
                                          labels: data.labels,
                                          datasets: [Pmasculino, Pfemenino, masculino, femenino]
                                      }
                                  } else {
                                      if (cat == 'Condicion de las TIC')
                                          dato2 = {
                                              labels: data.labels,
                                              datasets: [Pticbuena, Pticregular, Pticmala, ticbuena, ticregular, ticmala]
                                          }
                                      else {
                                          if (cat == 'Condicion en la que vive')
                                              dato2 = {
                                                  labels: data.labels,
                                                  datasets: [Pvivbuena, Pvivregular, Pvivmala, vivbuena, vivregular, vivmala]
                                              }
                                          else {
                                              if (cat == 'Rango de Edad')
                                                  dato2 = {
                                                      labels: data.labels,
                                                      datasets: [Pe17, Pe18y19, Pe20a28, Pemayoresde28, Pemenoresde17, e17, e18y19, e20a28, emayoresde28, emenoresde17]
                                                  }
                                              else {
                                                  if (cat == 'Estrato')
                                                      dato2 = {
                                                          labels: data.labels,
                                                          datasets: [Pes1, Pes2, Pes3, Pes4, Pes5, Pes6, es1, es2, es3, es4, es5, es6]
                                                      }
                                                  else {
                                                      if (cat == 'Nivel Educativo Padres')
                                                          dato2 = {
                                                              labels: data.labels,
                                                              datasets: [Pn, PPI, PPC, PBI, PBC, PETI, PETC, PEPI, PEPC, Ppostgrado, Pnosabe, n, PI, PC, BI, BC, ETI, ETC, EPI, EPC, postgrado, nosabe]
                                                          }
                                                  }
                                              }
                                          }
                                      }
                                  }
                                  if(graf=="tabla"){
                                        graf="bar";
                                        ban=1;
                                  }
                                  if(ano!="TODOS" && muni!="TODOS" && inst!="General"){
                                    dato2 = {
                                        labels: data.labels,
                                        datasets: [promedio,contador]
                                    }
                                  }
                                  window.grafica = new Chart(ctx, {

                                      type: graf,
                                      data: dato2,

                                      options: {
                                          tooltips: {
                                            callbacks: {
                                                label: function(item, data) {
                                                    console.log(data.labels, item);
                                                    return graf=="pie"||graf=="polarArea"||graf=="doughnut"?data.datasets[item.datasetIndex].label+ ": "+ data.labels[item.index]+ ": "+ data.datasets[item.datasetIndex].data[item.index]:data.datasets[item.datasetIndex].label+ ": "+ data.datasets[item.datasetIndex].data[item.index];
                                                }
                                            },
                                          },
                                          responsive: true,
                                          legend: {
                                              position: 'top',
                                          },
                                          title: {
                                              display: true,
                                              text: 'METRICA: ' + metrica + '     PUNTAJE: ' + punt + '     Categoria: ' + cat + '      AÑO: ' + ano + '        MUNICIPIO: ' + muni + '     INSTITUCION: ' + inst
                                          },
                                          scales: {
                                              yAxes: [{
                                                  id: 'A',

                                                  // type: 'linear',
                                                  position: 'left',
                                                  ticks: {
                                                    min: 0,

                                                    //callback: function(value) { return value + "%" }
                                                  },
                                                  scaleLabel: {
                                                      display: true,
                                                      labelString: 'Número de Estudiantes'
                                                  }
                                              }, {
                                                  id: 'B',
                                                  // type: 'linear',
                                                  position: 'right',
                                                  // ticks: {
                                                  //   max: 1,
                                                  //   min: 0
                                                  // }
                                                  scaleLabel: {
                                                      display: true,
                                                      labelString: 'Puntaje Promedio'
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
                                    var graph=document.getElementById("grafic-gest");
                                    var btn=document.getElementById("btn_resetZoom");
                                    var tb=document.getElementById("container");
                                    var tbd=document.getElementById("btn_download");
                                    if(ban==1){

                                        graph.style.display='none';
                                        btn.style.display='none';
                                        tb.style.display='block';
                                        tbd.style.display='none';
                                        const tableContainer = document.getElementById('container');
                                        const xAxis = grafica.data.labels;
                                        const yAxis = grafica.data.datasets;

                                        const tableHeader = `<tr>${
                                            xAxis.reduce((memo, entry) => {
                                                memo += `<th>${entry}</th>`;
                                                return memo;
                                            }, '<th>METRICAS:</th>')
                                        }</tr>`;

                                        const tableBody = yAxis.reduce((memo, entry) => {
                                            const rows = entry.data.reduce((memo, entry) => {
                                                memo += `<td>${entry}</td>`
                                                return memo;
                                            }, '');

                                            memo += `<tr><td>${entry.label}</td>${rows}</tr>`;

                                            return memo;
                                        }, '');

                                        const table = ` <div id="tabla" class="container-fluid">
                                                            <div class="card shadow mb-4">
                                                            <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                                              <h6 class="m-0 font-weight-bold text-dark">METRICA: ${metrica}&nbsp;&nbsp;&nbsp;PUNTAJE: ${punt}&nbsp;&nbsp;&nbsp;CATEGORIA: ${cat}&nbsp;&nbsp;&nbsp;AÑO: ${ano}&nbsp;&nbsp;&nbsp;<br> <br>MUNICIPIO: ${muni}&nbsp;&nbsp;&nbsp;INSTITUCION: ${inst}</h6>
                                                            </div>
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
                                        tbd.style.display='block';
                                    }

                              }
                        }
                    })

                })
            })