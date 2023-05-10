from cProfile import label
from gc import callbacks
from matplotlib.patheffects import PathEffectRenderer
from regex import F
import tensorflow as tf
import pandas as pd
import numpy as np
import os 
from numbers_parser import Document

country_name=['Netherlands', 'Switzerland', 'Poland', 'France', 'Scotland', 'Germany', 'Belgium', 'England', 'Portugal', 'Italy', 'Spain']
league_name=['Switzerland Super League', 'Poland Ekstraklasa', 'France Ligue 1', 'Scotland Premier League', 'Germany 1. Bundesliga', 'Belgium Jupiler League', 'England Premier League', 'Portugal Liga ZON Sagres', 'Netherlands Eredivisie', 'Italy Serie A', 'Spain LIGA BBVA']
home_team=['BSC Young Boys', 'FC Aarau', 'FC Luzern', 'Neuchâtel Xamax', 'FC Basel', 'AC Bellinzona', 'FC Zürich', 'FC Sion', 'FC Vaduz', 'Grasshopper Club Zürich', 'Legia Warszawa', 'Lech Poznań', 'AJ Auxerre', 'Girondins de Bordeaux', 'Le Havre AC', 'Le Mans FC', 'AS Monaco', 'AS Nancy-Lorraine', 'Stade Rennais FC', 'FC Sochaux-Montbéliard', 'Valenciennes FC', 'Wisła Kraków', 'Śląsk Wrocław', 'Widzew Łódź', 'Piast Gliwice', 'Falkirk', 'Heart of Midlothian', 'Kilmarnock', 'Aberdeen', 'Olympique Lyonnais', 'Polonia Bytom', 'Arka Gdynia', 'Celtic', 'Hamilton Academical FC', 'FC Bayern Munich', 'Cracovia', 'SV Zulte-Waregem', 'KSV Cercle Brugge', 'FCV Dender EH', 'KSV Roeselare', 'Tubize', 'KVC Westerlo', 'Arsenal', 'Sunderland', 'West Ham United', 'Everton', 'Middlesbrough', 'Bolton Wanderers', 'Hull City', 'SM Caen', 'LOSC Lille', 'FC Nantes', 'OGC Nice', 'Paris Saint-Germain', 'AS Saint-Étienne', 'Toulouse FC', 'Bayer 04 Leverkusen', 'FC Schalke 04', 'VfL Wolfsburg', 'DSC Arminia Bielefeld', 'FC Energie Cottbus', 'Karlsruher SC', 'Ruch Chorzów', 'P. Warszawa', 'GKS Bełchatów', 'Rangers', 'Motherwell', 'Hibernian', 'Inverness Caledonian Thistle', 'St. Mirren', 'KRC Genk', 'KAA Gent', 'Manchester United', 'Aston Villa', 'Chelsea', 'Grenoble Foot 38', 'FC Lorient', 'Olympique de Marseille', 'Eintracht Frankfurt', 'Borussia Mönchengladbach', 'Odra Wodzisław', 'Jagiellonia Białystok', 'Dundee United', 'Hannover 96', 'Vitória Guimarães', 'RSC Anderlecht', 'Standard de Liège', 'Sporting Charleroi', 'Sporting Lokeren', 'Royal Excel Mouscron', 'KV Kortrijk', 'Beerschot AC', 'Liverpool', 'Tottenham Hotspur', 'Newcastle United', 'Blackburn Rovers', 'Fulham', 'West Bromwich Albion', 'Stoke City', 'Hamburger SV', 'Borussia Dortmund', 'VfB Stuttgart', 'SV Werder Bremen', 'Hertha BSC Berlin', 'TSG 1899 Hoffenheim', 'Sporting CP', 'FC Paços de Ferreira', 'RAEC Mons', 'Manchester City', 'Wigan Athletic', '1. FC Köln', 'VfL Bochum', 'Lechia Gdańsk', 'FC Porto', 'Amadora', 'Rio Ave FC', 'Leixões SC', 'Naval 1° de Maio', 'Portsmouth', 'Vitesse', 'CF Os Belenenses', 'KV Mechelen', 'Sampdoria', 'Udinese', 'Roda JC Kerkrade', 'Willem II', 'N.E.C.', 'FC Utrecht', 'SL Benfica', 'Valencia CF', 'RCD Espanyol', 'Atalanta', 'Cagliari', 'Catania', 'Chievo Verona', 'Fiorentina', 'Milan', 'Roma', 'Torino', 'Heracles Almelo', 'Sparta Rotterdam', 'FC Volendam', 'AZ', 'Vitória Setúbal', 'CD Nacional', 'Académica de Coimbra', 'Trofense', 'CA Osasuna', 'RC Deportivo de La Coruña', 'CD Numancia', 'Racing Santander', 'Real Sporting de Gijón', 'Real Betis Balompié', 'Athletic Club de Bilbao', 'Atlético Madrid', 'CS Marítimo', 'SC Braga', 'SC Heerenveen', 'Club Brugge KV', 'Palermo', 'Inter', 'PSV', 'ADO Den Haag', 'FC Twente', 'Feyenoord', 'FC Barcelona', 'Sevilla FC', 'Real Valladolid', 'Bologna', 'Siena', 'Reggio Calabria', 'Napoli', 'Lecce', 'Lazio', 'Juventus', 'Genoa', 'De Graafschap', 'NAC Breda', 'FC Groningen', 'Ajax', 'Villarreal CF', 'Real Madrid CF', 'Getafe CF', 'RC Recreativo', 'Málaga CF', 'UD Almería', 'RCD Mallorca', 'FC St. Gallen', 'RKC Waalwijk', 'Korona Kielce', 'Zagłębie Lubin', 'Sint-Truidense VV', 'Montpellier Hérault SC', '1. FC Nürnberg', '1. FSV Mainz 05', 'SC Freiburg', 'VVV-Venlo', 'Wolverhampton Wanderers', 'RC Lens', 'St. Johnstone FC', "US Boulogne Cote D'Opale", 'União de Leiria, SAD', 'Birmingham City', 'Burnley', 'S.C. Olhanense', 'Livorno', 'Bari', 'Real Zaragoza', 'Parma', 'Xerez Club Deportivo', 'CD Tenerife', 'FC Thun', 'Lierse SK', 'KAS Eupen', 'AC Arles-Avignon', 'Stade Brestois 29', 'Excelsior', 'SC Beira Mar', 'Portimonense', '1. FC Kaiserslautern', 'Blackpool', 'FC St. Pauli', 'Hércules Club de Fútbol', 'Levante UD', 'Real Sociedad', 'Cesena', 'Brescia', 'Servette FC', 'Dunfermline Athletic', 'Oud-Heverlee Leuven', 'FC Lausanne-Sports', 'Podbeskidzie Bielsko-Biała', 'AC Ajaccio', 'FC Augsburg', 'Dijon FCO', 'Gil Vicente FC', 'Queens Park Rangers', 'Évian Thonon Gaillard FC', 'Feirense', 'Swansea City', 'Norwich City', 'Granada CF', 'Rayo Vallecano', 'Novara', 'Waasland-Beveren', 'Ross County FC', 'ES Troyes AC', 'Dundee FC', 'Stade de Reims', 'Pogoń Szczecin', 'Reading', 'SC Bastia', 'PEC Zwolle', 'RC Celta de Vigo', 'Southampton', 'SpVgg Greuther Fürth', 'Pescara', 'Estoril Praia', 'Moreirense FC', 'Fortuna Düsseldorf', 'Zawisza Bydgoszcz', 'Partick Thistle F.C.', 'SC Cambuur', 'Eintracht Braunschweig', 'Go Ahead Eagles', 'En Avant de Guingamp', 'Crystal Palace', 'Hellas Verona', 'Elche CF', 'Cardiff City', 'FC Arouca', 'Sassuolo', 'KV Oostende', 'Górnik Łęczna', 'Leicester City', 'FC Metz', 'FC Dordrecht', 'FC Penafiel', 'SC Paderborn 07', 'Boavista FC', 'SD Eibar', 'Córdoba CF', 'Empoli', 'Lugano', 'Termalica Bruk-Bet Nieciecza', 'Bournemouth', 'Tondela', 'Watford', 'Angers SCO', 'SV Darmstadt 98', 'Uniao da Madeira', 'GFC Ajaccio', 'FC Ingolstadt 04', 'Frosinone', 'Carpi', 'UD Las Palmas']
away_team=['FC Basel', 'FC Sion', 'FC Vaduz', 'FC Zürich', 'Grasshopper Club Zürich', 'Neuchâtel Xamax', 'FC Luzern', 'BSC Young Boys', 'FC Aarau', 'AC Bellinzona', 'P. Warszawa', 'GKS Bełchatów', 'FC Nantes', 'SM Caen', 'OGC Nice', 'FC Lorient', 'Paris Saint-Germain', 'LOSC Lille', 'Olympique de Marseille', 'Grenoble Foot 38', 'AS Saint-Étienne', 'Polonia Bytom', 'Lechia Gdańsk', 'Odra Wodzisław', 'Cracovia', 'Rangers', 'Motherwell', 'Hibernian', 'Inverness Caledonian Thistle', 'Toulouse FC', 'Ruch Chorzów', 'Jagiellonia Białystok', 'St. Mirren', 'Dundee United', 'Hamburger SV', 'Widzew Łódź', 'Sporting Lokeren', 'RSC Anderlecht', 'Standard de Liège', 'KV Kortrijk', 'Royal Excel Mouscron', 'Sporting Charleroi', 'West Bromwich Albion', 'Liverpool', 'Wigan Athletic', 'Blackburn Rovers', 'Tottenham Hotspur', 'Stoke City', 'Fulham', 'Valenciennes FC', 'Le Mans FC', 'AS Monaco', 'AS Nancy-Lorraine', 'Girondins de Bordeaux', 'FC Sochaux-Montbéliard', 'Le Havre AC', 'Borussia Dortmund', 'Hannover 96', '1. FC Köln', 'SV Werder Bremen', 'TSG 1899 Hoffenheim', 'VfL Bochum', 'Wisła Kraków', 'Piast Gliwice', 'Śląsk Wrocław', 'Heart of Midlothian', 'Aberdeen', 'Falkirk', 'Hamilton Academical FC', 'Kilmarnock', 'Beerschot AC', 'RAEC Mons', 'Newcastle United', 'Manchester City', 'Portsmouth', 'Stade Rennais FC', 'Olympique Lyonnais', 'AJ Auxerre', 'Hertha BSC Berlin', 'VfB Stuttgart', 'Legia Warszawa', 'Lech Poznań', 'Celtic', 'FC Energie Cottbus', 'Vitória Setúbal', 'KAA Gent', 'KVC Westerlo', 'KSV Roeselare', 'Tubize', 'KV Mechelen', 'KSV Cercle Brugge', 'FCV Dender EH', 'Middlesbrough', 'Sunderland', 'Bolton Wanderers', 'Hull City', 'Arsenal', 'Everton', 'Aston Villa', 'Karlsruher SC', 'FC Bayern Munich', 'Bayer 04 Leverkusen', 'FC Schalke 04', 'DSC Arminia Bielefeld', 'Borussia Mönchengladbach', 'Arka Gdynia', 'Trofense', 'SC Braga', 'KRC Genk', 'West Ham United', 'Chelsea', 'Eintracht Frankfurt', 'VfL Wolfsburg', 'CF Os Belenenses', 'Académica de Coimbra', 'SL Benfica', 'CD Nacional', 'CS Marítimo', 'Manchester United', 'Club Brugge KV', 'FC Groningen', 'FC Paços de Ferreira', 'SV Zulte-Waregem', 'Inter', 'Palermo', 'FC Twente', 'Ajax', 'De Graafschap', 'PSV', 'FC Porto', 'RCD Mallorca', 'Real Valladolid', 'Siena', 'Lazio', 'Genoa', 'Reggio Calabria', 'Juventus', 'Bologna', 'Napoli', 'Lecce', 'Feyenoord', 'ADO Den Haag', 'SC Heerenveen', 'NAC Breda', 'Amadora', 'Naval 1° de Maio', 'Rio Ave FC', 'Leixões SC', 'Villarreal CF', 'Real Madrid CF', 'FC Barcelona', 'Sevilla FC', 'Getafe CF', 'RC Recreativo', 'UD Almería', 'Málaga CF', 'Vitória Guimarães', 'Sporting CP', 'Heracles Almelo', 'Roma', 'Catania', 'Sparta Rotterdam', 'AZ', 'N.E.C.', 'FC Volendam', 'Racing Santander', 'Real Sporting de Gijón', 'Atlético Madrid', 'Atalanta', 'Cagliari', 'Torino', 'Fiorentina', 'Chievo Verona', 'Sampdoria', 'Udinese', 'Milan', 'Vitesse', 'Willem II', 'FC Utrecht', 'Roda JC Kerkrade', 'RC Deportivo de La Coruña', 'CD Numancia', 'Real Betis Balompié', 'RCD Espanyol', 'Athletic Club de Bilbao', 'Valencia CF', 'CA Osasuna', 'FC St. Gallen', 'Sint-Truidense VV', 'VVV-Venlo', 'Zagłębie Lubin', "US Boulogne Cote D'Opale", 'RKC Waalwijk', 'RC Lens', 'Burnley', 'Montpellier Hérault SC', 'SC Freiburg', '1. FC Nürnberg', '1. FSV Mainz 05', 'Korona Kielce', 'Birmingham City', 'S.C. Olhanense', 'Wolverhampton Wanderers', 'União de Leiria, SAD', 'St. Johnstone FC', 'Bari', 'Parma', 'CD Tenerife', 'Livorno', 'Xerez Club Deportivo', 'Real Zaragoza', 'FC Thun', 'Lierse SK', 'KAS Eupen', 'AC Arles-Avignon', 'Stade Brestois 29', 'Excelsior', 'Portimonense', 'Blackpool', '1. FC Kaiserslautern', 'FC St. Pauli', 'SC Beira Mar', 'Cesena', 'Brescia', 'Hércules Club de Fútbol', 'Levante UD', 'Real Sociedad', 'FC Lausanne-Sports', 'Servette FC', 'Oud-Heverlee Leuven', 'Évian Thonon Gaillard FC', 'Podbeskidzie Bielsko-Biała', 'Norwich City', 'AC Ajaccio', 'Dijon FCO', 'Dunfermline Athletic', 'FC Augsburg', 'Swansea City', 'Gil Vicente FC', 'Queens Park Rangers', 'Feirense', 'Rayo Vallecano', 'Novara', 'Granada CF', 'Waasland-Beveren', 'Dundee FC', 'SC Bastia', 'PEC Zwolle', 'Ross County FC', 'Estoril Praia', 'Stade de Reims', 'ES Troyes AC', 'Southampton', 'Moreirense FC', 'Reading', 'Fortuna Düsseldorf', 'RC Celta de Vigo', 'SpVgg Greuther Fürth', 'Pogoń Szczecin', 'Pescara', 'Zawisza Bydgoszcz', 'Go Ahead Eagles', 'SC Cambuur', 'Partick Thistle F.C.', 'Cardiff City', 'En Avant de Guingamp', 'Eintracht Braunschweig', 'FC Arouca', 'Elche CF', 'Crystal Palace', 'Sassuolo', 'Hellas Verona', 'KV Oostende', 'Górnik Łęczna', 'FC Metz', 'FC Dordrecht', 'Boavista FC', 'FC Penafiel', 'Leicester City', 'Córdoba CF', 'SC Paderborn 07', 'SD Eibar', 'Empoli', 'Lugano', 'Termalica Bruk-Bet Nieciecza', 'Watford', 'Angers SCO', 'GFC Ajaccio', 'FC Ingolstadt 04', 'Bournemouth', 'SV Darmstadt 98', 'UD Las Palmas', 'Carpi', 'Tondela', 'Uniao da Madeira', 'Frosinone']

path = r'FootballDataEurope.csv'

data=pd.read_csv(path)
data.pop('id')
data.pop('season')
data.pop('date')
data.pop('stage')
data.pop('home_team_goal')
data.pop('away_team_goal')

for i in data['country_name']:
    for f in range(len(country_name)):
        if i==country_name[f]:
            data['country_name']=f

for i in data['league_name']:
    for f in range(len(league_name)):
        if i==league_name[f]:
            data['league_name']=f
            
for i in data['home_team']:
    for f in range(len(home_team)):
        if i==home_team[f]:
            data['home_team']=f 
            
for i in data['away_team']:
    for f in range(len(away_team)):
        if i==away_team[f]:
            data['away_team']=f             
data=np.array(data)
print(data)

label=pd.read_csv(path)
label.pop('id')
label.pop('country_name')
label.pop('league_name')
label.pop('season')
label.pop('stage')
label.pop('date')
label.pop('home_team')
label.pop('away_team')
label=np.array(label)
print(label)
print(data.shape,label.shape)

model=tf.keras.models.Sequential()

model.add(tf.keras.layers.Dense(64))
model.add(tf.keras.layers.Dense(2))

model.compile(loss = tf.keras.losses.MeanSquaredError(),
                           optimizer = tf.keras.optimizers.Adam(),metrics=['accuracy'])

model.fit(data,label,epochs=100,batch_size=128,validation_split=0.1)

model.save('bet365_model')
json_model=model.to_json()
with open('fashionmnist_model.json', 'w') as json_file:
    json_file.write(json_model)