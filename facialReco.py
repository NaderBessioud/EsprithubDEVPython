import ftplib
import cv2
from SimpleFacerec import SimpleFacerec
import mysql.connector
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route('/api/facialreco')
def FacialReco():
    HOSTNAME = "192.168.1.19"
    USERNAME = "ftpuser"
    PASSWORD = "ftpuser"


    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
    print("cava1")
    ftp_server.encoding = "utf-8"

    try:
        connection = mysql.connector.connect(host='192.168.2.176',
                                         database='esprithub',
                                         user='root',
                                         password='guessitplease',
                                         port="3306")

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT username,image from user"""

        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            image = row[1]
            username = row[0]

            print("Storing employee image and bio-data on disk \n")

            with open("C:\\Users\\ASUS\\OneDrive\\Bureau\\stage\\python\\images\\" + username + ".png", 'wb') as file:
                ftp_server.retrbinary(f"RETR {image}", file.write)


    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


    nameA = "Unknown"
    #Encoded known faces
    sfr = SimpleFacerec()
    sfr.load_encoding_images("C:\\Users\\ASUS\\OneDrive\\Bureau\\stage\\python\\images/")
    # Load camera
    # Load camera
    cap = cv2.VideoCapture()
    cap.open(0, cv2.CAP_DSHOW)

    while True:
        ret, frame = cap.read()

        # Detect Faces

        face_locations, face_names = sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
            if name != "Unknown":
                nameA = name
                break

            cv2.imshow("Frame", frame)

        key = cv2.waitKey(1)
        if key == 2:
            break
        if nameA != "Unknown":
            break
            return nameA


    cap.release()
    cv2.destroyAllWindows()
    return nameA

if __name__ == "__main__":
    app.run(debug=True)







