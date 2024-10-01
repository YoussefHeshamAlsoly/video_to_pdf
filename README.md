# video_to_pdf
A CLI project dedicated to converting videos to pdf format for ease of access.
___
# Description
The main idea of the project is to detect when frames change in a video (indicating change of slide/scene in that frame). Then it captures that frame and moves on to the next frame, and keeps capturing those frames until it makes a library of -what could be- the slides presented in the video.

The project uses 4 comparison techniques of analyzing the frames to determine change of scenes or not, those techniques are:
1. Pixel-wise comparison
2. Histogram comparison
3. SSIM comparison
4. ORB comparison
___
# Usage
This is a CLI project, it needs an input file, choosing a comparison method, and choosing the comparison method's threshold.
`python3 main.py --input <path/to/the/input/video> --method <choose one of the 4 methods> --threshold <choose threshold>`

The methods are:
1. `pixel-wise`
2. `hist`
3. `ssim`
4. `orb`

Use the `--help` command to find more about the thresholds and more details about other parameters 
`python3 main.py --help`

## Examples
`python3 main.py --input test.mp4 --method pixel-wise --threshold 10`
`python3 main.py -i test.mp4 -m orb -t 25`
`python3 main.py --help`
___
# Output
The output of this process are
1. the main PDF
2. a folder with the frames the comparison method detected as changes in scenery (for manual use and understanding).
___
# Note
Note that for larger videos, with higher threshold tolerance, and low memory capacity, the program could run out of memory and result in halting the script.
___
# Future features
1. Better memory handling (capture/relese mechanism).  
2. Implement yt-dl library in the project (to work with online videos).
3. Create a GUI for the project.
