
UP = function (o, success, error, upload_func) {
	if (typeof success == 'function') {
		var file = new FormData();
		file.append("file", o);
		// file=o;
	}
	else {
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
	x.setRequestHeader("X-Requested-With", "XMLHttpRequest");
	x.send(file);

}
