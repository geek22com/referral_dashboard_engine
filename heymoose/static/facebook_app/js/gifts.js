(function() {
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
        $(".dialog").remove();
        var data = {title: title, text: text};
        var html = Mustache.to_html($("#dialogTemplate").html(), data);
        FB.Canvas.getPageInfo(function(page) {
            var top = Math.max(100, parseInt(page.scrollTop) + parseInt(page.offsetTop));
            $(html).css({top: top}).appendTo(document.body).find(".dialog_buttons input").click(function() {
                $(".dialog").remove();
            });
        });
    }

    function ask(title, text, callback, yes, no) {
        $(".dialog").remove();
        var yes = yes || 'Okay';
        var no = no || 'Cancel';
        var data = {title: title, text: text, yes: yes, no: no};
        var html = Mustache.to_html($("#askTemplate").html(), data);
        FB.Canvas.getPageInfo(function(page) {
            var top = Math.max(100, parseInt(page.scrollTop) + parseInt(page.offsetTop));
            $(html).css({top: top}).appendTo(document.body).find(".dialog_buttons input.silver").click(function() {
                $(".dialog").remove();
            }).end().find(".yes").click(function() {
                $(".dialog").remove();
                if(callback) {
                    callback();
                }
            });
        });
    }

    function reset() {
        typeahead.reset();
        /* Reset gift selector */
        $(".gifts .cancel").click();
        $("textarea[name='message']").val('');
        $("input,textarea,select").prop("disabled", false);
        $("#page_count").show();
        $("select[name='private']").val(0);
        $("#all_friends").hide();
        $("#select_friend").show();
    }



    function verify() {
        try {
            var gift = $("input[name='gift']").val();
            return (($("select[name='private']").val() == 2 && gift) || (typeahead.getValue().match(/^[0-9]+$/) && gift));
        } catch(e) { return false; }
    }


    /* Setup Gift Selector */
    $(function() {
        var gifts = $(".gifts"),
            selector = gifts.find(".selector"),
            selected = gifts.find(".selected"),
            title = gifts.find("#gift_title"),
            change = gifts.find(".cancel"),
            pager = $("#gift_pager"),
            page_count = $("#page_count"),
            gift_id = gifts.find("input[name='gift_id']"),
            value = gifts.find("input[name='gift']"),
            select = function() {
                var data = $(this).data();
                data.src = $(this).attr("src");
                value.val(data.src);
                gift_id.val(data.id);
                var html = Mustache.to_html($("#selectedTemplate").html(), data);
                selector.hide();
                pager.hide();
                selected.html(html).show();
                gifts.addClass("giftSelected");
                page_count.hide();
            }

        gifts.delegate(".gift", "mouseenter", function() {
            $(this).addClass("hover").stop().siblings().stop().fadeTo("fast", 0.5).end().fadeTo("fast", 1);
            title.text($(this).data("title"));
        }).delegate(".gift", "mouseleave", function() {
            $(this).removeClass("hover").siblings().andSelf().stop().fadeTo("fast", 1);
            title.html("&nbsp;");
        }).delegate(".gift", "click", select);

        change.click(function() {
            selector.show();
            selected.html('').hide();
            gifts.removeClass("giftSelected");
            value.val('');
            pager.show();
            page_count.show();
        });
    });



    /* Pre select a person */
    $(".person").live("click", function() {
        var person = $(this).data();
        typeahead.set(person);
        $(".dialog").hide();
        if($("select[name='private']").val() == 2) {
            $("select[name='private']").val(0);
            $("#all_friends").hide();
            $("#select_friend").show();
        }
    });

    $(function() {
        var type = $("select[name='private']").change(function() {
            if(type.val() == 2) {
                $("#all_friends").show();
                $("#select_friend").hide();
            } else {
                $("#all_friends").hide();
                $("#select_friend").show();
            }
        });
    });

    /* Gift form submit */
    $(function() {
        $("#send").submit(function(e) {
            e.preventDefault();
            /* Check if they selected a friend a gift */
            if(!verify()) { dialog("Whoops!", "Выберите друга и подарок!<br />"); return; }

            /* Get the form data */
            var data = $(this).serializeObject();
                data.private = parseInt(data.private);
                data.giftName = $("#gt").text();

            /* Build the gift params */
            var params = {
                message: data.message,
                name: data.giftName,
                caption: "Free Gifts",
                description: _USER.first_name + " sent you a gift. Click 'like' to show your appreciation!",
                picture: data.gift,
                method: "post",
                link: app_url,
                actions: [{"name":"Send a Gift", "link": ""}]
            };

            /* Disable the form */
            $("input,textarea,select").prop("disabled", true);

            /* Enable the form */
            $("input,textarea,select").prop("disabled", false);
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
