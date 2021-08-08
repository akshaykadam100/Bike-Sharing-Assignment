# import Flask class from the flask module
from flask import Flask, request, render_template
import joblib
from datetime import datetime
import numpy as np

# Create Flask object to run
app = Flask(__name__)

# Load the model from the file
lin_model_load = joblib.load('modelling/linear_model.pkl')

holiday_list = ['2018-01-17', '2018-02-21', '2018-04-15', '2018-05-30', '2018-07-04',
                '2018-09-05', '2018-10-10', '2018-11-11', '2018-11-24', '2018-12-26',
                '2019-01-02', '2019-01-16', '2019-02-20', '2019-04-16', '2019-05-28',
                '2019-07-04', '2019-09-03', '2019-10-08', '2019-11-12', '2019-11-22', '2019-12-25']


@app.route("/", methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        complete_date = request.form.get("date")

        yr = get_year_attribute(complete_date)
        mnth_January, mnth_February, mnth_March, mnth_May, mnth_June, mnth_July, mnth_August, mnth_September, mnth_October, mnth_November, mnth_December = get_month_attribute(complete_date)
        date = get_date_attribute(complete_date)
        weekday_monday, weekday_tuesday, weekday_wednesday, weekday_thursday, weekday_saturday, weekday_sunday = get_weekday_attribute(complete_date)
        weathersit_light, weathersit_mist = get_valid_weather_type(request)
        season_spring, season_summer, season_winter = get_valid_season_type(request)
        temp = get_valid_temperature(request)
        humidity = get_valid_humidity(request)
        windspeed = get_valid_windspeed(request)
        holiday = check_holiday(complete_date)
        workingday = check_working_day(complete_date)
        final_features = [np.array([yr, workingday, temp, mnth_August, mnth_December, mnth_January, mnth_November,
                                    mnth_September, season_spring, season_summer, season_winter, weekday_sunday,
                                    weathersit_light, weathersit_mist])]
        output = lin_model_load.predict(final_features)
        return render_template('index.html', prediction_text='Bike Requirement: {}'.format(int(output[0])))
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        return "Invalid Method Type"


def check_working_day(complete_date):
    if (complete_date in holiday_list) or \
            (datetime.strptime(complete_date, '%Y-%m-%d').weekday() == 5) or \
            (datetime.strptime(complete_date, '%Y-%m-%d').weekday() == 6):
        return 0
    else:
        return 1


def check_holiday(complete_date):
    if complete_date in holiday_list:
        return 1
    else:
        0


def get_year_attribute(complete_date):
    temp_year = int(complete_date.split('-')[0])
    if temp_year == 2018:
        return 0
    elif temp_year == 2019:
        return 1
    else:
        return None


def get_month_attribute(complete_date):
    month_num = int(complete_date.split('-')[1])
    if month_num == 1:
        return 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    elif month_num == 2:
        return 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0
    elif month_num == 3:
        return 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0
    elif month_num == 4:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    elif month_num == 5:
        return 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0
    elif month_num == 6:
        return 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0
    elif month_num == 7:
        return 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0
    elif month_num == 8:
        return 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0
    elif month_num == 9:
        return 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0
    elif month_num == 10:
        return 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0
    elif month_num == 11:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0
    elif month_num == 12:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1


def get_date_attribute(complete_date):
    return int(complete_date.split('-')[2])


def get_weekday_attribute(complete_date):
    weekday = datetime.strptime(complete_date, '%Y-%m-%d').weekday()
    if weekday == 0:
        # Monday
        return 1, 0, 0, 0, 0, 0
    elif weekday == 1:
        # Tuesday
        return 0, 1, 0, 0, 0, 0
    elif weekday == 2:
        # Wednesday
        return 0, 0, 1, 0, 0, 0
    elif weekday == 3:
        # Thursday
        return 0, 0, 0, 1, 0, 0
    elif weekday == 4:
        # Friday
        return 0, 0, 0, 0, 0, 0
    elif weekday == 5:
        # Saturday
        return 0, 0, 0, 0, 1, 0
    elif weekday == 6:
        # Sunday
        return 0, 0, 0, 0, 0, 1


def get_valid_weather_type(request):
    weather_val = int(request.form.get("weather"))
    if weather_val == 2:
        # Mist
        return 0, 1
    elif weather_val == 3:
        # Light
        return 1, 0
    elif weather_val == 1:
        # Clear
        return 0, 0
    else:
        return 0, 0


def get_valid_season_type(request):
    season_val = int(request.form.get("season"))
    if season_val == 1:
        # Spring
        return 1, 0, 0
    elif season_val == 2:
        # Summer
        return 0, 1, 0
    elif season_val == 3:
        # Fall
        return 0, 0, 0
    elif season_val == 4:
        # Winter
        return 0, 0, 1


def get_valid_temperature(request):
    return float(request.form.get("temperature"))


def get_valid_humidity(request):
    return float(request.form.get("humidity"))


def get_valid_windspeed(request):
    return float(request.form.get("windspeed"))


if __name__ == "__main__":
    app.run()
