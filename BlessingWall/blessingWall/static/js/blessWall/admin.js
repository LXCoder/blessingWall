var _state, _page;

$(document).ready(function () {
    // 获取链接中的参数
    _state = GetQueryString("state");
    _page = GetQueryString("page");

    if (!_state) {
        _state = 0;
    }

    // 高亮
    if (_state == "1") {
        $("#passed").addClass("active");
    } else if (_state == "2") {
        $("#blocked").addClass("active");
    } else {
        $("#pending").addClass("active");
    }

    $('[data-toggle="tooltip"]').tooltip();

    // 显示祝福语
    unpdateBlessData(_state, _page);
});

// 全选
function checkAll(obj) {
    let checked = $("#" + obj.id).prop('checked');
    $('.itemChecked').each(function () {
        $(this).prop('checked', checked);
    })
}

// 获得选中的复选框id
function getCheckedIds(){
    let ids = [];
    // 获取复选框选中的id
    $('.itemChecked').each(function () {
        if ($(this).prop('checked')) {
            ids.push(Number($(this).val()));
        }
    })
    return ids;
}

// 显示祝福语列表
function unpdateBlessData(state, page) {

    params = {
        state: state,
        page: page
    }

    $.get("/blesses", params, function (resp) {
        if ("4101" == resp.errno) {
            location.href = "/login.html";
        } else if ("0" == resp.errno) {
            if (0 == resp.data.total_page) {
                $(".container-fluid").html("暂时没有符合您查询的信息。");
            } else {
                $(".container-fluid").html(template("bless_list_tmpl", { data: resp.data }));
            }
        } else {
            alert(resp.errmsg)
        }
    }, "json")
}

// 更改祝福语状态
function passOrBlock(obj) {
    let state = $("#" + obj.id).data("type");
    let ids = getCheckedIds();// 获取复选框选中的id
    
    if (ids.length == 0) return;

    let req_data = {
        state: state,
        ids: ids
    };

    let req_json = JSON.stringify(req_data);

    // 发送请求
    $.ajax({
        url: "/blesses",
        type: "PUT",
        data: req_json,
        contentType: "application/json",
        dataType: "json",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        }, // 请求头，将csrf_token值放到请求中，方便后端csrf进行验证
        success: function (resp) {
            if (resp.errno == "0") {
                unpdateBlessData(_state, 1);//更改成功，更新列表
            } else if (resp.errno == "4101") {
                location.href = "/login.html";
            } else {
                alert(resp.errmsg)
            }
        }
    });
}

// 删除祝福语
function deleteBless(){
    let ids = getCheckedIds();
    
    if(ids.length == 0) return;

    let req_data = {
        ids: ids
    };

    let req_json = JSON.stringify(req_data);

    // 发送请求
    $.ajax({
        url: "/blesses",
        type: "delete",
        data: req_json,
        contentType: "application/json",
        dataType: "json",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        }, // 请求头，将csrf_token值放到请求中，方便后端csrf进行验证
        success: function (resp) {
            if (resp.errno == "0") {
                unpdateBlessData(_state, 1);//删除成功，更新列表
            } else if (resp.errno == "4101") {
                location.href = "/login.html";
            } else {
                alert(resp.errmsg)
            }
        }
    });
}

// 退出系统
$("#logout").on("click", function () {
    $.ajax({
        url: "/session",
        type: "delete",
        headers: {
            "X-CSRFToken": getCookie("csrf_token")
        },
        dataType: "json",
        success: function (resp) {
            if (resp.errno == "0") {
                // 退出成功，跳转到登陆页面
                location.href = "/login.html";
            } else {
                alert(resp.errmsg);
            }
        }
    })
});