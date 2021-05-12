$(document).ready(function () {

    $("#username").focus(function () {
        $("#lmsgSubmit").hide();
    });

    $("#password").focus(function () {
        $("#lmsgSubmit").hide();
    });

    // 为表单的提交补充自定义的函数行为 （提交事件e）
    $("#logInForm").submit(function (e) {
        // 阻止浏览器对于表单的默认自动提交行为
        e.preventDefault();
        let username = $("#username").val()
        let password = $("#password").val()

        if (!username || !password) {
            $("#username").val("");
            $("#password").val("");
            $("#lmsgSubmit").text("用户名或密码不能为空");
            $("#lmsgSubmit").show();
            return;
        }

        // 调用ajax向后端发送注册请求
        let req_data = {
            username: username,
            password: password
        };
        let req_json = JSON.stringify(req_data);

        $.ajax({
            url: "/sessions",
            type: "post",
            data: req_json,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            }, // 请求头，将csrf_token值放到请求中，方便后端csrf进行验证
            success: function (resp) {
                if (resp.errno == "0") {
                    // 登陆成功，跳转到分享业
                    location.href = "/admin.html";
                } else {
                    $("#username").val("");
                    $("#password").val("");
                    $("#lmsgSubmit").text(resp.errmsg);
                    $("#lmsgSubmit").show();
                }
            }
        })

    });
})