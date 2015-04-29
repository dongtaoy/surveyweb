/**
 * Created by dongtaoy on 4/30/15.
 */
var surveyDetail = (function () {



    var initSurveyDeleteAjax = function () {
        $('.deleteSurvey')
            .off('click')
            .on('click', function(){
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


    var initBarChart = function () {
        // bar chart:
        var data = GenerateSeries(0);

        function GenerateSeries(added) {
            var data = [];
            var start = 100 + added;
            var end = 200 + added;

            for (i = 1; i <= 20; i++) {
                var d = Math.floor(Math.random() * (end - start + 1) + start);
                data.push([i, d]);
                start++;
                end++;
            }

            return data;
        }

        var options = {
            series: {
                bars: {
                    show: true
                }
            },
            bars: {
                barWidth: 0.8,
                lineWidth: 0, // in pixels
                shadowSize: 0,
                align: 'left'
            },

            grid: {
                tickColor: "#eee",
                borderColor: "#eee",
                borderWidth: 1
            }


        };

        if ($('#chart_1_1').size() !== 0) {
            $.plot($("#chart_1_1"), [{
                data: data,
                lines: {
                    lineWidth: 1
                },
                shadowSize: 0
            }], options);
        }
    };


    return {
        init: function () {
            initSurveyDeleteAjax();

            initBarChart()
        }
    }

}());