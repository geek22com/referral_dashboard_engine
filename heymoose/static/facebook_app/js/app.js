function getKeys(obj){
         var keys = [];
         for(var key in obj){
             keys.push(key);
             }
             return keys;
};

function disableInput(){
    $(".i-button").attr('disabled', true);
    $(".i-input").attr('disabled', true);
}

function enableInput(){
    $('.i-button').removeAttr('disabled');
    $('.i-input').removeAttr('disabled');
}


// $.load reimplement complete so we need success and error,
// for all other we can use complete
$.ajaxSetup({
  beforeSend: function(){
      disableInput();
  },
  complete:function() {
      enableInput();
  },
  success: function() {
      enableInput();
  },
  error: function() {
      enableInput();
  }
});

function load_stat(){
    var tmpl = "stat";
    var url = app_domain + "/facebook_tmpl/" + tmpl;
    $('.b-maincontent').load(url);
}

function load_faq(){
    var tmpl = "faq";
    var url = app_domain + "/facebook_tmpl/" + tmpl;
    $('.b-maincontent').load(url);
}

function load_help(){
    var tmpl = "help";
    var url = app_domain + "/facebook_tmpl/" + tmpl;
    $('.b-maincontent').load(url);
}

function load_about(){
    var tmpl = "about";
    var url = app_domain + "/facebook_tmpl/" + tmpl;
    $('.b-maincontent').load(url);
}

function load_gifts(){
    var tmpl = "gifts";
    var url = app_domain + "/facebook_tmpl/" + tmpl;
    $('.b-maincontent').load(url);
}

function load_offers(){
/*    var url = "http://heymoose.com:8080/get_offers";
    $('.b-maincontent').load(url);*/
    var params = {
        app : heymoose_app_id,
        extId : _USER.uid,
        sig : heymoose_app_sig
    };
    var tmpl = "offers";
    var url = app_domain + "/rest_api/" + tmpl;
    url += "?" + $.param(params)

/*    var url = app_domain + "/facebook_tmpl/" + tmpl;
    $('.b-maincontent').load(url);*/
}


