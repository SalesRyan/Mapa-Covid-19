/*!
    * Start Bootstrap - SB Admin v6.0.0 (https://startbootstrap.com/templates/sb-admin)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/BlackrockDigital/startbootstrap-sb-admin/blob/master/LICENSE)
    */
(function($) {
    "use strict";

    // Add active state to sidbar nav links
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
        $("#layoutSidenav_nav .sb-sidenav a.nav-link").each(function() {
            if (this.href === path) {
                $(this).addClass("active");
            }
        });

    // Toggle the side navigation
    $("#sidebarToggle").on("click", function(e) {
        e.preventDefault();
        $("body").toggleClass("sb-sidenav-toggled");
    });
})(jQuery);

$(document).ready(function() {
    $('#dataTable').DataTable({
        'bLengthChange':false,
        "language": {
            "decimal": ",",
            "search":"Buscar:",
            "thousands":".",
            "info": "_START_ - _END_ de _TOTAL_",
            "infoFiltered": "(Filtrado de _MAX_ valores)",
            "paginate": {
                "first": "Primeira",
                "last": "Última",
                "next": "Próxima",
                "previous": "Anterior" 
            }
        }
    });
    document.querySelector("#dataTable_wrapper > div:nth-child(1) > div:nth-child(1)").classList.add("d-none")
    document.querySelector("#dataTable_wrapper > div:nth-child(1) > div:nth-child(2)").classList.remove('col-md-6')
    document.querySelector("#dataTable_wrapper > div:nth-child(1) > div:nth-child(2)").classList.add('col-md-12')

    $('#dataTable_filter > label').attr('class', 'd-flex justify-content-center')
    
});

$(document).ready(function() {
    $('#dataTableRegioes').DataTable({
        'bLengthChange':false,
        // "ordering":false,
        "paging":false,
        "info":false,
        // "searching":false,
        "language": {
            "decimal": ",",
            "search":"Buscar:",
            "thousands":".",
            "info": "_START_ - _END_ de _TOTAL_",
            "infoFiltered": "(Filtrado de _MAX_ valores)",
            "paginate": {
                "first": "Primeira",
                "last": "Última",
                "next": "Próxima",
                "previous": "Anterior" 
            }
        }
    });
    document.querySelector("#dataTableRegioes_wrapper > div:nth-child(1) > div:nth-child(1)").classList.add("d-none")
    document.querySelector("#dataTableRegioes_wrapper > div:nth-child(1) > div:nth-child(2)").classList.remove('col-md-6')
    document.querySelector("#dataTableRegioes_wrapper > div:nth-child(1) > div:nth-child(2)").classList.add('col-md-12')
    
    $('#dataTableRegioes_filter > label').attr('class', 'd-flex justify-content-center')
});

$(document).ready(function() {
    $('#dataTableCidades').DataTable({
        'bLengthChange':false,
        // "ordering":false,
        // "paging":false,
        // "info":false,
        // "searching":false,
        
        "language": {
            "decimal": ",",
            "search":"Buscar:",
            "thousands":".",
            "info": "_START_ - _END_ de _TOTAL_",
            "infoFiltered": "(Filtrado de _MAX_ valores)",
            "paginate": {
                "first": "Primeira",
                "last": "Última",
                "next": "Próxima",
                "previous": "Anterior" 
            }
        }
    });
    document.querySelector("#dataTableCidades_wrapper > div:nth-child(1) > div:nth-child(1)").classList.add("d-none")
    document.querySelector("#dataTableCidades_wrapper > div:nth-child(1) > div:nth-child(2)").classList.remove('col-md-6')
    document.querySelector("#dataTableCidades_wrapper > div:nth-child(1) > div:nth-child(2)").classList.add('col-md-12')
    
    $('#dataTableCidades_filter > label').attr('class', 'd-flex justify-content-center')
});

$(document).ready(function() {
    $('#dataTableDetalhes').DataTable({
        'bLengthChange':false,
        // "paging":false,
        // "searching":false,
        "pageLength": 8,
        "language": {
            "decimal": ",",
            "search":"Buscar:",
            "thousands":".",
            "info": "_START_ - _END_ de _TOTAL_",
            "infoFiltered": "(Filtrado de _MAX_ valores)",
            "paginate": {
                "first": "Primeira",
                "last": "Última",
                "next": "Próxima",
                "previous": "Anterior" 
            }
        }
    });
    document.querySelector("#dataTableDetalhes_wrapper > div:nth-child(1) > div:nth-child(1)").classList.add("d-none")
    document.querySelector("#dataTableDetalhes_wrapper > div:nth-child(1) > div:nth-child(2)").classList.remove('col-md-6')
    document.querySelector("#dataTableDetalhes_wrapper > div:nth-child(1) > div:nth-child(2)").classList.add('col-md-12')
    
    $('#dataTableDetalhes_filter > label').attr('class', 'd-flex justify-content-center')
});
