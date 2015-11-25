// GLOBALS
var webdriver = require('selenium-webdriver');
var chrome = require('chromedriver');
var fs = require('fs');

//var ids = ["REDACTED"];
//var mails = ["REDACTED"];




//var info = fs.createWriteStream('CBLINoSignIn.txt');
var header = "<html>";
var footer = "</html>";
var holder = [];
var openwrapper1 = "<div class = 'INFO' id = '";

var openwrapper2 = "'>"

var closewrapper = "</div>";
holder.push(header);

var done = false;
var written = false;


//var driver = new webdriver.Builder().
//   withCapabilities(webdriver.Capabilities.chrome()).
//   build();


var getLI = function(ids, mails, output) {
   var driver = new webdriver.Builder().
   withCapabilities(webdriver.Capabilities.chrome()).
   build();


	var total = ids.length;
	var totalMails = mails.length;
	console.log(total + ' ids and ' + totalMails + ' emails detected');
	var info = fs.createWriteStream(output);


	driver.get('https://www.google.com/').
	then(function(){
			console.log('About to start scraping!');
			for(var i = 0; i < total; i ++){
				getInfo(driver, ids, mails, i);
			}
		}, function(error){
			console.log('Wrong page?');
		}).then(function(){
			console.log('About to write info');
			var complete = 0;
			return holder.forEach(function(x){
				info.write(x, function(err,written,buffer){
					complete ++;
					if(complete === total + 2){
						console.log('Finished writing all ' + total + ' pieces of information');
						//written = true;
						return true;
					}
				});
			});
		}, function(error){
			console.log('Scraping unsuccessful:\r\n' + error);
		}).then(function(){
			console.log('Quitting successfully.');
			driver.quit();
			return true;
		//	return driver.wait(function(){
		//		return written;
		//	});	
		}, function(error) {
			console.log('Unable to write info:\r\n' + error);
			console.log('Quitting.');
			driver.quit();
			return;
	//	}).then(function(){
		//	console.log('Success! Quitting.');
		//	driver.quit();
	//	}, function(error) {
	//		console.log('Unknown error:\r\n' + error);
	//	});
	});
	};


var getInfo = function(driver, ids, mails, i){
	var base = 'http://www.linkedin.com/';
	var total = ids.length;	
	driver.get(base + ids[i]).then(function(){
		console.log('Now at index ' + i)	
		return driver.getPageSource();
		}, function(error){
			console.log('Unable to get profile for ' + ids[i]);
			}).then(function(s){
				holder.push(openwrapper1 + mails[i] + openwrapper2);
				holder.push(s);
				holder.push(closewrapper);
				console.log('Added info for person no. ' + (i + 1));
				if(i == total - 1){
					holder.push(footer)
					done = true;
					console.log('Finished collecting info')
				}
				}, function(error){
					console.log('Unable to get page source for ' + mails[i]);
				})
		};	

		module.exports = getLI;
