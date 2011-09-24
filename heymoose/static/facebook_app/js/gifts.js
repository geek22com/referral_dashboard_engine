(function() {

   function getKeys(obj){
            var keys = [];
            for(var key in obj){
                keys.push(key);
                }
                return keys;
            }

    var typeahead,
        birthdays,
        FRIENDS,
        qs = (function(l) {
                var result = {}, queryString = l.substring(1), re = /([^&=]+)=([^&]*)/g, m;
                while (m = re.exec(queryString)) {
                    result[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
                }

                return result;
        })(window.location.search);

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

    function ask(title, text, callback, yes, no) {
        $(".i-dialog").remove();
        var yes = yes || 'Okay';
        var no = no || 'Cancel';
        var data = {title: title, text: text, yes: yes, no: no};
        var html = Mustache.to_html($("#askTemplate").html(), data);
        FB.Canvas.getPageInfo(function(page) {
            var top = Math.max(100, parseInt(page.scrollTop) + parseInt(page.offsetTop));
            $(html).css({top: top}).appendTo(document.body).find(".i-dialog_buttons input.i-silver").click(function() {
                $(".i-dialog").remove();
            }).end().find(".i-yes").click(function() {
                $(".i-dialog").remove();
                if(callback) {
                    callback();
                }
            });
        });
    }

    function reset() {
        typeahead.reset();
        /* Reset gift selector */
        $("b-gift_select__gifts .b-selecter_params__other").click();
        $("textarea[name='message']").val('');
        $("input,textarea,select").prop("disabled", false);
        $("#page_count").show();
        $("select[name='private']").val(0);
        $("#all_friends").hide();
        $("#select_friend").show();
    }
    function success(data) {
        FB.Canvas.scrollTo(0,0);
        if(Math.ceil(Math.random() * 2) == 1) {
            ask("Отлично!", _USER.firstname + ", Ваш подарок отправлен, Хотите рассказать друзьям о HeyMoose?", function() {
                FB.ui({method: 'feed', 'link': 'http://apps.facebook.com/heymoose', picture: 'http://heymoose.com:8080/static/images/logo.png', name: 'Используйте HeyMoose', description: _USER.firstname + " рекомендует HeyMoose в Facebook!"}, 'Okay', 'No Thanks');
            });
        } else {
            dialog("Отлично!", _USER.firstname + ', Ваш подарок отправлен! <div class="divider mtl mbl"></div><iframe src="http://www.facebook.com/plugins/likebox.php?href=http%3A%2F%2Ffacebook.com%2Fpages%2Fheymoosecom%2F247852878576419&amp;width=475&amp;colorscheme=light&amp;show_faces=true&amp;border_color&amp;stream=true&amp;header=false&amp;height=175" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:475px; height:175px;" allowTransparency="true"></iframe>');
        }
    }


    function verify() {
        try {
            var gift = $("input[name='gift']").val();
            return ($("#b-friends_select").val() > 0 && gift);
        } catch(e) { return false; }
    }


    /* Setup Gift Selector */
    $(function() {
        var gifts = $(".b-gift_select__gifts"),
            selector = gifts.find(".b-gift_select__selector"),
            selected = gifts.find(".b-gift_select__selected"),
            title = gifts.find("#gift_title"),
            change = gifts.find(".b-selecter_params__other"),
            gift_id = gifts.find("input[name='gift_id']"),
            value = gifts.find("input[name='gift']"),
            select = function() {
                var data = $(this).data();
                data.src = $(this).attr("src");
                value.val(data.src);
                gift_id.val(data.id);
                var html = Mustache.to_html($("#selectedTemplate").html(), data);
                selector.hide();
                selected.html(html).show();
                gifts.addClass("giftSelected");
            }


        gifts.delegate(".b-gift_select__gift_item", "mouseenter", function() {
            $(this).addClass("hover").stop().siblings().stop().fadeTo("fast", 0.5).end().fadeTo("fast", 1);
            title.text($(this).data("title"));

            /*alert($(this).data("title"));*/
        }).delegate(".b-gift_select__gift_item", "mouseleave", function() {
            $(this).removeClass("hover").siblings().andSelf().stop().fadeTo("fast", 1);
            title.html("&nbsp;");
        }).delegate(".b-gift_select__gift_item", "click", select);

        change.click(function() {
            selector.show();
            selected.html('').hide();
            gifts.removeClass("giftSelected");
            value.val('');
        });
    });


    /* Gift form submit */
    $(function() {
        $("#b-gifts_from__send").submit(function(e) {
            e.preventDefault();
            /* Check if they selected a friend a gift */
            if(!verify()) { dialog("Whoops!", "Выберите друга и подарок!<br />"); return; }

            /* Get the form data */
            var data = $(this).serializeObject();
                data.to_id = $("#b-friends_select").val()

            /* Build the gift params */
            var params = {
                message: data.message,
                name: data.giftName,
                caption: "HeyMoose",
                description: _USER.firstname + "Послал вам подарок",
                picture: data.gift,
                method: "post",
                link: app_domain,
                actions: [{"name":"Самые интересные способы зароботка в сети", "link": "http://apps.facebook.com/heymoose/"}]
            };
            $.post("/facebook_send_gift", data);
            /*And now send via FB api*/
            FB.api(data.to_id + "/feed", params, function(res) {
                    if(res && res.id) {
                        FB.ui({method: 'apprequests', to: data.to_id, message: _USER.firstname + ' Послал вам подарок!'}, function() {
                            success(data);
                        });
                        // auto like?
                        FB.api(res.id + '/likes', {method: 'post'});
                    } else {
                        // fall back to sending a private message if wall posting didn't work
                        FB.ui({
                             method: 'send',
                             to: data.to_id,
                             display: 'iframe',
                             name: data.giftName,
                             link: app_domain,
                             picture: data.gift,
                             description: data.message
                        }, function() {
                            success(data);
                        });
                    }
             });
            /**/
        });
    });

    $(".button").live("mousedown", function() {
        $(this).addClass("downstate");
    }).live("mouseup mouseout", function() {
        $(this).removeClass("downstate");
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
