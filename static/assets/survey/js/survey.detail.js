/**
 * Created by dongtaoy on 4/30/15.
 */
var surveyDetail = (function () {

    //function that deletes a whole survey
    var initSurveyDeleteAjax = function () {
        $('.deleteSurvey')
            .off('click')
            .on('click', function () {
                //pop out a confirmation window
                bootbox.dialog({
                    title: "Delete Confirmation",
                    message: "Are you sure?",
                    buttons: {
                        cancelBtn: {
                            label: "Cancel",
                            className: "btn-default"
                        },
                        deleteBtn: {
                            label: "Confirm",
                            className: "btn-danger",
                            callback: function () {
                                $('#surveyDeleteForm').submit();
                            }
                        }
                    }
                })
            });
    };

    //function that inits the chart in the summary(detail) page
    var initBarChart = function (chart_data) {
        $('#trend_chart').highcharts({
            title: {
                text: ''
            },

            xAxis: {
                type: 'datetime',
                title: {
                    text: 'Date'
                }
            },

            yAxis: {
                title: {
                    text: 'number of Responses'
                },
                tickInterval:1,
                min:0

            },

            tooltip: {
                crosshairs: true,
                shared: true,
                xDateFormat: '%A, %Y-%m-%d'
            },

            legend: {
                enabled: false
            },

            series: [{
                name: 'responses',
                data: chart_data
            }]
        })


    };


    return {
        init: function (chart_data) {
            initSurveyDeleteAjax();
            initBarChart(chart_data)
        }
    }

}());