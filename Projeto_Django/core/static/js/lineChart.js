
// am4core.ready(function() {
//     //pegar dados
//     let ctx = document.getElementById('chartdiv')
//     value = ctx.getAttribute('dados')
//     let data = JSON.parse(value).data
    
//     // Themes begin
//     am4core.useTheme(am4themes_animated);
//     // Themes end
    
//     // Create chart instance
//     let chart = am4core.create("chartdiv", am4charts.XYChart);
    
//     chart.language.locale = am4lang_pt_BR;
//     chart.dateFormatter.language = new am4core.Language();
//     chart.dateFormatter.language.locale = am4lang_pt_BR;
    
//     // Add data
//     chart.data = data;
    
//     // Set input format for the dates
//     chart.dateFormatter.inputDateFormat = "dd-MM-yyyy";

//     // Create axes
//     let dateAxis = chart.xAxes.push(new am4charts.DateAxis());
//     let dateAxis2 = chart.xAxes.push(new am4charts.DateAxis());
//     let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

//     // Create series
//     let series = chart.series.push(new am4charts.LineSeries());
//     series.dataFields.valueY = "value";
//     series.dataFields.dateX = "date";
//     series.tooltipText = "{value}"
//     series.strokeWidth = 2;
//     series.minBulletDistance = 15;

//     let series2 = chart.series.push(new am4charts.LineSeries());
//     series2.dataFields.valueY = "teste";
//     series2.dataFields.dateX = "date";
//     series2.tooltipText = "{value}"
//     series2.strokeWidth = 2;
//     series2.minBulletDistance = 15;

//     // Drop-shaped tooltips
//     series.tooltip.background.cornerRadius = 20;
//     series.tooltip.background.strokeOpacity = 0;
//     series.tooltip.pointerOrientation = "vertical";
//     series.tooltip.label.minWidth = 40;
//     series.tooltip.label.minHeight = 40;
//     series.tooltip.label.textAlign = "middle";
//     series.tooltip.label.textValign = "middle";

//     series2.tooltip.background.cornerRadius = 20;
//     series2.tooltip.background.strokeOpacity = 0;
//     series2.tooltip.pointerOrientation = "vertical";
//     series2.tooltip.label.minWidth = 40;
//     series2.tooltip.label.minHeight = 40;
//     series2.tooltip.label.textAlign = "middle";
//     series2.tooltip.label.textValign = "middle";

//     // Make bullets grow on hover
//     let bullet = series.bullets.push(new am4charts.CircleBullet());
//     bullet.circle.strokeWidth = 2;
//     bullet.circle.radius = 4;
//     bullet.circle.fill = am4core.color("#fff");

//     let bullethover = bullet.states.create("hover");
//     bullethover.properties.scale = 1.3;

//     let bullet2 = series2.bullets.push(new am4charts.CircleBullet());
//     bullet2.circle.strokeWidth = 2;
//     bullet2.circle.radius = 4;
//     bullet2.circle.fill = am4core.color("#fff");

//     let bullethover2 = bullet2.states.create("hover");
//     bullethover2.properties.scale = 1.3;

//     // Make a panning cursor
//     chart.cursor = new am4charts.XYCursor();
//     chart.cursor.behavior = "panXY";
//     chart.cursor.xAxis = dateAxis;
//     chart.cursor.snapToSeries = series;

//     chart2.cursor = new am4charts.XYCursor();
//     chart2.cursor.behavior = "panXY";
//     chart2.cursor.xAxis = dateAxis2;
//     chart2.cursor.snapToSeries = series2;

//     // Create vertical scrollbar and place it before the value axis
//     /* chart.scrollbarY = new am4core.Scrollbar();
//     chart.scrollbarY.parent = chart.leftAxesContainer;
//     chart.scrollbarY.toBack(); */

//     // Create a horizontal scrollbar with previe and place it underneath the date axis
//     chart.scrollbarX = new am4charts.XYChartScrollbar();
//     chart.scrollbarX.series.push(series);
//     chart.scrollbarX.series.push(series2);
//     chart.scrollbarX.parent = chart.bottomAxesContainer;

//     dateAxis.start = 0.79;
//     dateAxis.keepSelection = true;

    
// }); 
// am4core.ready()


/**
 * ---------------------------------------
 * This demo was created using amCharts 4.
 *
 * For more information visit:
 * https://www.amcharts.com/
 *
 * Documentation is available at:
 * https://www.amcharts.com/docs/v4/
 * ---------------------------------------
 */


/**
 * ---------------------------------------
 * This demo was created using amCharts 4.
 *
 * For more information visit:
 * https://www.amcharts.com/
 *
 * Documentation is available at:
 * https://www.amcharts.com/docs/v4/
 * ---------------------------------------
 */

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
    chart.scrollbarX.series.push(series);
    chart.scrollbarX.series.push(series2);
    chart.scrollbarX.parent = chart.bottomAxesContainer;

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
    chart.scrollbarX.series.push(series);
    chart.scrollbarX.series.push(series2);
    chart.scrollbarX.parent = chart.bottomAxesContainer;

    dateAxis.start = 0.79;
    dateAxis.keepSelection = true;
})