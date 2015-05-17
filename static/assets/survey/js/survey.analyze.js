/**
 * Created by dongtaoy on 5/17/15.
 */
var surveyAnalyze = (function () {
    var initCharts = function () {
        $('[id^=chart]').each(function () {
            var type = $(this).attr('id').split('_')[1];
            var id = $(this).attr('id').split('_')[2];
            var chart = $(this);
            $.getJSON(Django.url('question.data', id), {'type': type})
                .success(function (response) {
                    if (response['status'] == 200) {
                        if (type == 'SC') {
                            var options = PIE_CHART_OPTIONS(response['content']);
                            chart.highcharts(options);
                        }
                        if (type == 'MC') {
                            var categories = $('#question_table_'+id);
                            console.log(categories);
                            chart.highcharts(BAR_CHART_OPTIONS(response['content']));
                        }
                    }
                });


        })
    };

    var BAR_CHART_OPTIONS = function (data) {
        return {
            chart: {
                type: 'bar'
            },
            title: {
                text: ''
            },
            xAxis: {
                categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania'],
                title: {
                    text: null
                }
            },
            yAxis: {
                min: 0,
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
            series: [{
                name: ' ',
                data: [107, 31, 635, 203, 2]
            }]
        }
    };


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
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    }
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