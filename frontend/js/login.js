(function($){
  $.fn.uxmessage = function(kind, text, max_length) {
    if (max_length == null) {
      max_length = 100;
    }

    if (text.length > max_length) {
      text = text.slice(0,max_length) + '\n...'
    }

    text = text.replace(/\n/g,'<br>')
    
    if (kind == 'notice') {
      $('#log_content').prepend('<div class="log_item log_notice well" style="display:none">' + text + '</div>');
      $('#log_content').children('div').first().show('blind');
      if ($("#log_content").is(':hidden')) {
        $().toastmessage('showNoticeToast', text);
      }
    } else if (kind == 'success') {
      $('#log_content').prepend('<div class="log_item log_success well" style="display:none">' + text + '</div>');
      $('#log_content').children('div').first().show('blind');
      if ($("#log_content").is(':hidden')) {
        $().toastmessage('showSuccessToast', text);   
      }
    } else if (kind == 'warning') {
      $('#log_content').prepend('<div class="log_item log_warning well" style="display:none">' + text + '</div>');
      $('#log_content').children('div').first().show('blind');
      if ($("#log_content").is(':hidden')) {
        $().toastmessage('showWarningToast', text);   
      }
    } else if (kind == 'error') {
      $('#log_content').prepend('<div class="log_item log_error well" style="display:none">' + text + '</div>');
      $('#log_content').children('div').first().show('blind');
      if ($("#log_content").is(':hidden')) {
        $().toastmessage('showErrorToast', text);   
      }
    }

    while ($('#log_content').children('div').length > 200) {
      $('#log_content').children('div').last().remove();
    }

  };
})(jQuery); 

function query_rfid() {
  console.log('query_rfid');
    $.getJSON('/rfid', function (data) {
        if (!data.user)
        {
            // No card present
            $('#dialogText').html('Please insert your card or keyfob');
            setTimeout(function() {query_rfid()}, 4000);
            return;
        }
        console.log('query_rfid: success: '+data.user+': '+data.approved);
        $().uxmessage('notice', 'Card inserted: '+data.user);
        if (!data.approved)
        {
            $('#dialogText').html('<b>You are not authorized to use this equipment</b>');
            setTimeout(function() {query_rfid()}, 4000);
            return;
        }
        $('#dialogText').html('Welcome, '+data.user);
        window.location.href = 'main.html'
    }).error(function (jqxhr, textStatus, error) {
        console.log('query_rfid: error: '+error);
        $().uxmessage('error', 'Timeout');
        setTimeout(function() {query_rfid()}, 8000);
    });
}


$(document).ready(function(){
    console.log('login.js: ready');
    $().uxmessage('notice', "Ready for login.");

    setTimeout(function() {query_rfid()}, 1000);

  
});  // ready

