from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from apod_model import APODModel

app = Flask(__name__)
apod_model = APODModel('JKeEoWHYuTjxXixLmJmY1byqRu5MfjMjTNJ7w4I9')  

@app.route('/')
def home():
    try:
        apod_data = apod_model.get_apod()
        return render_template('index.html', 
                            image_url=apod_data['url'],
                            title=apod_data['title'],
                            date=apod_data['date'],
                            description=apod_data['explanation'],
                            copyright=apod_data.get('copyright', 'Public Domain'))
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        date = request.form.get('date')
        if apod_model.validate_date(date):
            try:
                apod_data = apod_model.get_apod(date)
                return render_template('history.html',
                                    image_url=apod_data['url'],
                                    title=apod_data['title'],
                                    date=apod_data['date'],
                                    description=apod_data['explanation'],
                                    copyright=apod_data.get('copyright', 'Public Domain'))
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return "Invalid date. Please select a date between June 16, 1995 and today."
    
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)
