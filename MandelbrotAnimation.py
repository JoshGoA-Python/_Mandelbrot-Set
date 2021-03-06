import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from numba import jit


# * Mandelbrot set: https://en.wikipedia.org/wiki/Mandelbrot_set
# Mandelbrot set sequence
@jit(nopython=True)
def mandelbrot(re, im, max_i):
    c = complex(re, im)
    z = 0
    for i in range(0, max_i):
        if (abs(z) > 2):
            return i
        z = z * z + c
    return max_i

# Arrange pixels in array
def mandelbrotSet(miny, maxy, minx, maxx, pixels, max_i):
    pixels_N = np.empty([pixels, pixels])
    for row, im in enumerate(np.linspace(miny, maxy, pixels)):
        for column, re in enumerate(np.linspace(minx, maxx, pixels)):
            pixels_N[row, column] = mandelbrot(re, im, max_i)
    return pixels_N

# Run animation
def run_animation():

    anim_running = True
    # Click event
    def onClick(event):
        # Restart animation
        if event.dblclick:
            anim.frame_seq = anim.new_frame_seq()
        else:
            nonlocal anim_running
            # Pause animation
            if anim_running:
                anim.event_source.stop()
                anim_running = False
            # Unpause animation
            else:
                anim.event_source.start()
                anim_running = True

    # Mandelbrot set animation
    def func(i):
        # Remove previous drawing
        plt.cla()
        # Style and layout
        plt.style.use("seaborn")
        plt.tight_layout()
        # Remove grid
        ax.grid(b=False)
        # Labels
        ax.set_title("Mandelbrot set")
        ax.set_ylabel("Imaginary")
        ax.set_xlabel("Real")
        # Image
        # Default: miny=-1, maxy=1, minx=-2, maxx=1, pixels=500, max_i=i
        pixels_N = mandelbrotSet(miny=-1, maxy=1, minx=-2, maxx=1, pixels=500, max_i=i)
        ax.imshow(pixels_N, cmap="binary_r", interpolation="sinc", extent=[-2, 1, -1, 1])

    # Repeat animation
    fig.canvas.mpl_connect('button_press_event', onClick)
    anim = animation.FuncAnimation(fig, func)

# Subplots
fig, ax = plt.subplots(figsize=(5, 5))

# Menu
print("Pause---[click] ")
print("Restart-[dblclick] ")

# Show
run_animation()
plt.show()
