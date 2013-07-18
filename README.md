##Simple API-ish service for getting PVD(or your city) food truck location from Twitter.

### Sample Usage:

Get list of valid food trucks ```http://localhost:8080/trucks```

Get a single one ```http://localhost:8080/?truck=Lotus%20Pepper```

Get all of them at once ```http://localhost:8080/ #this takes a while since we are hitting the twitter api and cleaning up the results.```

###You can make this work for your city too!

Update the settings.example.py file by renaming it to settings.py

1. Set up your Twitter API creds
2. Update your Food Truck List
3. Deploy to app engine.



Check it out running here
https://pvdfoodtruckfinder.appspot.com/trucks
