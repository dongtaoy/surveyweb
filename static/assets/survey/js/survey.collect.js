

var surveyCollect = (function(){
    var initCollectDelete = function(){
        $(".collect-delete")
            .off('click')
            .on('click', function(){
                var currentrow = $(this).closest("tr");
                console.log(currentrow)
                var collectid = $(this).attr('id').replace(/[^\d.]/g, '');
                var surveyid = $(this).attr('name').replace(/[^\d.]/g, '');
                console.log(surveyid);
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
                                var notify = $.notify('Deleting....');
                                $.post(Django.url('collect.delete', surveyid, collectid))
                                    .success(function (response) {
                                        if (response['status'] == 200) {
                                            currentrow.remove();
                                            notify.close();
                                        } else {
                                            notify.update('type', "danger");
                                            notify.update('message', "Something went wrong.... Please try refreshing your browser.");
                                        }
                                    })
                            }
                        }
                    }
                });
            })
    };

    var initCollectURL = function(){
        $(".collect-show")
            .off('click')
            .on('click', function(){

            })
    }


    return {
        init : function(){
            initCollectDelete();
        }
    }
}());
