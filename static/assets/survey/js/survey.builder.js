/**
 * Created by GC-Mac on 28/04/15.
 */


var surveyBuilder = (function () {

    var WYSIHTML5OPTIONS = {
        toolbar: {
            "html": true,
            "link": false,
            "image": false,
            "blockquote": false,
            "size": "md"
        }
    };


    var initNavbar = function () {

        $(".nav-pills li a")
            .mouseover(function () {
                //alert($(this).html());
                $(this).find("span").attr("class", "icon-plus pull-right add");
            })
            .mouseout(function () {
                $(this).find("span").attr("class", "");
            });

        $('[data-toggle="tooltip"]').tooltip();

        var headerHeight = $('.page-header').height() + $('.survey-head').height();
        //var footerHeight = $('.page-footer').height() + $('.page-prefooter').height() + 0;
        var maximumTop = $(".pageCreateForm > button").offset().top - $('#builderNav').height() - 25;
        var navbarAdjust = function () {
            if ($(window).scrollTop() > headerHeight) {
                if ($(window).scrollTop() < maximumTop) {
                    $('#builderNav').css({
                        'margin-top': $(window).scrollTop() - headerHeight + 'px'
                    });
                } else {
                    $('#builderNav').css({
                        'margin-top': maximumTop - headerHeight + 'px'
                    });
                }

            } else {
                $('#builderNav').css({
                    'margin-top': 0 + 'px'
                });

            }
        };
        $(window)
            .scroll(navbarAdjust)
            .on('scrollstop', navbarAdjust);
    };

    var initQuestionCreateAjax = function () {
        $(".nav-pills li a")
            .off('click')
            .on('click', function () {
                if ($('.question-edit').length == 0) {
                    var notify = $.notify("Add new question...");
                    var pageNumber = $('#page-select').val();
                    pagePortlet = $('#survey-pages').children().eq(pageNumber - 1);
                    questionTypeId = $(this).attr('id').replace(/[^\d.]/g, '');
                    pageId = pagePortlet.attr('id').replace(/[^\d.]/g, '');
                    //console.log(questionTypeId, pageId);
                    // get question edit form
                    $.get(Django.url('question.create'), {
                        questionType: questionTypeId,
                        page: pageId,
                        containerType: 'QU'
                    })
                        .done(function (data) {
                            if (pagePortlet.find('.empty-page').length) {
                                pagePortlet.find('.page-body').html($(data));

                            } else {
                                pagePortlet.find('.page-body').append(data);
                            }
                            initQuestionPlugin();
                            // bind question save button
                            $('.question-edit form').submit(function () {
                                var notify = $.notify('Saving questions...');
                                console.log($(this));
                                $(this).ajaxSubmit({
                                    success: function (response) {
                                        $('.question-edit').remove();
                                        $('#page_' + pageId + '> .portlet-body > .row > .page-body').append(response);
                                        initQuestionTool();
                                        initNavbar();
                                    }
                                });
                                notify.close();
                                return false;
                            });

                            notify.close();
                        });
                } else {
                    $.notify({
                        message: "Please save your last question first!"
                    }, {
                        type: "warning",
                        onShow: function () {
                            $('.question-edit').attr('tabindex', -1).focus();
                        }
                    });
                }
                return false;
            });
    };


    var initQuestionPlugin = function () {
        $('.question-edit').find('textarea').wysihtml5(WYSIHTML5OPTIONS);
    };


    var initPageCreateAjax = function () {

        var notify;
        $('.pageCreateForm')
            .off('submit')
            .on('submit', function () {
                $(this).ajaxSubmit({
                    beforeSubmit: function () {
                        notify = $.notify("Creating new page...")
                    },
                    success: function (response) {
                        notify.close();
                        $(response).insertBefore('.pageCreateForm');
                        initPageDeleteAjax();
                        initPageEditAjax();
                        initNavbar();
                        initPageSelect();
                        initPageDirect();
                        initPageNumDisplay();
                    }
                });
                return false
            });
    };

    var initPageDeleteAjax = function () {
        $('.actions a.pageDelete')
            .off('click')
            .on('click', function () {
                pagePortlet = $(this).closest('.portlet');
                pageId = pagePortlet.attr('id').replace(/[^\d.]/g, '');
                pageOrder = pagePortlet.find('.caption-subject.bold.uppercase').text().replace(/[^\d.]/g, '');
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
                                // Post ajax request to delete a page
                                var notify = $.notify("Deleting page...")
                                $.post(Django.url('page.delete', pageId), function (response) {
                                    // if successfully deleted a page
                                    if (response['status'] == 200) {
                                        // loop all the portlet that is after current, change the title
                                        pagePortlet.nextAll('.portlet').each(function () {
                                            $(this).find('.caption-subject.bold.uppercase').text("page " + (pageOrder++));
                                        });
                                        // remove the current portlet
                                        pagePortlet.remove();
                                        initPageSelect();
                                        notify.close();
                                    } else {
                                        notify.update('message', 'Something went wrong... :(');
                                    }

                                });
                            }
                        }
                    }
                })
            });
    };

    var initPageEditAjax = function () {
        $('.pageEdit')
            .off('click')
            .on('click', function () {
                var notify = $.notify("Moving pages...");
                pagePortlet = $(this).closest('.portlet');
                pageId = pagePortlet.attr('id').replace(/[^\d.]/g, '');
                pageOrder = pagePortlet.find('.caption-subject.bold.uppercase').text().replace(/[^\d.]/g, '');
                isUp = false;
                if (/up/.test($(this).text().toLowerCase())) {
                    isUp = true;
                    pageOrder--;
                }
                else {
                    pageOrder++;
                }
                $.post(Django.url('page.edit', pageId), {"page": pageId, "order": pageOrder})
                    .done(function (response) {
                        if (response['status'] == 200) {
                            if (isUp) {
                                $(pagePortlet).find('.caption-subject.bold.uppercase.page').text('Page ' + pageOrder);
                                $(pagePortlet).prev('.portlet').find('.caption-subject.bold.uppercase.page').text('Page ' + (pageOrder + 1));
                                $(pagePortlet).insertBefore($(pagePortlet).prev('.portlet'));
                            } else {
                                $(pagePortlet).find('.caption-subject.bold.uppercase.page').text('Page ' + pageOrder);
                                $(pagePortlet).next('.portlet').find('.caption-subject.bold.uppercase.page').text('Page ' + (pageOrder - 1));
                                $(pagePortlet).insertAfter($(pagePortlet).next('.portlet'));

                            }
                            notify.close();
                        } else {
                            notify.update('message', 'Something went wrong....');
                            //bootbox.alert({
                            //    size: "medium",
                            //    message: "<br/><div class='note note-danger'><h4>Error!</h4><p>Cannot move up the first page or move down the last page</p></div>"
                            //});
                        }
                    });
            });
    };

    var initPageNumDisplay = function () {
        var currentTop = $(document).scrollTop();

        var pageNumber = $("#survey-pages").children("div").length;
        var toleranceHeight = 50;
        $(document).scroll(function () {
            currentTop = $(document).scrollTop();
            var currentBottom = currentTop + $(window).height();
            for (var i = 1; i <= pageNumber; i++) {
                var currentOffset = $("#survey-pages > div:nth-child(" + i + ")").offset();
                var currentDivTop = currentOffset.top;
                if (currentDivTop >= currentTop - toleranceHeight) {
                    if (currentDivTop >= currentBottom - ($(window).height())/2) {
                        var prev = i-1;
                        $("#page-select").val(prev);
                    }else{
                        $("#page-select").val(i);
                    }
                    return;
                }
            }
        })
    };

    var initPageDirect = function () {
        var pageNumber = $("#survey-pages").children("div").length;
        var toleranceHeight = 25;
        $("#page-select").click(function () {
            for (var i = 1; i <= pageNumber; i++) {
                if ($(this).val() == i) {
                    var offset = $("#survey-pages > div:nth-child(" + i + ")").offset();
                    var pageTop = offset.top;
                    $(document).scrollTop(pageTop - toleranceHeight);
                    return;
                }
            }
        });
    };

    var initPageSelect = function () {
        var pageNumber = $("#survey-pages").children("div").length;
        $("#page-select").find('option').remove();
        for (var i = 1; i <= pageNumber; i++) {
            $("#page-select").append("<option value=" + i + ">Page " + i + "</option>");
        }
        $("#page-select").val(pageNumber);
    };

    var initQuestionTool = function () {
        $("[id^='question-']").hover(
            function () {
                var questionId = $(this).attr('id').replace(/[^\d.]/g, '');
                $("#edit-btn-group-" + questionId).css("visibility", "visible");
                $(this).parent().addClass("highlight-frame");
                $(this).parent().removeClass("question-frame");
            },
            function () {
                var questionId = $(this).attr('id').replace(/[^\d.]/g, '');
                $("#edit-btn-group-" + questionId).css("visibility", "hidden");
                $(this).parent().addClass("question-frame");
                $(this).parent().removeClass("highlight-frame");
            });
    };

    return {
        init: function () {


            initNavbar();

            initPageCreateAjax();
            initPageDeleteAjax();
            initPageEditAjax();

            initQuestionCreateAjax();
            initQuestionTool();

            initPageNumDisplay();
            initPageDirect();

        }
    }
}());

//jQuery(document).ready(function () {
//    //$('.wysihtml5').wysihtml5();
//    //
//    //
//    //$("#image-edit-upload").dropzone({dictDefaultMessage: "Please drag your images and drop into these area :)"});
//    //
//    //$("#elo-edit-upload").dropzone({dictDefaultMessage: "Please drag your images and drop into these area :)"});
//
//    $(".nav-pills li")
//        .mouseover(function () {
//            //alert($(this).html());
//            $(this).find("span").attr("class", "icon-plus pull-right add");
//        })
//        .mouseout(function () {
//            $(this).find("span").attr("class", "");
//        })
//        .click(function (){
//            $(".pageBody").append('{% include "survey/builder/question/elo-edit.html" %}');
//        });
//
//    $('[data-toggle="tooltip"]').tooltip();
//
//    //$('form').ajaxForm();
//
//    $('.pageCreateForm').submit(function(){
//        $(this).ajaxSubmit({
//            success: function(response){
//                $('.portlet.light').last().after(response);
//            }
//        });
//
//        return false
//    })
//});
//
//var radioCount = 1, checkboxCount = 1, selectCount = 1;
//
//function radioAdd(element) {
//    var container = $(element);
//    radioCount++;
//    container.append('\
//                    <div class="input-group " style="margin:2px 0"> \
//                        <span class="input-group-addon count">' + radioCount + '.</span> \
//                        <div class="input-group-control"> \
//                            <input type="text" class="form-control" placeholder="Choice"> \
//                        </div> \
//                        <span class="input-group-btn btn-right actions"> \
//                            <button class="btn blue-madison"  onclick="radioRemove(this)" type="button"><i class="fa fa-minus fa-fw"></i>Remove \
//                            </button> \
//                        </span> \
//                    </div> \
//                    ');
//}
//
//function radioRemove(element) {
//    var container = $(element).parent().parent();
//    radioCount--;
//    container.remove();
//    for (var i = 1; i <= radioCount; i++) {
//        $(".radioAddChoice > .form-group > div:nth-child(" + i + ") > .count").html(i + ".");
//    }
//}
//
//var stockArea = $('.col-md-12.column.sortable').droppable({
//    drop: function (event, ui) {
//        var target = $(event.target);
//
//        //alert($('#accordion1_$'));
//        //var app = document.getElementById()
//        //rebindDraggables();
//        var droppedItem = ui.draggable.prop('tagName').toLowerCase();
//        //var droppedItem = ui.draggable.attr('class').toLowerCase();
//
//        var droppedType = ui.draggable.attr('id');
//        if (droppedItem == 'li') {
//            //alert(droppedType);
//            //alert(1);
//            var count = $('.portlet').length + 1;
//            //alert(count);
//            //alert(("<div class=\"panel panel-default\"><div class=\"panel-heading\"><h4 class=\"panel-title\"><a class=\"accordion-toggle\" data-toggle=\"collapse\" data-parent=\"#accordion1\" href=\"$id$count\">$id</a></h4></div><div id=\"$id$count\" class=\"panel-collapse collapse\"><div class=\"panel-body\">$id $count</div></div></div>").replace('$id', droppedType));
//            $.ajax({
//                url: "{% static 'singletext-edit.html' %}",
//                success: function (data) {
//                    target.append(data);
//                },
//                dataType: 'html'
//            });
//            //target.append("<div class=\"panel panel-default\"><div class=\"panel-heading\"><h4 class=\"panel-title\"><a class=\"accordion-toggle\" data-toggle=\"collapse\" data-parent=\"#accordion1\" href=\"#" + droppedType + count + "\">" + count + ". " + droppedType + "</a></h4></div><div id=\"" + droppedType + count + "\" class=\"panel-collapse collapse\" aria-expanded=\"false\"><div class=\"panel-body\">" + droppedType + count + "<p>This is just for Test Purpose</p></div></div></div>");
//        }
//    }
//});
