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
