import argparse
import subprocess
import numpy as np
import scipy.io

def loadmat(filename):
    def _check_keys(dict):
        for key in dict:
            if isinstance(dict[key], scipy.io.matlab.mio5_params.mat_struct):
                dict[key] = _todict(dict[key])
        return dict

    def _todict(matobj):
        dict = {}

        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem, scipy.io.matlab.mio5_params.mat_struct):
                dict[strg] = _todict(elem)
            else:
                dict[strg] = elem
        return dict

    data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def transform(coords, src_img, dest_img, transform_mat):
    coords_str = " ".join([str(x) for x in coords])

    # print(coords_str)
    cp = subprocess.run("echo %s | img2imgcoord -mm -src %s -dest %s -xfm %s" \
                            % (coords_str, src_img, dest_img, transform_mat),
                        shell=True, stdout=subprocess.PIPE)

    transformed_coords = cp.stdout.decode('ascii').strip().split('\n')[-1]
    # print(transformed_coords)
    return np.array([float(x) for x in transformed_coords.split(" ") if x])


def read_label_coords(elecfilemat, elecfiletxt):
    print("Reading ", elecfilemat)

    elecmat = loadmat(elecfilemat)
    elecxyz = elecmat['elecf']

    electxt = { elecxyz['label'][i]: list(elecxyz['elecpos'][i])
                for i in range(len(elecxyz['label']))}

    return electxt

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('clustered_points_file', help="The output datafile with all the electrode points clustered.")
    parser.add_argument('outputcoordsfile', help="The output datafile for electrodes mapped to correct coords.")
    args = parser.parse_args()

    # extract arguments from parser
    clustered_points_file = args.clustered_points_file
    outputcoordsfile = args.outputcoordsfile

    # read in electrodes file
    electxt = read_label_coords(clustered_points_file)

    # write the output to a txt file
    with open(outputcoordsfile, 'w') as f:
        for i, name in enumerate(electxt['label']):
            f.write('%s %.6f %.6f %.6f\n' % (name,
                                             electxt['elecpos'][i][0],
                                             electxt['elecpos'][i][1],
                                             electxt['elecpos'][i][2]))