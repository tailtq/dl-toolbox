# import the necessary packages
import glob
import os
import shutil

import cv2
import imutils


def save_frame(frameID, frame, dirPath, double_screen=False):
    def write_img(frameName, frame):
        framePath = os.path.join(dirPath, frameName)
        cv2.imwrite(framePath, frame)

    if double_screen:
        write_img('frame_%07d_1.jpg' % frameID, frame[:, 0:1920])
        write_img('frame_%07d_2.jpg' % frameID, frame[:, 1920:])
    else:
        write_img('frame_%07d.jpg' % frameID, frame)


def extract_frames_from_video(video_path, out_dir, frame_from=0, frame_to=None, save_after=15, double_screen=False):
    # initialize the pointer to the video file
    print('[INFO] Processing video %s ...' % video_path.split('/')[-1])
    cap = cv2.VideoCapture(video_path)
    video_name = video_path.split('/')[-1].split('.mp4')[0]
    # Directory to store frames
    dirPath = os.path.join(out_dir, video_name)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(total_frames)

    if os.path.isdir(dirPath):
        shutil.rmtree(dirPath)

    os.mkdir(dirPath)

    # loop over frames from the video file stream
    frameID = frame_from
    cap.set(cv2.CAP_PROP_POS_FRAMES, frameID)
    while True:
        # grab the next frame
        ret, frame = cap.read()
        frameID += 1

        # if the frame cannot be grabbed, then we have reached the end of the stream
        if not ret and frameID < total_frames:
            continue
        if not ret or (frame_to and frameID > frame_to):
            break

        if frameID % save_after == 0:
            save_frame(frameID, frame, dirPath, double_screen)

    print("Finish extracting video frames!")

    # close the video file pointers
    cap.release()


def visualize_frames(out_dir, video_path):
    video_name = video_path.split('/')[-1].split('.')[0]
    directory = out_dir + '/' + video_name
    directory_removed = directory + '_removed/'

    if not os.path.exists(directory_removed):
        os.mkdir(directory_removed)

    links = sorted(glob.glob('{}/*.jpg'.format(directory)))
    total_frames = len(links)
    index = 0

    while index < total_frames:
        link = links[index]

        image = cv2.imread(link)
        image = imutils.resize(image, width=1280)

        cv2.imshow('Screen', image)
        key = cv2.waitKey(-1)

        if key == ord('d'):
            shutil.move(link, directory_removed)
        elif key == ord('p') and index != 0:
            if os.path.exists(links[index - 1]):
                index -= 1
            continue
        elif key == ord('q'):
            break

        index += 1


if __name__ == '__main__':
    video_paths = ['trim_2.mp4', 'trim_3.mp4', 'trim_4.mp4', 'trim_5.mp4', 'trim_6.mp4']
    out_dir = './data'

    for video_path in video_paths:
        extract_frames_from_video(video_path, out_dir, frame_from=0, frame_to=50000, save_after=30)
    # visualize_frames(out_dir, video_path)
