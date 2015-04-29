/**
 * Created by GC-Mac on 28/04/15.
 */


var surveyBuilder = (function () {

    var surveyId;

    var initTooltip = function () {
        $('[data-toggle="tooltip"]').tooltip();
    };

    var initNavbarMouseover = function () {
        $(".nav-pills li")
            .mouseover(function () {
                //alert($(this).html());
                $(this).find("span").attr("class", "icon-plus pull-right add");
            })
            .mouseout(function () {
                $(this).find("span").attr("class", "");
            })
    };

    var initPageCreateFormAjax = function () {
        $('.pageCreateForm')
            .off('submit')
            .on('submit', function () {
                $(this).ajaxSubmit({
                    success: function (response) {
                        $(response).insertBefore('.pageCreateForm');
                        initPageDeleteFormAjax();
                    }
                });
                return false
            });
    };

    var initPageDeleteFormAjax = function () {
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
                                $.post(Django.url('page.delete', surveyId, pageId), function (response) {
                                    // if successfully deleted a page
                                    if (response['content']) {
                                        // loop all the portlet that is after current, change the title
                                        pagePortlet.nextAll('.portlet').each(function () {
                                            $(this).find('.caption-subject.bold.uppercase').text("page " + (pageOrder++));
                                        });
                                        // remove the current portlet
                                        pagePortlet.remove();
                                    }
                                });
                            }
                        }
                    }
                })
            });
    };


    return {
        init: function (id) {

            surveyId = id;

            initTooltip();
            initNavbarMouseover();

            initPageCreateFormAjax();
            initPageDeleteFormAjax();
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
