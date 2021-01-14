## Deploy (Heroku):
 
```sh
$ heroku login
$ heroku create app_name
$ git remote add heroku heroku_git_url
$ heroku addons:create heroku-postgresql:hobby-dev --app app_name
```
 
See database url with command:
```sh
$ heroku config --app app_name
```
Then Paste database URL to scripts/heroku_config.sh. Next commit your code changes and then:
 
```shell script
$ git push heroku master
$ ./scripts heroku_config.sh
$ heroku run python manage.py db upgrade
```
**Open app_name.herokuapp.com on your browser*
