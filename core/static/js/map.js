var id = "map"
var infowindow
var map;
var listadepoligonos = []
var piaui = document.querySelector('#map-pi')
piaui = piaui.getAttribute('dados')
piaui = JSON.parse(piaui)
piaui = piaui.data

let dicionario = {
    0: '#e85d04',
    1: '#dc2f02',
    2: '#9d0208',
    3: '#6a040f',
    4: '#370617',
    5: '#370617',
}

let dicionario_som = {
    0: '#67ad45',
    1: '#f20089',
    2: '#ff0000',
    3: '#008bbf',
    4: '#fca311',
}

function initMap() {
    let styledMap = new google.maps.StyledMapType(style)

    map = new google.maps.Map(document.querySelector('div#map'), {
        center: { lat: -7.0364390, lng: -42.822612 },
        zoom: 6.1,
        streetViewControl: false,
        mapTypeControl: false
    });
    map.mapTypes.set('styled_map', styledMap)
    map.setMapTypeId('styled_map')
    infowindow = new google.maps.InfoWindow(); //Cria a janela de informação usada para a área da ubs

    var linha = new google.maps.Polyline({
        path: piaui,
        geodesic: true,
        strokeColor: "#000000",
        strokeOpacity: 1,
        strokeWeight: 1
    })
    linha.setMap(map)
    poligono(infowindow, map)
}

function criaPoligono(path, cor, fill = 0.35) {
    var cidades_poligonoreal = new google.maps.Polygon({
        paths: path,
        strokeColor: cor,
        strokeOpacity: 0.8,
        strokeWeight: 3,
        fillColor: cor,
        fillOpacity: fill
    });
    return cidades_poligonoreal
}

function alterMap(iddiv) {
    listadepoligonos.forEach(element => {
        element.setMap(null)
    })
    listadepoligonos = []

    let busca = document.querySelector("#dataTable_filter > label > input")
    busca.value = ''
    busca.dispatchEvent(new Event('keyup', { 'key': 'Enter' }))

    infowindow.close();

    id = iddiv
    poligono(infowindow, map)
}

function buttonVerMais(nome) {
    if (id == "map") {
        return '<a href="/cidades/detalhes/' + nome + '"/>' + '<button id="botaoteste" class="btn btn-sm btn-link">Ver Mais</button>'
    }
    if (id == "map-agrupamento") {
        return '<a href="/agrupamento/detalhes/' + nome + '"/>' + '<button id="botaoteste" class="btn btn-sm btn-link">Ver Mais</button>'
    }
    return '<a href="/regioes/detalhes/' + nome + '"/>' + '<button id="botaoteste" class="btn btn-sm btn-link">Ver Mais</button>'
}

function LimparCampo() {
    let busca = document.querySelector("#dataTable_filter > label > input");
    busca.value = '';
    busca.dispatchEvent(new Event('keyup', { 'key': 'Enter' }));
}

function escolheCor(cor) {
    listadepoligonos.filter((obj) => obj.fillColor == cor).forEach(function (obj) {
        obj.setMap(map)
    })
    listadepoligonos.filter((obj) => obj.fillColor != cor).forEach(function (obj) {
        obj.setMap(null)
    })
}

function prepareString(index, color){
    return `<button style="border: none; " onclick="escolheCor('${color}')">
        <div class="d-flex justify-content-around">
            <span class="icon" style="border-radius: 1em !important; border: rgba(0, 0, 0, 0.651) 1px solid; width: 15px; height: 15px; align-self: baseline; background: ${color};"></span>
            <h6 style="align-self: baseline;">&nbsp;Grupo ${index}</h6>
        </div>
    </button>`
}

function poligono(infowindow, mapa) {
    // Evento para fechar a infowindow caso o usuário clique num lugar do mapa sem ser a área de alguma UBS
    google.maps.event.addListener(mapa, 'click', function () {
        let busca = document.querySelector("#dataTable_filter > label > input")
        busca.value = ''
        busca.dispatchEvent(new Event('keyup', { 'key': 'Enter' }))
        infowindow.close();
    });
    let ctx = document.getElementById(id)
    if (id == "map-agrupamento") {
        mapa.controls[google.maps.ControlPosition.LEFT_BOTTOM].push(document.getElementById('legend'));
        ctx = document.getElementById("map")
        document.querySelector('#legend-map-regioes').style.display = 'none'
        document.querySelector('#legend-map-cidades').style.display = 'none'
        document.querySelector('#legend').style.display = 'block'
    } else if (id=="map"){
        ctx = document.getElementById(id)
        document.querySelector('#legend').style.display = 'none'
        document.querySelector('#legend-map-regioes').style.display = 'none'
        document.querySelector('#legend-map-cidades').style.display = 'block'
    } else{
        ctx = document.getElementById(id)
        document.querySelector('#legend-map-cidades').style.display = 'none'
        document.querySelector('#legend-map-regioes').style.display = 'block'
        document.querySelector('#legend').style.display = 'none'
    }
    let value = ctx.getAttribute('dados')
    let data = JSON.parse(value).data
    
    let size = Math.max(...data.map((a) => a.classeSom))
    let str = ""
    while(size >= 0){
        str = prepareString(size+1, dicionario_som[size]) + str    
        size-=1
    }
    document.querySelector('#classes-container').innerHTML = str
    
        
    data.forEach(element => {
        if (id == "map-agrupamento") {
            cidades_poligono = criaPoligono(element.coordenadas, dicionario_som[element.classeSom])
        } else {
            cidades_poligono = criaPoligono(element.coordenadas, dicionario[element.classe])
        }
        cidades_poligono.setMap(mapa);

        listadepoligonos.push(cidades_poligono)

        // Evento para exibir a infowindow com o nome da UBS e a quantidade cada um dos tipos de notificações
        cidades_poligono.addListener('click', function (event) {
            let nome
            nome = element.nome
            if (id == 'map-agrupamento')
                nome = element.classeSom
            var contentString = '<div id="content" onunload="LimparCampo()">' + "<h6>" + String(element.nome) + "</h6>" + "Casos confirmados: " +
                String(element.confirmados) + "<br><br>" + "Obitos: " + String(element.obitos) + "<br><br>" +
                "Incidência: " + String(element.incidencia) +
                '<br><br>' + buttonVerMais(String(nome)) + '</div>';
            let busca = document.querySelector("#dataTable_filter > label > input")
            if (id == "map")
                busca.value = `^${element.nome}`
            else
                busca.value = element.nome
            busca.dispatchEvent(new Event('keyup', { 'key': 'Enter' }))
            infowindow.setContent(contentString);
            infowindow.setPosition(event.latLng);
            infowindow.open(mapa);
            google.maps.event.addListener(infowindow, 'closeclick', LimparCampo)
        });
    });

}