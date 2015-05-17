/**
 * Created by dongtaoy on 5/17/15.
 */
var surveyAnalyze = (function () {

    //function that inits the statistic charts for all questions in a survey
    var initCharts = function () {
        $('[id^=chart]').each(function () {
            //get information of a question
            var type = $(this).attr('id').split('_')[1],
                id = $(this).attr('id').split('_')[2],
                chart = $(this),
                table = $('#question_table_' + id + ' tbody tr'),
                data = [];
            //collect data for non-checkbox question
            if (type != 'checkbox') {
                $(table).each(function () {
                    data.push([$(this).find('td:first').text(), parseInt($(this).find('td:last').text())]);
                });
                //render a pie chart for non-checkbox question
                chart.highcharts(PIE_CHART_OPTIONS(data));
            }
            //collect data for checkbox question
            else {
                var categories = [];
                $(table).each(function () {
                    categories.push($(this).find('td:first').text());
                    data.push(parseInt($(this).find('td:nth-child(2)').text()));
                });
                //render a bar chart for non-checkbox question
                chart.highcharts(BAR_CHART_OPTIONS(categories, data));
            }

        })
    };

    //configure bar charts
    var BAR_CHART_OPTIONS = function (categories, data) {
        return {
            chart: {
                type: 'bar'
            },
            title: {
                text: ''
            },
            xAxis: {
                categories: categories,

                labels: {
                    formatter: function () {
                        return "Choice " + ($.inArray(this.value, categories) + 1);
                    }
                }

            },
            yAxis: {
                min: 0,
                minTickInterval: 1,
                title: {
                    text: 'Number of responses',
                    align: 'high'
                },
                labels: {
                    overflow: 'justify'
                }
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            tooltip: {
                formatter: function () {
                    return 'Total responses for choice <b>' + this.point.category + '</b>: <strong>' + this.point.y + '</strong>';
                }
            },
            series: [{
                name: 'responses',
                data: data
            }]
        }
    };


    //configure pie charts
    var PIE_CHART_OPTIONS = function (data) {
        return {
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false
            },
            title: {
                text: ''
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        formatter: function () {
                            return "Choice " + (this.point.index + 1) + ": " + this.point.percentage + '%';
                        },
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
                }
            },
            tooltip: {
                formatter: function () {
                    return 'Total responses for choice <b>' + this.point.name + '</b>: <strong>' + this.point.percentage + '%' + '</strong>';
                }
            },
            series: [{
                type: 'pie',
                name: 'percentage',
                data: data
            }]
        }
    };


    return {
        init: function () {
            initCharts();
        }
    }
}());