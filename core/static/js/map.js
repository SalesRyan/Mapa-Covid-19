let ctx = document.getElementById('map')
let value = ctx.getAttribute('dados')
let data = JSON.parse(value).data
var infowindow = window.infowindow
console.log(window.map)
let map = window.map




// Evento para fechar a infowindow caso o usuário clique num lugar do mapa sem ser a área de alguma UBS
google.maps.event.addListener(map, 'click', function () {
    infowindow.close();
});

data.forEach((element, index) => {
    cidades_poligono = criaPoligono(element.coordenadas,"#f14666")
    cidades_poligono.setMap(map);
    
    // Evento para exibir a infowindow com o nome da UBS e a quantidade cada um dos tipos de notificações
    cidades_poligono.addListener('click', function (event) {
        var contentString = '<div id="content">' + "<h6>" + String(element.nome) + "</h6>" + "Casos confirmados: " +
            String(element.confirmado) + "<br><br>" + "Obitos: " + String(element.obitos) + "<br><br>" +
            "Incidência: " + String(element.incidencia) + '</div>';
        infowindow.setContent(contentString);
        infowindow.setPosition(event.latLng);
        infowindow.open(map);
    });
});
