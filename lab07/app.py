from flask import Flask, render_template, request
import segno
import base64
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/form-handler', methods=['GET', 'POST'])
def form_handler():
    if request.method == 'POST':
        message = request.form['data']
        qrcode = segno.make_qr(message)
        
        buff = io.BytesIO()
        qrcode.save(buff, kind='png', scale=4)
        qr_base64 = base64.b64encode(buff.getvalue()).decode('utf-8')
        
        return render_template('index.html', message=message, qr_image=qr_base64)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)