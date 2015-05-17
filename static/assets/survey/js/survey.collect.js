var surveyCollect = (function () {

    //delete a collector
    var initCollectDelete = function () {
        $(".collect-delete")
            .off('click')
            .on('click', function () {
                var currentrow = $(this).closest("tr");
                //console.log(currentrow)
                var collectid = $(this).attr('id').replace(/[^\d.]/g, '');
                var surveyid = $(this).attr('name').replace(/[^\d.]/g, '');
                //pop out confirmation window
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


    //generate and keep in clipboard a hashed link to current survey that can be shared
    var initCollectShare = function () {
        $(".collect-share").each(function () {
            var client = new ZeroClipboard($(this));
            client.on("ready", function (readyEvent) {
                //bind the function to 'aftercopy' event
                client.on("aftercopy", function (event) {
                    // `this` === `client`
                    // `event.target` === the element that was clicked
                    //event.target.style.display = "none";
                    alert("Copied: " + event.data["text/plain"]);
                });
            });
        });


    };



    return {
        init: function () {
            initCollectDelete();
            initCollectShare();
        }
    }
}());
