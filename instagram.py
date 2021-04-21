import requests
import psycopg2
import pprint
import locale
import time
from datetime import datetime,date, timedelta

try:
  connection = psycopg2.connect(
      user = "y_ayyoub",
      password = "zer3raiw7YUMPknup",
      host = "reporting.chvcwsrzy2fr.eu-west-1.redshift.amazonaws.com",
      port = "5439",
      database = "reportingprod"
  )
  cursor = connection.cursor()
  print(connection.get_dsn_parameters(),"\n")
  cursor.execute("SELECT version();")
  record = cursor.fetchone()
except(Exception, psycopg2.Error) as error:
  print("Error connecting to PostgreSQL database", error)
  connection = None


def convert_date(day):
  locales = ['us_US']
  for loc in locales:
    locale.setlocale(locale.LC_ALL, loc)
    day_norway = day.strftime("%A %d. %B %Y")

  return  day_norway



def getMediaIDInsights(entity_id):
    entity = entity_id[5]
    token = entity_id[4]
    params = {
        'access_token':token,
        'pretty':1,
        'fields':'timestamp',
        'limit':500000000000
    }
    allMediaID = requests.get(f'https://graph.facebook.com/v9.0/{entity}/media',params=params)
    return allMediaID.json()

def getMediaInfo(entity_id,mediaID):
    entity = entity_id[5]
    token = entity_id[4]
    params = {
        'metric':'engagement,impressions,reach',
        'access_token':token,
    }
    allMediaID = requests.get(f'https://graph.facebook.com/v9.0/{mediaID}/insights',params=params)
    return allMediaID.json()

def getMediaUrl(entity_id,mediaID):
    entity = entity_id[5]
    token = entity_id[4]
    params = {
        'fields':'media_url,id',
        'access_token':token,
    }
    allMediaID = requests.get(f'https://graph.facebook.com/v9.0/{mediaID}',params=params)
    return allMediaID.json()

def saveInstagramMediaInsights(data,entity_id,mediaUrl,mediaInfo,media_id,timestamp):
    account_id = entity_id[5]
    community_id = entity_id[1]
    community_name = entity_id[0]
    cursor = connection.cursor()
    if 'data' in mediaInfo:
        if len(mediaInfo['data']) > 0 :
            engagement = mediaInfo['data'][0]['values'][0]['value']
            impressions = mediaInfo['data'][1]['values'][0]['value']
            reach = mediaInfo['data'][2]['values'][0]['value']
            media_url = ''
            if 'media_url' in mediaUrl:
               media_url = mediaUrl['media_url']
            pg_insert = """ INSERT INTO consultancy_integrations."instamediainsights" (community_id, community_name, account_id,media_url,reach,impressions,engagement,media_id,date)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            inserted_values = (community_id, community_name, account_id, media_url, reach, impressions, engagement, media_id,timestamp)
            cursor.execute(pg_insert, inserted_values)
            connection.commit()

def syncInstagramMediaInsights(entity_id):
    allMediaID = getMediaIDInsights(entity_id)
    if "data" in allMediaID:
        for mediaID in allMediaID['data']:
            timestamp = str(mediaID['timestamp'])
            timestamp = timestamp.split("T")[0]
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d')
            new_date = datetime.strptime("2020-01-01", '%Y-%m-%d')
            if timestamp >= new_date:
                timestamp = timestamp.strftime("%d.%m.%Y")
                mediaUrl = getMediaUrl(entity_id,mediaID['id'])
                mediaInfo = getMediaInfo(entity_id,mediaID['id'])
                media_id = mediaID['id']
                saveInstagramMediaInsights(allMediaID,entity_id,mediaUrl,mediaInfo,media_id,timestamp)

def getFollowerCount(entity_id):
    entity = entity_id[5]
    token = entity_id[4]
    params = {
        'fields':'followers_count',
        'access_token':token,
    }
    allMediaID = requests.get(f'https://graph.facebook.com/v9.0/{entity}',params=params)
    return allMediaID.json()

def saveFollowerCount(data,entity_id):
    account_id = entity_id[5]
    community_id = entity_id[1]
    community_name = entity_id[0]
    today = date.today()
    today = today.strftime("%A %d. %B %Y")
    cursor = connection.cursor()
    if 'followers_count' in data:
        followers_count = data['followers_count']
        pg_insert = """ INSERT INTO consultancy_integrations."instafollower" (community_id, community_name, account_id,followers_name,followers_value,date)
                        VALUES (%s,%s,%s,%s,%s,%s)"""
        inserted_values = (community_id, community_name, account_id,'followers_count',followers_count,today )
        cursor.execute(pg_insert, inserted_values)
        connection.commit()
def syncFollowerCount(entity_id):
    data = getFollowerCount(entity_id)
    saveFollowerCount(data,entity_id)

def sync_instagram_account(entity_id):
    syncInstagramMediaInsights(entity_id)
    # syncFollowerCount(entity_id)
def main():
    instagram_entity = get_instagram_entity()
    for entity in instagram_entity:
        print('---------------------------------')
        print(entity[0])
        sync_instagram_account(entity)

def get_instagram_entity():
  cursor = connection.cursor()  
  pg_select = """ select * from consultancy_integrations."alex_fb_tokens" """ 
#   pg_select = """ select * from consultancy_integrations."alex_fb_tokens" limit 100 OFFSET 19 """ 
#   SELECT * from consultancy_integrations.alex_fb_tokens limit 100 OFFSET 19
  cursor.execute(pg_select)
  record = cursor.fetchall()
  return record

if __name__ == '__main__':
    main()
