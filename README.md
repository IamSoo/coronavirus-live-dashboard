# coronavirus-live-dashboard

This is a realtime dashboard which loads data from https://opendata.ecdc.europa.eu/covid19/casedistribution/csv
and shows different chart to track corona virus status.

It uses streamlit and plotly library to show the charts.

### To run
```
git clone git@github.com:IamSoo/coronavirus-live-dashboard.git
cd coronavirus-live-dashboard
```
### Create a virtual env
```
python -m venv .
source bin/activate

```
### Install libs
pip install -r requirements.txt

### To run
streamlit run ./src/main.py

