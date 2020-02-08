var staticPath = '';
var apiUrl = 'https://apis.yum6.cn/api/5bd44dc94bcfc';
var YoungxjApisToken = 'f07b711396f9a05bc7129c4507fb65c5';

UP = function (o, success, error, upload, x, file, A) {
	// $.ajaxSettings.async = false; 
	// $.get('http://mouto.org/api/hosts',function(r){
	// var ip=''+r.cmcc.match(/[\d\.]+/);
	// staticPath='http://'+ip+':'+'672/';
	// alert(staticPath);
	// });
	if (typeof success == 'function') {
		var file = new FormData();
		file.append("file", o);
		// file=o;
	}
	else {
		if (!o.file)
			return console.log('并没有传入需要上传的文件')

		if (A = o.success)
			success = A

		if (A = o.upload)
			upload = A

		if (A = o.error)
			error = A
	}

	x = new XMLHttpRequest();
	// alert(staticPath+'v1/upload');
	// x.open('POST',apiUrl+'?token='+YoungxjApisToken , false);
	// url = '/api/upload'
	x.open('POST', '/api/upload', false);
	// x.open('POST','http://114.86.196.54:672/v1/upload',true);
	x.setRequestHeader("X-Requested-With", "XMLHttpRequest");

	if (upload) {
		x.upload.onprogress = function (e) {
			upload(e.loaded / e.total)
		}
	}
	x.onload = function (r) {
		r = JSON.parse(x.responseText);
		return success(r)
	}
	x.send(file);
	// $.ajaxSettings.async = true; 

}
