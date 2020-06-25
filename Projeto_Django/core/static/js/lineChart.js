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
    valueAxis.numberFormatter = new am4core.NumberFormatter()
    valueAxis.numberFormatter.numberFormat = '.##%'

    // Create series
    function createSeries(field, name, color) {
        let series = chart.series.push(new am4charts.LineSeries());
        series.dataFields.valueY = field;
        series.dataFields.dateX = "date";
        series.name = name;
        series.tooltipText = "{dateX.formatDate('dd/MM/yy')}: {valueY.formatNumber('.##%')}";
        series.strokeWidth = 2;
        
        let bullet = series.bullets.push(new am4charts.CircleBullet());
        bullet.circle.stroke = am4core.color("#fff");
        bullet.circle.strokeWidth = 2;
        
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
})


$(function graficosPizza() {

    let ctx = document.getElementById('chartdivsexocasos')
    let value = ctx.getAttribute('dados')
    let data = JSON.parse(value).data
        
    // Set theme
    am4core.useTheme(am4themes_animated);

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

})


$(function graficosPizzaObitos() {

    let ctx = document.getElementById('chartdivsexoobitos')
    let value = ctx.getAttribute('dados')
    let data = JSON.parse(value).data
        
    // Set theme
    am4core.useTheme(am4themes_animated);

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
})

$(function () {

    let ctx = document.getElementById('chartdivfaixaetaria')
    let value = ctx.getAttribute('dados')
    let data = JSON.parse(value).data
    console.log(data)
    
    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    // Create chart instance
    let chart = am4core.create("chartdivfaixaetaria", am4charts.XYChart);
    
    // Add data
    chart.data = data
    
    // Use only absolute numbers
    chart.numberFormatter.numberFormat = "#.#s";

    
    // Create axes
    let categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "faixaEtaria";
    categoryAxis.renderer.grid.template.location = 0;
    categoryAxis.renderer.inversed = true;
    
    let valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
    valueAxis.extraMin = 0.1;
    valueAxis.extraMax = 0.1;
    valueAxis.renderer.minGridDistance = 40;
    valueAxis.renderer.ticks.template.length = 5;
    valueAxis.renderer.ticks.template.disabled = false;
    valueAxis.renderer.ticks.template.strokeOpacity = 0.4;
    valueAxis.renderer.labels.template.adapter.add("text", function (text) {
        return text == "Obitos" || text == "Confirmados" ? text : text;
    })
    
    // Create series
    let male = chart.series.push(new am4charts.ColumnSeries());
    male.dataFields.valueX = "obitos";
    male.dataFields.categoryY = "faixaEtaria";
    male.clustered = false;
    
    let maleLabel = male.bullets.push(new am4charts.LabelBullet());
    maleLabel.label.text = "{valueX}";
    maleLabel.label.hideOversized = false;
    maleLabel.label.truncate = false;
    maleLabel.label.horizontalCenter = "right";
    maleLabel.label.dx = -10;
    
    let female = chart.series.push(new am4charts.ColumnSeries());
    female.dataFields.valueX = "confirmados";
    female.dataFields.categoryY = "faixaEtaria";
    female.clustered = false;
    
    let femaleLabel = female.bullets.push(new am4charts.LabelBullet());
    femaleLabel.label.text = "{valueX}";
    femaleLabel.label.hideOversized = false;
    femaleLabel.label.truncate = false;
    femaleLabel.label.horizontalCenter = "left";
    femaleLabel.label.dx = 10;
    
    let maleRange = valueAxis.axisRanges.create();
    maleRange.value = -10;
    maleRange.endValue = 0;
    maleRange.label.text = "Obitos";
    maleRange.label.fill = chart.colors.list[0];
    maleRange.label.dy = 20;
    maleRange.label.dx = -60;
    maleRange.label.fontWeight = '600';
    maleRange.grid.strokeOpacity = 1;
    maleRange.grid.stroke = male.stroke;
    
    let femaleRange = valueAxis.axisRanges.create();
    femaleRange.value = 0;
    femaleRange.endValue = 10;
    femaleRange.label.text = "Confirmados";
    femaleRange.label.fill = chart.colors.list[1];
    femaleRange.label.dy = 20;
    femaleRange.label.dx = 300;
    femaleRange.label.fontWeight = '600';
    femaleRange.grid.strokeOpacity = 1;
    femaleRange.grid.stroke = female.stroke;
})

    