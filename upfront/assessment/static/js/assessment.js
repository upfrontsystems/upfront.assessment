$(function() {

    $(".remove-from-assessment").live("click", function() {

        clearErrors();
        var remove_id = $(this).attr('value')
        $.ajax({
            url: '@@remove-assessmentitem',
            data: {
                'remove_id': remove_id
            },
            dataType: "json",
            success: updateAssessmentPostRemove,
            error: displayError,
        });
    });

});

function updateAssessmentPostRemove(data) {

    // delete the assessment item
    var remove_id = data.remove_id
    console.log(remove_id)
    $('.activity-container .item-actions-left .remove-from-assessment[value=' + 
      remove_id + ']').parent().parent().remove()

    showStatusMessage(data);
}
   
function displayError(data) {
    var data = {'status' : 'error', 'msg' : 'ajax error'}
    showStatusMessage(data);
}

function clearErrors() {
    $('.portalMessage').removeClass('info error').hide()
    // if there were more than one error boxes active, remove all but 1st one.
    $('#content').find(".portalMessage:gt(0)").remove()
}

function showStatusMessage(data) {
    $('.portalMessage').addClass(data.status)
    var msg = data.status.charAt(0).toUpperCase() + data.status.slice(1)
    $('.portalMessage dt').html(msg)
    $('.portalMessage dd').html(data.msg)
    $('.portalMessage').show()    
}
