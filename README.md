heroku buildpacks:clear 
heroku buildpacks:set heroku/python
git push heroku master
heroku ps:scale web=1
heroku logs -t