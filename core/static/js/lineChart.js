function ajaxGraficoCidade(){
    $.ajax({
        method: "GET",
        url: "/api/grafico/cidades",
        async: false,
        success: function (data_ajax) {
            data = data_ajax.data
            graficosLinhaSituacao(data)
            graficosLinhaLeitos()
        }
    })
}

function graficosLinhaSituacao(data) {   

    //am4core.useTheme(am4themes_animated);
    let chart = am4core.create(document.getElementById("chart-1"), am4charts.XYChart);
    
    chart.language.locale = am4lang_pt_BR;
    chart.dateFormatter.language = new am4core.Language();
    chart.dateFormatter.language.locale = am4lang_pt_BR;
    
    for(let item of data){
        if(item.lineColor){
            item.lineColor = am4core.color(item.lineColor) 
        }
    }

    chart.data = data;
    chart.dateFormatter.inputDateFormat = "dd-MM-yyyy";
    
    // Create axes
    let dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    
    let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    
    // Create series
    function createSeries(field, name) {
        let series = chart.series.push(new am4charts.LineSeries());
        series.dataFields.valueY = field;
        series.dataFields.dateX = "date";
        series.name = name;
        series.tooltipText = "{dateX.formatDate('dd/MM/yy')}: {valueY.formatNumber('#')}[/] [#fff]{additional}[/]";
        series.strokeWidth = 2;
        series.propertyFields.stroke = "lineColor"
        series.propertyFields.strokeDasharray = "lineDash";
        
        
        let bullet = series.bullets.push(new am4charts.CircleBullet());
        bullet.propertyFields.fill = "lineColor";
        bullet.stroke = am4core.color("#fff");
        // bullet.fill = am4core.color("#ff0000");
        bullet.strokeWidth = 1;
        //bullet.propertyFields.stroke = "bulletColor"
        //console.log(bullet)


        return series;
    }
    
    
    let series1 = createSeries("confirmados", "Confirmados");
    let series2 = createSeries("obitos", "Óbitos");
    
    chart.legend = new am4charts.Legend();
    chart.cursor = new am4charts.XYCursor();
    
    chart.scrollbarX = new am4charts.XYChartScrollbar();
    chart.scrollbarX.series.push(series1);
    chart.scrollbarX.series.push(series2);
    chart.scrollbarX.parent = chart.bottomAxesContainer;
    
    chart.chartContainer.pixelMarginTop = 100
    chart.chartContainer.MarginTop = 100
    chart.chartContainer.relativeMarginTop = 100
    dateAxis.start = 0.79;
    dateAxis.keepSelection = true;
}

function graficosLinhaLeitos() {
    
    //am4core.useTheme(am4themes_animated);
    
    var data = null
    let endpoint = "/api/grafico/leitos"
    $.ajax({
        method: "GET",
        url: endpoint,
        async: false,
        success: function (data_ajax) {
            data = data_ajax
            data = data.data
            
            
            // Create chart instance
            let chart = am4core.create("chartdivleitos", am4charts.XYChart);
            
            chart.language.locale = am4lang_pt_BR;
            chart.dateFormatter.language = new am4core.Language();
            chart.dateFormatter.language.locale = am4lang_pt_BR;
            
            for(let item of data){
                if(item.lineColor){
                    item.lineColor = am4core.color(item.lineColor) 
                }
            }
        
            // Add data
            chart.data = data;
            chart.dateFormatter.inputDateFormat = "dd-MM-yyyy";
            
            // Create axes
            let dateAxis = chart.xAxes.push(new am4charts.DateAxis());
            dateAxis.renderer.grid.template.location = 0;
            
            let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
            valueAxis.numberFormatter = new am4core.NumberFormatter()
            valueAxis.numberFormatter.numberFormat = '.##%'
            
            // Create series
            function createSeries(field, name, color) {
                let series = chart.series.push(new am4charts.LineSeries());
                series.dataFields.valueY = field;
                series.dataFields.dateX = "date";
                series.name = name;
                series.tooltipText = "{dateX.formatDate('dd/MM/yy')}: {valueY.formatNumber('.##%')}[/] [#fff]{additional}[/]";
                series.strokeWidth = 2;
                series.propertyFields.stroke = "lineColor"
                series.propertyFields.strokeDasharray = "lineDash";
                
                
                let bullet = series.bullets.push(new am4charts.CircleBullet());
                bullet.circle.stroke = am4core.color("#fff");
                bullet.circle.strokeWidth = 1;
                bullet.propertyFields.fill = "lineColor";
        
                
                return series;
            }
            
            let series1 = createSeries("ocupadosClinicos", "Clínicos");
            let series2 = createSeries("ocupadosUti", "UTI");
            let series3 = createSeries("ocupadosEstabilizacao", "Estabilização");
            let series4 = createSeries("ocupadosRespiradores", "Respiradores");
            
            chart.legend = new am4charts.Legend();
            chart.cursor = new am4charts.XYCursor();
            
            chart.scrollbarX = new am4charts.XYChartScrollbar();
            chart.scrollbarX.series.push(series1);
            chart.scrollbarX.series.push(series2);
            chart.scrollbarX.series.push(series3);
            chart.scrollbarX.series.push(series4);
            chart.scrollbarX.parent = chart.bottomAxesContainer;
            
            dateAxis.start = 0.79;
            dateAxis.keepSelection = true;
            graficosPizza()
        },
    })
}

function graficosPizza() {
    
    var data = null
    let endpoint = "/api/grafico/sexo/confirmados"
    $.ajax({
        method: "GET",
        url: endpoint,
        async: false,
        success: function (data_ajax) {
            data = data_ajax
            data = data.data
            
            // Set theme
            //am4core.useTheme(am4themes_animated);
            
            // Create chart instance
            let chart = am4core.create("chartdivsexocasos", am4charts.PieChart3D);
            chart.language.locale = am4lang_pt_BR;
            chart.dateFormatter.language = new am4core.Language();
            chart.dateFormatter.language.locale = am4lang_pt_BR;
            
            let title = chart.titles.create();
            title.text = "Confirmados";   
            title.fontSize = 15;
            title.marginBottom = 5;
            title.marginTop = 20;
            
            
            // Let's cut a hole in our Pie chart the size of 40% the radius
            chart.innerRadius = am4core.percent(40);
            
            // Add data
            chart.data = data;
            
            // Add and configure Series
            let pieSeries = chart.series.push(new am4charts.PieSeries3D());
            pieSeries.dataFields.value = "value";
            pieSeries.dataFields.category = "label";
            pieSeries.slices.template.stroke = am4core.color("#fff");
            pieSeries.slices.template.strokeWidth = 2;
            pieSeries.slices.template.strokeOpacity = 1;
            
            // Disabling labels and ticks on inner circle
            pieSeries.labels.template.disabled = true;
            pieSeries.ticks.template.disabled = true;
            
            // Disable sliding out of slices
            pieSeries.slices.template.states.getKey("hover").properties.shiftRadius = 0;
            pieSeries.slices.template.states.getKey("hover").properties.scale = 1.1;
            
            chart.legend = new am4charts.Legend();
            chart.legend.marginBottom = 20;
            graficosPizzaObitos()
        },
    })
    
}

function graficosPizzaObitos() {
    
    var data = null
    let endpoint = "/api/grafico/sexo/obitos"
    $.ajax({
        method: "GET",
        url: endpoint,
        async: false,
        success: function (data_ajax) {
            data = data_ajax
            data = data.data
            
            // Set theme
            //am4core.useTheme(am4themes_animated);
            
            // Create chart instance
            let chart = am4core.create("chartdivsexoobitos", am4charts.PieChart3D);
            chart.language.locale = am4lang_pt_BR;
            chart.dateFormatter.language = new am4core.Language();
            chart.dateFormatter.language.locale = am4lang_pt_BR;
            
            let title = chart.titles.create();
            title.text = "Óbitos";   
            title.fontSize = 15;
            title.marginBottom = 5;
            title.marginTop = 20;
            
            // Let's cut a hole in our Pie chart the size of 40% the radius
            chart.innerRadius = am4core.percent(40);
            
            // Add data
            chart.data = data;
            
            // Add and configure Series
            let pieSeries = chart.series.push(new am4charts.PieSeries3D());
            pieSeries.dataFields.value = "value";
            pieSeries.dataFields.category = "label";
            pieSeries.slices.template.stroke = am4core.color("#fff");
            pieSeries.slices.template.strokeWidth = 2;
            pieSeries.slices.template.strokeOpacity = 1;
            
            // Disabling labels and ticks on inner circle
            pieSeries.labels.template.disabled = true;
            pieSeries.ticks.template.disabled = true;
            
            // Disable sliding out of slices
            pieSeries.slices.template.states.getKey("hover").properties.shiftRadius = 0;
            pieSeries.slices.template.states.getKey("hover").properties.scale = 1.1;
            
            chart.legend = new am4charts.Legend();
            chart.legend.marginBottom = 20;
            graficosPessoaComordidades()
        },
    })
}

function graficosPessoaComordidades() {
    
    var data = null
    let endpoint = "/api/grafico/comorbidades"
    $.ajax({
        method: "GET",
        url: endpoint,
        async: false,
        success: function (data_ajax) {
            data = data_ajax
            data = data.data
            // Themes begin
            //am4core.useTheme(am4themes_animated);
            // Themes end
            
            let iconPath = "M53.5,476c0,14,6.833,21,20.5,21s20.5-7,20.5-21V287h21v189c0,14,6.834,21,20.5,21 c13.667,0,20.5-7,20.5-21V154h10v116c0,7.334,2.5,12.667,7.5,16s10.167,3.333,15.5,0s8-8.667,8-16V145c0-13.334-4.5-23.667-13.5-31 s-21.5-11-37.5-11h-82c-15.333,0-27.833,3.333-37.5,10s-14.5,17-14.5,31v133c0,6,2.667,10.333,8,13s10.5,2.667,15.5,0s7.5-7,7.5-13 V154h10V476 M61.5,42.5c0,11.667,4.167,21.667,12.5,30S92.333,85,104,85s21.667-4.167,30-12.5S146.5,54,146.5,42 c0-11.335-4.167-21.168-12.5-29.5C125.667,4.167,115.667,0,104,0S82.333,4.167,74,12.5S61.5,30.833,61.5,42.5z"
            
            let chart = am4core.create("chartdivcomorbidades", am4charts.SlicedChart);
            chart.language.locale = am4lang_pt_BR;
            chart.dateFormatter.language = new am4core.Language();
            chart.dateFormatter.language.locale = am4lang_pt_BR;
            chart.hiddenState.properties.opacity = 0; // this makes initial fade in effect
            
            chart.data = data;
            
            let series = chart.series.push(new am4charts.PictorialStackedSeries());
            series.dataFields.value = "value";
            series.dataFields.category = "name"; 
            series.alignLabels = false;
            series.labels.dy = 20
            series.labels.template.disabled = true
            
            series.maskSprite.path = iconPath;
            series.ticks.template.locationX = 1;
            series.ticks.template.locationY = 0.5;
            
            series.labelsContainer.width = 0;
            
            chart.legend = new am4charts.Legend();
            chart.legend.position = "left";
            chart.legend.valign = "bottom";
            graficosBarrasFaixaEtaria()
        },
    })
    
}

function graficosBarrasFaixaEtaria() {
    var data = null
    let endpoint = "/api/grafico/faixa-etaria"
    $.ajax({
        method: "GET",
        url: endpoint,
        async: false,
        success: function (data_ajax) {
            data = data_ajax
            data = data.data
        
            var chart = am4core.create("chartdivfaixaetaria", am4charts.XYChart);
            
            // Add data
            chart.data = data
            //         "year": 2009,
            //   "income": 24.6,
            //   "expenses": 25
        
            // Create axes
            var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
            categoryAxis.dataFields.category = "faixaEtaria";
            categoryAxis.numberFormatter.numberFormat = "#";
            categoryAxis.renderer.inversed = true;
            categoryAxis.renderer.grid.template.location = 0;
            categoryAxis.renderer.cellStartLocation = 0.1;
            categoryAxis.renderer.cellEndLocation = 0.9;
        
            var  valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
            valueAxis.renderer.opposite = true;
        
            // Create series
            function createSeries(field, name) {
                var series = chart.series.push(new am4charts.ColumnSeries());
                series.dataFields.valueX = field;
                series.dataFields.categoryY = "faixaEtaria";
                series.name = name;
                series.columns.template.tooltipText = "{name}: {valueX}[/]";
                series.columns.template.height = am4core.percent(100);
                series.sequencedInterpolation = true;
        
                var valueLabel = series.bullets.push(new am4charts.LabelBullet());
                valueLabel.label.text = "{valueX}";
                valueLabel.label.horizontalCenter = "left";
                valueLabel.label.dx = 10;
                valueLabel.label.hideOversized = false;
                valueLabel.label.truncate = false;
        
                /* var categoryLabel = series.bullets.push(new am4charts.LabelBullet());
                categoryLabel.label.text = "{name}";
                categoryLabel.label.horizontalCenter = "right";
                categoryLabel.label.dx = -10;
                categoryLabel.label.fill = am4core.color("#fff");
                categoryLabel.label.hideOversized = false;
                categoryLabel.label.truncate = false; */
            }
        
            createSeries("confirmados", "Confirmados");
            createSeries("obitos", "Óbitos");
            chart.legend = new am4charts.Legend();
            chart.legend.valign = "bottom";
        },
    })

}
