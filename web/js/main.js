function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
};


function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
};


function uploadFile(f, success, error, upload_func, uploadWay) {
    if (typeof success == 'function') {
        var file = new FormData();
        file.append("file", f);
        file.append("uploadWay", uploadWay);
        // file=o;
    } else {
        console.log('js错误')
    }

    x = new XMLHttpRequest();

    x.onload = function (r) {
        r = JSON.parse(x.responseText);
        return success(r)
    }

    x.upload.onprogress = function (e) {
        upload_func(e.loaded / e.total)
    } // 注册位置需要在 open send 之前， 同时需要异步

    x.open('POST', '/api/upload', true);
    // x.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    x.send(file);

}


//自定义弹框
function Toast(msg, duration) {
    duration = isNaN(duration) ? 3000 : duration;
    var m = document.createElement('div');
    m.innerHTML = msg;
    m.style.cssText = "width: 60%;min-width: 150px;opacity: 0.7;height: 40px;color: rgb(255, 255, 255);line-height: 40px;text-align: center;border-radius: 5px;position: fixed;top: 40%;left: 20%;z-index: 999999;background: rgb(0, 0, 0);font-size: 13px;";
    document.body.appendChild(m);
    setTimeout(function () {
        var d = 0.5;
        m.style.webkitTransition = '-webkit-transform ' + d + 's ease-in, opacity ' + d + 's ease-in';
        m.style.opacity = '0';
        setTimeout(function () {
            document.body.removeChild(m)
        }, d * 1000);
    }, duration);
};


$(function () {
    // $.ajaxSettings.async = false; // 取消异步
    var paste_image = null;

    // 刷新设置上次的选中作为默认选中
    uploadWay_last_check = getCookie('uploadWay');
    if (uploadWay_last_check) {
        $('#upLoadway').val(uploadWay_last_check);
    }
    ;

    // 更新本地的way状态
    $("#upLoadway").change(function () {
        uploadWay = $("#upLoadway option:selected").val().trim();
        setCookie('uploadWay', uploadWay, 365 * 10);
    })

    function upload_success(response) {
        Toast(response.msg)
        var url = response.url
        if (response.code === 0) {
            show_image.src = url;
            link.href = url;
            inner_content = '<div class="desc">' +
                '<span class="desc1" id="info"><h4>以下是分别是 原始、UBB 和 MD 链接：</h4></span>' +
                '<div class="input_box">' +
                '<input type="text" class="in" id="url_1" readonly="true" data-clipboard-target="p" onfocus="this.select()" value=' + url + ' />' +
                '<button class="btn" data-clipboard-action="copy" data-clipboard-target="#url_1">复制</button>' +
                '</div>' +
                '<div class="input_box">' +
                '<input type="text" class="in" id="url_2" readonly="true" data-clipboard-target="p" onfocus="this.select()" value=' + '[img]' + url + '[/img] />' +
                '<button class="btn" data-clipboard-action="copy" data-clipboard-target="#url_2">复制</button>' +
                '</div>' +
                '<div class="input_box">' +
                '<input type="text" class="in" id="url_3" readonly="true" data-clipboard-target="p" onfocus="this.select()" value=' + '![image](' + url + ') />' +
                '<button class="btn" data-clipboard-action="copy" data-clipboard-target="#url_3">复制</button>' +
                '</div>';
            $('.inner_html').html(inner_content);
        } else {
            inner_content = '<br/>'
            $('#show_image').attr("src", '');
            $('.inner_html').html('<div class="desc1">上传失败：' + response.msg);
            Toast(response.msg, 3000)
        }
    };

    function upload_error() {
        Toast('上传文件出错了！')
    };

    function uploading(process) {
        $('.inner_html').html('<div class="desc1">上传进度为：' + (process * 99).toFixed(2) + ' %');
        $('#show_image').load(function () {
            window.location.href = '#info';
        })
    };

    //  将粘贴事件绑定到 document 上
    document.addEventListener("paste", function (e) {
        var items = event.clipboardData && event.clipboardData.items;
        var file = null;
        if (items && items.length) {
            // 检索剪切板items中类型带有image的
            for (var i = 0; i < items.length; i++) {
                if (items[i].type.indexOf('image') !== -1) { // 或者 items[i].type.indexOf('image') !== -1
                    file = items[i].getAsFile(); // 此时file就是剪切板中的图片文件
                    break;
                }
            }
        }
        ;
        // console.log(file);
        if (file) {
            render_paste_image(file);
        } else {
            Toast('从剪贴板中没有找到图片!');
        }
        ;

    }, false);

    // 提供剪贴板预览
    function render_paste_image(file) {
        var reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = function (e) {
            var confirm_upload_button = '<button id="paste_upload_button" class="btn" style="float:right; margin-right: 20px; margin-top: 5px; margin-bottom: 5px;">确定上传</button>';
            $('.inner_html').html(confirm_upload_button);
            $('#show_image').attr("src", e.target.result);
            paste_image = file;  // 赋值给全局变量
        }
    };

    // 点击确定上传按钮(动态元素绑定事件),
    // 使用下面的注册失败，要先绑定在body上
    // $('#paste_upload_button').on('click', function () {
    $('body').on('click', '#paste_upload_button', function () {
        if (paste_image) {
            //  上传
            uploadWay = $("#upLoadway option:selected").val().trim();
            uploadFile(paste_image, upload_success, upload_error, uploading, uploadWay);
        }
    });

    $('.upload_area').click(function () {
        $('.file_upload').click();
    })

    $('.file_upload').change(function () {
        if (!this.files || !this.files[0])
            return alert('删除成功！或选取文件出错！')
        var this_image_file = this.files[0]
        if (this_image_file.type.indexOf('image') != 0)
            return alert('这不是一个图像或音频！')
        //  上传
        uploadWay = $("#upLoadway option:selected").val().trim();
        uploadFile(this_image_file, upload_success, upload_error, uploading, uploadWay);
    });

    var clipboard = new ClipboardJS('.btn');
    clipboard.on('success', function (e) {
        Toast("已成功复制剪贴板！", 1500);
    });
    clipboard.on('error', function (e) {
        Toast("复制失败，请手动选择进行复制!", 1500);
    });
});