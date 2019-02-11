##  Football

This project can import football results and visualize them in flask

It was created to learn flask, data processing and data visualization  


### Features

- Import soccer results
- Choose a club for more information
- Get the season overview
- Create a point diagram
- Calculate the ATT/DEF value and try to predict the results (based on poisson)
- Compare the predict results and real results by using the coefficient of determination

------------
------------
------------

### First Steps: 

#### Import the results

Open ```main.py``` and choose the url for a league
```
url = "https://www.dfb.de/bundesliga/spieltagtabelle/?spieledb_path=/competitions/12/seasons/17683/matchday&spieledb_path=%2Fcompetitions%2F12%2Fseasons%2F17820%2Fmatchday%2F13"
```
run:
```
GET_ALL(url)
```
The results will automatically saved in a csv-file (folder: CSV)

#### Choose the source 

Open ```main.py``` and choose the csv file you want to work with

------------
------------
------------

### Start the flask server: 

Start ```START_Gui.py```

Default IP: 127.0.0.1:5000

------------

Choose a club in the dropdown menu

------------

Now you can switch between the options and compare the data

