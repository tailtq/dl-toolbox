import cv2

if __name__ == '__main__':
    directory = 'data'
    vs = cv2.VideoCapture('{}/bus-video-1.mp4'.format(directory))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out1 = cv2.VideoWriter('{}/output1.mp4'.format(directory), fourcc, 20.0, (1920, 1080))
    out2 = cv2.VideoWriter('{}/output2.mp4'.format(directory), fourcc, 20.0, (1920, 1080))

    while True:
        ret, frame = vs.read()
        if not ret:
            break

        image1 = frame[:, :1920]
        out1.write(image1)

        image2 = frame[:, 1920:]
        out2.write(image2)

    vs.release()
    out1.release()
    out2.release()
    cv2.destroyAllWindows()
