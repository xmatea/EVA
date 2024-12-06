import numpy as np
from matplotlib import pyplot as plt


def linear_interpolation_between_points(x1, x2, y1, y2, x):
    m = (y2-y1) / (x2-x1)
    c = m * x1 + y1

    return m * x + c


def interpolate():
    Z, capture_prob, capture_prob_err = np.loadtxt("capture_probabilites.txt", unpack=True, delimiter=",")

    to_interpolate = [18, 79, 6, 72, 67, 77, 10, 8, 59, 78, 75, 45, 44, 65, 69]
    to_interpolate = sorted(to_interpolate)
    interpolated_points = []
    interpolated_lines = []

    for z in range(91):
        if z in to_interpolate and 2 < z < 90:
            z_lower = z
            while z_lower not in Z and z_lower > 1 or z_lower == 76:
                z_lower -= 1

            z_upper = z
            while z_upper not in Z and z_upper < 90 or z_upper == 76:
                z_upper += 1

            c_upper = capture_prob[np.where(Z == z_upper)][0]
            c_lower = capture_prob[np.where(Z == z_lower)][0]

            x = [z_lower, z_upper]
            y = [c_lower, c_upper]

            print("z=", z)
            print("x neighbors", x)
            print("y points", y)

            interpolated_points.append(np.interp(x=z, xp=x, fp=y))
            interpolated_lines.append((x,y))


    fig, ax = plt.subplots()
    ax.errorbar(Z, capture_prob, capture_prob_err, marker="s", linestyle="None", capsize=3, elinewidth=1,
                label="Egidy et al.")
    ax.plot(to_interpolate, interpolated_points, "o", label="Interpolated points")
    for line in interpolated_lines:
        ax.plot(line[0], line[1], color="black", linestyle="dashed", linewidth="1")

    ax.legend()
    plt.show()

    capture_probs = np.hstack([capture_prob, interpolated_points])
    z_s = np.hstack([Z, to_interpolate])

    data = list(zip(capture_probs, z_s))
    sorted_data = sorted(data, key=lambda f: f[0])
    capture_probs, z_s = zip(*sorted_data)

    print(z_s)

    with open("capture_probabilites_interpolated.txt", "w") as write_file:
        output = ""
        for i, prob in enumerate(capture_probs):
           output += f"{int(z_s[i])}, {prob}\n"
        write_file.write(output)

if __name__ == "__main__":
    interpolate()