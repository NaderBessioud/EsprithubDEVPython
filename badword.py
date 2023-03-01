from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from better_profanity import profanity
import ftplib
import mysql.connector
import json

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

@app.route('/api/profileU')
def profile():
    modules={}
    option=request.args.get('option')
    niveau=request.args.get('niveau')
    try:
        connection = mysql.connector.connect(host='192.168.2.176',
                                         database='esprithub',
                                         user='root',
                                         password='guessitplease',
                                         port="3306")

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT U.libelle from ue U INNER JOIN question Q ON U.idue = Q.ue_idue INNER JOIN
        user S ON Q.userquestions_id = S.id INNER JOIN options O ON S.option_id_option = O.id_option
        where  S.niveau ='%s' and O.libelle ='%s'"""


        cursor.execute(sql_fetch_blob_query %(niveau,option))
        record = cursor.fetchall()



        for row in record:
            lib = row[0]
            if (lib in modules.keys()):
                modules[lib] = modules[lib] + 1
            else:
                modules[lib]=1



        sql_fetch_question_from_reaction = """SELECT U.libelle from ue U INNER JOIN question Q ON U.idue = Q.ue_idue INNER JOIN
                reaction R ON Q.id_question=R.question_reaction_id_question INNER JOIN user S ON R.id_user = S.id INNER JOIN options O ON S.option_id_option = O.id_option
                where  S.niveau ='%s' and O.libelle ='%s'"""
        cursor.execute(sql_fetch_question_from_reaction %(niveau,option))
        recordr = cursor.fetchall()

        for rowr in recordr:


            libr = rowr[0]
            if (libr in modules.keys()):
                modules[libr] = modules[libr] + 1
            else:
                modules[lib]=1

        sql_fetch_question_from_response = """SELECT U.libelle from ue U INNER JOIN question Q ON U.idue = Q.ue_idue INNER JOIN
                           response R ON Q.id_question=R.responses_id_question INNER JOIN user S ON R.id_user = S.id INNER JOIN options O ON S.option_id_option = O.id_option
                           where S.niveau ='%s' and O.libelle ='%s' and R.approved=1"""
        cursor.execute(sql_fetch_question_from_response %(niveau,option))
        recordres = cursor.fetchall()

        for rowres in recordres:

            libres = rowres[0]
            if (libres in modules.keys()):
                modules[libres] = modules[libres] + 1
            else:
                modules[libres] = 1


    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

    modules = sorted(modules.items(), key=lambda x: x[1], reverse=True)
    print(modules)
    result = json.dumps(modules)
    return result


if __name__ == "__main__":
    app.run(debug=True , host='0.0.0.0', port=5000)


