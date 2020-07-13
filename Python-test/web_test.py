from flask import Flask, send_from_directory
app = Flask(__name__)


@app.route('/download')
def download():
    return send_from_directory(r"C:\Users\BZMBN4\Desktop", filename="123.txt", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
