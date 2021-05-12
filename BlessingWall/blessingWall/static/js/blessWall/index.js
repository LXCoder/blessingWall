$(document).ready(function () {
    //显示限制输入字符method
    $("#comment").on("keyup", function () {
        $("#word_nums").html($(this).val().length);
    })

    $("#comment").on("focus", function () {
        $("#err_msg").hide();
        let str = $(this).val()
        $(this).next().children('em').text(str.length);
    })

    $("#comment").on("blur", function () {
        let str = $(this).val()
        $(this).next().children('em').text(str.length);
    })

    // 为表单的提交补充自定义的函数行为 （提交事件e）
    $(".blessing_form").submit(function (e) {
        // 阻止浏览器对于表单的默认自动提交行为
        e.preventDefault();

        let name = $("#name").val().trim();
        let banji = $("#banji").val().trim();
        let comment = $("#comment").val().trim();
        if (!comment) {
            $("#comment").val("");
            $("#err_msg").text("祝福不能为空");
            $("#err_msg").show();
            return;
        }

        // 调用ajax向后端发送注册请求
        let req_data = {
            name: name,
            banji: banji,
            comment: comment
        };
        let req_json = JSON.stringify(req_data);


        $.ajax({
            url: "/blessing",
            type: "post",
            data: req_json,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            }, // 请求头，将csrf_token值放到请求中，方便后端csrf进行验证
            success: function (resp) {
                if (resp.errno == "0") {
                    // 注册成功，跳转到分享页
                    location.href = "/share.html?bless=" + encodeURI(encodeURI(comment));
                } else {
                    $("#err_msg").text(resp.errmsg);
                    $("#err_msg").show();
                    alert(resp.errmsg);
                }
            }
        })

    });
})