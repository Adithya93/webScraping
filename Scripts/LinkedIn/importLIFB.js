var fbScraper = require('./getFB.js');
var liScraper = require('./exportLI.js');
console.log('Imported both functions!');


var fbIDs = [];
var fbMails = [];
var fbOutput = '';

var liIDs = [];
var liMails = [];
var liOutput = '';


liScraper(liIDs, liMails, liOutput);
fbScraper(fbIDs, fbMails, fbOutput);
console.log('Yay! Done! Just kidding.');