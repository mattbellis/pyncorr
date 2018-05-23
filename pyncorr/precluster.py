import numpy as np

################################################################################
def define_boundaries(loedges, hiedges, voxel_widths):

    nvoxels = []

    for lo,hi,s in zip(loedges,hiedges,voxel_widths):

        nvox = int(np.floor((hi-lo)/s)) + 1

        nvoxels.append(nvox)

    return nvoxels

        
        

################################################################################
def divide_into_voxels(data, loedges, hiedges, voxel_widths, nvoxels):

    # Assume data is in columns

    data_T = data.transpose()

    voxel_coords = []

    for coord,loedge,width,nvox in zip(data,loedges,voxel_widths,nvoxels):

        tempcoord = coord - loedge

        vcoord = np.floor(tempcoord/width).astype(int)

        if len(vcoord[vcoord<0])>0:
            print("There is a voxel bin below 0!")

        if len(vcoord[vcoord>nvox-1])>0:
            print("There is a voxel bin greater than vmax!")

        voxel_coords.append(vcoord)

    return voxel_coords

################################################################################
def voxelize_data(data, nvoxels, vcoords):

    data_T = data.transpose()

    voxels = []
    for i in range(nvoxels[0]):
        voxels.append([])
        for j in range(nvoxels[1]):
            voxels[i].append([])
            for k in range(nvoxels[2]):
                #print(i,j,k)
                index = vcoords[0]==i
                index *= vcoords[1]==j
                index *= vcoords[2]==k
                #print(index)
                data_temp = data_T[index]
                #voxels[i][j].append(data_temp.transpose())
                if len(data_temp)>0:
                    voxels[i][j].append(data_temp.copy())
                else:
                    voxels[i][j].append(None)

    return voxels

################################################################################
def return_voxelized_data(data, voxel_widths, verbose=False):
    # Get the the range over which the data extends in all 3 dimensions
    loedges = [np.min(data[0]), np.min(data[1]), np.min(data[2])]
    hiedges = [np.max(data[0]), np.max(data[1]), np.max(data[2])]

    if verbose:
        print("low edges of voxels: ")
        print(loedges)
        print("high edges of voxels: ")
        print(hiedges)

    nvoxels = define_boundaries(loedges, hiedges, voxel_widths)

    if verbose:
        print("Numbers of voxels: ")
        print(nvoxels)

    vcoords = divide_into_voxels(data, loedges, hiedges, voxel_widths, nvoxels)

    if verbose:
        print(vcoords)
        print(vcoords[0][vcoords[0]!=0])
        print(vcoords[1][vcoords[1]!=0])
        print(vcoords[2][vcoords[2]!=0])

    voxels = voxelize_data(data, nvoxels, vcoords)

    dimensions = {}
    dimensions["loedges"] = loedges
    dimensions["hiedges"] = hiedges
    dimensions["nvoxels"] = nvoxels

    return voxels, dimensions


