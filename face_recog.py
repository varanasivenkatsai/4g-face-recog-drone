import face_recognition
import picamera
import numpy as np
import smtplib
smtpUser = 'from_name@gmail.com'
smtpPass = 'password'

toAdd = 'to_name@gmail.com'
fromAdd = smtpUser

subject ='Face detected'
header = 'to:' + toAdd + '\n' +'From: ' + fromAdd + '\n' + 'subject: ' + subject
body = 'Drone has detected Barak Obama'

camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

print("Loading known face image(s)")
obama_image = face_recognition.load_image_file("obama_small.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

face_locations = []
face_encodings = []
while True:
    print("Capturing image.")
    camera.capture(output, format="rgb")

    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)
    
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces([obama_face_encoding], face_encoding)
        name = "<Unknown Person>"

        if match[0]:
            name = "Barack Obama"
            s=smtplib.SMTP('smtp.gmail.com',587)
	        s.echo()
            s.starttls()
            s.echlo()
    	    s.login(smtpUser, smtpPass)
            s.sendmail(fromAdd, toAdd, header + '\n' + body)
	    s.quit()

        print("I see someone named {}!".format(name))
