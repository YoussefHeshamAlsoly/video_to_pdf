import cv2
import click
from frames_to_pdf import *
from util.progress_bar import progress_bar

from comparison_functions import (
    fixed_interval,
    frame_difference,
    histogram_difference,
    ssim_difference,
    mse_difference,
    orb
)


@click.command()
@click.option('-i',
                '--input',
                help='Input video path')

@click.option('-m',
                '--method',
                type=click.Choice(['fixed-interval','pixel-wise', 'hist', 'ssim', 'mse', 'orb'], case_sensitive=False),
                default='pixel-wise',
                help='Available frame comparison methods to use.')

@click.option('-t',
                '--threshold',
                default='10.0',
                help='Threshold pixel difference (default: 10.0). Suggested thresholds\
                    \n\fixed-interval (int): Capture frames in a fixed interval (e.g. every 3 seconds)\
                    \n\npixel-wise (int): 10\
                    \n\nhist (float): 0.9 (if pixel similarity < 90% then different pixels).\
                    \n\nssim (float): 0.9 (if pixel similarity far from 1 then different pixels).\
                    \n\nmse (float): Range (0 to 1) 0 indicates no similarity and 1 indicates identical frames. Adjust based on your observations.\
                    \n\norb (int): Adjust based on the desired number of match points.')

def main(input, method, threshold):
    video_path = input
    threshold = float(threshold)

    methods = {
        'fixed-interval': (fixed_interval, "fixed-interval"),
        'pixel-wise': (frame_difference, "Pixel-wise Difference"),
        'hist': (histogram_difference, "Histogram Comparison"),
        'ssim': (ssim_difference, "SSIM"),
        'mse': (mse_difference, "MSE"),
        'orb': (orb, "ORB Feature Matching")
    }

    comparison_method, method_name = methods[method.lower()]
    print(f"Using {method_name} method to compare frames with a threshold of {threshold}.")
    process_video(method, video_path, comparison_method, threshold)


def frame_generator(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        yield frame
    cap.release()


def process_frame():
    pass


def process_video(method, video_path, comparison_method, threshold):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    
    if not cap.isOpened():
        print("Error opening video file")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames to process: {total_frames}")

    ret, prev_frame = cap.read()  # Get the first frame
    different_frames = [prev_frame]  # List to hold frames that are different
    current_frame_count = 0  # Track how many frames processed (for progress bar)

    # Create a frame generator from the video
    frames = frame_generator(video_path)
    
    different_frames = []


    if comparison_method == frame_difference:
        threshold = int(threshold)
        for current_frame in frames:
            difference_value = comparison_method(prev_frame, current_frame, threshold=threshold)
            if difference_value > threshold:
                different_frames.append(current_frame)
            prev_frame = current_frame
            current_frame_count += 1
            progress_bar(current_frame_count, total_frames)
    
    elif comparison_method == fixed_interval:
        different_frames = comparison_method(cap, fps, threshold, total_frames)

    
    else:
        
        if comparison_method == ssim_difference:
            f_threshold = threshold or 0.9
            for current_frame in frames:
                difference_value = comparison_method(prev_frame, current_frame)
                if difference_value < f_threshold:  # SSIM values close to 1 indicate similar frames
                    different_frames.append(current_frame)
                prev_frame = current_frame
                current_frame_count += 1
                progress_bar(current_frame_count, total_frames)
        
        elif comparison_method == histogram_difference:
            f_threshold = threshold or 0.9
            for current_frame in frames:
                difference_value = comparison_method(prev_frame, current_frame)
                if difference_value < f_threshold:  # Lower histogram correlation indicates more difference
                    different_frames.append(current_frame)
                prev_frame = current_frame
                current_frame_count += 1
                progress_bar(current_frame_count, total_frames)
        
        elif comparison_method == mse_difference:
            f_threshold = threshold or 500
            for current_frame in frames:
                difference_value = comparison_method(prev_frame, current_frame)
                if difference_value > f_threshold:  # Adjust based on your observations
                    different_frames.append(current_frame)
                prev_frame = current_frame
                current_frame_count += 1
                progress_bar(current_frame_count, total_frames)
        
        elif comparison_method == orb:
            f_threshold = threshold or 10
            for current_frame in frames:
                difference_value = comparison_method(prev_frame, current_frame)
                if difference_value < f_threshold:  # Adjust based on the expected number of matches
                    different_frames.append(current_frame)
                prev_frame = current_frame
                current_frame_count += 1
                progress_bar(current_frame_count, total_frames)

    cap.release()
    progress_bar(total_frames, total_frames)
    print("\nProcessing complete.")
    print(f"Detected {len(different_frames)} different frames.")


    images, currrent_time = save_frames_as_images(method, different_frames)
    combine_images_to_pdf(method, images, currrent_time)


# Run the main function
if __name__ == "__main__":
    main()
