/**
 * Created by dongtaoy on 5/17/15.
 */
var surveyAnalyze = (function () {
    var initCharts = function () {
        $('[id^=chart]').each(function () {
            var type = $(this).attr('id').split('_')[1],
                id = $(this).attr('id').split('_')[2],
                chart = $(this),
                table = $('#question_table_' + id + ' tbody tr'),
                data = [];
            if (type != 'checkbox') {
                $(table).each(function () {
                    data.push([$(this).find('td:first').text(), parseInt($(this).find('td:last').text())]);
                });
                chart.highcharts(PIE_CHART_OPTIONS(data));
            }
            else {
                var categories = [];
                $(table).each(function () {
                    categories.push($(this).find('td:first').text());
                    data.push(parseInt($(this).find('td:nth-child(2)').text()));
                });
                chart.highcharts(BAR_CHART_OPTIONS(categories, data));
            }


            //$.getJSON(Django.url('question.data', id), {'type': type})
            //    .success(function (response) {
            //        if (response['status'] == 200) {
            //            if (type == 'SC') {
            //                var options = PIE_CHART_OPTIONS(response['content']);
            //                chart.highcharts(options);
            //            }
            //            if (type == 'MC') {
            //                var categories = $('#question_table_'+id);
            //                console.log(categories);
            //                chart.highcharts(BAR_CHART_OPTIONS(response['content']));
            //            }
            //        }
            //    });


        })
    };

    var BAR_CHART_OPTIONS = function (categories ,data) {
        return {
            chart: {
                type: 'bar'
            },
            title: {
                text: ''
            },
            xAxis: {
                categories: categories,
                title: {
                    text: null
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
            series: [{
                name: 'responses',
                data: data
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