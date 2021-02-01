# Hpp-decay-app

This dashboard was created with: 
  * Dash, to build the interactive dashboard.
  * Plotly, to make the nice looking plots.
  * And deployed in Heroku.
 
To deploy the Dash app in Heroku new a conda enviroment was created with the libraries imported in the app.py code. The libraries are Pandas, Dash, Plotly and also gunicorn.
The Procfile, runtime.txt and requirements.txt are files needed by Heroku for python apps. The requirements.txt was created through,

```
pip freeze > requirements.txt
```

I followed closelly the [Dash tutorial](https://dash.plotly.com/deployment) to deploying apps. The commands needed to actualize the app in Heroku are,

```
heroku create my-dash-app # To initialize the Heroku app.
git add . # add all files to git
git commit -m 'Initial app boilerplate'
git push heroku master # deploy code to heroku
```
