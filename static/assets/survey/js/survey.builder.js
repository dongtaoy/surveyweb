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


        // init mouse over of navbar
        $(".nav-pills li a")
            .off('mouseover')
            .on('mouseover', function () {
                $(this).find("span").attr("class", "icon-plus pull-right add");
            })
            .off('mouseout')
            .on('mouseout', function () {
                $(this).find("span").attr("class", "");
            });


        var headerHeight = $('.page-header').height() + $('.survey-head').height();
        var maximumTop = $("#page-create-form > button").offset().top - $('#builder-navbar').height() - 25;
        var navbarAdjust = function () {
            if ($(window).scrollTop() > headerHeight) {
                if ($(window).scrollTop() < maximumTop) {
                    $('#builder-navbar').css({
                        'margin-top': $(window).scrollTop() - headerHeight + 'px'
                    });
                } else {
                    $('#builder-navbar').css({
                        'margin-top': maximumTop - headerHeight + 'px'
                    });
                }

            } else {
                $('#builder-navbar').css({
                    'margin-top': 0 + 'px'
                });

            }
        };
        $(window)
            .off('scroll')
            .on('scroll', navbarAdjust);
        //.scroll(navbarAdjust)
        //.on('scrollstop', navbarAdjust);
    };

    var initQuestionCreateAjax = function () {
        $(".nav-pills li a")
            .off('click')
            .on('click', function () {
                if ($('.container-edit').length == 0) {
                    var notify = $.notify("Add new question...");
                    var pageNumber = $('#page-select').val();
                    var pagePortlet = $('[id^=page-no-]').eq(pageNumber - 1);
                    var pageId = pagePortlet.attr('id').replace(/[^\d.]/g, '');
                    var containerType = $(this).attr('id').substr(0, 2);
                    var url = null;
                    var data = null;
                    console.log(containerType);
                    if (containerType == 'QU') {
                        url = Django.url('question.create');
                        var questionTypeId = $(this).attr('id').replace(/[^\d.]/g, '');
                        data = {
                            questionType: questionTypeId,
                            page: pageId,
                            containerType: containerType
                        }
                    } else if(containerType == 'TE'){
                        url = Django.url('container.text.create');
                        data = {
                            page: pageId,
                            containerType: containerType
                        }
                    } else if(containerType == 'IM'){
                        url = Django.url('container.image.create');
                    }
                    if(url == null)
                        return;

                    $.get(url, data)
                        .done(function (data) {
                            if (pagePortlet.find('.empty-page').length) {
                                pagePortlet.find('.page-body').html($(data));

                            } else {
                                pagePortlet.find('.page-body').append(data);
                            }
                            initQuestionPlugin();

                            // bind question save button
                            $('.container-edit form').submit(function () {
                                $(this).find(':submit').attr('disabled', true);
                                var notify = $.notify('Saving questions...');
                                $(this).ajaxSubmit({
                                    success: function (response) {
                                        $('.container-edit').remove();
                                        $(pagePortlet).find('.page-body').append(response);
                                        initQuestionTool();
                                        initNavbar();
                                    }
                                });
                                notify.close();
                                return false;
                            });

                            // bind question cancel button
                            $('.container-edit button.cancel').click(function () {
                                $('.container-edit').remove();
                            });

                            notify.close();
                        });
                } else {
                    $.notify({
                        message: "Please save your last question first!"
                    }, {
                        type: "warning",
                        onShow: function () {
                            $('.container-edit').attr('tabindex', -1).focus();
                        }
                    });
                }
                return false;
            });
    };


    var initQuestionPlugin = function () {

        $('.container-edit').attr('tabindex', -1).focus();
        $('.container-edit').find('textarea').wysihtml5(WYSIHTML5OPTIONS);
    };


    var initPageCreateAjax = function () {

        var notify;
        $('#page-create-form')
            .off('submit')
            .on('submit', function () {
                $(this).find(':submit').attr('disabled', true);
                $(this).ajaxSubmit({
                    beforeSubmit: function () {
                        notify = $.notify("Creating new page...")
                    },
                    success: function (response) {
                        notify.close();
                        $(response).insertBefore('#page-create-form');
                        //console.
                        $('#page-create-form').find(':submit').attr('disabled', false);
                        initPageDeleteAjax();
                        initPageEditAjax();
                        initDisplay();
                        //console.log($('[id^=page-no-]').last().position().top);
                        //$('[id^=page-no-]').last().attr('tabindex', -1).focus();
                    }
                });
                return false
            });
    };

    var initPageDeleteAjax = function () {
        $('.actions a.page-delete')
            .off('click')
            .on('click', function () {
                if ($('[id^=page-no-]').length == 1) {
                    $.notify({
                        message: 'Cannot delete the last page!'
                    }, {
                        type: 'danger'
                    });
                    return;
                }
                var pagePortlet = $(this).closest('[id^=page-no-]');
                var pageId = pagePortlet.attr('id').replace(/[^\d.]/g, '');
                var pageOrder = pagePortlet.find('.page-order').val();

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
                                pagePortlet.find('.actions > a').attr('disabled', true);
                                // Post ajax request to delete a page
                                var notify = $.notify("Deleting page...")
                                $.post(Django.url('page.delete', pageId), function (response) {
                                    // if successfully deleted a page

                                    if (response['status'] == 200) {

                                        // remove the current portlet
                                        pagePortlet.remove();

                                        // loop all the portlet and change the title and order
                                        $('[id^=page-no-]').each(function (i) {
                                            $(this).find('.caption-subject.bold.uppercase.page').text('Page ' + (i + 1));
                                            $(this).find('.page-order').val(i + 1);
                                        });
                                        initDisplay();
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
        $('.page-edit')
            .off('click')
            .on('click', function () {
                var notify = $.notify("Moving pages...");
                var pagePortlet = $(this).closest('[id^=page-no-]');
                var pageId = pagePortlet.attr('id').replace(/[^\d.]/g, '');
                var pageOrder = pagePortlet.find('.page-order').val();
                var isUp = false;
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
                            $(pagePortlet).find('.caption-subject.bold.uppercase.page').text('Page ' + pageOrder);
                            $(pagePortlet).find('.page-order').val(pageOrder);
                            if (isUp) {
                                $(pagePortlet).prev('[id^=page-no-]').find('.caption-subject.bold.uppercase.page').text('Page ' + (pageOrder + 1));
                                $(pagePortlet).prev('[id^=page-no-]').find('.page-order').val(pageOrder + 1);
                                $(pagePortlet).insertBefore($(pagePortlet).prev('.portlet'));
                            } else {
                                $(pagePortlet).next('[id^=page-no-]').find('.caption-subject.bold.uppercase.page').text('Page ' + (pageOrder - 1));
                                $(pagePortlet).prev('[id^=page-no-]').find('.page-order').val(pageOrder - 1);
                                $(pagePortlet).insertAfter($(pagePortlet).next('.portlet'));
                            }
                            initDisplay();
                            notify.close();
                        } else {
                            var error = response['content'].split('\n')[1];
                            notify.update('message', error);
                        }
                    });
            });
    };


    var initDisplay = function () {
        initNavbar();
        initPageSelect();
        initQuestionTool();
        initPageNumDisplay();
        initPageDirect();
        $(window).scroll();
    };

    var initPageNumDisplay = function () {
        var currentTop = $(document).scrollTop();

        var pageNumber = $("#survey-pages").children("div").length;
        var toleranceHeight = 50;
        $(document)
            .off('scroll')
            .on('scroll', function () {
                currentTop = $(document).scrollTop();
                var currentBottom = currentTop + $(window).height();
                for (var i = 1; i <= pageNumber; i++) {
                    var currentOffset = $("#survey-pages > div:nth-child(" + i + ")").offset();
                    var currentDivTop = currentOffset.top;
                    if (currentDivTop >= currentTop - toleranceHeight) {
                        if (currentDivTop >= currentBottom - ($(window).height()) / 2) {
                            var prev = i - 1;
                            $("#page-select").val(prev);
                        } else {
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
        $("[id^='question-']")
            .off('mouseenter')
            .on('mouseenter', function () {
                var questionId = $(this).attr('id').replace(/[^\d.]/g, '');
                $("#edit-btn-group-" + questionId).css("visibility", "visible");
                $(this).parent().addClass("highlight-frame");
                $(this).parent().removeClass("question-frame");
            })
            .off('mouseleave')
            .on('mouseleave', function () {

                var questionId = $(this).attr('id').replace(/[^\d.]/g, '');
                $("#edit-btn-group-" + questionId).css("visibility", "hidden");
                $(this).parent().addClass("question-frame");
                $(this).parent().removeClass("highlight-frame");
            });
    };

    var initNavbarToolTip = function () {
        // init tooltip of navbar
        $('[data-toggle="tooltip"]').tooltip();
    };
    return {
        init: function () {

            initNavbarToolTip();

            initPageCreateAjax();
            initPageDeleteAjax();
            initPageEditAjax();

            initQuestionCreateAjax();

            initDisplay();

        }
    }
}());
