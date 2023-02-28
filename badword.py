from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from better_profanity import profanity

app = Flask(__name__)
CORS(app)
@app.route('/api/cencor')
def censor():

    text=request.args.get('text')
    custom_badwords = ['putain', 'merde', 'con','conne','ducon','connard','connasse','enculé','bordel','salaud','saloperie','Fils de pute']
    profanity.add_censor_words(custom_badwords)
    # text to be censored

    censored = profanity.censor(text, '-')
    print(censored)
    return censored

if __name__ == "__main__":
    app.run(debug=True , host='0.0.0.0', port=5000)


