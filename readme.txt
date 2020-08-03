The requirements.txt file is what you would need to install to run my code.  

pip install -r requirements.txt

You will need to be sure uvicorn is started up.  

uvicorn scratch:app --reload


Go to this URL to see the interface for my app and test the api's
http://127.0.0.1:8000/docs
On this screen you should be able to add order, list all order, and list scheduled emails.  


I obviously did not get done with everything.  
Domain orders work.  
I can add them.  
I can list them.  
It schedules emails and you can see the list of emails.  


I did not do Email, Hosting, Pdomain, or Edomain.
I do not think they would be that difficult with the work I have done now.  
I also did not add logging.  It would be nice to add logging.  
I wanted to add testing but I did not have time for that.  
I did however use the api testing to test my code fairly well
