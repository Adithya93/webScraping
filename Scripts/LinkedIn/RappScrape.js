// GLOBALS
var webdriver = require('selenium-webdriver');
var chrome = require('chromedriver');
var fs = require('fs');
//var email = "raghunathan.adithya@duke.edu";
//var email = "ermac_master_souls@yahoo.com.sg"
var email = "booyakashabandit@gmail.com";
var pass = "Quant_Mast93";

var rappUrl = "https://chrome.google.com/webstore/detail/rapportive/hihakjfhbmlmjdnnhegiciffjplmdhin";
var gmail = "https://mail.google.com/mail/u/0/#inbox";

//var GMAIL = "raghu.singapore";
//var GMAIL = "possessedbycaffeine";
//var GPASS = "raghu1962";
var GMAIL = email;
var GPASS = pass;

var emails = ['desy.herna@yahoo.co.id', 'frankleekongfei@gmail.com', 'sopheak_kc@yahoo.com', 'ansheard@yahoo.co.id', 'spetrosian@whitecase.com', 'vanialian2@gmail.com', 'mzdior63@yahoo.com.sg', 'jamesgan71@gmail.com', 'mahathis@pruadviser.com.sg', 'squall582@hotmail.com', 'monwida.intarasonti@basf.com', 'tan_markanthony@yahoo.com', 'annmin1@yahoo.com', 'paczesna@hotmail.com', 'aheng-0303@hotmail.com', 'lindasootan@gmail.com', 'lynn.park@aim.com', 'miemieyong@yahoo.com.sg', 'sophia_lim13@yahoo.com.sg', 'vasanthvallun@hotmail.com', 'vandenabharwani85@gmail.com', 'gerald@pacificenergy.com.sg', 'mengwai0@gmail.com', 'jennytanyk@yahoo.com.sg', 'jiangjunxy@msn.com', 'ritesh@kamssingapore.com', 'cowberries@hotmail.com', 'jennytanyk@yahoo.com.sg', '01_den@yahoo.com', 'dudleyt@singnet.lk', 'aarya@villaaarya.com', 'ben.chin@crmedia.com.sg', 'judychak@yahoo.com.sg', 'kennethjq@gmail.com', 'kori.millar@rwsentosa.com', 'leanne@villaarya.com', 'drakonide@gmail.com', 'yahnadam@gmail.com', 'loumag88@gmail.com', 'huijing_1993@hotmail.com', 'jacqueline@enmaru.com.sg', 'sukaya.baskara@gmail.com', 'ccill@live.com', 'ctanlp@hotmail.com', 'Shaholove@yahoo.com', 'elizgraceramos@yahoo.com.ph', 'danielleculton@gmail.com', 'isafiggins@yahoo.com', 'raven_karl2@yahoo.com', 'zoriaf_m@yahoo.com.sg', 'twinklenana@hotmail.com', 'ann.kosasil@gmail.com', 'ritakadin@yahoo.com.sg', 'kevmt07@msn.com', 'ellykhoshkele@gmail.com', 'laurentia.aurelia@yahoo.com', 'ananda.ariesta@gmail.com', 'alia_travelink@yahoo.com', 'roshui@hotmail.com', 'fionahoang@gmail.com', 'sangeeta@sg.clearpack.com', 'dudleyt@singnet.lk', 'lu_mc@163.com', 'artidikshit@gmail.com', 'lavinarain@yahoo.com', 'hapinmichael8@yahoo.com', 'solvi.ikdahl@gmail.com', 'michael.cho.australia@gmail.com', 'dantobtobing@yahoo.com', 'alberthleeth@gmail.com', 'wleong22@gmail.com', 'pot1030@hanmail.net', 'lynnlaurente@yahoo.com', 'sybil.derrible@gmail.com', 'lisadewi@hotmail.com', 'angie2211@live.com', 'gbr_mersi@hotmail.com', 'gbr_mersi@hotmail.com', 'nectahomeo@yahoo.com', 'kma53471@kpmg.com.au', 'lisadewi@hotmail.com', 'alicecheng@singnet.com.sg', 'chanise@3-three.biz', 'denise.tjokrosaputro@gmail.com', 'duane@3-three.biz', 'ngelizabeth@hotmail.com', 'athena0219@hotmail.com', 'gabriel.tanck@uobgroup.com', 'garrygoh@garrygoh.com', 'gwen.woon@garrygoh.com', 'jun_xia_wang@hotmail.com', 'lydia.lim@inuovi.com', 'loumag88@gmail.com', 'marielim@absolutpr.com.sg', 'nickykow@gmail.com', 'tim13323@gmail.com', 'weemeng_tan@singtel.com.sg'];
var total = emails.length;

var info = fs.createWriteStream('NewRapppInfo2.txt');
var header = "<html>";
var footer = "</html>";

var infoText = fs.createWriteStream('NewRappText2.txt');
infoText.write('START OF INFO');

info.write(header);

//var holder = [];

//var sidebar;

//var ready = true;
var done = false;
var written = false;

var driver = new webdriver.Builder().
   withCapabilities(webdriver.Capabilities.chrome()).
   build();

function hasAlert() 
{ 
    try 
    { 
        //driver.switchTo().alert().accept(); 
        var al = driver.switchTo().alert();
//        return true; 
		return al.accept();
    }    
    catch (error) 
    { 
        return false; 
    }    
}  

console.log('Driver successfully built!');
// TO-DO: MODULARIZE BELOW CODE INTO A FUNCTION, THEN EXPORT THAT FUNCTION FOR USE IN MAIN GMAILSELENIUM.JS MODULE
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
			console.log('Signed into LinkedIn! Locating body.');
			return driver.findElement(webdriver.By.tagName('body'));
		}, function(error){
			console.log('Title is wrong... Check URL.');
		}).then(function(bod){
			console.log('Body found! Opening new tab.');
		return bod.sendKeys(webdriver.Key.CONTROL + 't');
		}, function(error){
			console.log('LOLWUT? Can\'t find the body???');
		}).then(function(){
			console.log('PART 2\r\nNew tab opened! Navingating to Gmail Sign-In page.');
			return driver.get(gmail);
		}, function(error){
			console.log('Unable to open new tab...');
		}).then(function(){
			console.log('Sign-In option clicked! Going to main Sign-In page.');
			return driver.wait(function(){
				return driver.getTitle().then(function(title){
					return title === "Gmail";
				}, function(error){
					console.log('Unable to get title...');
				});
			}, 15000);
		}, function(error){
			console.log('Unable to click on "Sign-In" button...');
		}).then(function(){
			console.log('Page loaded! Trying to find the email input form.');
			return driver.findElement(webdriver.By.name('Email'));	
		}, function(error){
			console.log('Title does not match! Check URL maybe?');
		}).then(function(em){
			console.log('Found! Trying to enter email address.');
	    	return em.sendKeys(GMAIL);
	    }, function(error){
	    	console.log('Unable to find email input form!\r\n');
	    }).then(function(){
	    	console.log('Entered! Trying to find the "Next" button.');
	    	return driver.findElement(webdriver.By.id('next'));
	    }, function(error){
		console.log('Unable to type e-mail address!');
		}).then(function(n){
			console.log('Found! Trying to click.');
			return n.click();
		}, function(error){
			console.log('Unable to find the "Next" button!');
		}).then(function(){
			console.log('Clicked! Started waiting for e-mail field to disappear.');
			return driver.wait(webdriver.until.elementLocated(webdriver.By.id('Passwd')), 5000);
		}, function(error){
			console.log('Unable to click on "Next" button! Error:\r\n');
		}).then(function(p){
			console.log("Found the password form! Trying to enter password.");
			return p.sendKeys(GPASS);
		}, function(error){
			console.log('Unable to find the password form! Error:\r\n' + error);
		}).then(function(){
			console.log('Password entered! Trying to find the "Sign In" button.');
			return driver.findElement(webdriver.By.id('signIn'));
		}, function(error){
			console.log('Unable to type password! Error:\r\n');// + error);
		}).then(function(s){
			console.log('Found! Trying to click.');
			return s.click();
		}, function(error){
			console.log('Unable to find the sign-in button!');// Error:\r\n' + error);
		}).then(function(){
			console.log('Clicked! Waiting for page to load.');
			driver.wait(webdriver.until.stalenessOf(webdriver.By.name('signIn')), 2000);
			console.log("Sign-in button has disappeared!");
			
			return driver.wait(function(){
				return driver.getTitle().then(function(title){
						return title !== 'Gmail';
					}, function(error){
						console.log('Unable to get title!');
						return false;
					});
			}, 10000);
		}, function(error){
			console.log('Unable to click the sign-in button!');
		}).then(function(){
			console.log('Reached Inbox! Searching for "COMPOSE" button');
			return driver.wait(webdriver.until.elementLocated(webdriver.By.xpath('//div[@class="T-I J-J5-Ji T-I-KE L3"]')), 20000);
		}, function(error){
			console.log('Unable to click on Gmail icon! Error:\r\n' + error);
		}).then(function(){
			console.log("PART 3\r\nGmail sign-in successful! Waiting to let cookies sink in...."); 
			// Manually wait so that cookies can be placed to enable Rapportive Installation
			var start = + new Date();
			return driver.wait(function(){
				return (+ new Date() - start) > 5000;
			}, 6000);
			
		}, function(error){
			console.log('Unable to reach the Inbox page...');
		}).then(function(){
			console.log('Waited long enough. Navigating to Rapportive Installation page.');
			return driver.get(rappUrl);
		}, function(error){
			console.log('Your waiter\'s not working =.=');
		}).then(function(){
			return driver.wait(function(){
				return driver.getTitle().then(function(title){
					return title === 'Rapportive - Chrome Web Store';
				}, function(error){
					console.log('Unable to get title.');
				});
			}, 5000);
		}, function(error){
			console.log('Unable to get Rapportive page.');
		}).then(function(){
			console.log('Reached Rapportive page! Refreshing to find install button.');
			return driver.navigate().refresh();
		}, function(error){
			console.log('Title does not match...');
		}).then(function(){
			console.log('Sleeping');
//			return driver.wait(webdriver.until.elementLocated(webdriver.By.css('div.g-c-R.webstore-test-button-label')), 15000);
//			return driver.wait(webdriver.until.elementIsVisible(webdriver.By.css('div.g-c-R.webstore-test-button-label')), 15000);
//			return driver.wait(webdriver.until.elementIsEnabled(webdriver.By.css('div.g-c-R.webstore-test-button-label')), 15000);
			return driver.sleep(5000);
		}, function(error){
			console.log('Unable to refresh.');
		}).then(function(b){
			console.log('Locating button.');
//			console.log('Waiting for button\'s text to be visible');
//			BUTTON = b;
//			console.log('Waiting for button to be enabled..');
//			console.log('Sleeping');
//			return driver.wait(webdriver.until.elementIsEnabled(webdriver.By.css('div.g-c-R.webstore-test-button-label')), 15000);;
			return driver.wait(webdriver.until.elementLocated(webdriver.By.css('div.g-c-R.webstore-test-button-label')), 15000);			
//			return(driver.sleep(5000));
		}, function(error){
//			console.log('Unable to find the button.');
			console.log('Insomnia?\r\n' + error);
		}).then(function(b){
//			console.log('About to click the "Add to Chrome" button. Current window handle: ' + driver.getWindowHandle().toString());
			frame1 = driver.getWindowHandle();
			var blah = new webdriver.ActionSequence(driver);
			return blah.click(b).perform();
		}, function(error){
			console.log('Unable to find the button:\r\n' + error);
		}).then(function(){

			return driver.sleep(10000);

		}, function(error){
			console.log('Unable to click button:\r\n' + error);
		}).then(function(){
			console.log('Accepted alert.');
			return driver.wait(webdriver.until.elementLocated(webdriver.By.css('div.dd-Va.g-c-Lc.g-eg-ua-Uc-c-za.g-c.g-c-oa')), 5000);
			
		}, function(error){
			console.log('Unable to accept:\r\n' + error);
		}).then(function(){
			console.log('Found "ADDED TO CHROME" button. Returning to Gmail Inbox.\r\nPART 4');
			return driver.get(gmail);
		}, function(error){
			console.log('Unable to find the "ADDED TO CHROME" button... Check xpath or try different selector...');
		}).then(function(){
			console.log('Backtracking complete. Checking page title.')
			return driver.wait(function(){
				return driver.getTitle().then(function(title){
					return title.substr(0,5) === "Inbox";
				}, function(error){
					console.log('Unable to get title..');
				});
			}, 10000);
		}, function(error){
			console.log('Unable to go back ..');
		}).then(function(){
			console.log('Back to Inbox! Searching for "COMPOSE" button');
			return driver.wait(webdriver.until.elementLocated(webdriver.By.xpath('//div[@class="T-I J-J5-Ji T-I-KE L3"]')), 5000);
		}, function(error){
			console.log('Either title does not match or unable to get title...')
		}).then(function(but){
			console.log('Found the COMPOSE button! Trying to click it.');
			return but.click();
		}, function(error){
			console.log('Unable to find the COMPOSE button! Error: \r\n' + error);
		}).then(function(){
			console.log('Clicked on the COMPOSE button!');
			//return driver.wait(webdriver.until.elementLocated(webdriver.By.name('to')), 20000);
			//return driver.wait(webdriver.until.elementLocated(webdriver.By.id(':9q')));
			return driver.wait(webdriver.until.elementLocated(webdriver.By.css('textarea.vO')));
		}, function(error){
			console.log('Unable to click on the COMPOSE button! Error:\r\n' + error);
		}).then(function(a){
			console.log('Compose Window is now open! Type-Scrape begins');
			for(var num = 0; num < emails.length; num ++){
				typeScrape(emails, num, a);
			}
			return driver.wait(function(){
				return done;
			});
		}, function(error){
			console.log('Unable to find to field');
		}).then(function(){
			console.log('Task complete');
			driver.quit();
		}, function(error){
			console.log('Something went wrong:\r\n' + error);
			driver.quit();
		});

var typeScrape = function(mails, index){
	var mail = mails[index].toLowerCase();
	var sidebar;
	// Type the email
	
	console.log('Waiting for textbox to become active...');
	return driver.wait(webdriver.until.elementLocated(webdriver.By.css('textarea.vO'))).then(function(t){
		console.log('Now on index ' + index + ': ' + mail);
		var combo = webdriver.Key.chord(mail, webdriver.Key.SPACE);
		return t.sendKeys(combo);
	}, function(error){
		console.log('Textbox is always stale...\r\n' + error);		
	}).then(function(){
		console.log('Email typed. Trying to locate email field on sidebar');
		return driver.wait(webdriver.until.elementLocated(webdriver.By.css('span.email')));
	}, function(error){
		console.log('Unable to type emails:\r\n' + error);
	}).then(function(el){
		console.log('Old email located on sidebar. Waiting for it to go stale.');
		return driver.wait(webdriver.until.stalenessOf(el));
	}, function(error){
		console.log('Unable to locate the email on sidebar');
	}).then(function(){
		console.log('Old email on sidebar has gone stale. Waiting to find new one.');
		return driver.wait(webdriver.until.elementLocated(webdriver.By.css('span.email')));
	}, function(error){
		console.log('Old email never goes stale?');
	}).then(function(el){
		console.log('New Email field located. Waiting for it to be visible.');
		return driver.wait(webdriver.until.elementIsVisible(el));
	}, function(error){
		console.log('Unable to locate email on sidebar');	
	}).then(function(){
		console.log('Element visible. Finding the element again');
		return driver.findElement(webdriver.By.css('span.email'));
	}, function(error){
		console.log('Element is never visible\r\n' + error);
	}).then(function(el){
	// Check that email matches
		console.log('Found e-mail field. Checking for match with ' + mail);
		return driver.wait(webdriver.until.elementTextIs(el, mail), 3000);
	}, function(error){
		console.log('Unable to find email field:\r\n' + error);
	}).then(function(){
	// Scrape sidebar
		console.log('E-mails match. Retrieving sidebar to extract its HTML');
		return driver.wait(webdriver.until.elementLocated(webdriver.By.css('div#rapportive-sidebar div')), 2000);
	}, function(error){
		console.log('Emails do not match.\r\n' + error);
	}).then(function(s){
		sidebar = s;
		return s.getInnerHtml();
	}, function(error){
		console.log('Unable to find sidebar now? Strange...');
	}).then(function(html){
		var infostr = "<div class = 'INFO'>" + html + "</div>"
	//	holder.push(infostr);
		info.write(infostr);
		if(index === total - 1){
	//		holder.push(footer);
			info.write(footer);
			done = true;
		}
	//	return cross.click()
		return true;
	}, function(error){
		console.log('Unable to obtain HTML:\r\n' + error);

	}).then(function(){
		console.log('Getting text content');
		return sidebar.getText();
	}, function(error){
		console.log('Unable to write');
	
	}).then(function(text){
		console.log('Text extracted');
		infoText.write('START OF PERSON\r\n' + text +  '\r\nEND OF PERSON\r\n');
		return true;
	}, function(error){
		console.log('Unable to get text:\r\n' + error);
	}).then(function(){
		console.log('Finding cross')
		return driver.findElement(webdriver.By.className('vM'));

	}, function(error){
		console.log('Unable to write');
	}).then(function(c){
		console.log('Found cross, clicking it.');
		return c.click();
	}, function(error){
		console.log('Unable to find cross');
	}).then(function(){
		console.log('Done with ' + mail);
		return true;
	}, function(error){
		console.log('Unable to remove email:\r\n' + error);
	});
};
