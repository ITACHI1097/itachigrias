$(document).ready(function (){
                $("#formulario").submit(function (e){
                    e.preventDefault();
                    var $graficGest = $("#grafic-gest");
                    var graf = document.getElementById("graf").value;
                    var ano = document.getElementById("ano").options[document.getElementById("ano").selectedIndex].text;
                    var muni = document.getElementById("municipio").options[document.getElementById("municipio").selectedIndex].text;
                    var inst = document.getElementById("inst").options[document.getElementById("inst").selectedIndex].text;
                    let cat = document.getElementById("categoria").options[document.getElementById("categoria").selectedIndex].text;
                    $.ajax({
                        url: $(this).attr('action'),
                        type: $(this).attr('method'),
                        data: $(this).serialize(),


                        success: function (data){
                            var ctx = $graficGest[0].getContext("2d");

                            var masculino = {
                                label: 'Número de Estudiantes Masculino',
                                backgroundColor: 'red',
                                data:data.Cmasculino,
                                borderColor: 'red',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var femenino = {
                                label: 'Número de Estudiantes Femenino',
                                backgroundColor: 'blue',
                                data:data.Cfemenino,
                                borderColor: 'blue',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var ticbuena = {
                                label: 'Número de Estudiantes Buena',
                                backgroundColor: 'green',
                                data:data.Cticbuena,
                                borderColor: 'green',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var ticregular = {
                                label: 'Número de Estudiantes REGULAR',
                                backgroundColor: 'yellow',
                                data:data.Cticregular,
                                borderColor: 'yellow',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var ticmala = {
                                label: 'Número de Estudiantes Mala',
                                backgroundColor: 'red',
                                data:data.Cticmala,
                                borderColor: 'red',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var vivbuena = {
                                label: 'Número de Estudiantes en Hacinamiento Medio',
                                backgroundColor: 'green',
                                data:data.CHmedio,
                                borderColor: 'green',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var vivregular = {
                                label: 'Número de Estudiantes en Hacinamiento Critico',
                                backgroundColor: 'red',
                                data:data.CHcritico,
                                borderColor: 'red',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var vivmala = {
                                label: 'Número de Estudiantes Sin Hacinamiento',
                                backgroundColor: 'black',
                                data:data.CHsin,
                                borderColor: 'black',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var e17 = {
                                label: 'Número de Estudiantes de 17 años',
                                backgroundColor: 'blue',
                                data:data.Ce17,
                                borderColor: 'blue',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var e18y19 = {
                                label: 'Número de Estudiantes de 18 Y 19 años',
                                backgroundColor: 'red',
                                data:data.Ce18y19,
                                borderColor: 'red',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var e20a28 = {
                                label: 'Número de Estudiantes entre 20 Y 28 años',
                                backgroundColor: 'green',
                                data:data.Ce20a28,
                                borderColor: 'green',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var emayoresde28 = {
                                label: 'Número de Estudiantes MAYORES DE 28 años',
                                backgroundColor: 'yellow',
                                data:data.Cemayoresde28,
                                borderColor: 'yellow',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var emenoresde17 = {
                                label: 'Número de Estudiantes MENORES DE 17 años',
                                backgroundColor: 'brown',
                                data:data.Cemenoresde17,
                                borderColor: 'brown',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var es1 = {
                                label: 'Número de Estudiantes en ESTRATO 1',
                                backgroundColor: 'red',
                                data:data.Ces1,
                                borderColor: 'red',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var es2 = {
                                label: 'Número de Estudiantes en ESTRATO 2',
                                backgroundColor: 'blue',
                                data:data.Ces2,
                                borderColor: 'blue',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var es3 = {
                                label: 'Número de Estudiantes en ESTRATO 3',
                                backgroundColor: 'yellow',
                                data:data.Ces3,
                                borderColor: 'yellow',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var es4 = {
                                label: 'Número de Estudiantes en ESTRATO 4',
                                backgroundColor: 'green',
                                data:data.Ces4,
                                borderColor: 'green',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var es5 = {
                                label: 'Número de Estudiantes en ESTRATO 5',
                                backgroundColor: 'brown',
                                data:data.Ces5,
                                borderColor: 'brown',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var es6 = {
                                label: 'Número de Estudiantes en ESTRATO 6',
                                backgroundColor: 'black',
                                data:data.Ces6,
                                borderColor: 'black',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var n = {
                                label: 'Número de NINGUNO',
                                backgroundColor: 'red',
                                data:data.Cn,
                                borderColor: 'red',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }
                            var PI = {
                                label: 'Número de PRIMARIA INCOMPLETA',
                                backgroundColor: 'blue',
                                data:data.CPI,
                                borderColor: 'blue',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var PC = {
                                label: 'Número de PRIMARIA COMPLETA',
                                backgroundColor: 'green',
                                data:data.CPC,
                                borderColor: 'green',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var BI = {
                                label: 'Número de SECUNDARIA BACHILLERATO IMCOMPLETO',
                                backgroundColor: 'yellow',
                                data:data.CBI,
                                borderColor: 'yellow',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var BC = {
                                label: 'Número de SECUNDARIA BACHILLERATO COMPLETO',
                                backgroundColor: 'brown',
                                data:data.CBC,
                                borderColor: 'brown',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var ETI = {
                                label: 'Número de EDUCACION TECNICA O TECNOLOGICA INCOMPLETA',
                                backgroundColor: 'pink',
                                data:data.CETI,
                                borderColor: 'pink',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var ETC = {
                                label: 'Número de EDUCACION TECNICA O TECNOLOGICA COMPLETA',
                                backgroundColor: 'purple',
                                data:data.CETC,
                                borderColor: 'purple',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var EPI = {
                                label: 'Número de EDUCACION PROFECIONAL INCOMPLETA',
                                backgroundColor: 'orange',
                                data:data.CEPI,
                                borderColor: 'orange',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var EPC = {
                                label: 'Número de EDUCACION PROFECIONAL COMPLETA',
                                backgroundColor: 'violet',
                                data:data.CEPC,
                                borderColor: 'violet',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var postgrado = {
                                label: 'Número de POSTGRADO',
                                backgroundColor: 'gray',
                                data:data.Cpostgrado,
                                borderColor: 'gray',
                                lineTension: 0,
                                fill: false,
                                yAxisID: 'A'
                            }

                            var nosabe = {
                                label: 'Número de NO SABE',
                                backgroundColor: 'black',
                                data:data.Cnosabe,
                                borderColor: 'black',
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
                                datasets: [masculino]
                            }
                            if(cat =='Genero'){
                                dato = {
                                  labels: data.labels,

                                  datasets: [masculino,femenino]
                                }
                            }else{
                                if(cat == 'Condicion de las TIC')
                                    dato = {
                                        labels: data.labels,
                                        datasets: [ticbuena,ticregular,ticmala]
                                    }
                                else{
                                    if(cat == 'Condicion en la que vive')
                                        dato = {
                                            labels: data.labels,
                                            datasets: [vivbuena,vivregular,vivmala]
                                        }
                                    else{
                                        if(cat == 'Rango de Edad')
                                            dato = {
                                                labels: data.labels,
                                                datasets: [e17,e18y19,e20a28,emayoresde28,emenoresde17]
                                            }
                                        else{
                                            if(cat == 'Estrato')
                                                dato = {
                                                    labels: data.labels,
                                                    datasets: [es1,es2,es3,es4,es5,es6]
                                                }
                                            else{
                                                if(cat == 'Nivel Educativo Padres')
                                                    dato = {
                                                        labels: data.labels,
                                                        datasets: [n,PI,PC,BI,BC,ETI,ETC,EPI,EPC,postgrado,nosabe]
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
                            window.grafica = new Chart(ctx,{
                              type: graf,
                              data: dato,
                              options: {
                                responsive: true,
                                legend: {
                                  position: 'top',
                                },
                                title: {
                                  display: true,
                                  text: 'Categoria: '+cat+'      AÑO: '+ano+'        MUNICIPIO: '+muni+'     INSTITUCION: '+inst
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
                                              labelString: 'Número de Estudiantes'
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
                            var tbd=document.getElementById("btn_download");
                            if(ban==1){

                                graph.style.display='none';
                                btn.style.display='block';
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

