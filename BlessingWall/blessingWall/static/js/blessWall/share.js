$(document).ready(function () {

    var base64_imgs;    // 存储图片base64流的数组

    // 读取存储图片的base64流的json文件
    $.getJSON("/static/img/base64_imgs_v2.json", function (data) {
        base64_imgs = data.imgs;
        $("#danmubg").prop("src", base64_imgs[0]);
    })

    // 把留言添加在图片下面的div
    $("#blessContent").text(decodeURI(GetQueryString("bless")));
    $("#blessName").text(decodeURI("——"+GetQueryString("name")));

    // 点击小图显示相应的大图
    $(".img-thumbnail").on("click", function () {
        $("#danmubg").prop("src", base64_imgs[Number($(this).data("id"))]);
        $(".img-thumbnail.active").removeClass("active");
        $(this).addClass("active");
    })

    // 返回祝福墙
    $("#back").on("click", function () {
        location.href = "/index.html";
    })

    // 保存功能
    $("#share").on("click", function () {
        // 截图功能
        html2canvas(document.querySelector("#showArea")).then(canvas => {
            // 有滚轮的时候，截图前需把页面置顶，不然会出现截图会偏移，导致不全
            window.pageYoffset = 0;
            document.documentElement.scrollTop = 0;
            document.body.scrollTop = 0;
            // 截图功能
            html2canvas(document.querySelector("#showArea")).then(canvas => {
                let img_data = canvas.toDataURL();
                let ua = navigator.userAgent.toLowerCase();
                if (ua.match(/MicroMessenger/i) == "micromessenger") {//微信浏览器
                    $("#modalImg").prop("src", img_data);
                    $("#myModal").modal("show");
                } else {
                    // 下载功能
                    setTimeout(function () {
                        let anchor = document.createElement('a');
                        if ('download' in anchor) {
                            anchor.style.visibility = 'hidden';
                            anchor.href = img_data;
                            let fileName = (new Date()).getTime();
                            anchor.download = fileName + ".png";

                            document.body.appendChild(anchor);
                            var evt = document.createEvent('MouseEvents');
                            evt.initEvent('click', true, true);
                            anchor.dispatchEvent(evt);

                            document.body.removeChild(anchor);
                        } else {
                            location.href = img_data;
                        }
                    }, 1000)
                }

                /* 
                //截图成功后分享到朋友圈
                wx.updateTimelineShareData({
                    title: '建党100周年祝福墙', // 分享标题
                    link: '127.0.0.1:5000', // 分享链接
                    imgUrl: img_data, // 分享图标
                    success: function () {
                        // 用户确认分享后执行的回调函数
                        console.log("success");
                    },
                    cancel: function () {
                        // 用户取消分享后执行的回调函数
                        console.log("cancel");
                    },
                    error: function (e) {
                        console.log("error:" + e);
                    }
                });
    
                wx.error(function (res) {
                    alert("ERROR:" + res.errMsg);  //打印错误消息。及把 debug:false,设置为debug:ture就可以直接在网页上看到弹出的错误提示
                });*/
            });
        })

        //微信接口配置
        /*$.when(
            $.ajax({
                type: "POST",
                url: "/signpackage",
                data: JSON.stringify({ url: window.location.href }),
                contentType: "application/json",
                dataType: "json",
                headers: {
                    "X-CSRFToken": getCookie("csrf_token")
                },
                success: function (res) {
                    console.log(res)
                    wx.config({
                        debug: true, // 开启调试模式,调用的所有api的返回值会在客户端alert出来，若要查看传入的参数，可以在pc端打开，参数信息会通过log打出，仅在pc端时才会打印。
                        appId: res.appId, // 必填，公众号的唯一标识
                        timestamp: res.timestamp, // 必填，生成签名的时间戳
                        nonceStr: res.nonceStr, // 必填，生成签名的随机串
                        signature: res.signature,// 必填，签名
                        jsApiList: [
                            'updateAppMessageShareData', //分享给朋友、QQ
                            'updateTimelineShareData', //分享到朋友圈、QQ空间
                        ]
                    });
                }
            })
        ).done(function () {
            console.log("成功配置信息！");
        })*/
    })
})