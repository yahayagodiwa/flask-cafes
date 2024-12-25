from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location Url', validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time (e.g. 8AM)', validators=[DataRequired()])
    close_time = StringField('Closing Time (e.g. 5PM)', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', 
                                choices=[(str(i), f"{'☕️' * i}") for i in range(6)], 
                                validators=[DataRequired()])
    wifi_rating = SelectField('Wi-Fi Rating', 
                              choices=[(str(i), f"{'📶' * i}") for i in range(6)], 
                              validators=[DataRequired()])
    power_rating = SelectField('Power Outlet Rating', 
                               choices=[(str(i), f"{'🔌' * i}") for i in range(6)], 
                               validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe = [
            form.cafe.data,
            form.location.data,
            form.open_time.data,
            form.close_time.data,
            dict(form.coffee_rating.choices).get(form.coffee_rating.data),  
            dict(form.wifi_rating.choices).get(form.wifi_rating.data),  
            dict(form.power_rating.choices).get(form.power_rating.data),
        ]
        with open('cafe-data.csv', mode="a", encoding='utf-8', newline='') as new_item:
            writer = csv.writer(new_item)
            writer.writerow(new_cafe)  
        return redirect('/cafes')
       
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', encoding='utf-8', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
          
        
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
