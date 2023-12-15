import mysql.connector
import os
import json
import requests as req
from bs4 import BeautifulSoup as soup
import re

class save:
    @staticmethod
    def connect_to_database():
        try:
                connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='12345',              
                    database='WorldPopulation',
                    port=3306
                )
                return connection
        except mysql.connector.Error as e:
            print(f'Error Occured: {e}')
            return None
        
    @staticmethod
    
    def savetomysql(data_list: list):
        connection = save.connect_to_database()
        if connection:
            try:
                cursor = connection.cursor()

                # Insert into 'countries' table
                country_name = data_list[0][0]
                landarea = data_list[0][1]
                country_query = "INSERT INTO countries (country_name, land_area) VALUES (%s, %s)"
                values = (country_name, landarea)
                cursor.execute(country_query, values)

                # Retrieve the last inserted country_id
                cursor.execute("SELECT LAST_INSERT_ID()")
                country_id = cursor.fetchone()[0]

                # Insert into 'Population' table
                population_query = "INSERT INTO Population (country_id, world_year, global_ranking, population, urban_population, urban_population_percent, fertility_rate) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                for data in data_list:
                    population_values = (country_id, data[2], data[3], data[4], data[5], data[6], data[7])
                    cursor.execute(population_query, population_values)

                connection.commit()
                print('Complete', f'Data has been Added! {country_name}=A{country_id}')

            except mysql.connector.Error as e:
                print('Error', f"Can't Add Data! Check inputs: {e}")

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    def savetotxt(poplist:list, filename:str):
            try:
                base_path = os.getcwd() 
                temp_dir = os.path.join(base_path, 'temp')
                os.makedirs(temp_dir, exist_ok=True)
                file_path = os.path.join(temp_dir, f'{filename}.txt')
                with open(file_path, 'w', encoding='utf-8') as file:
                    for info in poplist:
                        file.write({filename:info})
            except:
                print('error')

    def savetojson(poplist: list, filename: str):
        try:
            base_path = os.getcwd() 
            temp_dir = os.path.join(base_path, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, f'{filename}.json')

            with open(file_path, 'w', encoding='utf-8') as jsonfile:
                for info in poplist:
                    json.dump(info, jsonfile, ensure_ascii=False)
                    jsonfile.write('\n')

            print(f"Data has been saved to {file_path}")
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

class scrape:
    
    def convert_to_int(value):
        try:
            return int(value.replace(',', ''))
        except (ValueError, AttributeError):
            return None
        
    def convert_to_float(value):
        try:
            return float(re.sub("[^0-9.]", "", value))
        except (ValueError, AttributeError):
            return None

    def format1scrapeinfo(sublink: str, country_name, land_area) -> list:
        try:
            information = []
            website = f'https://www.worldometers.info{sublink}'
            req_site = req.get(url=website).text
            content = soup(req_site, 'lxml')
            starter = content.find('div', class_='table-responsive')
            datasource = starter.find('table')

            if datasource:
                insidedata = datasource.find('tbody').find_all('tr')
                for insiderow in insidedata:
                    cell = insiderow.find_all('td')

                    # =====================transform or corrects the format and datatype=============================
                    raw_year = cell[0].text
                    year = scrape.convert_to_int(raw_year)

                    raw_global_ranking = cell[12].text
                    global_ranking = scrape.convert_to_int(raw_global_ranking)

                    raw_population = cell[1].text
                    population = scrape.convert_to_int(raw_population)

                    raw_urbanpop = cell[9].text
                    urbanpop = scrape.convert_to_int(raw_urbanpop)

                    raw_urbanperc = cell[8].text
                    urbanperc = scrape.convert_to_float(raw_urbanperc)

                    raw_fertrate = cell[6].text
                    fertrate = scrape.convert_to_float(raw_fertrate)

                    raw_landsize = land_area
                    landsize = scrape.convert_to_int(raw_landsize)

                    if int(year) > 2019:
                        information.append([country_name, landsize, year, global_ranking, population, urbanpop, urbanperc, fertrate])
                    else:
                        break
                return information
            else:
                print('Error: Unable to find the table on the page.')
        except Exception as e:
            print(f'Error: {e}. Unable to scrape the page: {website}')

    def format2scrapeinfo(sublink:str, country_name, land_area) -> list:
        try:
            information = []
            website = f'https://www.worldometers.info{sublink}'
            req_site = req.get(url=website).text
            content = soup(req_site, 'lxml')
            starter = content.find('div', class_='table-responsive')
            datasource = starter.find('table')

            if datasource:
                insidedata = datasource.find('tbody').find_all('tr')
                for insiderow in insidedata:
                    cell = insiderow.find_all('td')

                    # =====================transform corrects the format and datatype=============================
                    raw_year = cell[0].text
                    year = scrape.convert_to_int(raw_year)

                    raw_global_ranking = cell[9].text
                    global_ranking = scrape.convert_to_int(raw_global_ranking)

                    raw_population = cell[1].text
                    population = scrape.convert_to_int(raw_population)

                    raw_urbanpop = cell[6].text
                    urbanpop = scrape.convert_to_int(raw_urbanpop)

                    raw_urbanperc = cell[5].text
                    urbanperc = scrape.convert_to_float(raw_urbanperc)

                    # no fertility rate
                    fertrate = None

                    raw_landsize = land_area
                    landsize = scrape.convert_to_int(raw_landsize)

                    if int(year) > 2019:
                        information.append([country_name, landsize, year, global_ranking, population, urbanpop, urbanperc, fertrate])
                    else:
                        break
                return information
            else:
                print('Error: Unable to find the table on the page.')
        except Exception as e:
            print(f'Error: {e}. Unable to scrape the page: {website}')