$(document).ready(function(){

  $(".detail").hide(); 

  // clicks for touch interface
  $('div.vevent > header')
    .live('click', function() {
      $(this)
        .parent()
        .children(".detail")
        .slideToggle(300, Techism.Map.renderEventDetailMap);
    });

  // infinite scrolling
  $('#content').infinitescroll({
    navSelector  : ".next",  // selector for the paged navigation (it will be hidden)
    nextSelector : ".next",  // selector for the NEXT link (to page 2)
    itemSelector : ".vevent", // selector for all items you'll retrieve
    errorCallback: function(){ $('#infscr-loading').remove() }
    },function(arrayOfNewElems){
      // hide all event details
      $(".detail").hide();

      // add ajax click handler to more link
      var pagina = arrayOfNewElems[arrayOfNewElems.length - 1];

      // add click handler or remove pagina when there is no next page
      var next = $('.next', pagina);
      if (next.length > 0){
        next.bind('click', moreHandler);
      }
  });

  function moreHandler(e){
    e.preventDefault();

    // remove old pagina
    $(this).parent().parent().parent().remove();

    $(document).trigger('retrieve.infscr');
  }

  // kill scroll binding
  $(window).unbind('.infscr');

  // hook up the manual click guy.
  $('.next').bind('click', moreHandler);

  // highlight current day and selected month/day in calendar
  var today = new Date();
  var todayUrl = '/events/'+today.getFullYear()+'/'+(today.getMonth()+1)+'/'+today.getDate()+'/';
  $('#calendar a').each(function() {
    var isToday = $(this).attr('href').indexOf(todayUrl) != -1;
    if ($(this).attr('href') == document.location.pathname) {
      if(isToday) {
        $(this).addClass('today_selected');
      }
      else {
        $(this).addClass('selected');
      }
    }
    else if(isToday) {
      $(this).addClass('today');
    }
  });
});
