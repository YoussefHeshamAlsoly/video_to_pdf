# video_to_pdf

![Banner](.assets/banner.jpg)

A CLI project dedicated to converting videos to pdf format for ease of access.
___

## Description

The main idea of the project is to detect when frames change in a video (indicating change of slide/scene in that frame). Then it captures that frame and moves on to the next frame, and keeps capturing those frames until it makes a library of -what could be- the slides presented in the video.

Other than the fixed-interval extraction method, the project uses 4 comparison techniques of analyzing the frames to determine change of scenes or not, those techniques are:

1. Fixed-interval extraction (not a comparison method, rather saving frames with a fixed interval between every consecutive frames)
2. Pixel-wise comparison
3. Histogram comparison
4. SSIM comparison
5. ORB comparison

___

## Usage

First, install the required packages in the `requirements.txt` file using the following command

```cmd
python3 setup.py
```

### Input options

| Option                | Description                                                                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-i` or `-- input`    | Input video path. Could be local video<br>or online video (check [yt-dl supported sites list](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md))         |
| `-m` or `--method`    | Frame extraction/comparison methods<br>(default method is `fixed-interval`)                                                                                            |
| `-t` or `--threshold` | Threshold of the number of seconds/pixels to<br>do extraction/comparison on                                                                                            |
| `-o` or `--output`    | Path to a directory to save all the generated files/directories<br>(optional, if not provided, the script will save all the data<br>in the current directory it is in) |

This is a CLI project, it needs an input file, choosing a comparison method, and choosing the comparison method's threshold.

```cmd
python3 main.py --input <path/to/the/input/video> --method <choose one of the 4 methods> --threshold <choose threshold> --output <directory to save all the generated output data>
```

The methods are:

1. `fixed-interval`
2. `pixel-wise`
3. `hist`
4. `ssim`
5. `orb`

Use the `--help` command to find more about the thresholds and more details about other parameters
`python3 main.py --help`

## Examples

```cmd
python3 main.py --input test.mp4 --method fixed-interval --threshold 10 --output "C:\Users\SomeUser\Desktop\"
```

```cmd
python3 main.py -i test.mp4 -m orb -t 25
```

```cmd
python3 main.py --help
```

___

## Output

The output of this process are

1. the main PDF
2. a folder with the frames the comparison method detected as changes in scenery (for manual use and understanding).

___

## Note

Note that for larger videos, with higher threshold tolerance, and low memory capacity, the program could run out of memory and result in halting the script.
___

## Todo

- [x] Better memory handling (capture/release mechanism).
- [x] Add a method to extract frames with fixed interval (e.g. a frame every 2000 ms).
- [x] Let the user pick where to save the output folder and pdf.
- [x] Implement yt-dl library in the project (to work with online videos).
- [ ] (not planned soon) Restucture the whole thing. Make it cleaner, instead of code vomitting everywhere.
