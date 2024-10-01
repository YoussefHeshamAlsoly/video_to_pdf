# remember to add a new line to the print statements that follow any  
def progress_bar(current_point, total_points):
    if current_point == total_points:
        progress = 100
    else:
        progress = (current_point / total_points) * 100
    
    bar_length = 40
    block = int(bar_length * (progress / 100))
    bar = f"[{'#' * block}{'-' * (bar_length - block)}] {progress:.2f}%"
    print(f"\rProgress: {bar}", end="")
