import json

arrayAcara={
	"TemperatureofLove": 0,
	"DoubtfulVictory": 0,
	"NothingtoLose": 0,
	"SweetEnemy": 0,
	"HappySisters": 0,
	"BravoMyLife": 0,
	"Witch'sCourt": 0, 
	"Jugglers": 0,
	"MadDog": 0, 
	"BlackKnight": 0, 
	"DalSoon'sSpring": 0,
	"MyMan'sSecret": 0, 
	"MyGoldenLife": 0, 
	"HateToLoveYou": 0, 
	"Andantae": 0, 
	"TakeCareofMyRefrigerator": 0, 
	"ReturnofSuperman": 0, 
	"FantasticDuo2": 0, 
	"NightGoblin": 0, 
	"Mom'sDiary": 0, 
	"WeeklyIdol": 0, 
	"KnowingBros": 0, 
	"It'sOkaytoGoaLittleCrazy": 0, 
	"WednesdayFoodTalk": 0, 
	"Let'sEatDinnerTogether": 0, 
	"NewJourneytotheWest": 0, 
	"SocietyGame2": 0, 
	"AbnormalSummit": 0, 
	"20thCenturyBoyandGirl": 0, 
	"TwoCops": 0, 
	"I'mNotaRobot": 0, 
	"ReturnofLuckyPot": 0, 
	"BorgMom": 0, 
	"EnemiesFromthePast": 0, 
	"MoneyFlower": 0, 
	"ManWhoSetstheTable": 0, 
	"BecauseThisIsMyFirstLife": 0, 
	"RudeMissYoungAe": 0, 
	"WisePrisonLife": 0, 
	"RevolutionaryLove": 0, 
	"Meloholic": 0, 
	"RunningMan": 0, 
	"MIXNINE": 0, 
	"WannaOneGo": 0, 
	"TheUnit": 0, 
	"MasterKey": 0,
	"1Night2Days": 0, 
	"1N2D": 0
}

fileAcara = "daftar acara korea/acara.txt"


fileName = "classifiedTweet.csv"
with open(fileName, mode='r', encoding='utf-8') as feedsjson:
	feeds = json.load(feedsjson)

for tweet in feeds:
	for acara in tweet["nama_acara"]:
		acaraNoSpace = acara.replace(" ", "")
		arrayAcara[acaraNoSpace] = arrayAcara[acaraNoSpace] + 1

for item in arrayAcara:
	print(item, ",", arrayAcara[item])

