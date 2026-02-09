# This starter code requires functions in the Dolly Zoom Notebook to work
from dolly_zoom import *

import os
import imageio
import cv2
import matplotlib.pyplot as plt
import numpy as np

# Call this function to generate gif. make sure you have rotY() implemented.
def generate_gif():
    n_frames = 30
    if not os.path.isdir("frames"):
        os.mkdir("frames")
    fstr = "frames/%d.png"
    for i,theta in enumerate(np.arange(0,2*np.pi,2*np.pi/n_frames)):
        fname = fstr % i
        renderCube(f=15, t=(0,0,3), R=rotY(theta))
        plt.savefig(fname)
        plt.close()

    with imageio.get_writer("cube.gif", mode='I') as writer:
        for i in range(n_frames):
            frame = plt.imread(fstr % i)
            frame = (frame * 255).astype('uint8') 
            writer.append_data(frame)
            os.remove(fstr%i)
            
    os.rmdir("frames")
def q2_make_plots():
    theta = np.pi / 4

    # (a) rotX then rotY  => R = rotY @ rotX
    R_a = rotY(theta) @ rotX(theta)
    renderCube(f=15, t=(0,0,3), R=R_a)
    plt.savefig("q2_a_rotX_then_rotY.png")
    plt.close()

    # (b) rotY then rotX  => R = rotX @ rotY
    R_b = rotX(theta) @ rotY(theta)
    renderCube(f=15, t=(0,0,3), R=R_b)
    plt.savefig("q2_b_rotY_then_rotX.png")
    plt.close()


def q3_rotation_diagonal_to_point():
    """
    Goal: rotate cube so body diagonal aligns with camera z-axis,
    so its projection collapses to a point.
    Order: rotX(tx) then rotY(ty) => R = rotY(ty) @ rotX(tx)
    """
    tx = np.pi / 4
    ty = -np.arctan(1/np.sqrt(2))

    R_best = rotY(ty) @ rotX(tx)

    renderCube(f=15, t=(0,0,3), R=R_best)
    plt.savefig("q3_perspective_diagonal_point.png")
    plt.close()

    print("Q3 angles to report:")
    print("Order: rotX(tx) then rotY(ty)")
    print("tx =", tx, "(= pi/4)")
    print("ty =", ty, "(= -arctan(1/sqrt(2)))")

    return R_best


def projectLines_ortho(R, t, L):
    """
    Orthographic projection:
      u = x, v = y  (ignore z)
    Returns Nx4 [u1,v1,u2,v2]
    """
    pL = np.zeros((L.shape[0], 4))
    for i in range(L.shape[0]):
        p  = np.dot(R, L[i,:3]) + t
        pp = np.dot(R, L[i,3:]) + t

        pL[i,:2] = p[0], p[1]
        pL[i,2:] = pp[0], pp[1]

    return np.vstack(pL)


def q4_make_orthographic_plot(R_best):
    L = generateCube()
    t = np.array((0,0,3))
    pL = projectLines_ortho(R_best, t, L)

    plt.figure()
    plt.title("Q4: Orthographic (same rotation as Q3)")
    for i in range(pL.shape[0]):
        u1, v1, u2, v2 = pL[i,:]
        plt.plot((u1,u2), (v1,v2), linewidth=2)

    plt.axis('square')
    plt.xlim(-2,2)
    plt.ylim(-2,2)
    plt.savefig("q4_orthographic_same_rotation.png")
    plt.close()

def save_rgb_and_lab_channels(image_path, prefix):
    bgr = cv2.imread(image_path)
    if bgr is None:
        raise FileNotFoundError(f"Could not read {image_path}. Make sure it's in the same folder.")
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    # RGB channels as grayscale (avoid normalization issues)
    channel_names = ["R", "G", "B"]
    for c, name in enumerate(channel_names):
        plt.figure()
        plt.title(f"{prefix} - {name} channel")
        plt.imshow(rgb[:, :, c], cmap="gray", vmin=0, vmax=255)
        plt.axis("off")
        plt.savefig(f"{prefix}_RGB_{name}.png", bbox_inches="tight")
        plt.close()

    # LAB channels
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)  # L in [0,255], A/B in [0,255] (offset)
    lab_names = ["L", "A", "B"]
    for c, name in enumerate(lab_names):
        plt.figure()
        plt.title(f"{prefix} - LAB {name} channel")
        plt.imshow(lab[:, :, c], cmap="gray")
        plt.axis("off")
        plt.savefig(f"{prefix}_LAB_{name}.png", bbox_inches="tight")
        plt.close()
    
def run_part2_1():
    save_rgb_and_lab_channels("indoor.png", "indoor")
    save_rgb_and_lab_channels("outdoor.png", "outdoor")
    print("Generated Part 2.1 files (indoor/outdoor RGB + LAB channel images).")

def run_part1_all():
    # Q1
    generate_gif()

    # Q2
    q2_make_plots()

    # Q3
    R_best = q3_rotation_diagonal_to_point()

    # Q4
    q4_make_orthographic_plot(R_best)

    print("\nGenerated Part 1 files:")
    print(" - cube.gif")
    print(" - q2_a_rotX_then_rotY.png")
    print(" - q2_b_rotY_then_rotX.png")
    print(" - q3_perspective_diagonal_point.png")
    print(" - q4_orthographic_same_rotation.png")



if __name__ == "__main__":
    run_part1_all()
	run_part2_1()
