'''
                      The following functions read intraoperative points 
                and perform conversions from one coordinate system to another
'''

def read_intra_op_points(folderpath):
    print('Read IntraOp points.')
    if os.path.isfile(os.path.join(folderpath, 'fiducials.csv')):
        filepath = os.path.join(folderpath, 'fiducials.csv')
    else:
        filepath = os.path.join(folderpath, 'Intraop.fcsv')
    points = list()
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            # Check if this line is a IntraOp Point or Tumor.
            try:
                tmp = re.search('IntraOp', str(row[-3]))
                try:
                    # If it does not fail, it is a IntraOp Point
                    tmp.group(0)
                    x = float(row[1])
                    y = float(row[2])
                    z = float(row[3])
                    xyz = [x, y, z]
                    points.append(xyz)
                except AttributeError:
                    pass
            except IndexError:
                pass

    print('Done.')
    points = np.asarray(points)
    return points


def return_string_list_as_float_numpy_array(list_to_array):
    numpy_array = np.asarray(list(map(float, list_to_array)))
    return numpy_array

def read_nrrd_file(filepath):
    data, header = nrrd.read(filepath)
    return data, header

def get_ijk_to_lps(header):
    space_origin = return_string_list_as_float_numpy_array(header['space origin'])
    space_origin = np.append(space_origin, 1)

    row0 = return_string_list_as_float_numpy_array(header['space directions'][0])
    row0 = np.append(row0, 0)
    row1 = return_string_list_as_float_numpy_array(header['space directions'][1])
    row1 = np.append(row1, 0)
    row2 = return_string_list_as_float_numpy_array(header['space directions'][2])
    row2 = np.append(row2, 0)
    ijk_to_lps = np.array([row0, row1, row2, space_origin]).T

    return ijk_to_lps

def ijk_to_lps(ijk, header):
    if len(ijk) == 3:
        ijk = np.append(ijk, 1)

    ijk_to_lps = get_ijk_to_lps(header)

    lps = np.dot(ijk_to_lps, ijk)

    return lps[0:3]

def ijk_to_ras(ijk, header):
    if len(ijk) == 3:
        ijk = np.append(ijk, 1)

    ijk_to_lps = get_ijk_to_lps(header)
    lps_to_ras = np.diag([-1, -1, 1, 1])

    lps = np.dot(ijk_to_lps, ijk)
    ras = np.matmul(lps, lps_to_ras)

    return ras[0:3]

def lps_to_ijk(lps, header):
    if len(lps) == 3:
        lps = np.append(lps, 1)

    ijk_to_lps = get_ijk_to_lps(header)
    lps_to_ijk = LA.inv(ijk_to_lps)

    ijk = np.dot(lps_to_ijk, lps)

    return ijk[0:3]

def ras_to_ijk(ras, header):   #RAS points are in RAS coordinate sytem and header is in LPS coordinate system
    if len(ras) == 3:
        ras = np.append(ras, 1)
        
    ijk_to_lps = get_ijk_to_lps(header) 
    lps_to_ijk = LA.inv(ijk_to_lps)
    ras_to_lps = np.diag([-1, -1, 1, 1])  

    lps = np.matmul(ras, ras_to_lps)
    ijk = np.dot(lps_to_ijk, lps)

    return ijk[0:3]