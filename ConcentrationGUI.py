import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from scipy.interpolate import splrep, splev
from scipy.ndimage import gaussian_filter1d
import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import os

#TKINTER STUFF BY BYRON

#HOLDER VARIABLES
elements=[]
filenames=[]
elementsreal=[]

def save():
    global elements
    global silly
    print("SAVED")
    for i in elements:
        elementsreal.append(i.get())

def display(filenames):
    global f
    global f2
    global elements
    global silly
    elements=[]
    j = 0
    for i in filenames:
        thing=Image.open(str(i)).resize((190,450))
        thing=ImageTk.PhotoImage(thing)
        pic=Label(f2,image=thing)
        pic.image=thing
        Label(f2,text=f"{i}",padx=10,pady=10).grid(row=0,column=j)
        pic.grid(row=1,column=j,padx=10)
        silly=tk.Entry(f2)
        silly.grid(row=2,column=j,padx=10,pady=5)
        elements.append(silly)
        j+=1

def addimage():
    filepath = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    filenames.append(filepath)
    if filepath:
        display(filenames)

def reset():
    global b1
    global b2
    global b4
    global filenames
    global elements
    elements=[]
    filenames=[]
    mainframe.destroy()
    b2.destroy()
    b4.destroy()
    b1 = tk.Button(root, text="Select Image", font=("Arial", 12, "bold"), command=reconfigure)
    b1.pack(anchor="w", side=BOTTOM, padx=10, pady=10)

def reconfigure():
    global f2
    global mainframe
    global b2
    global b4
    global label
    global scrollbar1
    global c1

    # Destroy label
    labelmclabelface.destroy()

    # Create a mainframe
    mainframe = tk.Frame(root)
    mainframe.pack(fill=BOTH, expand=1)

    # Create a canvas
    c1 = tk.Canvas(mainframe)
    c1.pack(side=TOP, fill=BOTH, expand=1)

    # Create a scroll bar
    scrollbar1 = ttk.Scrollbar(mainframe, orient=HORIZONTAL, command=c1.xview)
    scrollbar1.pack(side=BOTTOM, fill=X)

    # Configure canvas
    c1.configure(xscrollcommand=scrollbar1.set)
    c1.bind('<Configure>', lambda e: c1.configure(scrollregion=c1.bbox("all")))

    # Create a frame
    f2 = tk.Frame(c1)

    # Merge f2 and canvas
    c1.create_window((0, 0), window=f2, anchor="nw")

    #Destroys old button to create new button that does not recreate this giant grid
    b1.destroy()
    b4=tk.Button(root,text="Select Image",font=("Arial",12,"bold"),command=addimage)
    b4.pack(anchor="w", side=BOTTOM,padx=10,pady=10)
    b2=tk.Button(root,text="Reset",command=reset,font=("Arial",12,"bold"))
    b2.pack(anchor="w",side=BOTTOM,padx=10)

    #Adds the first image
    filepath=filedialog.askopenfilename(
        filetypes=[("Image Files","*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    filenames.append(filepath)
    if filepath:
        display(filenames)

    #Adds a save button
    b3=tk.Button(f2,text="Save",font=("Arial",10),command=save)
    b3.grid(row=10,column=0,padx=10,pady=10)

# Create the main Tkinter window
root=tk.Tk()
root.title("Multi Image Selector")
root.geometry("750x750")

# Create a header
t=tk.Label(root,text="Image Selector",font=("Arial",14,"bold"))
t.pack()

# Create a button for adding images
b1=tk.Button(root,text="Select Image",font=("Arial",12,"bold"),command=reconfigure)
b1.pack(anchor="w", side=BOTTOM,padx=10,pady=10)

# Creates an important label
labelmclabelface=tk.Label(root,text="IMPORTANT: THE SCROLL BAR IS NOT PERFECT.\nIT CAN ONLY WORK AND UPDATE SIZE IF YOU "
                                    "ADJUST THE GUI WINDOW SIZE.\n CLICK THE A HORIZONTAL EDGE AND DRAG IT, IT WILL ADJUST"
                                    " THE SCROLL BAR SIZE",font=("Arial",10))
labelmclabelface.pack()

root.mainloop()

#TKINTER STUFF END

#FUNCTIONS CALLED IN LOOP

# Plot profiles and save a figure
def plot_profile(profile,height,element):
    depths = np.linspace(0, height, segments)

    # Optional data smoothing
    sigma = 2.0
    conc_profile_sm = gaussian_filter1d(profile, sigma)

    # Optional interpolation for smoother graph
    spline = splrep(depths, conc_profile_sm, s=0)

    # Generate spline for smoother plot
    spline_points = 500
    depths_spline = np.linspace(depths.min(), depths.max(), spline_points)
    spline_data = splev(depths_spline, spline)

    fig = plt.figure()
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1])
    ax1 = fig.add_subplot(gs[0, 0], )
    ax3 = fig.add_subplot(gs[0, 1], sharey=ax1)
    plt.subplots_adjust(wspace=0)
    # fig.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1,
    #                     wspace=0.0, hspace=0.0)
    # gs.update(wspace=0.2, hspace=0.4)  # More space between the subplots

    fig.set_figheight(5)
    fig.set_figwidth(12)

    fig.suptitle(f"{element} Precipitate Coverage vs Sample Depth")
    ax1.plot(spline_data * 100, depths_spline)

    #This sets the xlim of the plot so change it as neccessary if you would like a more clear plot.
    ax1.set_xlim(0)
    ax1.set_ylim(height, 0)
    ax1.set_xlabel("Precipitate coverage (%)")
    ax1.set_ylabel("Depth (nm)")
    ax1.grid()

    # Plot Cr data
    ax3.imshow(binary, cmap='gray', extent=[0, width, height, 0])
    ax3.set_xlim(0, width)
    ax3.set_ylim(height, 0)

    # Disable tick marks for all axes
    for ax in [ax3]:
        ax.tick_params(length=0, labelbottom=False, labelleft=False,
                       labelright=False, labeltop=False)  # Disable tick marks
    plt.show()
    fig.savefig(f"{element}_Precipitate_Coverage_Plot.png")

# Save data to a csv
def save_data(segments, depth, profile,element):
    data = {
            "Segment": np.arange(1, segments + 1),
            "Depth (nm)": np.linspace(0, depth, segments),
            "Precipitate coverage (%)": profile * 100
            }
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(f"{element}_precipitate_coverage.csv", index=False)

# Calculate concentration profiles and return them
def get_conc_profile(binary,segments):

    # Get the number of rows of pixels
    row_count = binary.shape[0]

    # Determine the interval of pixels between segments
    interval = row_count // segments

    # Preallocate the profiles
    profile = np.zeros(segments)
    for i in range(0, segments):
        # Calculate the segment indexes to count pixels
        prev_index = i * interval
        next_index = (i + 1) * interval

        # Select the segment from the pixel data
        segment = binary[prev_index:next_index, :]
        # Count white pixels in the segment
        profile[i] = np.sum(segment == 255) / segment.size
    return profile

# Show binary images and save a figure
def binary_images(binary, width, height,element):
    plt.imshow(binary,extent=[0, width, height, 0])
    plt.xlim(0,width)
    plt.ylim(height,0)
    plt.xlabel("Width (nm)")
    plt.ylabel("Depth (nm)")
    plt.title(f"{element} Precipatite Coverage")
    plt.savefig(f"{element}_Precipatite_Coverage.png")
    plt.show()

#LOOP BEGINS
f=0
for i in filenames:
    #brings element
    element=elementsreal[f]

    #imports image to be used
    image=cv.imread(str(i))

    #convert to grayscale (Not strictly needed)
    gray=cv.cvtColor(image,cv.COLOR_BGR2GRAY)

    # Image dimensions nm (Same for both and can be changed depending on )
    width=900
    height=2000

    # Extract binary data using thresholds
    threshold=85
    _, binary=cv.threshold(image, threshold, 255, cv.THRESH_BINARY)

    # Number of segments to use when profiling
    segments=100
    profile=get_conc_profile(binary, segments)

    #Creates binary image
    binary_images(binary,width,height,element)

    #Plots profile
    plot_profile(profile,height,element)

    #Save data
    save_data(segments,height,profile,element)
    f+=1
