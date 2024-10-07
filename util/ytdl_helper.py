import os
import yt_dlp
import validators
from tabulate import tabulate  # Import the tabulate library

def is_valid_url(url):
    return validators.url(url)

def download_driver(video_url, output_path='.'):
    video_info = {}

    def hook(d):
        if d['status'] == 'finished':
            video_info['name'] = d['filename']  # Retrieve the file name
            video_info['path'] = os.path.abspath(d['filename'])  # Get the absolute path

    # Set options for yt-dlp
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',  # Template for output file names
        'progress_hooks': [hook],  # Hook to get video info
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract information about the video
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', [])

            # Prepare data for the table
            table_data = []
            for f in formats:
                format_id = f.get('format_id', 'N/A')
                width = f.get('width', 'N/A')
                height = f.get('height', 'N/A')
                fps = f.get('fps', 'N/A')
                quality = f.get('format_note', 'N/A')

                # Append the data to the table
                table_data.append([format_id, f"{width}x{height}", fps, quality])

            # Print the table header and data
            print("Available qualities:")
            print(tabulate(table_data, headers=["Format ID", "Resolution", "FPS", "Quality"], tablefmt="grid"))

            desired_quality = str(input("Enter your desired quality ID (or press enter without entering any ID to download the best one): "))

            # Check if the desired quality exists
            if desired_quality and desired_quality in [f['format_id'] for f in formats]:
                ydl_opts['format'] = desired_quality
                print(f"Downloading with the specified quality ID: {desired_quality}")
            else:
                ydl_opts['format'] = 'bestvideo'
                print(f"Desired quality '{desired_quality}' not found. Downloading the best available quality.")

            # Update ydl_opts for format selection
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

    return video_info

# Example usage
if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    download_path = input("Enter the download path (leave blank for current directory): ")
    if not download_path:
        download_path = "."

    video_info = download_driver(url, download_path)
    if video_info:
        print(f"Video downloaded successfully.")
    else:
        print("Invalid URL.")
