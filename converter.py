import argparse
import os

import imageio


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Pasta com ppms para converter para JPG")
    args = parser.parse_args()
    # images.append(imageio.imread(filename))
    folder = os.path.abspath(args.folder)
    onlyfiles = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    # print(onlyfiles)
    out_path = folder + "_jpg"
    if ((not os.path.exists(out_path)) and (len(out_path) >= 1)):
        os.makedirs(out_path)
    for f in onlyfiles:
        path = folder + "/" + f
        print(path)
        im = imageio.imread(path)
        saida = folder + "_jpg" + "/" + f[0:-4] + ".png"
        print(saida)
        imageio.imsave(saida, im, "PNG")

if __name__ == "__main__":
    main()
