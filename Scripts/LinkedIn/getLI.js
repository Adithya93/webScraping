// GLOBALS
var webdriver = require('selenium-webdriver');
var chrome = require('chromedriver');
var fs = require('fs');
//var email = "raghunathan.adithya@duke.edu";
//var email = "ermac_master_souls@yahoo.com.sg"
var email = "booyakashabandit@gmail.com";
var pass = "Quant_Mast93";

var ids = ['https://www.linkedin.com/profile/view?id=282344224&authType=name&authToken=YxVo&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=298943318&authType=name&authToken=qujD&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=159533882&authType=name&authToken=uGoS&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=187272729&authType=name&authToken=6Uwp&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=63296612&authType=name&authToken=tpuI&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=145728703&authType=name&authToken=oYqR&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=19771747&authType=name&authToken=FRm6&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=19469011&authType=name&authToken=tOjj&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=19469011&authType=name&authToken=tOjj&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=17445589&authType=name&authToken=NDcO&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=17445589&authType=name&authToken=NDcO&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=407173571&authType=name&authToken=5k7_&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=74672742&authType=name&authToken=H-d7&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=27524596&authType=name&authToken=aJJp&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=18517672&authType=name&authToken=5bxn&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=18085756&authType=name&authToken=78Wv&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=26828565&authType=name&authToken=6Nkp&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=2597300&authType=name&authToken=Zm0O&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=115644738&authType=name&authToken=-RGq&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=1494863&authType=name&authToken=m5bh&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=47823045&authType=name&authToken=z4cW&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=18085756&authType=name&authToken=78Wv&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=32029684&authType=name&authToken=dQXn&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=19282059&authType=name&authToken=O5XG&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=4600429&authType=name&authToken=9VfW&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=165984848&authType=name&authToken=ESGb&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=72257708&authType=name&authToken=r1Gw&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=300220105&authType=name&authToken=UuAh&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=354751004&authType=name&authToken=Pzx_&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=20335717&authType=name&authToken=JkKx&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=31346648&authType=name&authToken=-7bi&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=58309758&authType=name&authToken=U57t&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=57346713&authType=name&authToken=F7HV&trk=api*a109924*s118458*', 'https://www.linkedin.com/profile/view?id=13381815&authType=name&authToken=F4tw&trk=api*a109924*s118458*'];
var total = ids.length;

var info = fs.createWriteStream('LIInfo.txt');
var header = "<html>";
var footer = "</html>";
var holder = [];
var openwrapper = "<div class = 'INFO'>";
var closewrapper = "</div>";
holder.push(header);

var done = false;
var written = false;


var driver = new webdriver.Builder().
   withCapabilities(webdriver.Capabilities.chrome()).
   build();


driver.get('https://www.linkedin.com/').
	then(function(){
		console.log('PART 1\r\n' + 'Signing into LinkedIn.')
	//	return driver.findElement(webdriver.By.id('login-email'));
		return driver.findElement(webdriver.By.id('session_key-login'))
	}, function(error){
		console.log('Unable to load page!');
	}).then(function(em){
		return em.sendKeys(email);
	}, function(error){
		console.log('Unable to find email form!');
	}).then(function(){
	//	return driver.findElement(webdriver.By.id('login-password')); 
		return driver.findElement(webdriver.By.id('session_password-login'))
	}, function(error){
		console.log('Unable to type e-mail address...');
	}).then(function(p){
		return p.sendKeys(pass);
	}, function(error){
		console.log('Unable to find password form...');
	}).then(function(){
	//	return driver.findElement(webdriver.By.name('submit')); 
		return driver.findElement(webdriver.By.id('signin'))
	}, function(error){
		console.log('Unable to type password...');
	}).then(function(s){
		return s.click();
	}, function(error){
		console.log('Unable to find "Submit" button...');
	}).then(function(){
			console.log('Signed in! Locating title.');
			return driver.wait(function(){
				return driver.getTitle().then(function(title){
					return title === "Welcome! | LinkedIn";
				}, function(error){
					console.log('Unable to get title...');
				});
			}, 15000);
		}, function(error){
			console.log('Unable to click Sign-In button....');
		}).then(function(){
			console.log('Signed into LinkedIn! Getting Info!');
			for(var i = 0; i < total; i ++){
				console.log('Now at index ' + i)
				driver.get(ids[i]).then(function(){
					return driver.getPageSource();
				}, function(error){
					console.log('Unable to get profile for ' + ids[i]);
				}).then(function(s){
					holder.push(openwrapper);
					holder.push(s);
					holder.push(closewrapper);
					console.log('Added info ')
					if(i == total - 1){
						holder.push(footer)
						done = true;
						console.log('Finished collecting info')
					}
				}, function(error){
					console.log('Unable to get page source for ' + ids[i]);
				})
			}
//			return driver.wait(function(){
//				return done;
//			});
		}, function(error){
			console.log('Wrong page?');
		}).then(function(){
			console.log('About to write info');
			return holder.forEach(function(x){
				info.write(x, function(err,written,buffer){
					console.log(written + 'bytes written');
					if(buffer === footer){
						console.log(buffer);
						written = true;
					}
				});
			});
		}, function(error){
			console.log('Scraping unsuccessful:\r\n' + error);
		});

