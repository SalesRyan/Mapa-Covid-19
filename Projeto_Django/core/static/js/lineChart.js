$(function graficosLinhaSituacao() {

    am4core.useTheme(am4themes_animated);
    
    let ctx = document.getElementById('chart-1')
    let value = ctx.getAttribute('dados')
    let data = JSON.parse(value).data
    
    
    // Create chart instance
    let chart = am4core.create(document.getElementById("chart-1"), am4charts.XYChart);
    
    chart.language.locale = am4lang_pt_BR;
    chart.dateFormatter.language = new am4core.Language();
    chart.dateFormatter.language.locale = am4lang_pt_BR;
    
    // Add data
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
        series.tooltipText = "{dateX.formatDate('dd/MM/yy')}: {valueY.formatNumber('#')}";
        series.strokeWidth = 2;
        
        let bullet = series.bullets.push(new am4charts.CircleBullet());
        bullet.circle.stroke = am4core.color("#fff");
        bullet.circle.strokeWidth = 2;
        
        return series;
    }
    
    
    let series1 = createSeries("confirmados", "Confirmados");
    let series2 = createSeries("obitos", "Óbitos");
    
    chart.legend = new am4charts.Legend();
    chart.cursor = new am4charts.XYCursor();
    
    chart.scrollbarX = new am4charts.XYChartScrollbar();
    chart.scrollbarX.series.push(series2);
    chart.scrollbarX.parent = chart.bottomAxesContainer;

    dateAxis.start = 0.79;
    dateAxis.keepSelection = true;
    
})

$(function graficosLinhaLeitos() {

    am4core.useTheme(am4themes_animated);
    
    let ctx = document.getElementById('chartdivleitos')
    let value = ctx.getAttribute('dados')
    let data = JSON.parse(value).data
    
    
    // Create chart instance
    let chart = am4core.create("chartdivleitos", am4charts.XYChart);
    
    chart.language.locale = am4lang_pt_BR;
    chart.dateFormatter.language = new am4core.Language();
    chart.dateFormatter.language.locale = am4lang_pt_BR;
    
    // Add data
    chart.data = data;
    chart.dateFormatter.inputDateFormat = "dd-MM-yyyy";

    // Create axes
    let dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;

    let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

    // Create series
    function createSeries(field, name, color) {
        let series = chart.series.push(new am4charts.LineSeries());
        series.dataFields.valueY = field;
        series.dataFields.dateX = "date";
        series.name = name;
        series.tooltipText = "{dateX.formatDate('dd/MM/yy')}: {valueY.formatNumber('#')}";
        series.strokeWidth = 2;
        
        let bullet = series.bullets.push(new am4charts.CircleBullet());
        bullet.circle.stroke = am4core.color("#fff");
        bullet.circle.strokeWidth = 2;
        
        return series;
    }
    
    let series1 = createSeries("ocupadosClinicos", "Leitos Clínicos Ocupados");
    let series2 = createSeries("ocupadosUti", "Leitos de UTI Ocupados");
    let series3 = createSeries("ocupadosEstabilizacao", "Leitos de Estabilização Ocupados");
    let series4 = createSeries("ocupadosRespiradores", "Leitos com Respiradores ocupados");

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
})