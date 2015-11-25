// GLOBALS
var webdriver = require('selenium-webdriver');
var chrome = require('chromedriver');
var fs = require('fs');

var email = "raghu_singapore@yahoo.com.sg";
var pass = "QuantMast93";

//var info = fs.createWriteStream('CBDemoFBInfo.txt');
var header = "<html>";
var footer = "</html>";
var holder = [];
var openwrapper1 = "<div class = 'INFO' id = '";
var openwrapper2 = "'>";
var closewrapper = "</div>";
holder.push(header);

var done = false;
var written = false;

//var driver = new webdriver.Builder().
//withCapabilities(webdriver.Capabilities.chrome()).
//build();

//var myIDs = ["REDACTED"];
//var myMails = ["REDACTED"];
//var total = myIDs.length;

var notFound = 'Unable to find element... Does its id on DOM change?';


var getFB = function(ids, mails, outfile){

   var driver = new webdriver.Builder().
   withCapabilities(webdriver.Capabilities.chrome()).
   build();

   var info = fs.createWriteStream(outfile);
   var total = ids.length


driver.get('https://www.facebook.com/').then(function(){
	console.log('Loaded page. Finding email form.');
	return driver.wait(webdriver.until.elementLocated(webdriver.By.id('email')), 5000);
}, function(error){
	console.log('Unable to load Facebook Sign-In page..');
}).then(function(e){
	console.log('Found email form. Entering email');
	return e.sendKeys(email);
}, function(error){
	console.log(notFound);
}).then(function(){
	console.log('Entered email. Finding password form.');
	return driver.wait(webdriver.until.elementLocated(webdriver.By.id('pass')), 5000);
}, function(error){
	console.log('Unable to type email. Was email form correctly returned?');
}).then(function(p){
	console.log('Password form found. Entering password.');
	return p.sendKeys(pass);
}, function(error){
	console.log(notFound);
}).then(function(){
	console.log('Password entered. Finding sign-in button.');
	return driver.wait(webdriver.until.elementLocated(webdriver.By.id('u_0_x')));
}, function(error){
	console.log('Unable to enter password. Was password form correctly returned?');
}).then(function(s){
	console.log('Sign-in button found. Clicking it.');
	return s.click();
}, function(error){
	console.log(notFound + "\r\n" + error);
}).then(function(){
	console.log('Clicked. Waiting for title to match.');
	return driver.wait(webdriver.until.titleContains('Facebook'), 5000);
}, function(error){
	console.log('Unable to click on Sign-In button. Is it a valid form with a "POST" action?');
}).then(function(){
	console.log('Successfully logged-in to Facebook! Starting to scrape.');
	for(var index = 0; index < total; index ++){
		getInfo(driver, ids, index, mails);
	}
	return driver.wait(function(){
		return done;
	});
}, function(error){
	console.log('Title does not match:\r\n' + error);
}).then(function(){
	var complete = 0;
	holder.forEach(function(x){
		info.write(x, function(error, written, buffer){
			if(error){
				console.log('Problem while writing to file:\r\n' + error);
			}
			else{
				complete ++;
				console.log(complete + ' pages written.');
				//if(buffer === footer){
				if(complete === total + 2){
					console.log('Task Complete. Quitting.');
				//	written = true;
					driver.quit();
					return true;
				}
			}
		});
	});
	//return driver.wait(function(){
	//	return written;
//	});
}, function(error){
	console.log('Problem in getting information:\r\n' + error);
//}).then(function(){
//	driver.quit();
//}, function(error){
//	console.log('Error occurred while writing:\r\n' + error);
//	driver.quit();
});
};

var getInfo = function(driver, Urls, index, emails){
	total = Urls.length
	return driver.get('https://www.facebook.com/' + Urls[index]).then(function(){
		console.log('Now at ' + Urls[index]);
		return driver.getPageSource();
	}, function(error){
		console.log('Unable to access page for ' + Url + '\r\n' + error);
	}).then(function(s){
		holder.push(openwrapper1 + emails[index] + openwrapper2 + s + closewrapper);
		if(index === total - 1){
			done = true;
			holder.push(footer);
			return;
		}
	}, function(error){
		console.log('Unable to obtain source html');
	});
};

module.exports = getFB
