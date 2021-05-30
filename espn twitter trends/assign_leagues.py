# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 10:16:12 2021

@author: alext
"""
import pandas as pd
import pickle
import random

def assign_league(t):
    
    sleague = {'nfl': [' nfl', '@nfl', '#nfl', 
                       '@chicagobears', 'chicago bears', '#bears100', 'bears',
                       '@bengals', 'cincinnati bengals', '#seizethedey', 'bengals',
                       '@buffalobills', 'buffalo bills', '#gobills', 'bills',
                       '@broncos','denver broncos', '#broncoscountry',  'broncos',
                       '@browns', 'cleveland browns', '#browns', 'browns',
                       '@buccaneers','tampa bay buccaneers', '#gobucs', 'bucs', 'buccanneers'
                       'arizona cardinals', '@azcardinals', '#redsea', 
                       '@chargers', 'san diego chargers', 'los angeles chargers', '#boltup', 'chargers',
                       '@chiefs', 'kansas city chiefs', '#chiefskingdom', 'chiefs',
                       '@colts',  'indianapolis colts', '#colts','colts',
                       '@dallascowboys', 'dallas cowboys', '#dallascowboys', 'cowboys',
                       '@miamidolphins', 'miami dolphins', '#finsup', 'dolphins',
                       '@eagles',  'philadelphia eagles', '#flyeaglesfly', 'eagles',
                       '@atlantafalcons',  'atlanta falcons', '#inbrotherhood', 'falcons'
                       '@giants', 'new york giants', '#giantspride', 'nyg'
                       'detroit lions', '@lions', '#onepride', 'lions',
                       '@jaguars', 'jacksonville jaguars', '#duuuval', 'jaguars',
                       'nyj', '@nyjets', 'new york jets', '#takeflight',
                       '@packers',  'green bay packers', '#gopackgo', 'packers',
                       '@panthers', 'carolina panthers', '#keeppounding', 
                       '@patriots', 'new england patriots', '#gopats', 'patriots',
                       '@raiders', 'oakland raiders', 'las vegas raiders', 'raiders',
                       '@ramsnfl', 'st. louis rams', 'los angeles rams', '#larams', 'rams',
                       '@ravens', 'baltimore ravens', '#ravensflock', 'ravens',
                       'washington redskins', 'wft', 'washington football team', '#httr', '@washingtonnfl',  '@redskins', 'redskins',
                       '@saints', 'new orleans saints', '#saints', 'saints',
                       '@seahawks', 'seattle seahawks', '#seahawks', 'seahawks',
                       '@steelers', 'pittsburgh steelers', '#herewego', 'steelers',
                       '@houstontexans', 'houston texans', '#wearetexans', 'texans',
                       '@titans', 'tennessee titans', '#titans', 'titans',
                       '@vikings', 'minnesota vikings', '#skol', 'vikings',
                       '@49ers', 'san francisco 49ers', '#goniners', 'niners', '49ers'
                       ],
               'nba': [' nba', '@nba', '#nba', 
                       'milwaukee bucks', '@bucks', 'bucks',
                       'chicago bulls', '@chicagobulls', 'bulls',
                       'cleveland cavaliers', '@cavs', 'cavs', 'cavaliers'
                       'boston celtics', '@celtics', 'celtics',
                       'los angeles clippers', '@laclippers', 'clippers',
                       'memphis grizzlies', '@memgrizz', 'grizzlies',
                       'miami heat', '@miamiheat', 'heat',
                       'atlanta hawks', '@atlhawks', ' hawks '
                       'charlotte hornets', 'charlotte bobcats','@hornets', 'hornets', 'bobcats',
                       'utah jazz', '@utahjazz', 'jazz',
                       'sacramento kings', '@sacramentokings', 
                       'new york knicks', '@nyknicks', 'knicks',
                       'los angeles lakers', '@lakers', 'lakers',
                       'orlando magic', '@orlandomagic', 'magic',
                       'dallas mavericks', '@dallasmavs', 'mavericks', 'mavs',
                       'brooklyn nets', 'new jersey nets', '@brooklynnets', 'nets',
                       'denver nuggets', '@nuggets', 'nuggets',
                       'indiana pacers', '@pacers', 'pacers',
                       'new orleans pelicans', 'new orleans hornets', '@pelicansnba', 'pelicans',
                       'detroit pistons', '@detroitpistons', 'pistons',
                       'toronto raptors', '@raptors', 'raptors', 'raps',
                       'houston rockets', '@houstonrockets', 'rockets',
                       'san antonio spurs', '@spurs', 'spurs', 
                       'pheonix suns', '@suns', 'suns',
                       'oklahoma city thunder', 'seattle sonics', 'seattle supersonics', '@okcthunder', 'thunder',
                       'minnesota timberwolves', '@timberwolves', 'twolves', 'timberwolves',
                       'portland trailblazers', '@trailblazers', 'blazers'
                       'san francisco warriors', '@warriors', 'warriors',
                       'washington wizards', '@washwizards', 'wizards',
                       'philadelphia 76ers', '@sixers', 'sixers', '76ers'
                       ],
               'mlb': [' mlb', '@mlb', '#mlb', 
                       'los angeles angels', 'anaheim angels', '@angels', 'angels',
                       'oakland as', '@oaklandas', 
                       'houston astros', '@astros', 'astros',
                       'toronto bluejays', '@bluejays', 'bluejays',
                       'atlanta braves', '@braves', 'braves',
                       'milwaukee brewers', '@brewers', 'brewers',
                       'st. louis cardinals', '@stlcardinals', 
                       'chicago cubs', '@cubs', 'cubs',
                       'arizona diamondbacks', '@dbacks', 'dbacks', 'diamondbacks',
                       'los angeles dodgers', '@dodgers', 'dodgers',
                       'san francisco giants', '@sfgiants', 
                       'cleveland indians', '@indians', 'indians',
                       'seattle mariners', '@mariners', 'mariners',
                       'florida marlins', 'miami marlins', '@marlins', 'marlins',
                       'new york mets', '@mets', 'mets',
                       'washington nationals', '@nationals', 'nationals', ' nats '
                       'baltimore orioles', '@orioles', 'orioles', 
                       'san diego padres', '@padres', 'padres',
                       'philadelphia phillies', '@phillies', 'phillies',
                       'pittsburgh pirates', '@pirates', 'pirates',
                       'texas rangers', '@rangers', 
                       'tampa bay rays', '@raysbaseball', 'rays',
                       'boston red sox', '@redsox','red sox',
                       'cincinnati reds', '@cincinnatireds', ' reds ',
                       'kansas city royals', '@royals', 'royals',
                       'colorodo rockies', '@rockies', 'rockies',
                       'detroit tigers', '@tigers', 'tigers',
                       'minnesota twins', '@twins', 'twins',
                       'chicago white sox', '@whitesox', 'white sox',
                       'new york yankees', '@yankees', 'yankees'
                       ],
               'nhl': [' nhl', '@nhl', '#nhl', 
                       'anaheim ducks', '@anaheimducks', '#letsgoducks', 'ducks',
                       'arizona coyotes', '@arizonacoyotes', '#yotes', 'coyotes',
                       'boston bruins', '@nhlbruins', '#nhlbruins', 'bruins',
                       'buffalo sabres', '@nhlsabres', '#sabres', 'sabres',
                       'calgary flames', '@nhlflames', '#cofred', 'flames',
                       'carolina hurricanes', '@nhlcanes', '#redvolution', 'canes',
                       'chicago blackhawks', '@nhlblackhawks', '#blackhawks', 'blackhawks',
                       'colorado avalanche', '@avalanche', '#goavsgo', 'avalanche',
                       'columbus blue jackets', '@bluejacketsnhl', '#cbj', 'blue jackets',
                       'dallas stars', '@dallasstars', '#gostars', 
                       'detroit red wings', '@detroitredwings', '#lgrw', 'red wings',
                       'edmonton oilers', '@edmontonoilers', '#letsgooilers', 'oilers',
                       'florida panthers', '@flapanthers', '#flapanthers', 
                       'los angeles kings', '@lakings', '#gokingsgo', 
                       'minnesota wild', '@mnwild', '#mnwild', 'wild'
                       'montreal canadians', '@canadiensmtl', '#gohabsgo', 'canadiens',
                       'nashville predators', '@predsnhl', '#preds', 'preds', 'predators',
                       'new jersey devils', '@njdevils', '#njdevils', 'devils',
                       'new york islanders', '@nyislanders', '#isles', 'islanders', 
                       'new york rangers', 'nyrangers', '#nyr', 
                       'ottawa senators', '@senators', '#sens', 'senators',
                       'philadelphia flyers', '@nhlflyers', '#letsgoflyers', 'flyers',
                       'pittsburgh penguins', '@penguins', '#letsgopens', ' pens ', 'penguins'
                       'san jose sharks', '@sanjosesharks', '#sjsharks', 'sharks',
                       'st. louis blues', '@stlouisblues', '#alltogethernowstl', 'blues',
                       'tampa bay lightning', '@tblightning', '#gobolts', 'lightning',
                       'toronto maple leafs', '@mapleleags', '#tmltalk', 'maple leafs',
                       'vancouver canucks', '@canucks', '#canucks', 'canucks', 
                       'vegas golden knights', '@goldenknights', '#vegasgoesgold', 'golden knights',
                       'washington capitals', '@capitals', '#allcaps', ' caps ', 'capitals',
                       'winnipeg jets', '@nhljets', '#gojetsgo'],
               'mls': [' mls', '@mls', '#mls', 
                       'atlanta united fc', '@atlutd',
                       'chicago fire', '@chicagofire', 'fire',
                       'colorado rapids', '@coloradorapids', 'rapids',
                       'columbus crew sc', '@columbuscrewsc', 
                       'dc united', 'd.c. united', '@dcunited',
                       'fc dallas', '@fcdallas', 
                       'houston dynamo', '@houston dynamo', 'dynamo',
                       'los angeles galaxy', 'la galaxy', '@lagalaxy', 'galaxy',
                       'minnesota united fc', '@mnufc', 
                       'montreal impact', '@impactmontreal', 'impact',
                       'new england revolution', '@nerevolution', 'revolution', ' revs ',
                       'new york city fc', '@nycfc', 
                       'new york red bulls', '@newyorkredbulls', 'red bulls',
                       'orlando city sc', 'orlandocitysc', 
                       'philadelphia union', '@philaunion', 
                       'portland timbers', '@timbersfc', 'timbers',
                       'real salt lake', '@realsaltlake',
                       'san jose earthquakes', '@sjearthquakes', 'earthquakes', 
                       'seattle sounders fc', '@soundersfc', 'sounders',
                       'sporting kansas city', '@sportingkc', 
                       'toronto fc', '@torontofc',
                       'vancouver whitecaps fc', '@whitecaps', 'whitecaps'
                        ],
               'wnba': [' wnba', '@wnba', '#wnba', 
                        'las vegas aces', '@lvaces', 'aces',
                        'dallas wings', '@dallaswings', 
                        'chicago sky', '@chicagosky', 
                        'los angeles sparks', '@lasparks', 'sparks',
                        'pheonix mercury', '@@pheonixmercury', 'mercury',
                        'indiana fever', '@indianafever', 'fever',
                        'connecticut sun', '@connecticutsun', ' sun ',
                        'new york liberty', '@nyliberty', 'liberty',
                        'washington mystics', '@washmystics', 'mystics',
                        'minnesota lynx', '@minnesotalynx', 'lynx',
                        'san antonio stars', '@sastars', 
                        'seattle storm', '@seattlestorm', 'storm',
                        'atlanta dream', '@atlantadream', 'dream'],
               'nwsl': [' nwsl', '@nwsl', '#nwsl', 
                        'houston dash', '@houstondash', 'dash',
                        'washington spirit', '@washspirit', 'spirit',
                        'ol reign', '@olreign', 'seattle reign fc', 
                        'portland thorns fc', '@thornsfc', 'thorns',
                        'fc kansas city', '@fckansascity', 
                        'wny flash', '@wnyflash', 'flash',
                        'sky blue fc', '@skybluefc', 
                        'boston breakers', '@bostonbreakers', 'breakers']}
    
    sleague2 = {'nwsl': [('houston', 'dash'), ('hou', 'dash'),
                         ('washington', 'spirit'), ('was', 'spirit'),
                         ('ol', 'reign'), ('sea', 'reign'),
                         ('portland', 'thorns'), ('por', 'thorns'),
                         ('kansas city', 'fc'), ('kc', 'fc'),
                         ('wny', 'flash'),
                         ('sky blue', 'fc'),
                         ('boston', 'breakers'), ('bos', 'breakers')
                         ],
        'wnba': [('las vegas', 'aces'), ('vegas', 'aces'), ('lv', 'aces'),
                         ('dallas', 'wings'), ('dal', 'wings'),
                         ('chicago', 'sky'), ('chi', 'sky'),
                         ('los angeles', 'sparks'), ('la', 'sparks'),
                         ('pheonix', 'mercury'), ('phx', 'mercury'),
                         ('indiana', 'fever'), ('ind', 'fever'),
                         ('connecticut', 'sun'),
                         ('new york', 'liberty'), ('ny', 'liberty'),
                         ('washington', 'mystics'), ('was', 'mystics'),
                         ('minnesota', 'lynx'), ('min', 'lynx'),
                         ('san antonio', 'stars'),
                         ('seattle', 'storm'), ('sea', 'storm'),
                         ('atlanta', 'dream'), ('atl', 'dream')
                         ],
        'mls': [('atlanta', 'united'),('atl', 'united'),
                        ('chi', 'fire'),
                        ('colorado', 'rapids'),
                        ('columbus', 'crew'),
                        ('dc', 'united'), ('d.c.', 'united'),
                        ('fc', 'dallas'), ('fc', 'dal'),
                        ('houston', 'dynamo'), ('hou', 'dynamo'),
                        ('los angeles', 'galaxy'), ('la', 'galaxy'),
                        ('minnesota', 'united'), ('min', 'united'),
                        ('montreal', 'impact'),
                        ('new england', 'revolution'), ('new england', 'revs'), ('ne', 'revolution'), ('ne', 'revs'),
                        ('new york', 'fc'), ('nyc', 'fc'),
                        ('new york', 'red bulls'), ('ny', 'red bulls'),
                        ('orlando', 'sc'), ('orl', 'sc'),
                        ('philadelphia', 'union'), ('philly', 'union'), ('phi', 'union'),
                        ('portland', 'timbers'), ('por', 'timbers'),
                        ('real', 'salt lake'),
                        ('san jose', 'earthquakes'), ('sj', 'earthquakes'),
                        ('seattle', 'sounders'), ('sea', 'sounders'),
                        ('sporting', 'kansas city'), ('sporting', 'kc'),
                        ('toronto', 'fc'), ('tor', 'fc'),
                        ('vancouver', 'whitecaps')
                        ],
                'nhl': [('anaheim', 'ducks'), 
                        ('arizona', 'coyotes'), ('ari', 'coyotes'),
                        ('boston', 'bruins'), ('bos', 'bruins'),
                        ('buffalo', 'sabres'), ('buf', 'sabres'),
                        ('calgary', 'flames'), ('cal', 'flames'),
                        ('carolina', 'hurricanes'), ('car', 'canes'),
                        ('chicago', 'blackhawks'), ('chi', 'blackhawks'), ('chi', 'hawks'),
                        ('colorado', 'avalanche'),
                        ('columbus', 'blue jackets'),
                        ('dallas', 'stars'), ('dal', 'stars'),
                        ('detroit', 'red wings'), ('det', 'wings'),
                        ('edmonton', 'oilers'),
                        ('florida', 'panthers'),
                        ('los angeles', 'kings'), ('la', 'kings'),
                        ('minnesota', 'wild'), ('min', 'wild'),
                        ('montreal', 'canadians'),
                        ('nashville', 'predators'), ('nashville', 'preds'),
                        ('new jersey', 'devils'), ('nj', 'devils'),
                        ('new york', 'islanders'), ('ny', 'islanders'),
                        ('new york', 'rangers'), ('ny', 'rangers'),
                        ('ottawa', 'senators'),
                        ('philadelphia', 'flyers'), ('philly', 'flyers'), ('phi', 'flyers'),
                        ('pittsburgh', 'penguins'), ('pit', 'penguins'), ('pit', 'pens'),
                        ('san jose', 'sharks'), ('sj', 'sharks'),
                        ('st. louis', 'blues'), ('st louis', 'blues'), ('stl', 'blues'),
                        ('tampa bay', 'lightning'), ('tb', 'lightning'),
                        ('vancouver', 'canucks'),
                        ('vegas', 'golden knights'),
                        ('washington', 'capitals'), ('was', 'capitals'), ('was', 'caps'),
                        ('winnipeg', 'jets')
                        ],
        'mlb': [('los angeles', 'angels'), ('la', 'angels'),
                        ('oakland', 'as'), ('oak', 'as'), ('oak', "a's"),
                        ('houston', 'astros'), ('hou', 'astros'),
                        ('toronto', 'bluejays'), ('tor', 'bluejays'),
                        ('atlanta', 'braves'), ('atl', 'braves'),
                        ('milwaukee', 'brewers'), ('mil', 'brewers'),
                        ('st louis', 'cardinals'), ('st. louis', 'cardinals'), ('stl', 'cardinals'),
                        ('chicago', 'cubs'), ('chi', 'cubs'),
                        ('arizona', 'diamondbacks'), ('arizona', 'dbacks'), ('ari', 'dbacks'), ('ari', 'diamondbacks'),
                        ('los angeles', 'dodgers'), ('la', 'dodgers'),
                        ('san francisco', 'giants'), ('sf', 'giants'),
                        ('cleveland', 'indians'), ('cle', 'indians'),
                        ('seattle', 'mariners'), ('sea', 'mariners'),
                        ('florida', 'marlins'), ('miami', 'marlins'), ('mia', 'marlins'), ('fl', 'marlins'),
                        ('new york', 'mets'), ('ny', 'mets'),
                        ('washington', 'nationals'), ('was', 'nationals'), ('washington', 'nats'), ('was', 'nats'),
                        ('baltimore', 'orioles'), ('bal', 'orioles'),
                        ('san diego', 'padres'), ('sd', 'padres'),
                        ('philadelphia', 'phillies'), ('phi', 'phillies'), ('philly', 'phillies'),
                        ('pittsburgh', 'pirates'), ('pit', 'pirates'),
                        ('texas', 'rangers'), ('tex', 'rangers'),
                        ('tampa bay', 'rays'), ('tb', 'rays'),
                        ('boston', 'red sox'), ('bos', 'red sox'), ('bos', 'sox'),
                        ('cincinnati', 'reds'), ('cin', 'reds'),
                        ('kansas city', 'royals'), ('kc', 'royals'),
                        ('colorado', 'rockies'), ('col', 'rockies'),
                        ('detroit', 'tigers'), ('det', 'tigers'),
                        ('minnesota', 'twins'), ('min', 'twins'),
                        ('chicago', 'white sox'), ('chi', 'sox'),
                        ('new york', 'yankees'), ('ny', 'yankees')
                        ],
        'nba': [('milwaukee', 'bucks'), ('mil', 'bucks'),
                        ('chicago', 'bulls'), ('chi', 'bulls'),
                        ('cleveland', 'cavaliers'), ('cleveland', 'cavs'), ('cle', 'cavaliers'), ('cle', 'cavs'),
                        ('boston', 'celtics'), ('bos', 'celtics'),
                        ('los angeles', 'clippers'), ('la', 'clippers'),
                        ('memphis', 'grizzlies'), ('mem', 'grizzlies'), ('memphis', 'griz'), ('mem', 'griz'),
                        ('miami', 'heat'), ('mia', 'heat'),
                        ('atlanta', 'hawks'), ('atl', 'hawks'),
                        ('charlotte', 'hornets'), ('charlotte', 'bobcats'), ('cha', 'hornets'), ('cha', 'bobcats'),
                        ('utah', 'jazz'), ('uta', 'jazz'),
                        ('sacramento', 'kings'), ('sac', 'kings'),
                        ('new york', 'knicks'), ('ny', 'knicks'),
                        ('los angeles', 'lakers'), ('la', 'lakers'),
                        ('orlando', 'magic'), ('orl', 'magic'),
                        ('dallas', 'mavericks'), ('dallas', 'mavs'), ('dal', 'mavericks'), ('dal', 'mavs'),
                        ('brooklyn', 'nets'), ('new jersey', 'nets'), ('nj', 'nets'), ('brk', 'nets'),
                        ('denver', 'nuggets'), ('den', 'nuggets'),
                        ('indiana', 'pacers'), ('ind', 'pacers'),
                        ('new orleans', 'pelicans'), ('no', 'pelicans'), ('new orleans', 'hornets'), ('no', 'hornets'),
                        ('detroit', 'pistons'), ('det', 'pistons'),
                        ('toronto', 'raptors'), ('tor', 'raptors'), 
                        ('houston', 'rockets'), ('hou', 'rockets'),
                        ('san antonio', 'spurs'), ('sa', 'spurs'),
                        ('pheonix', 'suns'), ('phx', 'suns'),
                        ('oklahoma city', 'thunder'), ('okc', 'thunder'),
                        ('minnesota', 'timberwolves'), ('min', 'timberwolves'),
                        ('portland', 'trailblazers'), ('por', 'trailblazers'), ('portland', 'blazers'), ('por', 'blazers'),
                        ('san francisco', 'warriors'), ('sf', 'warriors'),
                        ('washington', 'wizards'), ('washington', 'wiz'), ('was', 'wizards'), ('was', 'wiz'),
                        ('philadelphia', '76ers'), ('philly', '76ers'), ('phi', '76ers'), ('philadelphia', 'sixers'), ('philly', 'sixers'), ('phi', 'sixers')
                        ],
        'nfl': [('chicago', 'bears'), ('chi', 'bears'),
                        ('cincinnati', 'bengals'), ('cin', 'bengals'), 
                        ('buffalo', 'bills'), ('buf', 'bills'),
                        ('denver', 'broncos'), ('den', 'broncos'),
                        ('cleveland', 'browns'), ('cle', 'browns'), 
                        ('tampa bay', 'buccaneers'), ('tampa bay', 'bucs'), ('tb', 'buccaneers'), ('tb', 'bucs'), 
                        ('arizona', 'cardinals'), ('az', 'cardinals'), 
                        ('san diego', 'chargers'), ('los angeles', 'chargers'), ('sd', 'chargers'), ('la', 'chargers'),
                        ('kansas city', 'chiefs'), ('kc', 'chiefs'),
                        ('indianapolis', 'colts'), ('ind', 'colts'),
                        ('dallas', 'cowboys'), ('dal', 'cowboys'),
                        ('miami', 'dolphins'), ('mia', 'dolphins'), 
                        ('philadelphia', 'eagles'), ('phi', 'eagles'),
                        ('atlanta', 'falcons'), ('atl', 'falcons'),
                        ('new york', 'giants'), ('ny', 'giants'), 
                        ('washington', 'redskins'), ('was', 'redskins'), 
                        ('detroit', 'lions'), ('det', 'lions'), 
                        ('new york', 'jets'), ('ny', 'jets'), 
                        ('green bay', 'packers'), ('gb', 'packers'), 
                        ('new england', 'patriots'), ('ne', 'patriots'), ('new england', 'pats'), ('ne', 'pats'),
                        ('oakland', 'raiders'), ('oak', 'raiders'), ('las vegas', 'raiders'), ('lv', 'raiders'),
                        ('los angeles', 'rams'), ('la', 'rams'), ('stl', 'rams'), ('st louis', 'rams'), ('st. louis', 'rams'), 
                        ('baltimore', 'ravens'), ('bal', 'ravens'),
                        ('washington', 'redskins'), ('was', 'redskins'),
                        ('new orleans', 'saints'), ('no', 'saints'),
                        ('seattle', 'seahawks'), ('sea', 'seahawks'),
                        ('pittsburgh', 'steelers'), ('pit', 'steelers'), 
                        ('houston', 'texans'), ('hou', 'texans'),
                        ('tennessee', 'titans'), ('ten', 'titans'),
                        ('minnesota', 'vikings'), ('min', 'vikings'),
                        ('san francisco', '49ers'), ('san francisco', 'niners'), ('sf', '49ers'), ('sf', 'niners')
                        ]}
    
    kps = {'mlb': ['gary sanchez', 'carlos santana', 'dj lemahieu', 'alex bregman', 'jorge polanco', 'michael brantley', 'mike trout', 'george springer', 'justin verlander', 'j.d. martinez', 'willson contreras', 'freddie freeman', 'ketel marte', 'nolan arendo', 'javier baez', 'christian yelich', 'ronals acuna jr.', 'cody bellinger', 'hyun jin ryu', 'josh bell',
                   'salvador perez', 'jose abreu', 'jose altuve', 'jose ramirez', 'manny machado', 'aaron judge', 'mookie betts', 'chris sale', 'brandon crawford', 'matt kemp', 'bryce harper', 'nick markakis', 'paul goldschmidt', 
                   'justin smoak', 'carlos correa', 'corey dickerson', 'buster posey', 'ryan zimmerman', 'daniel murphey', 'zack cozart', 'macell ozuna', 'charlie blackmon', 'giancarlo stanton',
                   'eric hosmer', 'xander bogaerts', 'jackie bradley jr.', 'david ortiz', 'anthony rizzo', 'ben zobrist', 'kris briant', 'addison russell', 'carlos gonzalez', 'johnny cueto', 'wil myers',
                   'albert pujols', 'josh donaldson', 'alcides escobar', 'adam jones', 'lorenzo cain', 'dallas keuchel', 'nelson cruz', 'todd frazier', 'jhonny peralta', 'joc pederson', 'andrew mccutchen', 'zack greinke', 
                   'miguel cabrera', 'robinson cano', 'derek jeter', 'jose bautista', 'felix hernandez', 'jonathan lucroy', 'chase utley', 'aramis ramirez', 'troy tulowitzki', 'carlos gomez', 'yasiel puig', 'adam wainwright', 
                   'joe mauer', 'chris davis', 'j.j. hardy', 'max sherzer', 'yadier molina', 'joey votto', 'brandon phillips', 'david wright', 'carlos beltran', 'matt harvey', 'michael cuddyer',
                   'mike napoli', 'prince fielder', 'adrian', 'beltre', 'josh hamilton', 'curtis granderson', 'dan uggla', 'pablo sandoval', 'rafael furcal', 'ryan braun', 'melky cabrera', 'matt cain', 
                   'alex avila', 'adrian gonzalez', 'asdrubal cabrera', 'jered weaver', 'brian mccann', 'rickie weeks', 'scott rolen', 'matt holiday', 'matt kemp', 'lance berkman', 
                   'evan longoria', 'carl crawford', 'ichiro suzuki', 'david price', 'vladimir guerroro', 'martin prado', 'david wright', 'hanley ramirez', 'andre ethier', 'corey hart', 'ublaldo jimenez', 'ryan howard',
                   'mark teixeira', 'aaron hill', 'michael young', 'jason bay', 'roy halladay', 'raul ibanez', 'shane victorino', 'tim lincecum',
                   'kevin youkilis', 'dustin pedroia', 'alex rodriguez', 'manny ramirez', 'cliff lee', 'milton bradley', 'geovany soto', 'lance berkman', 'chipper jones', 'kosuke fukodome', 'ben sheets', 
                   'ivan rodriguez', 'placido polanco', 'magglio ordonez', 'dan haren', 'russell martin', 'jose reyes', 'barry bonds', 'ken griffey jr.', 'jake peavy'],
           'mls': ['brad guzan', 'leandro gonzalez pirez', 'josef martinez', 'jonathan dos santos', 'zlatan ibrahimovic', 'carlos vela', 'maximiliano moralez', 'paxton pomykal', 'chris wondolowski', 'nicolas lodeiro', 'mark-anthony kaye', 'diego rossi', 'nani', 'nick rimando', 'romain metanire', 'alejandro pozuelo', 'diego chara', 'gonzalo martinez', 'wayne rooney', 'matt hedges', 'walker zimmerman', 'andre blake', 'ezequiel barco', 'graham zusi', 'bastian schweinsteiger', 'kemar lawrence',
                   'tyler adams', 'michael parkhurst', 'fancisco calvo', 'ilie', 'miguel almiron', 'sebastian giovonco', 'alexander ring', 'alberth elis', 'zack steffen', 'yoshimar yotun', 'ignacio piatti', 'laurent ciman', 'matt hedges', 'darwin wuintero', 'graham zusi', 'aaron long', 'michael murillo', 'alphonso davies', 'wilfried zahibo', 'bradley wright-phillips', 'david villa',
                   'tim howard', 'hernan grana', 'dax mccarty', 'kaka', 'damarcus beasley', 'dom dwyer', 'greg garza', 'johan kappelhof', 'jozy altidore', 'nemanja nikolic', 'kellyn acosta', 'stefan frei', 'miguel almiron', 'ignacio piatti', 'bastian scheinsteiger', 'jelle van damme',
                   'andre blake', 'clint dempsey', 'brandon vincent', 'kendall waston', 'darlington nagbe', 'chris wondolowski', 'clye larin', 'didier drogba', 'keegan rosenberry', 'jermaine jones', 'andrew farrell', 'steve birnbaum', 'sacha kljestan', 'matt besler', 'liam ridgewell', 'wil trapp', 'andrea pirlo', 'laurent ciman', 'josh saunders', 'kyle beckerman', 'mauro diaz', 'david bingham', 
                   'david ousted', 'drew moor', 'omar gonzalez', 'ethan finley', 'jununho', 'jozy altidore', 'fabian castillo', 'tony beltran', 'chad marshall', 'damarcus beasley', 'benny feilhaber', 'waylin francis', 'sam cronin', 'kei kamara', 'gyasi zardes', 'clint irwin', 'chris tierney', 'michael bradley', 'steven gerrard', 'frank ;ampard', 'obafemi martins', 'robbie keane',
                   'osvaldo alonso', 'sean franklin', 'landon donovan', 'tim cahill', 'thierry henry', 'deandre yedlin', 'erick torres', 'maurice edu', 'liam ridgewell', 'bill hamid', 'bobby boswell', 'will johnson', 'aurelien collin', 'bradley wright-phillips', 'kyle beckerman', 'jermain defoe', 'omar conzalez', 'chad marshall',
                   'raul fernandez', 'mike magee', 'chis wondolowski', 'marco di valo', 'patrice bernier', 'brad davis', 'will johnson', 'jack mcinerney', 'camilo sanvezzo', 'corey ashe', 'aurelien collin', 
                   'jimmy nielsen', 'carlos valdes', 'jay demerit', 'dwayne de rosario', 'eddie johnson', 'ramiro corrales', 'chris pontius', 'justin morrow', 'michael farfan', 'dan kennedy', 'david beckham', 'steven beitashour', 'jon busch', 'jamison olave', 'geoff cameron', 'brad davis', 'marco pappa', 'brek shea', 'roger espinoza', 'marvin chavez', 'kenny cooper', 'fabian espindola', 'fredy montero',
                   'faryd mondragon', 'sean franklin', 'heath pearce', 'jamison olave', 'nick labrocca', 'omar cummings', 'bobby convey', 'jack jewsbury', 'tim ream', 'juan agudelo', 'kasey keller', 'geoff cameron', 'shalre joseph', 'tally hall', 'omar bravo', 'rafael marquez', 'dwayn de rosario', 'joel lindpere', 'jununho', 'eric hassli',
                   'donovan ticketts', 'jeff larentowicz', 'guillermo barros schelotto', 'chad marshall', 'juan pablo angel', 'javier morales', 'jonathan bornstein', 'edson buddle', 'bobby convey', 'marco pappa', 'sebastien le toux', 'david ferreira', 'shalrie joseph', 'wilman conde', 'brian ching', 'kevin alston', 'jaime moreno',
                   'zach thorton', 'wilman conde', 'bakary soumare', 'will johnson', 'freddie ljungberg', 'conor casey', 'davy arnaud', 'fredy montero', 'stuart holden', 'jhon kennedy hurtado', 'cuauhtemoc blanco', 'javier morales', 'pat onstad', 'brian ching',
                   'matt reis', 'frankie hejduk', 'christian gomez', 'steve ralston', 'juan toja', 'jim brennan', 'jimmy conrad', 'jonathan bornstein', 'edson buddle', 'pat onstad', 'pablo mastroeni', 'kenny cooper', 'jon busch', 'maurice edu', 'luciano emilio', 'sacha kljestan', 'robbie rogers', 'gonzalo segares',
                   'eddie johnson', 'juan toja', 'ricardo clark', 'ronnie obrien', 'jonathan bornstein', 'matt reis', 'cobi jones', 'pablo mastroeni', 'christian gmez', 'eddie pope', 'kevin hartman'],
           'nba': ['luka doncic', ' luka ','stephen curry', 'steph curry', ' steph ','giannis antetokounmpo', 'giannis', 'nikola jokic', 'lebron james', 'lebron', 'kingjames', 'chris paul', 'cp3', 'jaylen brown', 'paul george', 'damian lillard', 'dame','domantas sabonis', 'rudy gobert', 'gobert','kyrie irving', 'kyrie', 'bradley beal', 'kawhi leonard', 'kawhi', 'jayson tatum', 'tatum', 'zion williamson', 'zion', 'james harden', 'harden', 'donovan mitchell', 'zach lavine', 'nikola vucevic', 'julius randle', 'mike conley', 'devin booker', 'anthony davis', 'kevin durant', 'durant','joel embiid', 'embiid', 'ben simmons',
                   'russell westbrook', 'westbrook', 'domantas sabonis', 'kemba walker', 'pascal siakam', 'trae young', 'kyle lowry', 'khris middleton', 'jimmy butler', 'bam adebayo', 'brandon ingram',
                   'klay thompson', 'karl-anthony towns', 'lamarcus aldridge', 'dwayne wade', 'paul george', 'blake griffin', 'dangelo russell', "d'angelo russell", 'dirk nowitzki', 'victor oladipo',
                   'andre drummond', 'goran dragix', 'demar derozan', 'draymond green', 'al horford', 'demarcus cousins', 'kevin love', 'kristaps przingis', 'john wall',
                   'marc gasol', 'gordon hayward', 'deandre jordan', 'carmelo anthony', 'isiah thomas', 'paul millsap',
                   'kobe bryant', 'kobe', 'pau gasol', 'chris bosh',
                   'tim duncan', 'duncan', ' dirk ', ' melo ', 'kyle korver', 'jeff teague', 
                   'joakim noah', 'roy hibbert', 'joe johnson', 'tony parker',
                   'dwight howard', 'david lee', 'zach randolph', 'kevin garnett', 'garnett', 'luol deng', 'tyson chandler', 'jrue holiday', 'brook lopez', 'rajon rondo', 'rondo',
                   'andrew bynum', 'steve nash', 'derrick rose', 'deron williams', 'andre iguodala', 'paul pierce', 'joe johnson',
                   'manu ginobili', 'amare stoudemire', "amar'e stoudemire", 'ray allen', 'yao ming',
                   'gerald wallace', 'chauncey billups', 'chris kaman', 'jason kidd', 'allen iverson', 'brandon roy',
                   'david west', 'shaquille oneal', "shaquille o'neal", 'shaq', 'rashard lewis', 'devin harris', 'mo williams', 'danny granger', 'jameer nelson',
                   'richard hamilton', 'rasheed wallace', 'antawn jamison', 'carlos boozer', 'caron butler',
                   'tracy mcgrady', 'shawn marion', 'josh howard', 'mehmet okur', 'gilber arenas', 'jermain oneal', "jermaine o'neal", 'vince carter', 'richard hamilton'],
           'nfl': ['lamar jackson', 'russell wilson', 'drew brees', 'brees', 'kirk cousins', 'patrick mahomes', 'mahomes', 'aaron rodgers', 'ryan tannehill', 'deshaun watson', 'christian mccaffrey', 'derrick henry', 'nick chubb', 'dalvin cook', 'ezekiel elliott', 'mark ingram', 'alvin kamara', 'michael thomas', 'deandre hopkins', 'julio jones', 'chris godwin', 'keenan allen', 'mike evans', 'davante adams', 'dj chark', 'amari cooper', 'kenny golladay', 'tyreek hill', 'jarvis landry', 'courtland sutton', 'george kittle', 'travis kelce', 'mark andrews', 'zach ertz', 'cameron heyward', 'cameron jordan', 'joey bosa', 'danielle hunter', 'calais campbell', 'josh allen', 'nick bosa', 'frank clark', 'everson griffen', 'melvin ingram', 'aaron donald', 'chris jones', 'fletcher cox', 'geno atkins', 't.j. watt', 'matt judon', 'von miller', 'darius leonard', 'chandler jones', 'bobby wagner', 'eric kendricks', 'luke kuechly', 'donta hightower', 'khalil mack', 'jaylon smith', 'joe haden', 'earl thomas', 'stephon gilmore', 'jamal adams', 'minkah fitzpatrick', 'tredavious white', 'marcus peters', 'richard sherman', 'marlon humphrey', 'marson lattimore', 'budda baker', 'jalen ramsey', 'xavier rhodes', 'justin tucker',
                   'tom brady', 'brady', 'jared goff', 'andrew luck', 'dak prescott', 'philip rivers', 'todd gurley', 'saquon barkley', 'james conner', 'melvin gordon', 'julio jones', 'antonio brown', 'juju smith-schister', 'adam thielen', 'eric ebron', 'j.j. watt', ' watt ', 'myles garrett', 'demarcus lawrence', 'deforest buckner', 'kawann short', 'ryan kerrigan', 'jadeveon clowney', 'dee ford', 'olivier vernon', 'c.j. mosley', 'patrick peterson', 'chris harris jr.', 'darius slay', 'denzel ward', 'jamal adams', 'landon collins', 'derwin james', 'eric weddle',
                   'carson wentz', 'ben roethlisberger', 'alex smith', 'leveon bell', 'kareem hunt', 'lesean mccoy', 'doug baldwin', 'larry fitzgerald', 'aj green', 'ty hulton', 'rob gronkowski', 'gronl', 'jimmy graham', 'jason witten', 'joey bosa', 'michael bennett', 'yannick ngakoue', 'malik jackson', 'mike daniels', 'gerald mccoy', 'thomas davis', 'terrell suggs', 'ryan shazier', 'deion jones', 'kwon alexander', 'joe schobert', 'aj bouye', 'aqib talib', 'micah hyde', 'leanu neal', 'earl thomas', 'greg zuerlein', 'matthew slater', 
                   'matt ruan', 'derek carr', 'andy dalton', 'david johnson', 'demarco murray', 'jay ajayi', 'devonta freeman', 'jordan howard', 'darre sproles', 'odell beckam jr.', 'dez bryant', 'emmanuel sanders', 'demaryius thomas', 'greg olsen', 'jordan reed', 'vic beasley', 'cliff avril', 'cameron wake', 'carlos dunlap', 'leonard williams', 'ndamukong suh', 'bran orakpo', 'sean lee', 'janoris jenkins', 'eric berry', 'devin mccourty', 'reggie nelson', 'ha ha clinton-dix', 
                   'cam newton', 'carson palmer', 'teddy bridgewater', 'eli manning', 'manning', 'tyrod taylor', 'jameis winston', 'doug martin', 'adrian peterson', 'jonathan stewart', 'brandon marshall', 'calvin johnson', 'allen robinson', 'ezekiel ansah', 'everson griffen', 'tamba hali', 'julius peppers', 'demarcus ware', 'derrick johnson', 'clay matthews', 'navorro bowman', 'justin houston', 'lavonte david', 'jamie collins', 'elvis dumervil', 'vontae davis', 'brent grimes', 'darelle revis', 'dominique radgers-cromarie', 'desmond trufant', 'jason verrett', 'kam chancellor', 'charles woodson', 'tyrann mathieu', 'josh norman', 'tyler lockett',
                   'tony romo', 'peyton manning', 'matthew stafford', 'marshawn lynch', 'justin forsett', 'jamaal charles', 'arian foster', 'alfred morris', 'jordy nelson', 'devin hester', 'randall cobb', 'golden tate', 'martellus bennet', 'julius thomas', 'mario williams', 'marcell dareus', 'sheldon richardson', 'kyle williams', 'dontari poe', 'lawrence timmons', 'antonie cromartie', 'sam shields', 'adam vinatieri',
                   'nick foles', 'matt forte', 'frank gore', 'josh gordon', 'andre johnson', 'desean jackson', 'alshon jeffrey', 'tony gonzalez', 'vernon davis', 'robert quinn', 'greg hardy', 'justin smith', 'haloti ngata', 'robert mathis', 'john abraham', 'terrell suggs', 'patrick willis', 'paul posluszny', 'brandon flowers', 'troy polamalu',
                   'robert griffin iii', 'rg3', 'matt schaub', 'ray rice', 'reggie wayne', 'vincent jackson', 'victor cruz', 'wes welker', 'heath miller', 'vince wilfork', 'aldon smith', 'robert matthis', 'jerod mayo', 'charles tillman', 'champ bailey', 'johnathan joseph', 'donte whitner', 'ed reed', 
                   'maurice jones-drew', 'willis mcgahee', 'mike wallace', 'steve smith', 'roddy white', 'antonio gates', 'jared allen', 'jason babin', 'dwight freeney', 'richard seymour', 'lance briggs', 'ray lewis', 'brian urlacher', 'brandon browner', 'brain dawkins', 'adrian wilson', 'michael vick', 'matt cassel', 'michael turner', 'steven jackson', 'chris johnson', 'miles austin', 'justin tuck', 'darnell dockett', 'james harrison', 'jon beason', 'london fletcher', 'asante samuel', 'nnamdi asomugha', 'deangelo hall',
                   'brett favre', 'david garrard', 'donovan mcnabb', 'vince young', 'vincent jackson', 'sidney rice', 'shad johnson', 'dallas clark', 'vernon davis', 'casey hampton', 'brian cushing', 'demeco ryans', 'jonathan vilma',
                   'albert haynesworth', 'joey porter', 'anquan boldin', 'kerry collins', 'kurt warner',
                   'randy moss', 'bob sanders', 'ladainian tomlinson', 'terrell owens', 'mike vrabel', 'brian westbrook', 'shawne merriman', 'fred taylor', 'joseph addai', 'jeff garcia', 'matt hasselbeck', 'torry holt', 'tj houshmandzadeh', 'john lynch'],
           'nhl': ['leon draisaitl', 'mark giordano', 'tomas hertl', 'quinn hughes', 'anze kopitar', 'jacob markstrom', 'connor mcdavid', 'max pacioretti', 'elias pettersson', 'david rittich', 'matthew tkachuk', 'frederik anderson', 'tyler bertuzzi', 'anthony duclair', 'jack eichel', 'victor hedman', 'jonathan huberdeau', 'mitch marner', 'david pastrnak', 'brady tkachuk', 'andrei vasilevskiy', 'shea weber',
                   'sebastian aho', 'cam atkinson', 'mathew barzal', 'john carlson', 'sidney crosby', 'claude giroux', 'braden holtby', 'set jones', 'kris letang', 'henrik lundqvist', 'kyle palmieri', 'devan dubnyk', 'miro heiskanen', 'roman josi', 'patrick kane', 'gabriel landeskog', 'nathan mackinnon', 'ryan oreilly', 'mikko rantanen', 'pekka rinne', 'mark sheifele', 'blake wheeler',
                   'brock boeser', 'brent burns', 'drew doughty', 'oliver ekman-larsson', 'marc-andre fleury', 'johnny gaudreau', 'anze kopitar', 'connor mcdavid', 'james neal', 'rickard rakell', 'mike smith', 'aleksander barkov', 'mike green', 'erik karlsson', 'nikita kucherov', 'brad marchand', 'auston matthews', 'brayden point', 'carey price', 'steven stamkos', 'connor hellebuyck', 'john klingberg', 'pekka rinne', 'alex pietragelo', 'brayden schenn', 'tyler seguin', 'eric staal', 'pk subban', 'blake wheeler', 'josh bailey', 'brian boyle', 'noah hanifin', 'braden holtby', 'alex ovechkin', 'john tavares', 'zach werenski',
                   'sergei bobrovsky', 'justin faulk', 'taylor hall', 'seth jones', 'wayne simmonds', 'jeff carter', 'cam fowler', 'bo horvat', 'martin jones', 'ryan kesler', 'joe pavelski', 'mike smith', 'corey crawford', 'duncan keith', 'patrik laine', 'ryan suter', 'vladimir tarasenko', 'jonathan toews', 'victor hedman', 'nikita kucherov', 'brad marchand', 'auston matthews', 'frans nielsen', 'kyle okposo', 'tuuka rask', 'shea weber',
                   'johnny gaudreau', 'john gibson', 'mark giordano', 'corey perry', 'jonathan quick', 'john scott', 'daniel sedin', 'patrice berderon', 'ben bishop', 'aaron erkblad', 'joromir jagr', 'erik karlsson', 'leo komarov', 'dylan larkin', 'roberto luongo', 'ryan oreilly', 'nicklas backstrom', 'braden holtby', 'evgeny kuznetsov', 'evgeni malkin', 'ryan mcdonagh', 'brandon saad', 'cory schneider', 'john tavares', 'jamie benn', 'dustin byfluglien', 'matt duchene', 'roman josi', 'james neal', 'pekka rinne', 
                   'aaron ekblad', 'filip forsberg', 'ryan getzlaf', 'jaroslav halak', 'tyler johnson', 'roberto luongo', 'rick nash', 'bent seabrook', 'ryan suter', 'jakub voracek', 'dustin byfluglien', 'oliver ekman-larsson', 'brian elliott', 'nick foligno', 'zemgus girgensons', 'ryan johansen', 'phil kessel', 'anze kopitar', 'bobby ryan', 'kevin shattenkirk', 'radim vrbata',
                   'jamie benn', 'brian campbell', 'zdeno chara', 'pavel datsyuk', 'jordan eberle', 'marian gaborik', 'marian hossa', 'jimmy howard', 'jarome iginla', 'joffrey lupol', 'evgeni malkin', 'dion phaneuf', 'tim thomas', 'kimmo timonen', 'dennis wideman', 'daniel alfredsson', 'logan couture', 'alexander edler', 'dan girardi', 'scott hartnell', 'erik karlsson', 'milan michalek', 'jason pominville', 'jonathan quick', 'daniel sedin', 'henrick sedin', 'jason spezza', 'john tavares', 'keith yandle',
                   'daniel briere', 'matt duchene', 'loui eriksson', 'martin havlat', 'nicklas lidstrom', 'brad richards', 'henrick sedin', 'martin st. louis', 'david backes', 'dan boyle', 'patrick elias', 'mike green', 'kris letang', 'daniel sedin', 'patrick sharp', 'jeff skinner', 'eric staal', 'marc staal', 'paul stastny', 'cam ward',
                   'jay bouwmeester', 'dany heatley', 'tomas kaberle', 'mike komisarek', 'ilya kovalchuk', 'alex kovalev', 'vincent lecavalier', 'andrei markov', 'zach parise', 'marc savard', 'thomas vanek', 'niklas backstrom', 'dan boyle', 'dustin brown', 'brian campbell', 'shane doan', 'ryan getzlaf', 'sean-sebastien giguere', 'milan hejduk', 'jarome iginla', 'patrick marleau', 'mike modano', 'scott niedermayer', 'stephane robidas', 'sheldon souray', 'joe thorton',
                   'rick dipietro', 'scott gomez', 'sergei gonchar', 'marian hossa', 'tomas kaberle', 'ilya kovalchuk', 'andrei markov', 'mike richards', 'marc savard', 'jason spezza', 'tomas vokoun', 'jason arnott', 'pavel datsyuk', 'marian gaborik', 'shawn horcoff', 'ed jovanovski', 'manny legace', 'evgeni nabokov', 'scott niedermayer', 'chris osgood', 'chis pronger', 'mike ribeiro', 
                   'philippe boucher', 'jonathan cheechoo', 'bill guerin', 'ed javonovski', 'miikka kiprusoff', 'andy mcdonald', 'yanic perreault', 'brian rolston', 'joe sakic', 'teemy selanne', 'marty turco', 'lubomir visnovsky', 'jason blake', 'martin brodeur', 'simon gagne', 'cristobal huet', 'ryan miller', 'brian rafalski', 'brendan shanahan', 'justin williams'],
           'nwsl': ['abby dahlkemper', 'crystal dunn', 'julie ertz', 'indsey horan', 'rose lavelle', 'carli lloyd', 'kristie mewis', 'alex morgan', 'alyssa naeher', 'christen press', 'megan rapinoe', 'becky sauerbrunn', 'sophia smith', 'emily sonnett', 'lynn williams', 'casey krueger', 'catarina macario', 'margaret purce', 'jane campbell', 'alana cook', 'tierna davidson', 'emily fox', 'ali krieger', 'sam mewis', 'kelly ohara', 'tobin heath', 'jaelin howell', 'adrianna franch', 'mallor pugh', 'jessica mcdonald', 'ashlyn harris', 'andi sulliban', 'morgan gautrat', 'allie long', 'kristen hamilton', 'mccall zerboni', 'danielle colaprico', 'hailie mace', 'amy rodriguez', 'sofia huerta', 'merritt mathias', 'savannah mccaskill', 'haley hanson', 'tegan mcgrady', 'ashley hatch', 'taylor smith', 'sydney leroux', 'meghan klingenberg', 'megan oyster', 'kealia watt', 'whitney engen', 'heather oreilly', 'hope solo', 'jaelene daniels', 'stephanie mccaffrey', 'abby wambach', 'lori chalupny', 'lauren holiday', 'gina lewandowski', 'shannon boxx', 'christie pearce', 'rachel van hollebeke', 'stephanie cox', 'jillian loyden', 'sarah hagen', 'erika tymrak', 'yael averbuch', 'amber brooks', 'leigh ann brown', 'nicole barnhart', 'lori lindsey', 'amy lepeilbet', 'heather mitts', 'lindsay tarpley', 'brittany kolmel', 'kristine lilly', 'kate markgraf', 'meghan schnur', 'sarah huffman', 'casey loyd', 'cat whitehill', 'ella masar', 'lacey white', 'angela hucles', 'christine nairn', 'leslie osborne', 'marian dougherty', 'christina dimartino', 'natasha kai', 'angie kerr', 'kendall fletcher', 'tina ellertson', 'aly wagner', 'briana scurry', 'marci jobson', 'joanna lohman', 'india trotter'],
           'wnba': ['sue bird', 'tamika catchings', 'tina thompson', 'diana taurasi', 'lisa leslie', 'seimone augustus', 'yolanda griffith', 'katie smith', 'lauren jackson', 'cappie pondexter', 'candice dupree', 'tina charles', 'taj mcwilliams-franklin', 'becky hammon', 'sylvia fowles', 'maya moore', 'elena delle donne', 'brittney griner', 'nneka ogwumike', 'katie douglas', 'lindsay whalen', 'rebekkah brunson', 'candace parker', 'angel mccoughtry', 'cheryl ford', 'deanna nolan', 'alana beard', 'swin cash', 'sskylar diggins-smith', 'sophia young', 'penny taylor', 'erika de souza', 'danielle robinson', 'liz cambage', 'krista toliver', 'dewanna bonner', 'kaylamcbride', 'chelsea gray', 'allie quigley', 'delisha milton-jones', 'tammy sutton-brown', 'asjhi jones', 'crystal langhorne', 'epiphanny prince', 'courtney vandersloot', 'glory johnson', 'ivory latta', 'shoni schimmel', 'stefanie dolson', 'chiney ogwumike', 'breanna stewart', 'jonquel jones', 'alyssa thomas', 'jewell loyd', 'aja wilson', 'kara brazxton', 'anna deforge', 'kara lawson', 'nicky anosike', 'shameka christon', 'charde houston', 'sancho lyttle', 'jia perkins', 'nicole powell', 'danielle adams', 'essence carson', 'renee montgomery', 'allison hightower', 'shavonte sellous', 'jessica breland', 'briann january', 'alex bently', 'kelsey bone', 'marissa coleman', 'jantel lavender', 'emma meeseman', 'plenette pierson', 'riquna williams', 'layshia larendon', 'tiffany hayes', 'sugar radgers', 'jasmine thomas', 'elizabeth williams', 'napheesa collier', 'diamon deshields', 'natasha howard', 'kia nurse', 'odyssey sims', 'erica wheeler']}
    k1 = list(sleague.keys())
    random.shuffle(k1)
    k2 = list(sleague2.keys())
    random.shuffle(k2)
    for k in k1:
        for i in sleague[k]:
            if i in t.lower():
                return k
            
    for k in k2:
        for i in sleague2[k]:
            if i[0] in t.lower() and i[1] in t.lower():
                return k
            
    for k in kps.keys():
        for i in kps[k]:
            intweet = True
            for j in i.split(' '):
                if j not in t.lower():
                    intweet = False
            if intweet:
                return k
    return None

def contract_focus(x):
    for i in ['signs', 'signed', 'signing', 'contract', 
              'GM', 
              'trade', 'trading', 'traded',
              'released', 'releasing', 'cut']:
        if i in x:
            return True
        
    return False
if __name__ == '__main__':
    
    df = pickle.load(open('espn_tweets_96209.pickle', 'rb'))
    
    df['league'] = df.text.apply(lambda x: assign_league(x))
    df['gmfocus'] = df.text.apply(lambda x: contract_focus(x))
    

#%%

    import seaborn as sns
    import numpy as np
    import matplotlib.pyplot as plt
    
    df['month'] = df.date.apply(lambda x: x.month)
    df['year'] = df.date.apply(lambda x: x.year)
    df['day'] = df.date.apply(lambda x: x.dayofweek)
    df['my'] = df.date.apply(lambda x: pd.Timestamp(year=x.year, month = x.month, day = 1))
    
    gdf = df[['tid', 'league','month', 'year']].groupby(['league', 'month','year']).count().reset_index()
    
    leagues = ['nfl', 'mlb', 'nhl', 'mls', 'nba']#, 'wnba', 'nwsl']
    
    ayticks = {'nfl': ['', '0', '50', '100', '150', '200', '250', '300'],
              'mlb': ['', '0', '20', '40', '60', '80', '100', '120', '140'],
              'nhl': ['', '0', '10', '20','30', '40', '50', '60', '70'],
              'mls': ['', '0', '10', '20', '30', '40'],
              'nba': ['', '0', '50', '100', '150', '200', '250', '300', '350']}
    
    fig, axs = plt.subplots(2,3)
    for i in range(len(leagues)):
        
        r = int(np.floor(i/3))
        c = i%3
        
        
        sns.lineplot(x = 'month', 
                     y = 'tid', 
                     hue = 'year', 
                     data = gdf[gdf.league == leagues[i]],
                     ax = axs[r,c], palette = sns.color_palette('Blues', as_cmap = True))
        axs[r,c].set_title(leagues[i].upper(), fontsize = '32')
        axs[r,c].set_ylabel('Number of Tweets', fontsize = '28')
        axs[r,c].set_xlabel('Month', fontsize = '28')
        axs[r,c].set_xticklabels(labels = ['0', '2', '4', '6', '8', '10', '12'], 
                                 fontdict = {'fontsize': 24})
        axs[r,c].set_yticklabels(labels = ayticks[leagues[i]], 
                                  fontdict = {'fontsize': 24})
        
    #%%
    colors = {'nfl': "#BA4311", 'nba': "#EE6730", 'nhl': "#2B2D2F", "mlb": "#000089", 'mls': '#B30838'}
    plt.figure()
    sns.lineplot(x = 'month', 
                 y = 'tid', 
                 hue = 'league', 
                 data= gdf[gdf.league.isin(leagues)], 
                 palette = colors,
                 linewidth = 6)
    plt.ylabel('Number of Tweets', fontsize = 26)
    plt.yticks(fontsize = 24)
    plt.xticks(fontsize = 24)
    plt.xlabel('Month', fontsize = 26)
    plt.title('Tweet Volume by Month per league', fontsize = 28)
    plt.legend(fontsize = 24)
    
    #%%
    plt.figure()
    sns.pointplot(x = 'year', 
                  y = 'tid', 
                  hue = 'league', 
                  data= gdf[(gdf.league.isin(leagues)) & (gdf.year < 2021)].groupby(['year', 'league']).sum().reset_index(),
                  palette = colors,
                  scale = 2)
    plt.ylabel('Number of Tweets', fontsize = 26)
    plt.yticks(fontsize = 24)
    plt.xticks(fontsize = 24)
    plt.xlabel('Year', fontsize = 26)
    plt.title('Tweet Volume by year per league', fontsize = 28)
    plt.legend(fontsize = 24)

#%%
    gdf = df[['tid', 'league', 'day']].groupby(['league', 'day']).count().reset_index()
    gdf['Day of Week'] = gdf.day.map({0: 'Monday', 
                                     1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'})
    sns.pointplot(x = 'Day of Week', 
                  y = 'tid', 
                  hue = 'league', 
                  data = gdf[gdf.league.isin(leagues)],
                  palette = colors)
    plt.ylabel('Number of Tweets')


    #%%
    colors = {'nfl': "#BA4311", 'nba': "#EE6730", 'nhl': "#2B2D2F", "mlb": "#000089", 'mls': '#B30838'}
    gdf = df[df.league.isin(['nfl', 'nba', 'mls', 'mlb', 'nhl'])][['tid', 'league']].groupby('league').count().reset_index().sort_values('tid', ascending = False)
    
    plt.figure()
    sns.barplot(x = 'league', y = 'tid', data = gdf, palette = colors, linewidth = 2, edgecolor = '.2')
    plt.ylabel('Number of Tweets')
    plt.title('Total Tweets since 2007 by League')
    #%%
    gdf = df[df.league.isin(['nfl', 'nba', 'mls', 'mlb', 'nhl'])][['league', 'num_retweets', 'num_likes']].groupby('league').max().reset_index()
    
    fig, axs = plt.subplots(1,2)
    sns.barplot(ax = axs[0], x = 'league', y = 'num_retweets', data = gdf.sort_values('num_retweets', ascending = False), palette = colors)
    sns.barplot(ax = axs[1], x = 'league', y = 'num_likes', data = gdf.sort_values('num_likes', ascending = False), palette = colors)
    axs[0].set_title('Number of Retweets')
    axs[1].set_title('Number of Likes')
    axs[0].set_ylabel('Number of Retweets')
    axs[1].set_ylabel('Number of Likes')

    
    #%%
    gdf = df[['num_likes', 'league','month', 'year']].groupby(['league', 'month','year']).median().reset_index()
    
    leagues = ['nfl', 'mlb', 'nhl', 'mls', 'nba', 'wnba', 'nwsl']
    
    fig, axs = plt.subplots(3,3)
    for i in range(len(leagues)):
        
        r = int(np.floor(i/3))
        c = i%3
        
        axs[r,c].set_title(leagues[i])
        sns.lineplot(x = 'month', 
                     y = 'num_likes', 
                     hue = 'year', 
                     data = gdf[gdf.league == leagues[i]],
                     ax = axs[r,c])
    
    #%%
    gdf = df[['tid', 'league']].groupby('league').count().reset_index().sort_values('tid', ascending = False)
    gdf = gdf[gdf.league.isin(['nba', 'wnba', 'nwsl', 'mls'])]
    
    def get_gender(x):
        if x in ['nba', 'mls']:
            return 'men'
        else:
            return 'women'
        
    def get_sport(x):
        if x in ['nba', 'wnba']:
            return 'basketball'
        else:
            return 'soccer'
    gdf['gender'] = gdf.league.apply(lambda x: get_gender(x))
    gdf['sport'] = gdf.league.apply(lambda x: get_sport(x))
    
    fig, axs = plt.subplots(1,2)
    
    sns.barplot(ax = axs[0], x = 'gender', y = 'tid', data = gdf[gdf.sport == 'basketball'])
    sns.barplot(ax = axs[1], x = 'gender', y = 'tid', data = gdf[gdf.sport == 'soccer'])    
    
    
    #%%
    from numpy import median
    
    gdf = df[['league', 'num_retweets', 'num_likes']]
    gdf = gdf[(gdf.league.isin(['nba', 'wnba', 'nwsl', 'mls']))]
    def get_gender(x):
        if x in ['nba', 'mls']:
            return 'men'
        else:
            return 'women'
        
    def get_sport(x):
        if x in ['nba', 'wnba']:
            return 'basketball'
        else:
            return 'soccer'
    gdf['gender'] = gdf.league.apply(lambda x: get_gender(x))
    gdf['sport'] = gdf.league.apply(lambda x: get_sport(x))
    
    fig, axs = plt.subplots(2,2)
    sns.barplot(ax = axs[0,0], x = 'gender', y = 'num_retweets', data = gdf[gdf.sport == 'basketball'], order = ['men', 'women'], estimator = median)
    sns.barplot(ax = axs[0,1], x = 'gender', y = 'num_retweets', data = gdf[gdf.sport == 'soccer'], order = ['men', 'women'], estimator = median)
    sns.barplot(ax = axs[1,0], x = 'gender', y = 'num_likes', data = gdf[gdf.sport == 'basketball'], order = ['men', 'women'], estimator = median)
    sns.barplot(ax = axs[1,1], x = 'gender', y = 'num_likes', data = gdf[gdf.sport == 'soccer'], order = ['men', 'women'], estimator = median)
    axs[0,0].set_title('Basketball')
    axs[0,1].set_title('Soccer')
    
    #%%
    
    gdf = df[['tid', 'league','my']].groupby(['league', 'my']).count().reset_index()
    
    adf = gdf.groupby(['my']).sum()
    ddf = pd.merge(gdf, adf, on = ['my'])
    
    ddf['per_vol'] = ddf.tid_x/ddf.tid_y
    a = pd.pivot_table(data = ddf, values = 'per_vol', index = 'my', columns = 'league')
    
    a.plot.area(sort_columns = False)
    
    
    #%%
    
    gdf = df[['tid', 'league', 'my', 'gmfocus']].groupby(['my', 'gmfocus']).count().reset_index()
    
    sns.lineplot(x = 'my', y = 'tid', data = gdf[gdf.gmfocus == True])