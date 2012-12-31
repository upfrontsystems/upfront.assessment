$(function() {

    $(document).ready(function() {
        // upon load, show the ratings
        $('table.rating .answer_red').each(function(index,answer) {
            var selected = $(answer).attr('selected_answer_red');
            if (selected == 'True') {
                $(this).addClass('selected');
            }
        });
        $('table.rating .answer').each(function(index,answer) {
            var selected = $(answer).attr('selected_answer');
            if (selected == 'True') {
                $(this).addClass('selected');
            }
        });
    });

    // evaluation view - rating buttons click handlers
    $("td.answer").live("click", function() {
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');
        var value = $(this).attr('value');
        $(this).siblings('input').attr('value',value);
    });

    $("td.answer_red").live("click", function() {
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');
        var value = $(this).attr('value');
        $(this).siblings('input').attr('value',value);
    });

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

    var activity = $('.activity-container .item-actions-left\
        .remove-from-assessment[value='+data.remove_id+']').parent().parent()

    // check if this is the only activity in the list
    if (( activity.next().size() == 0 ) && ( activity.prev().size() == 0 )) {
        // do nothing
    }
    else {  
      
        // if you are about to remove last activity from list        
        if ( activity.next().size() == 0 ) {
            // make sure the new last, doesnt have move-down link
            activity.prev().find('a.move-down').remove()
        }
        // if you are about to remove first activity from list        
        if ( activity.prev().size() == 0 ) {
            // make sure the new first, doesnt have move-up link
            activity.next().find('a.move-up').remove()
        }
    }

    // remove assessment item
    activity.remove()

    showStatusMessage(data);
}

function updateAssessmentPostMoveUp(data) {

    var activity = $('.activity-container .item-actions-left\
        .remove-from-assessment[value=' + data.id + ']').parent().parent()

    // if moving up from last position
    if ( activity.next().size() == 0 ) {

        // activity moving up needs a move-down link
        var html ='<a id='+'"'+data.id+'"'+'class="move-down">Move down</a>'
        $(html).insertAfter(activity.find('a.move-up'))

        // do edge case check for when there are only two activities
        if ( activity.prev().prev().size() == 0 ) {            
            // the activity that will be last needs move-up link
            activity.prev().find('a.move-down').removeClass("move-down")
                    .addClass("move-up").html("Move up")
        }
        else {
            // remove move-down link from activity that will be in last place
            activity.prev().find('a.move-down').remove()
        }
    
    }

    // if moving up into first position, remove move-up link
    if ( activity.prev().prev().size() == 0 ) {
        activity.find('a.move-up').remove()

        // activity that is being moved-down from first needs a moveup link
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

        // activity moving down needs a move-up link
        var html ='<a id='+'"'+data.id+'"'+'class="move-up">Move up</a>'
        $(html).insertBefore(activity.find('a.move-down'))

        // do edge case check for when there are only two activities
        if ( activity.next().next().size() == 0 ) {            
            // the activity that will be first needs move-down link
            activity.next().find('a.move-up').removeClass("move-up")
                    .addClass("move-down").html("Move down")
        }
        else {
            // remove move-up link from activity that will be in first place
            activity.next().find('a.move-up').remove()
        }
    }

    // if moving down into last position, remove move-down link
    if ( activity.next().next().size() == 0 ) {
        activity.find('a.move-down').remove()

        // activity that is being moved-up from last needs a movedown link
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
