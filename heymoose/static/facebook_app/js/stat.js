(function() {

    function dialog(title, text) {
        $(".i-dialog").remove();
        var data = {title: title, text: text};
        var html = Mustache.to_html($("#dialogTemplate").html(), data);
        FB.Canvas.getPageInfo(function(page) {
            var top = Math.max(100, parseInt(page.scrollTop) + parseInt(page.offsetTop));
            $(html).css({top: top}).appendTo(document.body).find(".i-dialog_buttons input").click(function() {
                $(".i-dialog").remove();
            });
        });
    }

    function success(data) {
        dialog("Отлично!", _USER.firstname + ', Ваш друг получил приглашение! <div class="divider mtl mbl"></div><iframe src="http://www.facebook.com/plugins/likebox.php?href=http%3A%2F%2Ffacebook.com%2Fpages%2Fheymoosecom%2F247852878576419&amp;width=475&amp;colorscheme=light&amp;show_faces=true&amp;border_color&amp;stream=true&amp;header=false&amp;height=175" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:475px; height:175px;" allowTransparency="true"></iframe>');
    }

    $(function() {
        $(".b-invite_button").onclick(function(e){
            disableInput();
            FB.ui({method: 'apprequests', message: _USER.firstname + ' Приглашает вас!'}, function(res) {
                enableInput();
                success(data);
            });
        });
    });
})();

/* For ajax form submission */
$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

