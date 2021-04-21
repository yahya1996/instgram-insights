# instgram-insights with redshift , posgres

you only have to setup up and create redshift , postgres DB 

with the following tables:

-instafollower

-----------------+------------------------+-----------+----------+---------
 
 community_name  | character varying(256) |           |          | 
 
 community_id    | integer                |           |          | 
 
 account_id      | character varying(256) |           |          | 
 
 followers_value | character varying(256) |           |          | 
 
 followers_name  | character varying(256) |           |          | 
 
 date            | character varying(256) |           |          | 

-instamediainsights


     Column     |          Type           | Collation | Nullable | Default 
----------------+-------------------------+-----------+----------+---------
 community_name | character varying(256)  |           |          | 
 community_id   | integer                 |           |          | 
 account_id     | character varying(256)  |           |          | 
 media_id       | character varying(256)  |           |          | 
 media_url      | character varying(3000) |           |          | 
 date           | character varying(256)  |           |          | 
 engagement     | character varying(256)  |           |          | 
 impressions    | character varying(256)  |           |          | 
 reach          | character varying(256)  |           |          | 


-alex_fb_tokens

     Column     |          Type          | Collation | Nullable | Default 
----------------+------------------------+-----------+----------+---------
 community_name | character varying(60)  |           |          | 
 community_id   | integer                |           |          | 
 account_id     | character varying(60)  |           |          | 
 fb_token       | character varying(255) |           |          | 
 ig_token       | character varying(255) |           |          | 
 ig_account_id  | character varying(60)  |           |          | 




# Note:

in this section of code you have to change the crednatils

  connection = psycopg2.connect(
      user = "something",#here you add the username of redshift conn
      password = "password", #here you add the password of redshift conn
      host = "host",#here you add the host of redshift conn
      port = "5439",#port of redshift host
      database = "something"
  )

