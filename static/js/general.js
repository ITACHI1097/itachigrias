$(document).ready(function (){
                $("#formulario").submit(function (e){
                    e.preventDefault();
                    var $graficGest = $("#grafic-gest");
                    var graf = document.getElementById("graf").value;
                    var punt = document.getElementById("puntaje").options[document.getElementById("puntaje").selectedIndex].text;
                    var ano = document.getElementById("ano").options[document.getElementById("ano").selectedIndex].text;
                    // var periodo = document.getElementById("periodo").options[document.getElementById("periodo").selectedIndex].text;
                    var muni = document.getElementById("municipio").options[document.getElementById("municipio").selectedIndex].text;
                    var inst = document.getElementById("inst").options[document.getElementById("inst").selectedIndex].text;
                    let cat = document.getElementById("categoria").options[document.getElementById("categoria").selectedIndex].text;
                    let metrica = document.getElementById("metrica").options[document.getElementById("metrica").selectedIndex].text;
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
                              label: 'Puntaje',
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
                                  ],
                                  data:data.data
                            };

                            var categoria1 = {
                              label: 'categoria',
                              backgroundColor: 'red',
                              data:data.categoria
                            };
                            // var dato1=(metrica=='Puntaje') ? data.masculino:data.Cmasculino;
                            // var dato2=(metrica=="Puntaje") ? data.femenino:data.Cfemenino;

                            var masculino = {
                                label: 'Masculino',
                                backgroundColor: 'red',
                                // data:dato1
                                data:(metrica=="Puntaje") ? data.masculino:data.Cmasculino,

                                // data:data.masculino
                            }

                            var femenino = {
                                label: 'Femenino',
                                backgroundColor: 'blue',
                                // data:dato2,
                                data:(metrica=="Puntaje")?data.femenino:data.Cfemenino,
                            }

                            var ticbuena = {
                                label: 'Buena',
                                backgroundColor: 'green',
                                data:(metrica=="Puntaje")?data.ticbuena:data.Cticbuena,
                            }

                            var ticregular = {
                                label: 'REGULAR',
                                backgroundColor: 'yellow',
                                data:(metrica=="Puntaje")?data.ticregular:data.Cticregular
                            }

                            var ticmala = {
                                label: 'Mala',
                                backgroundColor: 'red',
                                data:(metrica=="Puntaje")?data.ticmala:data.Cticmala
                            }

                            var vivbuena = {
                                label: 'Buena',
                                backgroundColor: 'green',
                                data:(metrica=="Puntaje")?data.vivbuena:data.Cvivbuena
                            }

                            var vivregular = {
                                label: 'REGULAR',
                                backgroundColor: 'yellow',
                                data:(metrica=="Puntaje")?data.vivregular:data.Cvivregular
                            }

                            var vivmala = {
                                label: 'Mala',
                                backgroundColor: 'red',
                                data:(metrica=="Puntaje")?data.vivmala:data.Cvivmala
                            }

                            var e17 = {
                                label: '17',
                                backgroundColor: 'blue',
                                data:(metrica=="Puntaje")?data.e17:data.Ce17
                            }

                            var e18y19 = {
                                label: '18 Y 19',
                                backgroundColor: 'red',
                                data:(metrica=="Puntaje")?data.e18y19:data.Ce18y19
                            }

                            var e20a28 = {
                                label: '20 A 28',
                                backgroundColor: 'green',
                                data:(metrica=="Puntaje")?data.e20a28:data.Ce20a28
                            }

                            var emayoresde28 = {
                                label: 'MAYORES DE 28',
                                backgroundColor: 'yellow',
                                data:(metrica=="Puntaje")?data.emayoresde28:data.Cemayoresde28
                            }

                            var emenoresde17 = {
                                label: 'MENORES DE 17',
                                backgroundColor: 'brown',
                                data:(metrica=="Puntaje")?data.emenoresde17:data.Cemenoresde17
                            }

                            var es1 = {
                                label: 'ESTRATO 1',
                                backgroundColor: 'red',
                                data:(metrica=="Puntaje")?data.es1:data.Ces1
                            }

                            var es2 = {
                                label: 'ESTRATO 2',
                                backgroundColor: 'blue',
                                data:(metrica=="Puntaje")?data.es2:data.Ces2
                            }

                            var es3 = {
                                label: 'ESTRATO 3',
                                backgroundColor: 'yellow',
                                data:(metrica=="Puntaje")?data.es3:data.Ces3
                            }

                            var es4 = {
                                label: 'ESTRATO 4',
                                backgroundColor: 'green',
                                data:(metrica=="Puntaje")?data.es4:data.Ces4
                            }

                            var es5 = {
                                label: 'ESTRATO 5',
                                backgroundColor: 'brown',
                                data:(metrica=="Puntaje")?data.es5:data.Ces5
                            }

                            var es6 = {
                                label: 'ESTRATO 6',
                                backgroundColor: 'black',
                                data:(metrica=="Puntaje")?data.es6:data.Ces6
                            }

                            var n = {
                                label: 'NINGUNO',
                                backgroundColor: 'red',
                                data:(metrica=="Puntaje")?data.n:data.Cn
                            }
                            var PI = {
                                label: 'PRIMARIA INCOMPLETA',
                                backgroundColor: 'blue',
                                data:(metrica=="Puntaje")?data.PI:data.CPI
                            }

                            var PC = {
                                label: 'PRIMARIA COMPLETA',
                                backgroundColor: 'green',
                                data:(metrica=="Puntaje")?data.PC:data.CPC
                            }

                            var BI = {
                                label: 'SECUNDARIA BACHILLERATO IMCOMPLETO',
                                backgroundColor: 'yellow',
                                data:(metrica=="Puntaje")?data.BI:data.CBI
                            }

                            var BC = {
                                label: 'SECUNDARIA BACHILLERATO COMPLETO',
                                backgroundColor: 'brown',
                                data:(metrica=="Puntaje")?data.BC:data.CBC
                            }

                            var ETI = {
                                label: 'EDUCACION TECNICA O TECNOLOGICA INCOMPLETA',
                                backgroundColor: 'pink',
                                data:(metrica=="Puntaje")?data.ETI:data.CETI
                            }

                            var ETC = {
                                label: 'EDUCACION TECNICA O TECNOLOGICA COMPLETA',
                                backgroundColor: 'purple',
                                data:(metrica=="Puntaje")?data.ETC:data.CETC
                            }

                            var EPI = {
                                label: 'EDUCACION PROFECIONAL INCOMPLETA',
                                backgroundColor: 'orange',
                                data:(metrica=="Puntaje")?data.EPI:data.CEPI
                            }

                            var EPC = {
                                label: 'EDUCACION PROFECIONAL COMPLETA',
                                backgroundColor: 'violet',
                                data:(metrica=="Puntaje")?data.EPC:data.CEPC
                            }

                            var postgrado = {
                                label: 'POSTGRADO',
                                backgroundColor: 'gray',
                                data:(metrica=="Puntaje")?data.postgrado:data.Cpostgrado
                            }

                            var nosabe = {
                                label: 'NO SABE',
                                backgroundColor: 'black',
                                data:(metrica=="Puntaje")?data.nosabe:data.Cnosabe
                            }

                            var genero = {
                              label: 'Genero',
                              backgroundColor: 'dark'
                            };
                            if (window.grafica) {
                                window.grafica.clear();
                                window.grafica.destroy();
                            }
                            let dato = {
                                labels: data.labels,
                                datasets: [puntaje]
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
                                    if(cat == 'Condicion de la vivienda')
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
                                  text: 'PUNTAJE: '+punt +'     Categoria: '+cat+'      AÑO: '+ano+'        MUNICIPIO: '+muni+'     INSTITUCION: '+inst
                                },
                                scales: {
                                     yAxes: [{
                                          scaleLabel: {
                                              display: true,
                                              labelString: (metrica=="Puntaje")?'Puntaje':'Cantidad'
                                          }
                                     }]
                                }
                              }
                            });
                        }
                    })

                })
            })