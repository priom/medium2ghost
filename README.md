# Script to migrate Medium to Ghost

> This script facilitates the migration of your entire Medium publication to Ghost, as Medium does not offer a straightforward way to export all your content.  
> You should really consider migrating and consider Ghost, it's awesome, open-source and free.

To complete the migration in a few minutes, follow these steps:
1. Install ghost locally following this [link](https://ghost.org/docs/install/local/) 
2. Setup Ghost locally and browse through the admin settings
3. Make sure you have Python3 installed locally
4. Sign up for a RapidAPI account and subscribe to the API [here](https://rapidapi.com/nishujain199719-vgIfuFHZxVZ/api/medium2). Opt for a paid plan for a month to finish the migration, otherwise, you might incur significant overusage fees.
5. Run the locally-installed Ghost and create an API key [here](http://localhost:2369/ghost/#/settings/integrations/new)
6. Store the necessary variables in the `.env` file, which the script will reference.
7. Install the required dependencies using `pip install -r requirements.txt`
8. Modify the `timedelta(days=X)` on **line 47**. The value of X should be **1 less than the actual days**.
9. Execute the script with `python medium2ghost.py`
10. Voilà! The migration is complete! You should now see your posts in your Ghost instance. Enjoy!

### Note
- Medium does not, by default, export content in markdown format, also Ghost primarily accepts imports in JSON and mobiledoc formats only. In this script, articles from Medium are exported in markdown format, then transformed and uploaded to Ghost in its default mobiledoc format.
- Authors are not imported through this method. By default, content is uploaded under the primary user on Ghost so, consider creating a common organizational user. Due to time constraints, I prepended the author name dynamically to the top of the article before uploading to Ghost
While testing the api, reduce the value of X `timedelta(days=X)` in **line 47** so, you save on the rapidapi bill ;)
- This script works in production too, just change the ENV variables. Digitalocean has 1-click Ghost app which simplifies the installation and management
- Sometimes if there's a lot articles it can get rate limited default in ghost production so, try doing the migration locally, then export from local and import in production, All the articles, design and format is going to be same


&copy; Copyright Protected & All Rights Reserved by [Priom Chowdhury](https://0xpriom.com/)