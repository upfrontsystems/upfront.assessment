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

    $(".move-up").live("click", function() {

        clearErrors();
        var id = $(this).attr('id')
        $.ajax({
            url: '@@move-up-assessmentitem',
            data: {
                'id': id
            },
            dataType: "json",
            success: updateAssessmentPostMoveUp,
            error: displayError,
        });
    });

    $(".move-down").live("click", function() {

        clearErrors();
        var id = $(this).attr('id')
        $.ajax({
            url: '@@move-down-assessmentitem',
            data: {
                'id': id
            },
            dataType: "json",
            success: updateAssessmentPostMoveDown,
            error: displayError,
        });
    });

});

function updateAssessmentPostRemove(data) {

    // delete the assessment item
    var remove_id = data.remove_id
    $('.activity-container .item-actions-left .remove-from-assessment[value=' + 
      remove_id + ']').parent().parent().remove()

    showStatusMessage(data);
}

function updateAssessmentPostMoveUp(data) {

    var activity = $('.activity-container .item-actions-left\
        .remove-from-assessment[value=' + data.id + ']').parent().parent()

    // if moving up from last position
    if ( activity.next().size() == 0 ) {

        //activity moving up needs a move-down link
        var html ='<a id='+'"'+data.id+'"'+'class="move-down">Move down</a>'
        $(html).insertAfter(activity.find('a.move-up'))

        //remove move-down link from activity that will be in last place
        activity.prev().find('a.move-down').remove()
    }

    // if moving up into first position, remove move-up link
    if ( activity.prev().prev().size() == 0 ) {
        activity.find('a.move-up').remove()

        //activity that is being moved-down from first needs a moveup link
        var id = activity.prev().find('a.move-down').attr('id')
        var html ='<a id='+'"'+id+'"'+'class="move-up">Move up</a>'
        $(html).insertBefore(activity.prev().find('a.move-down'))
    }

    // move up
    activity.insertBefore(activity.prev())
}

function updateAssessmentPostMoveDown(data) {

    var activity = $('.activity-container .item-actions-left\
        .remove-from-assessment[value=' + data.id + ']').parent().parent()

    // if moving down from first position
    if ( activity.prev().size() == 0 ) {

        //activity moving down needs a move-up link
        var html ='<a id='+'"'+data.id+'"'+'class="move-up">Move up</a>'
        $(html).insertBefore(activity.find('a.move-down'))

        //remove move-up link from activity that will be in first place
        activity.next().find('a.move-up').remove()
    }

    // if moving down into last position, remove move-down link
    if ( activity.next().next().size() == 0 ) {
        activity.find('a.move-down').remove()

        //activity that is being moved-up from last needs a movedown link
        var id = activity.next().find('a.move-up').attr('id')
        var html ='<a id='+'"'+id+'"'+'class="move-down">Move down</a>'
        $(html).insertAfter(activity.next().find('a.move-up'))
    }

    // move down
    activity.insertAfter(activity.next())
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
