$(document).ready(function (){
                $("#formulario").submit(function (e){
                    e.preventDefault();
                    var $graficGest = $("#grafic-gest");
                    var graf = document.getElementById("graf").value;
                    var punt = document.getElementById("puntaje").options[document.getElementById("puntaje").selectedIndex].text;
                    var ano = document.getElementById("ano").options[document.getElementById("ano").selectedIndex].text;
                    var muni = document.getElementById("municipio").options[document.getElementById("municipio").selectedIndex].text;
                    var inst = document.getElementById("inst").options[document.getElementById("inst").selectedIndex].text;
                    $.ajax({
                        url: $(this).attr('action'),
                        type: $(this).attr('method'),
                        data: $(this).serialize(),


                        success: function (data){
                            var ctx = $graficGest[0].getContext("2d");
                            function getRandomColor() {
                                var letters = "0123456789ABCDEF".split("");
                                var color = "#";
                                for (var i = 0; i < 6; i++ ) {
                                  color += letters[Math.floor(Math.random() * 16)];
                                }
                                return color;
                            }

                            var puntaje = {
                              label: 'Puntaje Promedio',
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
                                  data:data.data,
                                  borderColor: 'red',
                                  lineTension: 0,
                                  fill: false,
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
                            if (window.grafica) {
                                window.grafica.clear();
                                window.grafica.destroy();
                            }
                            if(graf=="tabla"){
                                graf="bar";
                                ban=1;
                            }
                            window.grafica = new Chart(ctx, {
                              type: graf,
                              data: {
                                labels: data.labels,
                                datasets: [puntaje]
                              },
                              options: {
                                responsive: true,
                                legend: {
                                  position: 'top',
                                },
                                title: {
                                  display: true,
                                  text: 'PUNTAJE: '+punt +'      AÑO: '+ano+'        MUNICIPIO: '+muni+'     INSTITUCION: '+inst
                                },
                                scales: {
                                     yAxes: [{
                                          ticks: {
                                                    min: 0,

                                                    //callback: function(value) { return value + "%" }
                                                  },
                                          scaleLabel: {
                                              display: true,
                                              labelString: 'Puntaje'
                                          }
                                     }]
                                },
                                pan: {
                                  enabled: true,
                                  mode: "x",
                                  speed: 10,
                                  threshold: 10
                                },
                                zoom: {
                                    enabled: true,
                                    drag: false,
                                    mode: "x",
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
                                    }, '<th></th>')
                                }</tr>`;

                                const tableBody = yAxis.reduce((memo, entry) => {
                                    const rows = entry.data.reduce((memo, entry) => {
                                        memo += `<td>${entry}</td>`
                                        return memo;
                                    }, '');

                                    memo += `<tr><td>${entry.label}</td>${rows}</tr>`;

                                    return memo;
                                }, '');

                                const table = ` <div class="container-fluid">
                                                    <div class="card shadow mb-4">
                                                            <div class="card-body">
                                                                <div class="table-responsive">
                                                                    <table class="table table-striped table-bordered" id="dataTable" width="100%" cellspacing="1"><thead>${tableHeader}</thead><tbody>${tableBody}</tbody></table>
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
                    })

                })
            })