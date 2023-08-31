import numpy as np 
from shapely import geometry as geo
import itasca as it
it.command("python-reset-state false")


#0 for Fx, 1 for Fy, 2 for Fz, 3 for Mx, 4 for My, 5 for Mz

def loading(group,load,Type):
    Jx = Jy = Jp = 0
    Node_ref = []
    N = 0
    for sn in it.structure.node.list():
        if sn.group('reference') == group:
            Jx = Jx + sn.pos()[0]**2
            Jy = Jx
            Jp = Jx + Jy
            Node_ref.append(sn)
            N = N + 1

    load_n = load / N

    for sn_ref in Node_ref:
        if Type == 0:
            sn_ref.set_apply(Type,load_n)
        elif Type == 1:
            sn_ref.set_apply(Type,load_n)
        elif Type == 2:
            sn_ref.set_apply(Type,load_n)
        elif Type == 3:
            load_n = load*sn_ref.pos()[1]/Jx
            load_n_final = sn_ref.apply()[0][2] + load_n
            sn_ref.set_apply(Type-1,load_n_final)
        elif Type == 4:
            load_n = -load*sn_ref.pos()[0]/Jy
            load_n_final = sn_ref.apply()[0][2] + load_n
            sn_ref.set_apply(Type-2,load_n_final)
        elif Type == 5:
            r = np.sqrt(sn_ref.pos()[0]**2+sn_ref.pos()[1]**2)
            theta = np.arcsin(sn_ref.pos()[1]/r)
            load_n = load*r/Jy
            if sn_ref.pos()[0] < 0:
                load_n_final_x = sn_ref.apply()[0][0] + -load_n*np.sin(theta)
                load_n_final_y = sn_ref.apply()[0][1] + -load_n*np.cos(theta)
                sn_ref.set_apply(Type-5,load_n_final_x)
                sn_ref.set_apply(Type-4,load_n_final_y)
            else:
                load_n_final_x = sn_ref.apply()[0][0] + -load_n*np.sin(theta)
                load_n_final_y = sn_ref.apply()[0][1] +  load_n*np.cos(theta)
                sn_ref.set_apply(Type-5,load_n_final_x)
                sn_ref.set_apply(Type-4,load_n_final_y)

# loading('loading_ref', 1000, 0)
# loading('loading_ref', 1000, 1)
# loading('loading_ref', 1000, 2)
# loading('loading_ref', 1000, 5)

def ListIsZero(List):
    for i in range(len(List)):
        if List[i] == 0:
            return True
        else:
            return False

def loading_procedure(soil_layers,load_final,load_matrix_final,prj_dir):
    it.command(f"model restore '{prj_dir}\Foundation'")
    
    command ='''
    zone gridpoint initialize displacement 0.0 0.0 0.0
    zone gridpoint initialize velocity 0.0 0.0 0.0
    structure node initialize displacement 0.0 0.0 0.0
    structure node initialize displacement-rotational 0.0 0.0 0.0
    structure node initialize velocity 0.0 0.0 0.0
    structure node initialize velocity-rotational 0.0 0.0 0.0
    '''
    it.command(command)

    command = f'''
    structure node group 'loading_ref' slot 'reference' range position-z {soil_layers[0]} group 'Skirt' slot 'SC'
    structure node history displacement-x position 0 0 {soil_layers[0]}
    structure node history displacement-y position 0 0 {soil_layers[0]}
    structure node history displacement-z position 0 0 {soil_layers[0]}
    structure node history velocity-x position 0 0 {soil_layers[0]}
    structure node history velocity-y position 0 0 {soil_layers[0]}
    structure node history velocity-z position 0 0 {soil_layers[0]}
    '''
    it.command(command)
    
    if ListIsZero(load_final) == False:
        loading('loading_ref', load_final[0], 0)
        loading('loading_ref', load_final[1], 1)
        loading('loading_ref', load_final[2], 2)
        loading('loading_ref', load_final[3], 3)
        loading('loading_ref', load_final[4], 4)
        loading('loading_ref', load_final[5], 5)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(f"The loads are {load_final}")
        it.command("model solve ratio 1e-6")
        it.command(f"model save '{prj_dir}\{load_final[-1]}'")
        print(f"'{load_final[-1]}' saved!")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
    if ListIsZero(load_matrix_final) == False:
        for i in range(6):
            loading('loading_ref', load_final[i], i)
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(f"The load of comp-{i+1} is {load_final[i]}")
            it.command("model solve ratio 1e-6")
            it.command(f"model save '{prj_dir}\Matrix_{i}'")
            print(f"'Matrix_{i}' saved!")
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++")