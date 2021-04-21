# instgram-insights with redshift , posgres

you only have to setup up and create redshift , postgres DB 

with the following tables:

-instafollower

fileds:

 community_name 
 
 community_id    
 
 account_id     
 
 followers_value 
 
 followers_name 
 
 date          

-instamediainsights

fileds:

 community_name 

 community_id   
 
 account_id    
 
 media_id      
 
 media_url     
 
 date          
 
 engagement    
 
 impressions   
 
 reach          


-alex_fb_tokens

 community_name 
 
 community_id  
 
 ig_token      
 
 ig_account_id 
 




# Note:

in this section of code you have to change the crednatils

  connection = psycopg2.connect(
      user = "something",#here you add the username of redshift conn
      password = "password", #here you add the password of redshift conn
      host = "host",#here you add the host of redshift conn
      port = "5439",#port of redshift host
      database = "something"
  )

