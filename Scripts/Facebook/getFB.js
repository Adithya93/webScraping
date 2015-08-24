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

//var myIDs = ["717480524", "1291564455", "1312634901"]//, "227600059", "524365670", "687833831", "100001467803696", "ayterry", "595538895", "gianfranco.chicco", "1155423444", "100000155228292", "100000564491107", "gilad.bonjack", "871690392", "653149156", "739654517", "mbenincampi", "670814730", "895160656", "kees.mulder.359", "1050071818", "suhelbanerjee", "740807523", "1469101957", "100001347332857", "683838041", "702963543", "782250248", "1522869778", "1463419114", "576716797", "1005682372", "100001823585642", "759364584", "596854378", "100001175821190", "576291401", "1069996559", "651837780", "1391876260", "100000479149687", "1088930918", "1294814537", "690113026", "1273174843", "1347812679", "100001463002652", "532826611", "1345567073", "1140189349", "830192995", "100000903043588", "1115806282", "1363781087", "725010826", "1465323054", "778365648", "531872880", "583898822", "100000908196634", "1030518810", "100002023221799", "531410751", "1586730805", "1314613370", "717948717", "712070580", "732121103", "891095034", "620991681", "568669465", "1057882697", "100000933920041", "1648335349", "588453966", "613720781", "697041877", "576586885", "628447483", "100000793382959", "100000716897505", "543261482", "1815507153", "1619601886", "685501363", "100000562486684", "603108490", "651519534", "1384286283", "615515807", "100004001401679", "1109522974", "765334428", "1534579366", "1318419594", "1809055718", "640586793", "716740313", "615936176", "557957621", "679137265", "665432849", "100000939134539", "1675909673", "622843588", "1618535121", "1003330431", "725791588", "567504721", "1608764192", "745612648", "719260010", "100000070254775", "1354234120", "1298296767", "894110337", "718018123", "522395788", "100000224991142", "699681213", "100000290607135", "616441677", "619460432", "1678900243", "777855113", "1114838563", "1053958167", "1248516163", "666171799", "1308995602", "1459841470", "659107534", "1702403829", "4501634", "1606692731", "545094461", "1182193566", "1082180296", "672768256", "ali.syedzaidi", "761454829", "1103088075", "100000307225517", "4800399", "40701189", "586242904", "1047279445", "671067290", "787940248", "100000921929024", "528230712", "754332387", "100001018114491", "613047803", "615130010", "1316696601", "100001119432115", "694971638", "738826487", "100000079905499", "100000718181591", "584954015", "1669899215", "100002314645695", "1071763576", "646410114", "528636511", "724509590", "1266437612", "714001149", "1024866080", "1620572445", "750538647", "100000261878742", "1414306534", "7912102", "760860157", "662540724", "600147328", "1644873589", "1602310152", "525370913", "568522624", "1092171161", "583422719", "571700030", "790771589", "611235958", "568953495", "100000946425501", "503185516", "724232816", "100001575319439", "613750817", "718943870", "754807138", "1260934514", "757347369", "568128422", "568686400", "538851103", "764667939", "1835839850", "100000676823463", "828218562", "100000438945990", "1594705056", "741500156", "1106434363", "100000002172494", "100000352731138", "678459144", "100000572183064", "774269180", "1637423844", "716098853", "1481471497", "1077110438", "1353941145", "100000276805338", "689663714", "564720147", "1375674947", "607618781", "100000907465924", "566882786", "602963145", "694525985", "1755857025", "516921108", "1353730958", "708393004", "655341102", "716276468", "739803607", "617403213", "100002044729306", "1516310782", "613063600", "785599369", "1485990993", "596524308", "878750360", "chew.mok.lee", "1462388229", "100001570016888", "100002054993084", "1370499821", "625677281", "1461726855", "574966520", "609560192", "5717902", "1597761742", "1447140422", "533143723", "100000048737398", "1077489259", "1271877230", "545830983", "578407142", "1048813609", "1225797445", "731493953", "733950476", "655085773", "740504442", "830297487", "645638870", "574909744", "100001268340903", "807900581", "540035378", "612641013", "679008815", "703823041", "1445755722", "523891222", "768911613", "768563079", "1246299153", "1130666770", "636590737", "100000234442100", "700415492", "726913135", "646190819", "544822637", "1304215", "2252635", "676294362", "557206714", "100006967988177", "597824325", "1198685505", "1120807766", "1906333", "1538951936", "899115374", "1098397014", "738624039", "651598441", "36921043", "759754549", "1387266057", "743866340", "770557145", "100000461995441", "679308161", "1482327969", "100001633023102", "724627593", "584792887", "607182481", "641269009", "1179487730", "1133817110", "560553697", "798828376", "560542576", "574723274", "822095466", "814520969", "100000830403114", "617468753", "1032442859", "724632212", "659114369", "frederic.lippi", "100002521934573", "100001237182668", "612792853", "595193882", "690782321", "1800077853", "pareshpandit", "1645929073", "100000002807086", "1065302959", "1112142723", "581492338", "619178682", "554899517", "8634848", "100000012540102", "722746152", "100001119844522", "100001157824487", "100000218036803", "644375967", "1189115451", "1425977841", "520713291", "camille.personne", "690191456", "676323269", "779554111", "530197077", "1020514305", "710738114", "100001856713369", "100004319884369", "100003104260218", "100000583184479", "662611861", "1100288", "732677683", "792229477", "100000748852609", "1233539", "597361507", "100007817671616", "100002649570052", "1660843001", "704562927", "100000681004016", "710938864", "836329450", "651286445", "843234484", "510027734", "smithexeced", "1294698879", "570666604", "668075666", "100000521967817", "100004988431717", "577479554", "584221064", "1529670210", "1230542317", "100002582331895", "100001493205491", "553578146", "1446581052", "1627913889", "634332319", "1343170729", "744846438", "100000322868124", "1456861777", "856850555", "689757090", "100001215576317", "1091310220", "1206079", "612908877", "734103722", "678889069", "andrei.frolov", "514666879", "557453620", "534212598", "100002469174992", "663459399", "661994313", "100001792869830", "654477705", "100000978562398", "663374117", "100001220917175", "6802461", "644002710", "100001536565605", "586348351", "1712778704", "100002248895848", "1365095564", "710227136", "3117", "626155332", "100000996382059", "718937411", "809942459", "1646227260", "1108471216", "100000040479702", "722092217"];
//var myMails = ["bmoggridge@ideo.com", "valdur.laid@elion.ee", "furukawa@globaledu-j.com"]//, "maelkins@cokecce.com", "mnitin@yahoo-inc.com", "alan.macintosh@actawireless.com", "jim.violette@averydennison.com", "amanda.terry@gmail.com", "ken@kenbyrne.com", "gianfranco.chicco@gmail.com", "deco@chevron.com", "bhutanigs@yahoo.com", "abhijit31@hotmail.com", "giladbonjack@gmail.com", "tsolakn@visa.com", "hmunneke@hotmail.com", "sacha.rose@derek-rose.com", "mbenincampi@hotmail.com", "chaumartin@gmail.com", "rahulthappa@gmail.com", "kmulder@ascolo.com", "rosa-xiaohong.lee@chn.dupont.com", "suhel.banerjee@gmail.com", "marcello.cicerone@gmail.com", "michael.grubich@cnh.com", "wooseok.lee@samsung.com", "giorgia.aresu@it.pwc.com", "yeekou.tiong@intel.com", "martin@rotman.utoronto.ca", "ward.dirix@proximus.net", "arnaud.marcade@unilog.fr", "dasha.ivkina@gb.unisys.com", "claudiocarreno@yahoo.com", "bertda@singnet.com.sg", "puatfong.lye@energizer.com", "rvalenti@arglobal.com", "sidhartha_b@hotmail.com", "fionad@srilankan.aero", "ayind.mahamba@kiss-technologies.com", "melanie.kong@linkageasia.com", "gverissimo@hikma.pt", "somagec@somagec.ma", "bella_stavchansky@mastercard.com", "fdmartin@caixagalicia.es", "rtamimi@ncci.com.sa", "andrew.mackichan@bmw.de", "karen.caddick@ft.com", "vanleeuwen@octoplus.nl", "bianca.nestle@zf.com", "jon.stowell@hexcel.com", "p.escalle@sdv.com", "rhassim@makiplast.com", "g.rutgers@saba.nl", "khe@ecolabel.dk", "livio.gallo@enel.it", "frzin@libero.it", "lgonzalez@gonzalezbyass.es", "rohit.gambhir@hewitt.com", "martine.b.smidt@marsh.com", "yonatz@idc.ac.il", "m.belingue@cto.int", "karin.geerts@eds.com", "gillescousin@free.fr", "aleks.konakov@au.vuitton.com", "rsparks@oldmutual.com", "jbailey@cera.com", "annemette.walbom@marsh.com", "watsonc@bcie.org", "santiago.gowland@unilever.com", "diane.scott@viewpointe.com", "sara_regan@hotmail.com", "francoise.russo@diageo.com", "sirilak_raya@berninathailand.com", "klongmuir@stollberg.com", "lecnpg@singnet.com.sg", "asiasb@starhub.net.sg", "yasemin.akkozak@tr.imptob.com", "kinchong.u@kpmg.com.hk", "george.mcgregor@hp.com", "tlaffoley@aointl.com", "kalanta@petronas.com.my", "rcuif@devanlay.fr", "linda.rosendahl@ifl.se", "marshall.kearns@us.henkel.com", "cornelia.fahrner@helbling.ch", "hrafik@knowledgeacademy.com", "yho@sybase.com", "acassis@mintra.com.eg", "alefp@netvision.net.il", "petertan@chambersinternational.com.sg", "zoe@yahoo-inc.com", "sunny21.kim@samsung.com", "achavez@adb.org", "hasti@bi.go.id", "desianto@cpjf.co.id", "thierry.willieme@facto.fr", "yuwa_hedrick_wong@mastercard.com", "bdg@globsyn.co.in", "julnche@yahoo.com", "rosy@nakhooda.com", "johnson.kan@ap.rhodia.com", "martina.johansson@jwt.com", "isabel.todenhoefer@dlh.de", "wojciech_gala@o2.pl", "ton.schurink@cft-advisoryservices.com", "dwarmenhoven@netapp.com", "amoliveira@sonaesierra.com", "dmoreira@um.edu.uy", "moscatelli.giovanni@bcg.com", "jacki@insideout-consulting.com", "tquadracci@qg.com", "see-khiang.tan@nsn.com", "jrbandre@slb.com", "miranda.tam@bis.org", "gilles.auriault@eumetsat.int", "neal.kulick@mcd.com", "dtejadabiarge@epo.org", "kamarudinmeranun@airasia.com", "kpanekeke@yahoo.com", "chongkwee@hotmail.com", "grsmith@cisco.com", "tlty@free.fr", "jenimaclellan@kpmg.com", "leiterebeca@hotmail.com", "lucila@sp.senac.br", "lozano@avimex.com.mx", "sudarshan.rangapathy@igate.com", "malins@us.ibm.com", "mmeadors@kmg.com", "patricia.taylor@nao.gsi.gov.uk", "mochi@dow.com", "kiyawatv@duralineindia.com", "cjausserand@ppr.com", "guillermo.martinez@cemex.es", "daniellaub@gmail.com", "ann.v.burns@accenture.com", "spettit@deloitte.co.uk", "jean-yves.pare@ubifrance.fr", "hdsoultrait@edaptms.po.my", "dirk.adler@gmail.com", "yalisyed@hotmail.com", "taly.fiegenbaum@teva.co.il", "peter@5040services.com", "chnaris@central.co.th", "gshroff@andrew.cmu.edu", "chiomasibeudu@yahoo.com", "derekyeo@tigerairways.com", "dkruisinga@ups.com", "ahameed@lums.edu.pk", "w.bark@alpencapital.com", "miklos.fekete@hu.pwc.com", "veeyyoo@gmail.com", "madhivanan.arunachalam@ril.com", "praveenk@titanin.com", "jesper.lc.madsen@accenture.com", "natalie.seaman@dukece.com", "robertoformato@libero.it", "r.solignac@fr.vuitton.com", "liugenping@gmail.com", "ramsmail2002@yahoo.com", "martijn.vanderweijst@pmintl.com", "mvasey@microsoft.com", "halina@uow.edu.au", "lemarmion@mindspring.com", "thaipepper@earthlink.net", "mga@novonordisk.com", "keithkee@pacific.net.sg", "nattsrinara@yahoo.com.sg", "kuldip_paliwal@yahoo.com", "karsten.benz@dlh.de", "suyashprasad@hotmail.com", "chongqk@m1.com.sg", "mustafa.alhendi@dubaiaerospace.com", "teckleong.kee@ascendas.com", "tverhagen@cinergy.com", "jean-louis.detaille@orange.fr", "sarina.hickey@bba03.mccombs.utexas.edu", "stevensl@fleishman.com", "jadj02@handelsbanken.se", "andybruna@mac.com", "rnervi@scj.com", "karikle@regent.edu", "amyim@starhub.com.sg", "kumardev.chatterjee@thalesgroup.com", "maop@shelman.gr", "ana.y.vekilova@britishairways.com", "manoo@mac.com", "i-selmb@microsoft.com", "nicoletan@khattarwong.com", "nhagege@bouyguestelecom.fr", "harry.yoon@ssi.samsung.com", "keiyamamoto@hotmail.com", "stefano.odaglia@ericsson.com", "thijssen.bolck@hccnet.nl", "rachie@ibf.org.sg", "a.cohen-scali@endemolfrance.com", "mustapha.tabba@ipsos-mena.com", "werner.koss@swisscom.com", "qusai_hashim@yahoo.com", "darren.yates@eur.cushwake.com", "ewakeling@catalystwomen.org", "pvrmurthy@clickitjobs.com", "florian.sartre@asecautomation.com", "jean.fabrice.faria@zurich.com", "jean.charles.lambron@fr.kinnarps.com", "cyheng@metalwood.com.sg", "rhc72e@yahoo.com", "beverly.chau@nortonrose.com", "gcanver@yahoo.com", "bphillips@altron.co.za", "jungkh@seri.org", "ravi@themediacampus.com", "francesco.de-mojana@permira.com", "loych@ccis.com.sg", "priscillia.buissiere@chq.alstom.com", "schuricht@change-group.net", "abbygoh@singtel.com", "dmcloughlin@apac.ko.com", "cecil.chappelow@polyone.com", "stefan.butter@lexmark.fr", "rbomeny@bobs.com.br", "edward.houng@kalmarind.com", "jduah@hotmail.com", "seehoe.lau@metso.com", "anthony.briscoe@tnzi.com", "francoise.semin@avid.com", "cheekong@surfgold.com", "mdh@capgroup.com", "thibaultmonnoyeur@hotmail.com", "decio@seportal.com.br", "jenny.kwan@shell.com", "michelle.waddington@sanofi-aventis.com", "marc-olivier.linder@pmintl.com", "olivier_kouvarakis@yahoo.fr", "carmen.bekker@jwt.com", "xmorcillo@sword-group.com", "janice_pua@yahoo.com", "mawh@chevron.com", "andrew.north@nlg.nhs.uk", "phb@spiltan.se", "jolimcnh@singnet.com.sg", "michelene.flanigon@genzyme.com", "lmgan@singnet.com.sg", "rupert.hope@db.com", "chew_mok_lee@spring.gov.sg", "maurice.bellomo@paulwurth.com", "saitou-motosaburou@sei.co.jp", "ricsai@yahoo.com", "mcgloner@wharton.upenn.edu", "nicolas_vangelder@merck.com", "dgboldrini@uol.com.br", "pierre@jourdain.com", "kriti27@hotmail.com", "vsitler@umd.edu", "fbrletich@lfgsm.edu", "rich.browne@estreet.com", "dshklyarov@yandex.ru", "btain@ipa.edu.sa", "enrique_cuevas_codon@hotmail.com", "syutsui@cn.ibm.com", "samar@eventsunlimited.com.jo", "sysuh84@hotmail.com", "yrjo.sotamaa@uiah.fi", "carol_strobl@datacard.com", "hh@rias.dk", "sophie.gest@mc.abnamro.com", "hbouvier@kr.estee.com", "kulksnikhil@hotmail.com", "dml@danfoss.com", "zailani.ali@ing.com.my", "aniekan.esenam@power.alstom.com", "cwsoh@pji.co.kr", "lvandepol@angloamerican.co.uk", "walid.finan@dadgroup.com", "o_kmalik@hotmail.com", "carolinemcguigan@eircom.net", "ozgur_aksakal@yahoo.com", "tejujaa@bharatpetroleum.com", "apeducasse@theramex.mc", "kychew@wangi-industrial.com", "deanna.r.clark@boeing.com", "vr_vivek@yahoo.com", "fadhlina@bnm.gov.my", "hardug@iafrica.com", "isabelle@exo.com.br", "elias@bd-consult.com", "ajaygkrishna@yahoo.com", "merez@ie.technion.ac.il", "reto.bleisch@cablecom.ch", "charlene.chen@alumni.duke.edu", "xiuhtan@umich.edu", "msayouty@elayouty.com", "magellan@ibest.com.br", "m.schublin@eif.org", "sandrine.halleux@alcatel.be", "gianpaolo_fontana@yahoo.it", "madelein.leegwater@sns.nl", "anita_083@yahoo.com", "alexander.feischl@arcor.de", "caonabo.delarosa@shell.com", "peter_lemmens@be.ibm.com", "alexandre.roujon@tbwa-paris.com", "anastasiyaav@hotmail.com", "ailawadi@yahoo.com", "jessie@toeic.com.sg", "krivenko.m@united-europe.ru", "thomas.hornburg@schibsted.no", "adriana_vanova@carrefour.com", "jackie.smith@yahoo.com", "agarwalananda@yahoo.co.in", "toukam2@slb.com", "andre.lo-bono@wanadoo.fr", "alwadi@go.com.jo", "shetreet@aol.com", "patrick.riou@eu.rhodia.com", "juneman89@hotmail.com", "yingalls@microsoft.com", "ngim@novonordisk.com", "zoff.khan@motorola.com", "iogorman@deloitte.ie", "samira.mandil@unilever.com", "twalker@lgi.com", "aymeric@dehemptinne.net", "t.pauporte@eif.org", "suthikiatich@chr.co.th", "serge.withouck@skynet.be", "omaralnaser@hotmail.com", "shahzadali@jaffer.com", "sven.malmberg@foreign.ministry.se", "frederic.lippi@lippi.fr", "fse-sg@ifbgroup.net", "albert.tee@pacific.net.sg", "g.senk@kommunalkredit.at", "mahsa_javaheri@yahoo.com", "jcbo@bglactic.com", "kimanh.nguyen@sheraton.com", "pareshpandit@gmail.com", "mtraders@eth.net", "cpais@ahorro.com", "s4_b@hotmail.com", "jmmegar@inco.com.lb", "twix_emac@yahoo.fr", "stellaau@gmail.com", "sapo@fgroup.com.ar", "kajordan@wisc.edu", "rig@sageinfologia.com", "monica@lccieb.com.br", "thomaz@fenacor.com.br", "paulo@taler.com.br", "gingerchi@hotmail.com", "matthias.deferrieres@axa.com.sg", "doml@lundbeck.com", "mha@cefic.be", "alvintan@uobkayhian.com", "apollo1385@hotmail.com", "rafeea@qcb.gov.qa", "wchow@attglobal.net", "kim-peng.goh@exxonmobil.com", "creid@mastclimbers.co.uk", "ajmerriman@btinternet.com", "smirnov@rsys.ru", "janet.impey@bbr.com", "cintiarezende@fdc.org.br", "christer.svard@volvo.com", "lokitapr@centrin.net.id", "jlapovsky@hotmail.com", "allison.lee@gs.com", "intraway@otenet.gr", "hennesmp@yahoo.com", "tumnoble@alum.mit.edu", "panova@alum.mit.edu", "lrobson@askjeeves.co.uk", "ktmamb@um.dk", "maciej.sawicki@dajar.pl", "greg_worden@rsewind.com", "elaine.curran@db.com", "sskim@onmedia.co.kr", "carolyn_averill@hotmail.com", "tariq.s@mobilink.net", "peiqing01@hotmail.com", "sugai@tkfd.or.jp", "poojam@geetex.com", "execed@smith.edu", "jlfblanco@yahoo.com", "ngayed@yahoo.com", "anishjohn@yahoo.com", "fatimapedro@ipt.pt", "ps@iwt.be", "grace_adliariff@yahoo.co.uk", "hashimguinomla@yahoo.com", "psikkel@aointl.com", "ibrahim.gueye@eu.ikon.com", "bianca.albers@essent.nl", "ernanikato@hotmail.com", "ghassan@ghassanco.com", "vanasw_d@mtn.co.za", "apatnaik@tkmeurope.de", "d_sham@shen-laroche.com", "johan_coppens@be.ibm.com", "mavros@gennetsa.com", "sophia.schlette@bertelsmann.de", "althanika@qcb.gov.qa", "linousse@hotmail.com", "mattiasd@stanfordalumni.org", "mdarwiche@hotmail.com", "jgaudet@bluewin.ch", "josephine.hung@morganstanley.com", "jayachandran.ramakrishnan@gs.com", "ys_wang@yahoo.com", "su.yin.lee@fremantlemedia.com", "afroloff@gmail.com", "shawn.khazzam@mail.mcgill.ca", "j.schwarz@sap.com", "kennethverschooten@hotmail.com", "camille.emelina@jacuzzifrance.com", "ccapacch@cisco.com", "mm@nimbus.com", "monique.tanaka@rabobank.com", "keenan.perry@bcg.com", "posthu_l@mtn.co.za", "halgb@tdc.dk", "rsilber@silber.com.br", "raechelle.medellin@gs.com", "info@andersonlloydintl.com", "jhjoe@dsmac.or.kr", "jeesoolim@hotmail.com", "mandhir.singh@uk.bp.com", "suh2000@hotmail.com", "hank.gibson@volvo.com", "tania.amar@nice.com", "mtherrer@fas.harvard.edu", "k.palicha@sarasin-alpen.com", "junseokhan@giordano.co.kr", "philippe.jutard@compagniedesalpes.fr", "charlotte.delbes@bicworld.com", "segt33@yahoo.fr", "cwragg@twrgrp.com", "jack.chandler@lasalle.com", "bertrand.gueguen@carrier.utc.com"];
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