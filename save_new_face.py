import cv2
import numpy as np
import dlib
import argparse


def save_image(file, person_name, detect_faces, predictor, face_rec):
    # Grab a single frame from a file
    frame = cv2.imread(file)

    # Find all the faces and face encodings in the frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detect_faces.detectMultiScale(gray, 1.3, 5)
    face_locations = []
    for (x, y, w, h) in faces:
        face_locations.append(dlib.rectangle(x, y, x + w, y + h))

    # If there is at least 1 face then do face recognition
    if 0 < len(face_locations) < 2:
        for face_location in face_locations:
            face_encoding = predictor(frame, face_location)
            face_descriptor = face_rec.compute_face_descriptor(frame, face_encoding, 1)
            # Save encoding in a numpy file
            np.save("face_encodings/" + person_name, np.array(face_descriptor))
    else:
        print("Either no face or more then one face detected. Please check the image file again")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="File for to extract face from it", required=True)
    parser.add_argument("-n", "--name", type=str, help="Name for the person", required=True)

    args = parser.parse_args()

    file = args.file
    person_name = args.name

    detect_faces = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    face_rec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

    save_image(file, person_name, detect_faces, predictor, face_rec)


if __name__ == '__main__':
    main()