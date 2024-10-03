import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from util.progress_bar import progress_bar


# Define comparison methods
def fixed_interval(video_capture, fps, interval, total_frames):
    capture_index_val = int(fps * interval)
    captured_frames = []

    for i in range(0, total_frames, capture_index_val):
        # Jump directly to the frame at index 'i' (generator obj sucks!)
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = video_capture.read()
        if not ret:
            break
        captured_frames.append(frame)
        progress_bar(i, total_frames)

    progress_bar(total_frames, total_frames)
    return captured_frames


def frame_difference(frame1, frame2, threshold=50):
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(frame1_gray, frame2_gray)
    _, diff_thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    non_zero_count = np.count_nonzero(diff_thresholded)
    total_pixels = frame1_gray.size
    percent_change = (non_zero_count / total_pixels) * 100
    return percent_change

def histogram_difference(frame1, frame2):
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    hist1 = cv2.calcHist([frame1_gray], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([frame2_gray], [0], None, [256], [0, 256])
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()
    diff = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return diff

def ssim_difference(frame1, frame2):
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(frame1_gray, frame2_gray, full=True)
    return score

def mse_difference(frame1, frame2):
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    err = np.sum((frame1_gray.astype("float") - frame2_gray.astype("float")) ** 2)
    err /= float(frame1_gray.shape[0] * frame1_gray.shape[1])
    return err

def orb(frame1, frame2):
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create()
    keypoints1, descriptors1 = orb.detectAndCompute(frame1_gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(frame2_gray, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    good_matches = [m for m in matches if m.distance < 50]
    return len(good_matches)
