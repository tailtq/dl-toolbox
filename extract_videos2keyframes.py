# import the necessary packages
import cv2
import os
import glob


def extract_frames_from_video(video_path, out_dir, skip_num):
    print('[INFO] Processing video %s ...' % video_path.split('/')[-1])
    cap = cv2.VideoCapture(video_path)
    video_name = video_path.split('/')[-1].split('.')[0]
    frameID = 0

    dir_path = os.path.join(out_dir, video_name)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        if frame % skip_num != 0:
            continue        

        frame_name = 'frame_%08d.jpg' % frameID
        frame_path = os.path.join(dir_path, frame_name)
        cv2.imwrite(frame_path, frame)
        
        print('Saved %s' % frame_path)

    frameID += 1
    print('Finish extracting video frames!')

    # close the video file pointers
    cap.release()


if __name__ == '__main__':
    video_path = 'GH010863_30FPS_NEW4.mp4'
    out_dir = './'
    extract_frames_from_video(video_path, out_dir, skip_num=10)
