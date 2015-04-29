/**
 * Created by GC-Mac on 28/04/15.
 */
jQuery(document).ready(function () {
    $('.wysihtml5').wysihtml5();


    $("#image-edit-upload").dropzone({dictDefaultMessage: "Please drag your images and drop into these area :)"});

    $("#elo-edit-upload").dropzone({dictDefaultMessage: "Please drag your images and drop into these area :)"});

    $(".nav-pills li")
        .mouseover(function () {
            //alert($(this).html());
            $(this).find("span").attr("class", "icon-plus pull-right add");
        })
        .mouseout(function () {
            $(this).find("span").attr("class", "");
        })
        .click(function (){
            $(".pageBody").append('{% include "survey/builder/question/elo-edit.html" %}');
        });

    $('[data-toggle="tooltip"]').tooltip();

    //$('form').ajaxForm();

    $('.pageCreateForm').submit(function(){
        $(this).ajaxSubmit({
            success: function(response){
                $('.portlet.light').last().after(response);
            }
        });

        return false
    })
});

var radioCount = 1, checkboxCount = 1, selectCount = 1;

function radioAdd(element) {
    var container = $(element);
    radioCount++;
    container.append('\
                    <div class="input-group " style="margin:2px 0"> \
                        <span class="input-group-addon count">' + radioCount + '.</span> \
                        <div class="input-group-control"> \
                            <input type="text" class="form-control" placeholder="Choice"> \
                        </div> \
                        <span class="input-group-btn btn-right actions"> \
                            <button class="btn blue-madison"  onclick="radioRemove(this)" type="button"><i class="fa fa-minus fa-fw"></i>Remove \
                            </button> \
                        </span> \
                    </div> \
                    ');
}

function radioRemove(element) {
    var container = $(element).parent().parent();
    radioCount--;
    container.remove();
    for (var i = 1; i <= radioCount; i++) {
        $(".radioAddChoice > .form-group > div:nth-child(" + i + ") > .count").html(i + ".");
    }
}

var stockArea = $('.col-md-12.column.sortable').droppable({
    drop: function (event, ui) {
        var target = $(event.target);

        //alert($('#accordion1_$'));
        //var app = document.getElementById()
        //rebindDraggables();
        var droppedItem = ui.draggable.prop('tagName').toLowerCase();
        //var droppedItem = ui.draggable.attr('class').toLowerCase();

        var droppedType = ui.draggable.attr('id');
        if (droppedItem == 'li') {
            //alert(droppedType);
            //alert(1);
            var count = $('.portlet').length + 1;
            //alert(count);
            //alert(("<div class=\"panel panel-default\"><div class=\"panel-heading\"><h4 class=\"panel-title\"><a class=\"accordion-toggle\" data-toggle=\"collapse\" data-parent=\"#accordion1\" href=\"$id$count\">$id</a></h4></div><div id=\"$id$count\" class=\"panel-collapse collapse\"><div class=\"panel-body\">$id $count</div></div></div>").replace('$id', droppedType));
            $.ajax({
                url: "{% static 'singletext-edit.html' %}",
                success: function (data) {
                    target.append(data);
                },
                dataType: 'html'
            });
            //target.append("<div class=\"panel panel-default\"><div class=\"panel-heading\"><h4 class=\"panel-title\"><a class=\"accordion-toggle\" data-toggle=\"collapse\" data-parent=\"#accordion1\" href=\"#" + droppedType + count + "\">" + count + ". " + droppedType + "</a></h4></div><div id=\"" + droppedType + count + "\" class=\"panel-collapse collapse\" aria-expanded=\"false\"><div class=\"panel-body\">" + droppedType + count + "<p>This is just for Test Purpose</p></div></div></div>");
        }
    }
});
