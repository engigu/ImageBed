
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
	x.open('POST', '/api/upload', false);
	x.setRequestHeader("X-Requested-With", "XMLHttpRequest");

	// if (upload) {
	// 	console.log('progress!!!');
	// 	x.upload.onprogress = function (e) {
	// 		console.log(e);

	// 		upload(e.loaded / e.total)
	// 	}
	// }
	console.log(upload_func);
	x.upload.addEventListener("progress", upload_func, false);
	// x.upload.onprogress = function (e) {
		// console.log(e);
		// upload_func(e.loaded / e.total)
	// }

	x.onload = function (r) {
		r = JSON.parse(x.responseText);
		return success(r)
	}
	x.send(file);
	// $.ajaxSettings.async = true; 

}
