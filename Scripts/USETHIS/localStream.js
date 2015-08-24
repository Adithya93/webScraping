var adi = require('http');
var fs = require('fs');


var numReqs = 0;

var page = 'compCustom.html';
//var page = 'try.html';

adi.createServer(function(request, response){
	response.writeHeader(200, {'content-type':'text/html'});
	var doc = fs.createReadStream(page);

	doc.pipe(response, 'html', {end:false});
	numReqs ++;

	doc.on('end', function(last){
		console.log('At Request No.' + numReqs);
	});	
}).listen(3050);

