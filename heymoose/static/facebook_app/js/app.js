//additional properties for jQuery object
$(document).ready(function(){
   //align element in the middle of the screen
   $.fn.alignCenter = function() {
      //get margin left
      var marginLeft =  - $(this).width()/2 + 'px';
      //get margin top
      var marginTop =  - $(this).height()/2 + 'px';
      //return updated element
      return $(this).css({'margin-left':marginLeft, 'margin-top':marginTop});
   };
   $.fn.togglePopup = function(){
     //detect whether popup is visible or not
     if($('#popup').hasClass('hidden'))
     {
       //hidden - then display
       //when IE - fade immediately
       if($.browser.msie)
       {
         $('#opaco').height($(document).height()).toggleClass('hidden')
                    .click(function(){$(this).togglePopup();});
       }
       else
       //in all the rest browsers - fade slowly
       {
         $('#opaco').height($(document).height()).toggleClass('hidden').fadeTo('slow', 0.7)
                    .click(function(){$(this).togglePopup();});
       }
       $('#popup')
         .html($(this).html())
         .alignCenter()
         .toggleClass('hidden');
     }
     else
     {
       //visible - then hide
       $('#opaco').toggleClass('hidden').removeAttr('style').unbind('click');
       $('#popup').toggleClass('hidden');
     }
   };
});

function load_stat(){
    var tmpl = "stat";
    var url = "http://heymoose.com:8080/facebook_tmpl/" + tmpl;
    $('.b-main-content').load(url);
}

function load_faq(){
    var tmpl = "faq";
    var url = "http://heymoose.com:8080/facebook_tmpl/" + tmpl;
    $('.b-main-content').load(url);
}

function load_help(){
    var tmpl = "help";
    var url = "http://heymoose.com:8080/facebook_tmpl/" + tmpl;
    $('.b-main-content').load(url);
}

function load_about(){
    var tmpl = "about";
    var url = "http://heymoose.com:8080/facebook_tmpl/" + tmpl;
    $('.b-main-content').load(url);
}

function load_gifts(){
    var tmpl = "gifts";
    var url = "http://heymoose.com:8080/facebook_tmpl/" + tmpl;
    $('.b-main-content').load(url);
}

function load_offers(){
	var app_id = $('#happ_app_id').attr('value');
	var sig = $('#happ_sig').attr('value');
	//var data = "app_id=" + app_id + "&sig=" + sig;
    var data = {'app_id' : app_id, 'sig' : sig};
    var url = "http://heymoose.com:8080/get_offers";
/*	$.ajax({
		type: "POST",		
		url: url,
		data : data,
		context: document.body,
		success: function(msg){
			$('#offer_list').append(msg);
			// Add user_id to template
			$('.user_id').each(function(){
				$(this).attr('value', $('#happ_user_id').attr('value'));
			})

		},
		error: function(){ 
			$('#offer_list').append("Извините, нет доступных предложений. Попробуйте позже");
		}
	});*/
    $('.b-main-content').load(url, data);
}


