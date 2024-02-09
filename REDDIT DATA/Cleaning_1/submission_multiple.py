import zstandard
import os
import json
import csv
from datetime import datetime
import logging.handlers
import pandas as pd

def convert_zst_to_csv(input_file_path, output_file_path, fields, filter_by=None, filter_values=None, batch_size=10000):
    log = logging.getLogger("bot")
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())

    max_window_size = 2 ** 31

    def read_lines_zst(file_name):
        with open(file_name, 'rb') as file_handle:
            reader = zstandard.ZstdDecompressor(max_window_size=max_window_size).stream_reader(file_handle)
            buffer = b''
            while True:
                chunk = reader.read(2 ** 27)
                if not chunk:
                    break
                chunk = buffer + chunk
                lines = chunk.split(b"\n")

                for line in lines[:-1]:
                    yield line.decode(errors='replace')

                buffer = lines[-1]
            reader.close()

    file_lines = 0

    with open(output_file_path, "w", encoding='utf-8', newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(fields)

        for line_number, line in enumerate(read_lines_zst(input_file_path)):
            try:
                obj = json.loads(line)

                if filter_by and filter_values and obj.get(filter_by) in filter_values:
                    output_obj = [str(obj.get(field, '')).replace('\n', '').replace('\r', '') for field in fields]
                    writer.writerow(output_obj)
                    file_lines += 1

                    if file_lines % 100000 == 0:
                        log_time = datetime.utcfromtimestamp(int(obj.get('created_utc', 0))).strftime('%Y-%m-%d %H:%M:%S')
                        print(f"{log_time} : {file_lines:,}")

            except json.JSONDecodeError:
                pass  # Handle JSON decode errors if needed

    return


columns = ['author', 'id', 'selftext', 'subreddit', 'subreddit_id', 'title']

# Filter values
filter_by = 'subreddit'



subreddit_dict = {
    'AmsterdamEnts': 'netherlands',
    'ResearchChemicalsNL': 'netherlands',
    'DutchEnts': 'netherlands',
    'germantrees': 'germany',
    'PsychonautDE': 'germany',
    'Drogen': 'germany',
    'MDMA_de': 'germany',
    'sucht': 'germany',
    'psychnaut_de': 'germany',
    'ResearchChemicalsFR': 'french',
    'swedents': 'sweden',
    'SwissTrees': 'sweden',
    'droger': 'danish',
    'DanishEnts': 'danish',
    'Crainn': 'ireland',
    'NorwegENTs': 'norway',
    'norwegients': 'norway',
    'ccportugal': 'portugal',
    'uktrees': 'uk',
    'uktreesmeets': 'uk',
    'EdinburghTrees': 'uk',
    'Bristoltrees': 'uk',
    'CoedCymru': 'uk',
    'AberdeenTrees': 'scotland',
    'BelfastEnts': 'north Ireland',
    'nederlands': 'netherlands',
    'thenetherlands': 'netherlands',
    'Belgium2': 'Belgium',
    'belgium': 'Belgium',
    'de': 'Germany',
    'germany': 'Germany',
    'france': 'France',
    'paris': 'France',
    'sweden': 'Sweden',
    'stockholm': 'Sweden',
    'switzerland': 'Switzerland',
    'AskSwitzerland': 'Switzerland',
    'Luxembourg': 'Luxembourg',
    'Luxembourg': 'Luxembourg',
    'spain': 'Spain',
    'es': 'Spain',
    'portugal': 'Portugal',
    'lisboa': 'Portugal',
    'italy': 'Italy',
    'italy': 'Italy',
    'norway': 'Norway',
    'norway': 'Norway',
    'denmark': 'Denmark',
    'denmark': 'Denmark',
    'finland': 'Finland',
    'finland': 'Finland',
    'poland': 'Poland',
    'poland': 'Poland',
    'czech': 'Czechia',
    'czech': 'Czechia',
    'austria': 'Austria',
    'austria': 'Austria',
    'CasualUK': 'UK',
    'unitedkingdom': 'UK'
}

print(subreddit_dict)

filter_values = list(subreddit_dict.keys())


folder_location = "D:/reddit 2019/reddit/submissions/"
folder_location_csv = "C:/Users/Jonathon/OneDrive/UVA/Data System Project/reddit_csv/submission2/"

name_pre = "reddit_submission"
import glob
list_of_zst = glob.glob("{}*.zst".format(folder_location))
number_done = 0 
for x in list_of_zst:
    date_post = x.split("RS_")[-1][:7].replace("-","_")
    name = '{}_{}'.format(name_pre, date_post)
    location_csv = "{}{}.csv".format(folder_location_csv, name)
    
    print(location_csv)
    
    convert_zst_to_csv(input_file_path = x, output_file_path = location_csv,
                       fields=columns, filter_by=filter_by, filter_values=filter_values)
#,
 #                      batch_size = 1000) # batch doesnt really do anything 
    
    #loading in the country
    
    number_done = number_done + 1
    print(number_done)



list_of_csv = glob.glob("{}*.csv".format(folder_location_csv))

for x in list_of_csv:
    print(x)    
    submissions = pd.read_csv(x)
    submissions['Country'] = submissions['subreddit'].map(subreddit_dict)
    submissions.to_csv(x, index=False)







drug_related_subr = ['AmsterdamEnts', 'ResearchChemicalsNL', 'DutchEnts', #netherlands drug
                     'germantrees', 'PsychonautDE', 'Drogen', 'MDMA_de', 'sucht', 'psychnaut_de', #germany drug
                     'ResearchChemicalsFR', #french
                     'swedents','SwissTrees', 'droger', #sweden 
                     'DanishEnts', #danish
                     'Crainn', #ireland
                     'NorwegENTs', 'norwegients', #norway
                     'ccportugal', #portugal
                     'uktrees', 'uktreesmeets','EdinburghTrees', 'Bristoltrees', 'CoedCymru', #uk
                     'AberdeenTrees', #scotland
                     'BelfastEnts' #north Ireland
                     ]
country_related_subr = [
    'nederlands', 'thenetherlands', # all NL
    'Belgium2', 'belgium', # all Belgium
    'de', 'germany', # all German
    'france', 'paris', # France
    'sweden', 'stockholm', # Sweden
    'switzerland', 'AskSwitzerland', # Switzerland
    'Luxembourg', 'Luxembourg', # Luxembourg
    'spain', 'es', # Spain
    'portugal', 'lisboa', # Portugal
    'italy', 'italy', # Italy
    'norway', 'norway', # Norway
    'denmark', 'denmark', # Denmark
    'finland', 'finland', # Finland
    'poland', 'poland', # Poland
    'czech', 'czech', # Czechia
    'austria', 'austria', # Austria
    'CasualUK','unitedkingdom' #uk
]
















