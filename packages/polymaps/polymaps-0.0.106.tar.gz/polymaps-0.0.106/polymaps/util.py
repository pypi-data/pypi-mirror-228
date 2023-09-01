import re, io
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.spatial import distance_matrix
import re

mass2element = {
    16: 'O',
    12: "C",
    1: "H",
    14: 'N', 
    -999: 'X',
}
element2color = {
    "O": 'rgba(255, 0, 0, 1.0)',
    "C": 'rgba(105, 105, 105, 1.0)',
    "H": 'rgba(255, 255, 255, 1.0)',
    'N': 'rgba(255, 0, 255, 1.0)',
    "X": 'rgba(138, 43, 226, 1.0)',
}
element2size = {
    "O": 74.,
    'N': 74.,
    "C": 77.,
    "H": 46.,
    "X": 90.,
}


def read_lmp_template(fname):
    lmp_str = ""
    with open(fname, 'r') as lmp_data:
        lmp_str = lmp_data.read()

    sec_names = []
    for sec_name in re.finditer('\n+[A-Z][a-z]*.*\n+', lmp_str):
        sec_names.append(sec_name.group(0))

    sec_strs = []
    next_str = lmp_str

    for sec_name in sec_names:
        _str_list = next_str.split(sec_name)
        sec_strs.append(_str_list[0])
        next_str = _str_list[1]


    sec_names = ['head',] + sec_names
    sec_strs.append(next_str)
    
    return sec_names, sec_strs

def write_lmp_template(fname, sec_names, sec_strs):
    
    lmp_str = sec_strs[0]
    
    for i in range(1, len(sec_strs)):
        lmp_str = lmp_str + '\n\n' + sec_names[i] + '\n\n' + sec_strs[i]
    
    with open(fname, 'w') as lmp_data:
        lmp_data.write(lmp_str)
    
    print('Written to file: ' + fname)
    return

def viz_lmp_template(filename):
    sec_names, sec_strs =read_lmp_template(filename)
    double_bonds=[]
    triple_bonds=[]
    sec_df = {}
    
    for i in range(1, len(sec_names)):
        
        if 'Types' in sec_names[i]:
            names = ['id', 'type']
        elif 'Charges' in sec_names[i]:
            names = ['id', 'q']
        elif 'Coords' in sec_names[i]:
            names = ['id', 'x', 'y', 'z']
        elif 'Bonds' in sec_names[i]:
            names = ['id', 'type', 'at1', 'at2']
        elif 'Angles' in sec_names[i]:
            names = ['id', 'type', 'at1', 'at2', 'at3']
        elif 'Dihedrals' in sec_names[i]:
            names = ['id', 'type', 'at1', 'at2', 'at3', 'at4']
        elif 'Impropers' in sec_names[i]:
            names = ['id', 'type', 'at1', 'at2', 'at3', 'at4']

        df = pd.read_csv(io.StringIO(sec_strs[i]), sep=r'\s+', names=names).reset_index(drop=True)
        df.index = df.index + 1
        sec_df[sec_names[i]] = df.copy(deep=True)
        del df
        df=None
    df = pd.concat([sec_df['\n\nTypes\n\n'], sec_df['\n\nCharges\n\n'], sec_df['\n\nCoords\n\n'], ], axis=1)
    df['mol'] = 1
    df = df[['id', 'mol', 'type', 'q', 'x', 'y', 'z']]
    df = df.loc[:,~df.columns.duplicated()]

    df['color'] = 'rgba(155, 155, 0, 1.0)'
    df['size'] = 15.2*3
    df['tip']=None
    bond_df = sec_df['\n\nBonds\n\n']
    bond_df['bond_order'] = 1
    bond_df.loc[double_bonds, 'bond_order'] = 2
    bond_df.loc[triple_bonds, 'bond_order'] = 3
    viz_mol(df, bond_df, annotation=True)

def read_lmp_data(fname):
    lmp_str = ""
    with open(fname, 'r') as lmp_data:
        lmp_str = lmp_data.read()
    
    sec_names = []
    for sec_name in re.finditer('\n+[A-Z][a-z]*.*\n+', lmp_str):
        sec_names.append(sec_name.group(0))
    
    sec_strs = []
    next_str = lmp_str
    mass_sec_id = -1
    atom_sec_id = -1
    bond_sec_id = -1
    angle_sec_id = -1
    dihedral_sec_id = -1
    improper_sec_id = -1
    
    lj_coeff_sec_id = -1
    bond_coeff_sec_id = -1
    angle_coeff_sec_id = -1
    dihedral_coeff_sec_id = -1
    improper_coeff_sec_id = -1
    for sec_name in sec_names:
        _str_list = next_str.split(sec_name)
        sec_strs.append(_str_list[0])
        next_str = _str_list[1]
        if "Masses" in sec_name:
            mass_sec_id = sec_names.index(sec_name) + 1
        if "Atoms" in sec_name:
            atom_sec_id = sec_names.index(sec_name) + 1
        if "Bonds" in sec_name:
            bond_sec_id = sec_names.index(sec_name) + 1
        if "Angles" in sec_name:
            angle_sec_id = sec_names.index(sec_name) + 1
        if "Dihedrals" in sec_name:
            dihedral_sec_id = sec_names.index(sec_name) + 1
        if "Impropers" in sec_name:
            improper_sec_id = sec_names.index(sec_name) + 1
        if 'Pair Coeffs' in sec_name:
            lj_coeff_sec_id = sec_names.index(sec_name) + 1
        if 'Bond Coeffs' in sec_name:
            bond_coeff_sec_id = sec_names.index(sec_name) + 1
        if 'Angle Coeffs' in sec_name:
            angle_coeff_sec_id = sec_names.index(sec_name) + 1
        if 'Dihedral Coeffs' in sec_name:
            dihedral_coeff_sec_id = sec_names.index(sec_name) + 1
        if 'Improper Coeffs' in sec_name:
            improper_coeff_sec_id = sec_names.index(sec_name) + 1

    sec_names = ['head',] + sec_names
    sec_strs.append(next_str)
    
    return sec_names, sec_strs, mass_sec_id, atom_sec_id, bond_sec_id, angle_sec_id, dihedral_sec_id, improper_sec_id, lj_coeff_sec_id, bond_coeff_sec_id, angle_coeff_sec_id, dihedral_coeff_sec_id, improper_coeff_sec_id

def write_lmp_data(fname, sec_names, sec_strs):
    lmp_str = sec_strs[0]
    for i in range(1, len(sec_strs)):
        lmp_str = lmp_str + sec_names[i] + sec_strs[i]
    with open(fname, 'w') as lmp_data:
        lmp_data.write(lmp_str)
    print('Written to file: ' + fname)
    return

def viz_mol(_df, _bond_df, annotation=False, box=None, writeHTML=False):
    
    df = _df.copy(deep=True)
    bond_df = _bond_df.copy(deep=True)
    
    df.loc[:, 'text'] = ['atom-'] * len(df)
    df.loc[:, 'text'] = df.loc[:, 'text'] + df.loc[:, 'id'].astype('str')

    df['tip'] = 'id: ' + df['id'].astype('str') + '<br>type: ' + df['type'].astype('str')
    if "element" in df.columns:
        df['tip'] = df['tip'] + '<br>element: ' + df['element'].astype('str')
    if "q" in df.columns:
        df['tip'] = df['tip'] + '<br>charge: ' + df['q'].astype('str')
    if "mol" in df.columns:
        df['tip'] = df['tip'] + '<br>mol: ' + df['mol'].astype('str')
    if "comment" in df.columns:
        df['tip'] = df['tip'] + '<br>comment: ' + df['comment'].astype('str')
    bond_df.loc[:, 'text'] = ['bond-'] * len(bond_df)
    bond_df.loc[:, 'text'] = bond_df.loc[:, 'text'] + bond_df.loc[:, 'id'].astype('str')
    
    bond_dict_x = df.set_index('id').to_dict()['x']
    bond_dict_y = df.set_index('id').to_dict()['y']
    bond_dict_z = df.set_index('id').to_dict()['z']
    bond_df.loc[:, 'x1'] = bond_df['at1'].map(bond_dict_x)
    bond_df.loc[:, 'y1'] = bond_df['at1'].map(bond_dict_y)
    bond_df.loc[:, 'z1'] = bond_df['at1'].map(bond_dict_z)

    bond_df.loc[:, 'x2'] = bond_df['at2'].map(bond_dict_x)
    bond_df.loc[:, 'y2'] = bond_df['at2'].map(bond_dict_y)
    bond_df.loc[:, 'z2'] = bond_df['at2'].map(bond_dict_z)
    
    df.loc[:, 'showarrow'] = False
    df.loc[:, 'opacity'] = 0.8
    df.loc[:, 'font']=[{'color':'rgba(0,0,255,1)',}] * len(df)
    bond_df.loc[:, 'showarrow'] = False
    bond_df.loc[:, 'opacity'] = 0.8
    bond_df.loc[:, 'font']=[{'color':'rgba(0,0,255,1)',}] * len(bond_df)
    bond_df.loc[:, 'x'] = (bond_df.loc[:, 'x1'] + bond_df.loc[:, 'x2']) * 0.5
    bond_df.loc[:, 'y'] = (bond_df.loc[:, 'y1'] + bond_df.loc[:, 'y2']) * 0.5
    bond_df.loc[:, 'z'] = (bond_df.loc[:, 'z1'] + bond_df.loc[:, 'z2']) * 0.5

    
    if annotation:
        annotation_list = df[['x', 'y', 'z', 'showarrow', 'opacity', 'text', 'font']].to_dict('records') + \
            bond_df[['x', 'y', 'z', 'showarrow', 'opacity', 'text', 'font']].to_dict('records')
    else:
        annotation_list = []
    data=[go.Scatter3d(x=df['x'], y=df['y'], z=df['z'], 
                       text=df['tip'],
                       mode='markers',
                       marker=dict(
                           color=df['color'],
                           size=df['size'] * 3.4 / (len(df)**(1./3.)),
                           opacity=1.0,
                       ))]
    
    for index, row in bond_df.iterrows():
        data.append(go.Scatter3d(x=[row['x1'], row['x2']], 
                                 y=[row['y1'], row['y2']], 
                                 z=[row['z1'], row['z2']], 
                                 mode='lines',
                                 line=dict(
                                     color='rgba(220, 200, 200, 0.5)',
                                     width=5,
                                 )))
        if row['bond_order'] == 2:
            
            
            data.append(go.Scatter3d(x=[row['x1'], row['x2']], 
                                     y=[row['y1'], row['y2']], 
                                     z=[row['z1'], row['z2']],
                                     mode='lines',
                                     line=dict(
                                         color='rgba(150, 150, 150, 0.35)',
                                         width=30,
                                     )))
            
            if row['bond_order'] == 3:            
                data.append(go.Scatter3d(x=[row['x1'], row['x2']], 
                                         y=[row['y1'], row['y2']], 
                                         z=[row['z1'], row['z2']],
                                         mode='lines',
                                         line=dict(
                                             color='rgba(100, 100, 100, 0.25)',
                                             width=50,
                                         )))
                
    xyzmin = min([df['x'].min(), df['y'].min(), df['z'].min()])
    xyzmax = max([df['x'].max(), df['y'].max(), df['z'].max()])
    if box != None:
        xlo = box[0][0]
        xhi = box[0][1]
        ylo = box[1][0]
        yhi = box[1][1]
        zlo = box[2][0]
        zhi = box[2][1]
        
        xyzmin = min([df['x'].min(), df['y'].min(), df['z'].min(), xlo, ylo, zlo])
        xyzmax = max([df['x'].max(), df['y'].max(), df['z'].max(), xhi, yhi, zhi])
        annotation_list.append({'x': xhi, 
                                'y': ylo, 
                                'z': zlo, 
                                'showarrow': False, 
                                'opacity': 1.0, 
                                'text': "X",  
                                'font': {'size': 30, 'color':'rgba(255,0,0,1)',}})
        annotation_list.append({'x': xlo, 
                                'y': yhi, 
                                'z': zlo, 
                                'showarrow': False, 
                                'opacity': 1.0, 
                                'text': "Y",  
                                'font': {'size': 30, 'color':'rgba(0,255,0,1)',}})
        annotation_list.append({'x': xlo, 
                                'y': ylo, 
                                'z': zhi, 
                                'showarrow': False, 
                                'opacity': 1.0, 
                                'text': "Z",  
                                'font': {'size': 30, 'color':'rgba(0,0,255,1)',}})
        data.append(go.Scatter3d(x=[xlo, xhi], 
                                 y=[ylo, ylo], 
                                 z=[zlo, zlo], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(225, 0, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        data.append(go.Scatter3d(x=[xlo, xlo], 
                                 y=[ylo, yhi], 
                                 z=[zlo, zlo], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(0, 225, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        data.append(go.Scatter3d(x=[xlo, xlo], 
                                 y=[ylo, ylo], 
                                 z=[zlo, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(0, 0, 225, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        
        data.append(go.Scatter3d(x=[xhi, xhi], 
                                 y=[ylo, ylo], 
                                 z=[zlo, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        data.append(go.Scatter3d(x=[xlo, xlo], 
                                 y=[yhi, yhi], 
                                 z=[zlo, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        data.append(go.Scatter3d(x=[xhi, xhi], 
                                 y=[yhi, yhi], 
                                 z=[zlo, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        
        data.append(go.Scatter3d(x=[xlo, xhi], 
                                 y=[ylo, ylo], 
                                 z=[zhi, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        data.append(go.Scatter3d(x=[xlo, xhi], 
                                 y=[yhi, yhi], 
                                 z=[zlo, zlo], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        data.append(go.Scatter3d(x=[xlo, xhi], 
                                 y=[yhi, yhi], 
                                 z=[zhi, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        
        data.append(go.Scatter3d(x=[xhi, xhi], 
                                 y=[ylo, yhi], 
                                 z=[zlo, zlo], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        data.append(go.Scatter3d(x=[xlo, xlo], 
                                 y=[ylo, yhi], 
                                 z=[zhi, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        data.append(go.Scatter3d(x=[xhi, xhi], 
                                 y=[ylo, yhi], 
                                 z=[zhi, zhi], 
                                 mode='lines', 
                                 line=dict(
                                     color='rgba(255, 255, 0, 1.0)',
                                     width=3,
                                 ),
                                 hovertemplate=None,
                                 hoverinfo="skip",
                                 ))
        
    
    fig = go.Figure(data=data)
    
    
    DeltaX = xyzmax - xyzmin
    fig.update_layout(
        scene = dict(
            annotations=annotation_list,
            xaxis = dict(nticks=10, range=[xyzmin-10,xyzmax+10],
                         backgroundcolor="rgba(80, 70, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            yaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 80, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            zaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 70, 80, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                         ),
        ),
        width=1400,
        height=1400,
        margin=dict(r=10, l=10, b=10, t=10),
        showlegend=False)
    fig.update_layout(scene_aspectmode='cube', paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
        scene_aspectmode='cube', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_layout(
        font_color="rgba(150,150,150,1)",
        title_font_color="rgba(150,150,150,1)",
        legend_title_font_color="rgba(150,150,150,1)",
    )

    if writeHTML:
        fig.write_html("vizmol.html")
    fig.show()
    
    
    
def open_lmp_data(lammps_data_file, viz=True, annotation=False, double_bonds=[], triple_bonds=[], box=False, unwrap=False, resize=False):
    sec_names, sec_strs, \
    mass_sec_id, atom_sec_id, \
    bond_sec_id, angle_sec_id, \
    dihedral_sec_id, improper_sec_id, \
    lj_coeff_sec_id, bond_coeff_sec_id, \
    angle_coeff_sec_id, dihedral_coeff_sec_id, \
    improper_coeff_sec_id = read_lmp_data(lammps_data_file)

    L_df = pd.read_csv(io.StringIO('\n'.join([x for x in sec_strs[0].split('\n') if "xlo" in x or "ylo" in x or "zlo" in x])), 
                sep=r'\s+', 
                names=['_min', '_max'], 
                usecols=[0, 1]).reset_index(drop=True)

    xhi = L_df.loc[0, '_max']
    xlo = L_df.loc[0, '_min']
    yhi = L_df.loc[1, '_max']
    ylo = L_df.loc[1, '_min']
    zhi = L_df.loc[2, '_max']
    zlo = L_df.loc[2, '_min']

    Lx = xhi - xlo
    Ly = yhi - ylo
    Lz = zhi - zlo

    mass_df = pd.read_csv(io.StringIO(sec_strs[mass_sec_id]), sep=r'\s+', names=['type', 'mass'], usecols=[0, 1]).reset_index(drop=True)
    mass_df['element'] = mass_df['mass'].round().map(mass2element)
    type_element_map = mass_df.set_index('type').to_dict()['element']

    if unwrap:
        comments = [x.split("#")[-1] for x in sec_strs[atom_sec_id].split("\n")]
        try:
            df = pd.read_csv(io.StringIO(sec_strs[atom_sec_id]), sep=r'\s+', 
                             names=['id', 'mol', 'type', 'q', 'x', 'y', 'z', 'ix', 'iy', 'iz'], 
                             usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).reset_index(drop=True)
        except:
            df = pd.read_csv(io.StringIO(sec_strs[atom_sec_id]), sep=r'\s+', 
                             names=['id', 'mol', 'type', 'q', 'x', 'y', 'z'], 
                             usecols=[0, 1, 2, 3, 4, 5, 6]).reset_index(drop=True)
            df["ix"] = 0
            df["iy"] = 0
            df["iz"] = 0

        df.index = df.index + 1
        df["comment"] = comments        
        df['_x'] = df['x']
        df['x'] = df['x'] + (Lx * df['ix'])
        df['_y'] = df['y']
        df['y'] = df['y'] + (Ly * df['iy'])
        df['_z'] = df['z']
        df['z'] = df['z'] + (Lx * df['iz'])
    else:
        comments = [x.split("#")[-1] for x in sec_strs[atom_sec_id].split("\n")]
        df = pd.read_csv(io.StringIO(sec_strs[atom_sec_id]), sep=r'\s+', names=['id', 'mol', 'type', 'q', 'x', 'y', 'z'], usecols=[0, 1, 2, 3, 4, 5, 6]).reset_index(drop=True)
        df.index = df.index + 1
        df["comment"] = comments
        if resize:
            xhi = df["x"].max() + 1.
            xlo = df["x"].min() - 1.
            yhi = df["y"].max() + 1.
            ylo = df["y"].min() - 1.
            zhi = df["z"].max() + 1.
            zlo = df["z"].min() - 1.
            Lx = xhi - xlo
            Ly = yhi - ylo
            Lz = zhi - zlo

    df['element'] = df['type'].map(type_element_map)
    df['color'] = df['element'].map(element2color)
    df['size'] = df['element'].map(element2size)

    try:
        bond_df = pd.read_csv(io.StringIO(sec_strs[bond_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2'], usecols=[0, 1, 2, 3]).reset_index(drop=True)
        bond_df.index = bond_df.index + 1
        bond_df['bond_order'] = 1
        bond_df.loc[double_bonds, 'bond_order'] = 2
        bond_df.loc[triple_bonds, 'bond_order'] = 3
    except:
        bond_df = pd.DataFrame()
        pass

    try:
        angle_df = pd.read_csv(io.StringIO(sec_strs[angle_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2', 'at3'], usecols=[0, 1, 2, 3, 4]).reset_index(drop=True)
        angle_df.index = angle_df.index + 1
    except:
        angle_df = pd.DataFrame()
        pass

    try:
        dihedral_df = pd.read_csv(io.StringIO(sec_strs[dihedral_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2', 'at3', 'at4'], usecols=[0, 1, 2, 3, 4, 5]).reset_index(drop=True)
        dihedral_df.index = dihedral_df.index + 1
    except:
        dihedral_df = pd.DataFrame()
        pass

    try:
        improper_df = pd.read_csv(io.StringIO(sec_strs[improper_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2', 'at3', 'at4'], usecols=[0, 1, 2, 3, 4, 5]).reset_index(drop=True)
        improper_df.index = improper_df.index + 1
    except:
        improper_df = pd.DataFrame()
        pass

    lj_coeff = None
    if lj_coeff_sec_id != -1:
        lj_coeff = pd.read_csv(io.StringIO(sec_strs[lj_coeff_sec_id]), names=['type', 'epsilon', 'sigma'], sep=r'\s+')
    bond_coeff = None
    if bond_coeff_sec_id != -1:
        bond_coeff = pd.read_csv(io.StringIO(sec_strs[bond_coeff_sec_id]), names=['type', 'kr', 'r0'], sep=r'\s+')
    angle_coeff = None
    if angle_coeff_sec_id != -1:
        angle_coeff = pd.read_csv(io.StringIO(sec_strs[angle_coeff_sec_id]), names=['type', 'ktheta', 'theta0'], sep=r'\s+')
    dihedral_coeff = None
    if dihedral_coeff_sec_id != -1:
        dihedral_coeff = pd.read_csv(io.StringIO(sec_strs[dihedral_coeff_sec_id]), names=['type', 'k1', 'k2', 'k3', 'k4'], sep=r'\s+')
    improper_coeff = None
    if improper_coeff_sec_id != -1:
        improper_coeff = pd.read_csv(io.StringIO(sec_strs[improper_coeff_sec_id]), names=['type', 'k', 'd', 'n'], sep=r'\s+')
    if viz==True: 
        if box==True:
            viz_mol(df, bond_df, annotation=annotation, box=[[xlo, xhi], [ylo, yhi], [zlo, zhi]])
        else:
            viz_mol(df, bond_df, annotation=annotation, box=None)
    
    return mass_df, df, bond_df, angle_df, dihedral_df, improper_df, [[xlo, xhi], [ylo, yhi], [zlo, zhi]], lj_coeff, bond_coeff, angle_coeff, dihedral_coeff, improper_coeff



def read_xyz_traj(filename='traj.xyz'):
    colnames = ["at", "x", "y", "z"]
    with open(filename, 'r') as myfile:
        xyz = myfile.read()
    frame_natoms = []
    frame_nsteps = []
    frame_xyzs = []
    line_list = xyz.split('\n')
    i = 0
    while i < len(line_list):
        if line_list[i].isdigit():
            frame_natoms.append(int(line_list[i]))
            frame_nsteps.append(int(re.sub("[^0-9]", "", line_list[i+1])))
            frame_xyzs.append(pd.read_csv(io.StringIO("\n".join(line_list[i+2:i+2+frame_natoms[-1]])), sep=r"\s+", names=colnames))
            i = i + 2 + frame_natoms[-1]
        else:
            i = i + 1
    print("Read xyz file with: " + str(frame_natoms[-1]) + " atoms, " + str(len(frame_nsteps)) + " frames. ")
    return frame_natoms, frame_nsteps, frame_xyzs


def viz_xyz_traj(_natoms, _nsteps, _xyzs, mass_df, writeHTML=False):
    _xyz_lims = pd.DataFrame([[_xyzs[i]["x"].min(), _xyzs[i]["x"].max(), 
                               _xyzs[i]["y"].min(), _xyzs[i]["y"].max(), 
                               _xyzs[i]["z"].min(), _xyzs[i]["z"].max()] for i in range(0, len(_xyzs))], 
                             columns=["xmin", "xmax", "ymin", "ymax", "zmin", "zmax"])
    xyzmin = min(_xyz_lims["xmin"].min(), _xyz_lims["ymin"].min(), _xyz_lims["zmin"].min())
    xyzmax = max(_xyz_lims["xmax"].max(), _xyz_lims["ymax"].max(), _xyz_lims["zmax"].max())
    duration = 150

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": duration, 
                                              "redraw": True},
                                    "fromcurrent": True, 
                                    "mode": "immediate",
                                    "transition": {"duration": duration,
                                                   "easing": "quadratic-in-out"}
                                   }],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": duration, 
                                                "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": duration}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Step:",
            "visible": True,
            "xanchor": "left"
        },
        "transition": {"duration": duration, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }


    # make frames
    for k in range(0, len(_xyzs)):
        _xyzs[k]["element"] = _xyzs[k]["at"].map(dict(zip(mass_df["type"], mass_df["element"])))
        _xyzs[k]["mass"] = _xyzs[k]["at"].map(dict(zip(mass_df["type"], mass_df["mass"])))
        _xyzs[k]["color"] = _xyzs[k]["element"].map(element2color)
        _xyzs[k]["size"] = _xyzs[k]["element"].map(element2size)
        _xyzs[k]['id'] = _xyzs[k].index + 1
        _xyzs[k]['tip'] = "id: " + _xyzs[k]['id'].astype('str') + '<br>' + 'type: ' + _xyzs[k]['at'].astype('str') + '<br>'
        curr_frame = go.Frame(
            data=[
                go.Scatter3d(
                #dict(
                    mode="markers",
                    x=_xyzs[k]["x"],
                    y=_xyzs[k]["y"],
                    z=_xyzs[k]["z"],
                    text=_xyzs[k]['tip'],
                    marker=dict(
                        color=_xyzs[k]["color"],
                        size=_xyzs[k]["size"] * 3.4 / (len(_xyzs[k])**(1./3.)),
                        opacity=1.0,
                    ),
                )
            ],
            name=str(_nsteps[k]),
        )


        fig_dict["frames"].append(curr_frame)

        slider_step = {
            "args": [
                [str(_nsteps[k])],
                {
                    "frame": {
                        "duration": duration,
                        "redraw": True,
                    },
                    "mode": "immediate",
                    "transition": {
                        "duration": duration,
                    }
                }
            ],
            "label": str(_nsteps[k]),
            "method": "animate",
            "name": str(_nsteps[k]),
        }
        sliders_dict["steps"].append(slider_step)


    fig_dict['data'] = fig_dict["frames"][0]['data']
    fig_dict["layout"]["sliders"] = [sliders_dict]
    fig = go.Figure(fig_dict)

    DeltaX = xyzmax - xyzmin
    annotation_list = []
    fig.update_layout(
        scene = dict(
            annotations=annotation_list,
            xaxis = dict(nticks=10, range=[xyzmin-10,xyzmax+10],
                         backgroundcolor="rgba(80, 70, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            yaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 80, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            zaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 70, 80, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                         ),
        ),
        width=1400,
        height=1400,
        margin=dict(r=10, l=10, b=10, t=10),
        showlegend=False)
    fig.update_layout(scene_aspectmode='cube', paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
        scene_aspectmode='cube', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_layout(
        font_color="rgba(150,150,150,1)",
        title_font_color="rgba(150,150,150,1)",
        legend_title_font_color="rgba(150,150,150,1)",
    )

    if writeHTML:
        fig.write_html("xyztraj.html")
    fig.show()
    
def lmp_traj2pandas(fname="traj.lammpstrj"):
    traj = None
    with open(fname, 'r') as myfile:
        traj = myfile.read()

    _nsteps = []
    _natoms = []
    _xyzs = []
    traj_list = traj.split("\n")

    xlo = []
    xhi = []
    ylo = []
    yhi = []
    zlo = []
    zhi = []
    i = 0
    while i < len(traj_list):
        if traj_list[i].startswith("ITEM:"):
            if "TIMESTEP" in traj_list[i]:
                _nsteps.append(int(traj_list[i+1]))
                _natoms.append(int(traj_list[i+3]))
                _x, _y, _z = traj_list[i+5:i+8]
                _xlo, _xhi = _x.split(" ")
                _ylo, _yhi = _y.split(" ")
                _zlo, _zhi = _z.split(" ")
                xlo.append(float(_xlo))
                xhi.append(float(_xhi))
                ylo.append(float(_ylo))
                yhi.append(float(_yhi))
                zlo.append(float(_zlo))
                zhi.append(float(_zhi))
                _xyz = pd.read_csv(io.StringIO(traj_list[i+8].replace("ITEM: ATOMS ", "") + "\n" + "\n".join(traj_list[i+9:i+9+_natoms[-1]])), header=0, sep=r"\s+")
                _xyzs.append(_xyz)
                i = i+9+_natoms[-1]
        else:
            i = i + 1
    return _xyzs

def viz_lmp_traj(type2cgenff, fname="traj.lammpstrj", writeHTML=False):
    traj = None
    with open(fname, 'r') as myfile:
        traj = myfile.read()

    _nsteps = []
    _natoms = []
    _xyzs = []
    traj_list = traj.split("\n")


    xlo = []
    xhi = []
    ylo = []
    yhi = []
    zlo = []
    zhi = []
    i = 0
    while i < len(traj_list):
        if traj_list[i].startswith("ITEM:"):
            if "TIMESTEP" in traj_list[i]:
                _nsteps.append(int(traj_list[i+1]))
                _natoms.append(int(traj_list[i+3]))
                _x, _y, _z = traj_list[i+5:i+8]
                _xlo, _xhi = _x.split(" ")
                _ylo, _yhi = _y.split(" ")
                _zlo, _zhi = _z.split(" ")
                xlo.append(float(_xlo))
                xhi.append(float(_xhi))
                ylo.append(float(_ylo))
                yhi.append(float(_yhi))
                zlo.append(float(_zlo))
                zhi.append(float(_zhi))
                _xyz = pd.read_csv(io.StringIO(traj_list[i+8].replace("ITEM: ATOMS ", "") + "\n" + "\n".join(traj_list[i+9:i+9+_natoms[-1]])), header=0, sep=r"\s+")
                _xyz["element"] = _xyz["mass"].round(0).map(mass2element)
                _xyz["cgenff"] = _xyz["type"].map(type2cgenff)
                _xyz["color"] = _xyz["element"].map(element2color)
                _xyz["size"] = _xyz["element"].map(element2size)
                _xyz['tip'] = "id: " + _xyz['id'].astype('str') + '<br>' + \
                              'type: ' + _xyz['type'].astype('str') + '<br>' + \
                              'cgenff: ' + _xyz['cgenff'].astype('str') + '<br>' + \
                              'charge: ' + _xyz["q"].apply(lambda i: ("+" if i > 0 else "") + str(i)).astype('str')
                _xyzs.append(_xyz)
                i = i+9+_natoms[-1]
        else:
            i = i + 1


    xyzmin = min(min(xlo), min(ylo), min(zlo))
    xyzmax = max(max(xhi), max(yhi), max(zhi))

    duration = 100

    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": duration, 
                                              "redraw": True},
                                    "fromcurrent": True, 
                                    "mode": "immediate",
                                    "transition": {"duration": duration,
                                                   "easing": "quadratic-in-out"}
                                   }],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": duration, 
                                                "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": duration}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Step:",
            "visible": True,
            "xanchor": "left"
        },
        "transition": {"duration": duration, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    annotation_list = []
    annotation_list.append({'x': xhi[0]+1, 
                            'y': ylo[0], 
                            'z': zlo[0], 
                            'showarrow': False, 
                            'opacity': 1.0, 
                            'text': "X",  
                            'font': {'size': 30, 'color':'rgba(255,0,0,1)',}})
    annotation_list.append({'x': xlo[0], 
                            'y': yhi[0]+1, 
                            'z': zlo[0], 
                            'showarrow': False, 
                            'opacity': 1.0, 
                            'text': "Y",  
                            'font': {'size': 30, 'color':'rgba(0,255,0,1)',}})
    annotation_list.append({'x': xlo[0], 
                            'y': ylo[0], 
                            'z': zhi[0]+1, 
                            'showarrow': False, 
                            'opacity': 1.0, 
                            'text': "Z",  
                            'font': {'size': 30, 'color':'rgba(0,0,255,1)',}})
    # make frames
    for k in range(0, len(_xyzs)):
        _xyzs[k]["color"] = _xyzs[k]["element"].map(element2color)
        _xyzs[k]["size"] = _xyzs[k]["element"].map(element2size)
        curr_frame = go.Frame(
            data=[
                go.Scatter3d(
                    mode="markers",
                    x=_xyzs[k]["x"],
                    y=_xyzs[k]["y"],
                    z=_xyzs[k]["z"],
                    text=_xyzs[k]['tip'],
                    marker=dict(
                        color=_xyzs[k]["color"],
                        size=_xyzs[k]["size"] * 3.4 / (len(_xyzs[k])**(1./3.)),
                        opacity=1.0,
                    ),
                ),

                go.Scatter3d(x=[xlo[k], xhi[k]], 
                    y=[ylo[k], ylo[k]], 
                    z=[zlo[k], zlo[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(225, 0, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xlo[k]], 
                    y=[ylo[k], yhi[k]], 
                    z=[zlo[k], zlo[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(0, 225, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xlo[k]], 
                    y=[ylo[k], ylo[k]], 
                    z=[zlo[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(0, 0, 225, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xhi[k], xhi[k]], 
                    y=[ylo[k], ylo[k]], 
                    z=[zlo[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xlo[k]], 
                    y=[yhi[k], yhi[k]], 
                    z=[zlo[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xhi[k], xhi[k]], 
                    y=[yhi[k], yhi[k]], 
                    z=[zlo[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xhi[k]], 
                    y=[ylo[k], ylo[k]], 
                    z=[zhi[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xhi[k]], 
                    y=[yhi[k], yhi[k]], 
                    z=[zlo[k], zlo[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xhi[k]], 
                    y=[yhi[k], yhi[k]], 
                    z=[zhi[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xhi[k], xhi[k]], 
                    y=[ylo[k], yhi[k]], 
                    z=[zlo[k], zlo[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xlo[k], xlo[k]], 
                    y=[ylo[k], yhi[k]], 
                    z=[zhi[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                )), 
                go.Scatter3d(x=[xhi[k], xhi[k]], 
                    y=[ylo[k], yhi[k]], 
                    z=[zhi[k], zhi[k]], 
                    mode='lines', 
                    line=dict(
                     color='rgba(255, 255, 0, 1.0)',
                     width=3,
                ))
            ],
            name=str(_nsteps[k]),
        )






        fig_dict["frames"].append(curr_frame)

        slider_step = {
            "args": [
                [str(_nsteps[k])],
                {
                    "frame": {
                        "duration": duration,
                        "redraw": True,
                    },
                    "mode": "immediate",
                    "transition": {
                        "duration": duration,
                    }
                }
            ],
            "label": str(_nsteps[k]),
            "method": "animate",
            "name": str(_nsteps[k]),
        }
        sliders_dict["steps"].append(slider_step)


    fig_dict['data'] = fig_dict["frames"][0]['data']
    fig_dict["layout"]["sliders"] = [sliders_dict]
    fig = go.Figure(fig_dict)

    DeltaX = xyzmax - xyzmin
    fig.update_layout(
        scene = dict(
            annotations=annotation_list,
            xaxis = dict(nticks=10, range=[xyzmin-10,xyzmax+10],
                         backgroundcolor="rgba(80, 70, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            yaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 80, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            zaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 70, 80, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                         ),
        ),
        width=1400,
        height=1400,
        margin=dict(r=10, l=10, b=10, t=10),
        showlegend=False)
    fig.update_layout(scene_aspectmode='cube', paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
        scene_aspectmode='cube', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_layout(
        font_color="rgba(150,150,150,1)",
        title_font_color="rgba(150,150,150,1)",
        legend_title_font_color="rgba(150,150,150,1)",
    )
    if writeHTML:
        fig.write_html(fname+".html")
    fig.show()


def viz_lmp_data(lammps_data_file, annotation=False, double_bonds=[], triple_bonds=[]):
    #lammps_data_file = './mcmd/ec/monomer.data'
    sec_names, sec_strs, mass_sec_id, atom_sec_id, bond_sec_id, angle_sec_id, dihedral_sec_id, improper_sec_id, lj_coeff_sec_id, bond_coeff_sec_id, angle_coeff_sec_id, dihedral_coeff_sec_id, improper_coeff_sec_id = read_lmp_data(lammps_data_file)
    #sec_names, sec_strs, mass_sec_id, atom_sec_id, bond_sec_id, angle_sec_id, dihedral_sec_id, improper_sec_id = read_lmp_data(lammps_data_file)

    mass_df = pd.read_csv(io.StringIO(sec_strs[mass_sec_id]), sep=r'\s+', names=['type', 'mass'], usecols=[0, 1]).reset_index(drop=True)
    mass_df['element'] = mass_df['mass'].round().map({
        16: 'O',
        12: "C",
        1: "H",
        14: 'N', 
    })
    type_element_map = mass_df.set_index('type').to_dict()['element']

    df = pd.read_csv(io.StringIO(sec_strs[atom_sec_id]), sep=r'\s+', names=['id', 'mol', 'type', 'q', 'x', 'y', 'z'], usecols=[0, 1, 2, 3, 4, 5, 6]).reset_index(drop=True)
    df.index = df.index + 1
    df['element'] = df['type'].map(type_element_map)
    df['color'] = df['element'].map({
        "O": 'rgba(255, 255, 255, 1.0)',
        "C": 'rgba(105, 105, 105, 1.0)',
        "H": 'rgba(255, 0, 0, 1.0)',
        'N': 'rgba(255, 0, 255, 1.0)',
    })
    df['size'] = df['element'].map({
        "O": 15.2*3,
        'N': 16.3*3,
        "C": 17.0*3,
        "H": 12.0*3,
    })
    df['<br>'] = '<br>'
    df['id: '] = 'id: '
    df['type: '] = 'type: '
    df['charge: '] = 'charge: '
    df['mol: '] = 'mol: '
    df['tip'] = df['id: '] + df['id'].astype('str') + df['<br>'] + df['type: '] + df['type'].astype('str') + df['<br>'] + df['mol: '] + df['mol'].astype('str') + df['<br>'] + df['charge: '] + df['q'].astype('str')

    bond_df = pd.read_csv(io.StringIO(sec_strs[bond_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2'], usecols=[0, 1, 2, 3]).reset_index(drop=True)
    bond_df.index = bond_df.index + 1
    bond_df['bond_order'] = 1
    bond_df.loc[double_bonds, 'bond_order'] = 2
    bond_df.loc[triple_bonds, 'bond_order'] = 3
    #print(df, bond_df)
    angle_df = pd.read_csv(io.StringIO(sec_strs[angle_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2', 'at3'], usecols=[0, 1, 2, 3, 4]).reset_index(drop=True)
    angle_df.index = angle_df.index + 1

    dihedral_df = pd.read_csv(io.StringIO(sec_strs[dihedral_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2', 'at3', 'at4'], usecols=[0, 1, 2, 3, 4, 5]).reset_index(drop=True)
    dihedral_df.index = dihedral_df.index + 1

    improper_df = pd.read_csv(io.StringIO(sec_strs[improper_sec_id]), sep=r'\s+', names=['id', 'type', 'at1', 'at2', 'at3', 'at4'], usecols=[0, 1, 2, 3, 4, 5]).reset_index(drop=True)
    improper_df.index = improper_df.index + 1

    viz_mol(df, bond_df, annotation=annotation)
    return mass_df, df, bond_df, angle_df, dihedral_df, improper_df
    
def build_react_template(df, bond_df, angle_df, dihedral_df, improper_df, selected_atoms, template_file_name):
    atom_id_remap = dict(zip(selected_atoms, [x + 1 for x in range(len(selected_atoms))]))

    out_type = df.loc[selected_atoms, 'type'].reset_index(drop=True).copy(deep=True)
    out_type.index += 1
    out_q = df.loc[selected_atoms, 'q'].reset_index(drop=True).copy(deep=True)
    out_q.index += 1
    out_xyz = df.loc[selected_atoms, ['x', 'y', 'z']].reset_index(drop=True).copy(deep=True)
    out_xyz.index += 1
    out_str = "\n\nTypes\n\n" + out_type.to_string(header=False) + "\n\nCharges\n\n" + out_q.to_string(header=False) + "\n\nCoords\n\n" + out_xyz.to_string(header=False)

    bond_set1 = set(bond_df[bond_df['at1'].isin(selected_atoms)].index.to_list())
    bond_set2 = set(bond_df[bond_df['at2'].isin(selected_atoms)].index.to_list())
    bond_list = list(bond_set1 & bond_set2)
    bond_df2 = bond_df.loc[bond_list, :].reset_index(drop=True).copy(deep=True)
    bond_df2.index = bond_df2.index + 1

    bond_df2 = bond_df2.assign(at1=bond_df2.loc[:,'at1'].map(atom_id_remap))
    bond_df2 = bond_df2.assign(at2=bond_df2.loc[:,'at2'].map(atom_id_remap))
    out_str = out_str + "\n\nBonds\n\n" + bond_df2[['type', 'at1', 'at2']].to_string(header=False)

    angle_set1 = set(angle_df[angle_df['at1'].isin(selected_atoms)].index.to_list())
    angle_set2 = set(angle_df[angle_df['at2'].isin(selected_atoms)].index.to_list())
    angle_set3 = set(angle_df[angle_df['at3'].isin(selected_atoms)].index.to_list())
    angle_list = list(angle_set1 & angle_set2 & angle_set3)
    angle_df2 = angle_df.loc[angle_list, :].reset_index(drop=True).copy(deep=True)
    angle_df2.index = angle_df2.index + 1
    angle_df2 = angle_df2.assign(at1=angle_df2.loc[:,'at1'].map(atom_id_remap))
    angle_df2 = angle_df2.assign(at2=angle_df2.loc[:,'at2'].map(atom_id_remap))
    angle_df2 = angle_df2.assign(at3=angle_df2.loc[:,'at3'].map(atom_id_remap))
    out_str = out_str + "\n\nAngles\n\n" + angle_df2[['type', 'at1', 'at2', 'at3']].to_string(header=False)

    dihedral_set1 = set(dihedral_df[dihedral_df['at1'].isin(selected_atoms)].index.to_list())
    dihedral_set2 = set(dihedral_df[dihedral_df['at2'].isin(selected_atoms)].index.to_list())
    dihedral_set3 = set(dihedral_df[dihedral_df['at3'].isin(selected_atoms)].index.to_list())
    dihedral_set4 = set(dihedral_df[dihedral_df['at4'].isin(selected_atoms)].index.to_list())
    dihedral_list = list(dihedral_set1 & dihedral_set2 & dihedral_set3 & dihedral_set4)
    dihedral_df2 = dihedral_df.loc[dihedral_list, :].reset_index(drop=True).copy(deep=True)
    dihedral_df2.index = dihedral_df2.index + 1
    dihedral_df2 = dihedral_df2.assign(at1=dihedral_df2.loc[:,'at1'].map(atom_id_remap))
    dihedral_df2 = dihedral_df2.assign(at2=dihedral_df2.loc[:,'at2'].map(atom_id_remap))
    dihedral_df2 = dihedral_df2.assign(at3=dihedral_df2.loc[:,'at3'].map(atom_id_remap))
    dihedral_df2 = dihedral_df2.assign(at4=dihedral_df2.loc[:,'at4'].map(atom_id_remap))
    out_str = out_str + "\n\nDihedrals\n\n" + dihedral_df2[['type', 'at1', 'at2', 'at3', 'at4']].to_string(header=False)
    
    improper_set1 = set(improper_df[improper_df['at1'].isin(selected_atoms)].index.to_list())
    improper_set2 = set(improper_df[improper_df['at2'].isin(selected_atoms)].index.to_list())
    improper_set3 = set(improper_df[improper_df['at3'].isin(selected_atoms)].index.to_list())
    improper_set4 = set(improper_df[improper_df['at4'].isin(selected_atoms)].index.to_list())
    improper_list = list(improper_set1 & improper_set2 & improper_set3 & improper_set4)
    improper_df2 = improper_df.loc[improper_list, :].reset_index(drop=True).copy(deep=True)
    improper_df2.index = improper_df2.index + 1
    improper_df2 = improper_df2.assign(at1=improper_df2.loc[:,'at1'].map(atom_id_remap))
    improper_df2 = improper_df2.assign(at2=improper_df2.loc[:,'at2'].map(atom_id_remap))
    improper_df2 = improper_df2.assign(at3=improper_df2.loc[:,'at3'].map(atom_id_remap))
    improper_df2 = improper_df2.assign(at4=improper_df2.loc[:,'at4'].map(atom_id_remap))
    out_str = out_str + "\n\nImpropers\n\n" + improper_df2[['type', 'at1', 'at2', 'at3', 'at4']].to_string(header=False)

    header_str = 'EC templated, generated by xyan11@uic.edu\n\n' + str(len(out_type)) + ' atoms\n' + \
    str(len(bond_df2)) + ' bonds\n' + \
    str(len(angle_df2)) + ' angles\n' + \
    str(len(dihedral_df2)) + ' dihedrals\n' + \
    str(len(improper_df2)) + ' impropers'

    sec_strs = [header_str,
               out_type.to_string(header=False), 
               out_q.to_string(header=False), 
               out_xyz.to_string(header=False), 
               bond_df2[['type', 'at1', 'at2']].to_string(header=False), 
               angle_df2[['type', 'at1', 'at2', 'at3']].to_string(header=False), 
               dihedral_df2[['type', 'at1', 'at2', 'at3', 'at4']].to_string(header=False), 
               improper_df2[['type', 'at1', 'at2', 'at3', 'at4']].to_string(header=False),
              ]
    sec_names = ['', 'Types', 'Charges', 'Coords', 'Bonds', 'Angles', 'Dihedrals', 'Impropers',]

    write_lmp_template(template_file_name, sec_names, sec_strs)
    return atom_id_remap

def build_map_file(map_fname, 
                   template_df, 
                   initiator_atom_ids, 
                   edge_atom_ids, 
                   delete_atom_template_ids, 
                   edge_atom_template_ids):
    mol1 = template_df[template_df["mol"]==1]
    mol2 = template_df[template_df["mol"]==2]
    initiator_atom_template_ids = template_df[template_df["id"].isin(initiator_atom_ids)]["template_atom_id"].tolist()
    outstr = """LAMMPS reaction map file generated by xyan11@uic.edu

""" + "%d" % len(edge_atom_template_ids) + """ edgeIDs
""" + "%d" % len(delete_atom_template_ids) + """ deleteIDs
""" + "%d" % len(template_df) + """ equivalences

InitiatorIDs

""" + "\n".join(["%d" % x for x in initiator_atom_template_ids]) + """

DeleteIDs

""" + "\n".join(["%d" % x for x in delete_atom_template_ids]) + """

EdgeIDs

""" + "\n".join(["%d" % x for x in edge_atom_template_ids]) + """

Equivalences

""" + "\n".join(["%d" % x + " " + "%d" % x for x in template_df["template_atom_id"]]) + """
"""
    with open(map_fname, "w") as wf:
        wf.write(outstr)

def build_peo(dop):

    head_mass_df, head_df, head_bond_df, head_angle_df, head_dihedral_df, head_improper_df, \
    [[head_xlo, head_xhi], [head_ylo, head_yhi], [head_zlo, head_zhi]], \
    head_lj_coeff, head_bond_coeff, head_angle_coeff, head_dihedral_coeff, head_improper_coeff = open_lmp_data('./MeOH_head.lmp', viz=False)
    head_cgenff = ['OG311', 'HGP1', 'CG321', 'HGA2', 'HGA2', 'X']
    head_df['cgenff'] = head_cgenff

    monomer_mass_df, monomer_df, monomer_bond_df, monomer_angle_df, monomer_dihedral_df, monomer_improper_df, \
    [[monomer_xlo, monomer_xhi], [monomer_ylo, monomer_yhi], [monomer_zlo, monomer_zhi]], \
    monomer_lj_coeff, monomer_bond_coeff, monomer_angle_coeff, monomer_dihedral_coeff, monomer_improper_coeff = open_lmp_data('./eo_monomer.lmp', viz=False)
    monomer_cgenff = ['CG321', 'HGA2', 'HGA2', 'OG301', 'CG321', 'HGA2', 'HGA2', 'X']
    monomer_df['cgenff'] = monomer_cgenff

    monomer_mass_df["type"] = monomer_mass_df["type"] + head_mass_df["type"].max() - 1
    monomer_df["type"] = monomer_df["type"] + head_df["type"].max() - 1
    monomer_bond_df["type"] = monomer_bond_df["type"] + head_bond_df["type"].max()
    monomer_angle_df["type"] = monomer_angle_df["type"] + head_angle_df["type"].max()
    monomer_dihedral_df["type"] = monomer_dihedral_df["type"] + head_dihedral_df["type"].max()
    monomer_improper_df["type"] = monomer_improper_df["type"] + head_improper_df["type"].max()

    tail_mass_df, tail_df, tail_bond_df, tail_angle_df, tail_dihedral_df, tail_improper_df, \
    [[tail_xlo, tail_xhi], [tail_ylo, tail_yhi], [tail_zlo, tail_zhi]], \
    tail_lj_coeff, tail_bond_coeff, tail_angle_coeff, tail_dihedral_coeff, tail_improper_coeff = open_lmp_data('./MeOH_tail.lmp', viz=False)
    tail_cgenff = ['CG321', 'HGA2', 'HGA2', 'OG311', 'HGP1']
    tail_df['cgenff'] = tail_cgenff

    tail_mass_df["type"] = tail_mass_df["type"] + monomer_mass_df["type"].max() - 1
    tail_df["type"] = tail_df["type"] + monomer_df["type"].max() - 1
    tail_bond_df["type"] = tail_bond_df["type"] + monomer_bond_df["type"].max()
    tail_angle_df["type"] = tail_angle_df["type"] + monomer_angle_df["type"].max()
    tail_dihedral_df["type"] = tail_dihedral_df["type"] + monomer_dihedral_df["type"].max()
    tail_improper_df["type"] = tail_improper_df["type"] + monomer_improper_df["type"].max()

    polymer_df = head_df.copy(deep=True)
    polymer_bond_df = head_bond_df.copy(deep=True)
    polymer_angle_df = head_angle_df.copy(deep=True)
    polymer_dihedral_df = head_dihedral_df.copy(deep=True)
    polymer_improper_df = head_improper_df.copy(deep=True)

    polymer_mass_df = head_mass_df.copy(deep=True)
    polymer_mass_df = pd.concat([polymer_mass_df.drop(polymer_mass_df.tail(1).index), monomer_mass_df], axis=0, ignore_index=True)
    polymer_mass_df.index = polymer_mass_df.index + 1

    polymer_mass_df = pd.concat([polymer_mass_df.drop(polymer_mass_df.tail(1).index), tail_mass_df], axis=0, ignore_index=True)
    polymer_mass_df.index = polymer_mass_df.index + 1

    for i in range(0, dop):
        tail_anchor = len(polymer_df)

        _df = monomer_df.copy(deep=True)
        head_atom = 1
        _bond_df = monomer_bond_df.copy(deep=True)
        _angle_df = monomer_angle_df.copy(deep=True)
        _dihedral_df = monomer_dihedral_df.copy(deep=True)
        _improper_df = monomer_improper_df.copy(deep=True)

        # process coordinates
        # reflection about X-Y plane
        if i % 2 == 1:
            _df.loc[:, 'z'] = 0.0 - _df.loc[:, 'z']
        # translate
        disp_vec = polymer_df.loc[tail_anchor, 'x':'z'] - _df.loc[1, 'x':'z']
        _df.loc[:, 'x':'z'] = _df.loc[:, 'x':'z'] + disp_vec

        # drop the anchor row, it will be replaced by the new head atom from _df
        polymer_df = polymer_df.drop(polymer_df.tail(1).index)

        # update ids in the new monomer
        max_atom_id = polymer_df['id'].max()
        max_bond_id = polymer_bond_df['id'].max()
        max_angle_id = polymer_angle_df['id'].max()
        max_dihedral_id = polymer_dihedral_df['id'].max()
        max_improper_id = polymer_improper_df['id'].max()

        _df['id'] = _df['id'] + max_atom_id
        _bond_df['at1'] = _bond_df['at1'] + max_atom_id
        _bond_df['at2'] = _bond_df['at2'] + max_atom_id
        _angle_df['at1'] = _angle_df['at1'] + max_atom_id
        _angle_df['at2'] = _angle_df['at2'] + max_atom_id
        _angle_df['at3'] = _angle_df['at3'] + max_atom_id
        _dihedral_df['at1'] = _dihedral_df['at1'] + max_atom_id
        _dihedral_df['at2'] = _dihedral_df['at2'] + max_atom_id
        _dihedral_df['at3'] = _dihedral_df['at3'] + max_atom_id
        _dihedral_df['at4'] = _dihedral_df['at4'] + max_atom_id
        _improper_df['at1'] = _improper_df['at1'] + max_atom_id
        _improper_df['at2'] = _improper_df['at2'] + max_atom_id
        _improper_df['at3'] = _improper_df['at3'] + max_atom_id
        _improper_df['at4'] = _improper_df['at4'] + max_atom_id

        head_atom = 1 + max_atom_id
        _bond_df['id'] = _bond_df['id'] + max_bond_id
        _angle_df['id'] = _angle_df['id'] + max_angle_id
        _dihedral_df['id'] = _dihedral_df['id'] + max_dihedral_id
        _improper_df['id'] = _improper_df['id'] + max_improper_id

        # combine polymer and new monomer
        polymer_df = pd.concat([polymer_df, _df], axis=0, ignore_index=True)
        polymer_df.index = polymer_df.index + 1
        polymer_bond_df = pd.concat([polymer_bond_df, _bond_df], axis=0, ignore_index=True)
        polymer_bond_df.index = polymer_bond_df.index + 1
        polymer_angle_df = pd.concat([polymer_angle_df, _angle_df], axis=0, ignore_index=True)
        polymer_angle_df.index = polymer_angle_df.index + 1
        polymer_dihedral_df = pd.concat([polymer_dihedral_df, _dihedral_df], axis=0, ignore_index=True)
        polymer_dihedral_df.index = polymer_dihedral_df.index + 1
        polymer_improper_df = pd.concat([polymer_improper_df, _improper_df], axis=0, ignore_index=True)
        polymer_improper_df.index = polymer_improper_df.index + 1


    tail_anchor = len(polymer_df)

    _df = tail_df.copy(deep=True)
    head_atom = 1
    _bond_df = tail_bond_df.copy(deep=True)
    _angle_df = tail_angle_df.copy(deep=True)
    _dihedral_df = tail_dihedral_df.copy(deep=True)
    _improper_df = tail_improper_df.copy(deep=True)

    # process coordinates
    # reflection about X-Y plane
    if i % 2 != 1:
        _df.loc[:, 'z'] = 0.0 - _df.loc[:, 'z']
    # translate
    disp_vec = polymer_df.loc[tail_anchor, 'x':'z'] - _df.loc[1, 'x':'z']
    _df.loc[:, 'x':'z'] = _df.loc[:, 'x':'z'] + disp_vec

    # drop the anchor row, it will be replaced by the new head atom from _df
    polymer_df = polymer_df.drop(polymer_df.tail(1).index)

    # update ids in the new monomer
    max_atom_id = polymer_df['id'].max()
    max_bond_id = polymer_bond_df['id'].max()
    max_angle_id = polymer_angle_df['id'].max()
    max_dihedral_id = polymer_dihedral_df['id'].max()
    max_improper_id = polymer_improper_df['id'].max()

    _df['id'] = _df['id'] + max_atom_id
    _bond_df['at1'] = _bond_df['at1'] + max_atom_id
    _bond_df['at2'] = _bond_df['at2'] + max_atom_id
    _angle_df['at1'] = _angle_df['at1'] + max_atom_id
    _angle_df['at2'] = _angle_df['at2'] + max_atom_id
    _angle_df['at3'] = _angle_df['at3'] + max_atom_id
    _dihedral_df['at1'] = _dihedral_df['at1'] + max_atom_id
    _dihedral_df['at2'] = _dihedral_df['at2'] + max_atom_id
    _dihedral_df['at3'] = _dihedral_df['at3'] + max_atom_id
    _dihedral_df['at4'] = _dihedral_df['at4'] + max_atom_id
    _improper_df['at1'] = _improper_df['at1'] + max_atom_id
    _improper_df['at2'] = _improper_df['at2'] + max_atom_id
    _improper_df['at3'] = _improper_df['at3'] + max_atom_id
    _improper_df['at4'] = _improper_df['at4'] + max_atom_id

    head_atom = 1 + max_atom_id
    _bond_df['id'] = _bond_df['id'] + max_bond_id
    _angle_df['id'] = _angle_df['id'] + max_angle_id
    _dihedral_df['id'] = _dihedral_df['id'] + max_dihedral_id
    _improper_df['id'] = _improper_df['id'] + max_improper_id

    # combine polymer and new monomer
    polymer_df = pd.concat([polymer_df, _df], axis=0, ignore_index=True)
    polymer_df.index = polymer_df.index + 1
    polymer_bond_df = pd.concat([polymer_bond_df, _bond_df], axis=0, ignore_index=True)
    polymer_bond_df.index = polymer_bond_df.index + 1
    polymer_angle_df = pd.concat([polymer_angle_df, _angle_df], axis=0, ignore_index=True)
    polymer_angle_df.index = polymer_angle_df.index + 1
    polymer_dihedral_df = pd.concat([polymer_dihedral_df, _dihedral_df], axis=0, ignore_index=True)
    polymer_dihedral_df.index = polymer_dihedral_df.index + 1
    polymer_improper_df = pd.concat([polymer_improper_df, _improper_df], axis=0, ignore_index=True)
    polymer_improper_df.index = polymer_improper_df.index + 1

    return polymer_mass_df, polymer_df, polymer_bond_df, polymer_angle_df, polymer_dihedral_df, polymer_improper_df

def build_peo_ppo_diblock(dop_peo, dop_ppo):

    head_mass_df, head_df, head_bond_df, head_angle_df, head_dihedral_df, head_improper_df, \
    [[head_xlo, head_xhi], [head_ylo, head_yhi], [head_zlo, head_zhi]], \
    head_lj_coeff, head_bond_coeff, head_angle_coeff, head_dihedral_coeff, head_improper_coeff = open_lmp_data('./MeOH_head.lmp', viz=False)
    head_cgenff = ['OG311', 'HGP1', 'CG321', 'HGA2', 'HGA2', 'X']
    head_df['cgenff'] = head_cgenff

    monomer_mass_df, monomer_df, monomer_bond_df, monomer_angle_df, monomer_dihedral_df, monomer_improper_df, \
    [[monomer_xlo, monomer_xhi], [monomer_ylo, monomer_yhi], [monomer_zlo, monomer_zhi]], \
    monomer_lj_coeff, monomer_bond_coeff, monomer_angle_coeff, monomer_dihedral_coeff, monomer_improper_coeff = open_lmp_data('./eo_monomer.lmp', viz=False)
    monomer_cgenff = ['CG321', 'HGA2', 'HGA2', 'OG301', 'CG321', 'HGA2', 'HGA2', 'X']
    monomer_df['cgenff'] = monomer_cgenff

    monomer_mass_df["type"] = monomer_mass_df["type"] + head_mass_df["type"].max() - 1
    monomer_df["type"] = monomer_df["type"] + head_df["type"].max() - 1
    monomer_bond_df["type"] = monomer_bond_df["type"] + head_bond_df["type"].max()
    monomer_angle_df["type"] = monomer_angle_df["type"] + head_angle_df["type"].max()
    monomer_dihedral_df["type"] = monomer_dihedral_df["type"] + head_dihedral_df["type"].max()
    monomer_improper_df["type"] = monomer_improper_df["type"] + head_improper_df["type"].max()

    monomer_mass_df2, monomer_df2, monomer_bond_df2, monomer_angle_df2, monomer_dihedral_df2, monomer_improper_df2, \
    [[monomer_xlo2, monomer_xhi2], [monomer_ylo2, monomer_yhi2], [monomer_zlo2, monomer_zhi2]], \
    monomer_lj_coeff2, monomer_bond_coeff2, monomer_angle_coeff2, monomer_dihedral_coeff2, monomer_improper_coeff2 = open_lmp_data('./po_monomer.lmp', viz=False)
    #                   1        2        3       4        5       6        7       8       9       10      11
    monomer_cgenff2 = ['CG321', 'OG301', 'HGA3', 'CG331', 'HGA3', 'HGA2', 'HGA2', 'HGA1', 'HGA3', 'CG321', 'X']
    monomer_df2['cgenff'] = monomer_cgenff2

    monomer_mass_df2["type"] = monomer_mass_df2["type"] + monomer_mass_df["type"].max() - 1
    monomer_df2["type"] = monomer_df2["type"] + monomer_df["type"].max() - 1
    monomer_bond_df2["type"] = monomer_bond_df2["type"] + monomer_bond_df["type"].max()
    monomer_angle_df2["type"] = monomer_angle_df2["type"] + monomer_angle_df["type"].max()
    monomer_dihedral_df2["type"] = monomer_dihedral_df2["type"] + monomer_dihedral_df["type"].max()
    monomer_improper_df2["type"] = monomer_improper_df2["type"] + monomer_improper_df["type"].max()

    tail_mass_df, tail_df, tail_bond_df, tail_angle_df, tail_dihedral_df, tail_improper_df, \
    [[tail_xlo, tail_xhi], [tail_ylo, tail_yhi], [tail_zlo, tail_zhi]], \
    tail_lj_coeff, tail_bond_coeff, tail_angle_coeff, tail_dihedral_coeff, tail_improper_coeff = open_lmp_data('./MeOH_tail.lmp', viz=False)
    tail_cgenff = ['CG321', 'HGA2', 'HGA2', 'OG311', 'HGP1']
    tail_df['cgenff'] = tail_cgenff

    tail_mass_df["type"] = tail_mass_df["type"] + monomer_mass_df2["type"].max() - 1
    tail_df["type"] = tail_df["type"] + monomer_df2["type"].max() - 1
    tail_bond_df["type"] = tail_bond_df["type"] + monomer_bond_df2["type"].max()
    tail_angle_df["type"] = tail_angle_df["type"] + monomer_angle_df2["type"].max()
    tail_dihedral_df["type"] = tail_dihedral_df["type"] + monomer_dihedral_df2["type"].max()
    tail_improper_df["type"] = tail_improper_df["type"] + monomer_improper_df2["type"].max()

    polymer_df = head_df.copy(deep=True)
    polymer_bond_df = head_bond_df.copy(deep=True)
    polymer_angle_df = head_angle_df.copy(deep=True)
    polymer_dihedral_df = head_dihedral_df.copy(deep=True)
    polymer_improper_df = head_improper_df.copy(deep=True)

    polymer_mass_df = head_mass_df.copy(deep=True)
    polymer_mass_df = pd.concat([polymer_mass_df.drop(polymer_mass_df.tail(1).index), monomer_mass_df], axis=0, ignore_index=True).reset_index(drop=True)
    polymer_mass_df.index = polymer_mass_df.index + 1

    for i in range(0, dop_peo):
        tail_anchor = len(polymer_df)

        _df = monomer_df.copy(deep=True)
        head_atom = 1
        _bond_df = monomer_bond_df.copy(deep=True)
        _angle_df = monomer_angle_df.copy(deep=True)
        _dihedral_df = monomer_dihedral_df.copy(deep=True)
        _improper_df = monomer_improper_df.copy(deep=True)

        # process coordinates
        # reflection about X-Y plane
        if i % 2 == 1:
            _df.loc[:, 'z'] = 0.0 - _df.loc[:, 'z']
        # translate
        disp_vec = polymer_df.loc[tail_anchor, 'x':'z'] - _df.loc[1, 'x':'z']
        _df.loc[:, 'x':'z'] = _df.loc[:, 'x':'z'] + disp_vec

        # drop the anchor row, it will be replaced by the new head atom from _df
        polymer_df = polymer_df.drop(polymer_df.tail(1).index)

        # update ids in the new monomer
        max_atom_id = polymer_df['id'].max()
        max_bond_id = polymer_bond_df['id'].max()
        max_angle_id = polymer_angle_df['id'].max()
        max_dihedral_id = polymer_dihedral_df['id'].max()
        max_improper_id = polymer_improper_df['id'].max()

        _df['id'] = _df['id'] + max_atom_id
        _bond_df['at1'] = _bond_df['at1'] + max_atom_id
        _bond_df['at2'] = _bond_df['at2'] + max_atom_id
        _angle_df['at1'] = _angle_df['at1'] + max_atom_id
        _angle_df['at2'] = _angle_df['at2'] + max_atom_id
        _angle_df['at3'] = _angle_df['at3'] + max_atom_id
        _dihedral_df['at1'] = _dihedral_df['at1'] + max_atom_id
        _dihedral_df['at2'] = _dihedral_df['at2'] + max_atom_id
        _dihedral_df['at3'] = _dihedral_df['at3'] + max_atom_id
        _dihedral_df['at4'] = _dihedral_df['at4'] + max_atom_id
        _improper_df['at1'] = _improper_df['at1'] + max_atom_id
        _improper_df['at2'] = _improper_df['at2'] + max_atom_id
        _improper_df['at3'] = _improper_df['at3'] + max_atom_id
        _improper_df['at4'] = _improper_df['at4'] + max_atom_id

        head_atom = 1 + max_atom_id
        _bond_df['id'] = _bond_df['id'] + max_bond_id
        _angle_df['id'] = _angle_df['id'] + max_angle_id
        _dihedral_df['id'] = _dihedral_df['id'] + max_dihedral_id
        _improper_df['id'] = _improper_df['id'] + max_improper_id

        # combine polymer and new monomer
        polymer_df = pd.concat([polymer_df, _df], axis=0, ignore_index=True)
        polymer_df.index = polymer_df.index + 1
        polymer_bond_df = pd.concat([polymer_bond_df, _bond_df], axis=0, ignore_index=True)
        polymer_bond_df.index = polymer_bond_df.index + 1
        polymer_angle_df = pd.concat([polymer_angle_df, _angle_df], axis=0, ignore_index=True)
        polymer_angle_df.index = polymer_angle_df.index + 1
        polymer_dihedral_df = pd.concat([polymer_dihedral_df, _dihedral_df], axis=0, ignore_index=True)
        polymer_dihedral_df.index = polymer_dihedral_df.index + 1
        polymer_improper_df = pd.concat([polymer_improper_df, _improper_df], axis=0, ignore_index=True)
        polymer_improper_df.index = polymer_improper_df.index + 1

    polymer_mass_df = pd.concat([polymer_mass_df.drop(polymer_mass_df.tail(1).index), monomer_mass_df2], axis=0, ignore_index=True).reset_index(drop=True)
    polymer_mass_df.index = polymer_mass_df.index + 1

    for i in range(dop_peo, dop_ppo + dop_peo):
        tail_anchor = len(polymer_df)

        _df = monomer_df2.copy(deep=True)
        head_atom = 1
        _bond_df = monomer_bond_df2.copy(deep=True)
        _angle_df = monomer_angle_df2.copy(deep=True)
        _dihedral_df = monomer_dihedral_df2.copy(deep=True)
        _improper_df = monomer_improper_df2.copy(deep=True)

        # process coordinates
        # reflection about X-Y plane
        if i % 2 == 1:
            _df.loc[:, 'z'] = 0.0 - _df.loc[:, 'z']
        # translate
        disp_vec = polymer_df.loc[tail_anchor, 'x':'z'] - _df.loc[1, 'x':'z']
        _df.loc[:, 'x':'z'] = _df.loc[:, 'x':'z'] + disp_vec

        # drop the anchor row, it will be replaced by the new head atom from _df
        polymer_df = polymer_df.drop(polymer_df.tail(1).index)

        # update ids in the new monomer
        max_atom_id = polymer_df['id'].max()
        max_bond_id = polymer_bond_df['id'].max()
        max_angle_id = polymer_angle_df['id'].max()
        max_dihedral_id = polymer_dihedral_df['id'].max()
        max_improper_id = polymer_improper_df['id'].max()

        _df['id'] = _df['id'] + max_atom_id
        _bond_df['at1'] = _bond_df['at1'] + max_atom_id
        _bond_df['at2'] = _bond_df['at2'] + max_atom_id
        _angle_df['at1'] = _angle_df['at1'] + max_atom_id
        _angle_df['at2'] = _angle_df['at2'] + max_atom_id
        _angle_df['at3'] = _angle_df['at3'] + max_atom_id
        _dihedral_df['at1'] = _dihedral_df['at1'] + max_atom_id
        _dihedral_df['at2'] = _dihedral_df['at2'] + max_atom_id
        _dihedral_df['at3'] = _dihedral_df['at3'] + max_atom_id
        _dihedral_df['at4'] = _dihedral_df['at4'] + max_atom_id
        _improper_df['at1'] = _improper_df['at1'] + max_atom_id
        _improper_df['at2'] = _improper_df['at2'] + max_atom_id
        _improper_df['at3'] = _improper_df['at3'] + max_atom_id
        _improper_df['at4'] = _improper_df['at4'] + max_atom_id

        head_atom = 1 + max_atom_id
        _bond_df['id'] = _bond_df['id'] + max_bond_id
        _angle_df['id'] = _angle_df['id'] + max_angle_id
        _dihedral_df['id'] = _dihedral_df['id'] + max_dihedral_id
        _improper_df['id'] = _improper_df['id'] + max_improper_id

        # combine polymer and new monomer
        polymer_df = pd.concat([polymer_df, _df], axis=0, ignore_index=True)
        polymer_df.index = polymer_df.index + 1
        polymer_bond_df = pd.concat([polymer_bond_df, _bond_df], axis=0, ignore_index=True)
        polymer_bond_df.index = polymer_bond_df.index + 1
        polymer_angle_df = pd.concat([polymer_angle_df, _angle_df], axis=0, ignore_index=True)
        polymer_angle_df.index = polymer_angle_df.index + 1
        polymer_dihedral_df = pd.concat([polymer_dihedral_df, _dihedral_df], axis=0, ignore_index=True)
        polymer_dihedral_df.index = polymer_dihedral_df.index + 1
        polymer_improper_df = pd.concat([polymer_improper_df, _improper_df], axis=0, ignore_index=True)
        polymer_improper_df.index = polymer_improper_df.index + 1

    tail_anchor = len(polymer_df)

    polymer_mass_df = pd.concat([polymer_mass_df.drop(polymer_mass_df.tail(1).index), tail_mass_df], axis=0, ignore_index=True).reset_index(drop=True)
    polymer_mass_df.index = polymer_mass_df.index + 1

    _df = tail_df.copy(deep=True)
    head_atom = 1
    _bond_df = tail_bond_df.copy(deep=True)
    _angle_df = tail_angle_df.copy(deep=True)
    _dihedral_df = tail_dihedral_df.copy(deep=True)
    _improper_df = tail_improper_df.copy(deep=True)

    # process coordinates
    # reflection about X-Y plane
    if i % 2 != 1:
        _df.loc[:, 'z'] = 0.0 - _df.loc[:, 'z']
    # translate
    disp_vec = polymer_df.loc[tail_anchor, 'x':'z'] - _df.loc[1, 'x':'z']
    _df.loc[:, 'x':'z'] = _df.loc[:, 'x':'z'] + disp_vec

    # drop the anchor row, it will be replaced by the new head atom from _df
    polymer_df = polymer_df.drop(polymer_df.tail(1).index)

    # update ids in the new monomer
    max_atom_id = polymer_df['id'].max()
    max_bond_id = polymer_bond_df['id'].max()
    max_angle_id = polymer_angle_df['id'].max()
    max_dihedral_id = polymer_dihedral_df['id'].max()
    max_improper_id = polymer_improper_df['id'].max()

    _df['id'] = _df['id'] + max_atom_id
    _bond_df['at1'] = _bond_df['at1'] + max_atom_id
    _bond_df['at2'] = _bond_df['at2'] + max_atom_id
    _angle_df['at1'] = _angle_df['at1'] + max_atom_id
    _angle_df['at2'] = _angle_df['at2'] + max_atom_id
    _angle_df['at3'] = _angle_df['at3'] + max_atom_id
    _dihedral_df['at1'] = _dihedral_df['at1'] + max_atom_id
    _dihedral_df['at2'] = _dihedral_df['at2'] + max_atom_id
    _dihedral_df['at3'] = _dihedral_df['at3'] + max_atom_id
    _dihedral_df['at4'] = _dihedral_df['at4'] + max_atom_id
    _improper_df['at1'] = _improper_df['at1'] + max_atom_id
    _improper_df['at2'] = _improper_df['at2'] + max_atom_id
    _improper_df['at3'] = _improper_df['at3'] + max_atom_id
    _improper_df['at4'] = _improper_df['at4'] + max_atom_id

    head_atom = 1 + max_atom_id
    _bond_df['id'] = _bond_df['id'] + max_bond_id
    _angle_df['id'] = _angle_df['id'] + max_angle_id
    _dihedral_df['id'] = _dihedral_df['id'] + max_dihedral_id
    _improper_df['id'] = _improper_df['id'] + max_improper_id

    # combine polymer and new monomer
    polymer_df = pd.concat([polymer_df, _df], axis=0, ignore_index=True)
    polymer_df.index = polymer_df.index + 1
    polymer_bond_df = pd.concat([polymer_bond_df, _bond_df], axis=0, ignore_index=True)
    polymer_bond_df.index = polymer_bond_df.index + 1
    polymer_angle_df = pd.concat([polymer_angle_df, _angle_df], axis=0, ignore_index=True)
    polymer_angle_df.index = polymer_angle_df.index + 1
    polymer_dihedral_df = pd.concat([polymer_dihedral_df, _dihedral_df], axis=0, ignore_index=True)
    polymer_dihedral_df.index = polymer_dihedral_df.index + 1
    polymer_improper_df = pd.concat([polymer_improper_df, _improper_df], axis=0, ignore_index=True)
    polymer_improper_df.index = polymer_improper_df.index + 1

    return polymer_mass_df, polymer_df, polymer_bond_df, polymer_angle_df, polymer_dihedral_df, polymer_improper_df

def assign_cgenff(data_fname, polymer_mass_df, polymer_df, polymer_bond_df, polymer_angle_df, polymer_dihedral_df, polymer_improper_df):
    polymer_df['comment'] = '# ' + polymer_df['cgenff']
    id2cgenff = polymer_df.set_index('id').to_dict()['cgenff']
    polymer_bond_df['cgenff'] = polymer_bond_df['at1'].map(id2cgenff) + '-' + polymer_bond_df['at2'].map(id2cgenff)
    polymer_bond_df['comment'] = '# ' + polymer_bond_df['cgenff']
    polymer_angle_df['cgenff'] = polymer_angle_df['at1'].map(id2cgenff) + '-' + polymer_angle_df['at2'].map(id2cgenff) + '-' + polymer_angle_df['at3'].map(id2cgenff)
    polymer_angle_df['comment'] = '# ' + polymer_angle_df['cgenff']
    polymer_dihedral_df['cgenff'] = polymer_dihedral_df['at1'].map(id2cgenff) + '-' + polymer_dihedral_df['at2'].map(id2cgenff) + '-' + polymer_dihedral_df['at3'].map(id2cgenff) + '-' + polymer_dihedral_df['at4'].map(id2cgenff)
    polymer_dihedral_df['comment'] = '# ' + polymer_dihedral_df['cgenff']
    polymer_improper_df['cgenff'] = polymer_improper_df['at1'].map(id2cgenff) + '-' + polymer_improper_df['at2'].map(id2cgenff) + '-' + polymer_improper_df['at3'].map(id2cgenff) + '-' + polymer_improper_df['at4'].map(id2cgenff)
    polymer_improper_df['comment'] = '# ' + polymer_improper_df['cgenff']

    prm_str = None
    with open('./par_all36_cgenff.prm', 'r') as prm:
        prm_str = prm.read()

    lj_str = [x for x in prm_str.split('\nNONBONDED')[1].split('\nNBFIX')[0].split('!hydrogens')[1].split('\n') if (x and not x.startswith('!'))]
    lj_prm_list, lj_prm_comment = list(map(list, zip(*[x.split('!') for x in lj_str])))

    lj_prm = pd.read_csv(io.StringIO('\n'.join(lj_prm_list)),
                        comment='!', sep=r'\s+', usecols=[0, 1, 2, 3, 4, 5, 6],
                        names=['at', 'ignored1', 'epsilon', 'Rmin/2', 'ignored2', 'eps,1-4', 'Rmin/2,1-4']).fillna(0)

    # V(Lennard-Jones) = Eps,i,j[(Rmin,i,j/ri,j)**12 - 2(Rmin,i,j/ri,j)**6]
    # epsilon: kcal/mole, Eps,i,j = sqrt(eps,i * eps,j)
    # Rmin/2: A, Rmin,i,j = Rmin/2,i + Rmin/2,j
    lj_prm['comment'] = lj_prm_comment
    lj_prm['comment'] = '# ' + lj_prm['comment']

    lj_prm = lj_prm[lj_prm['at'].isin(polymer_df['cgenff'])].reset_index(drop=True)
    lj_prm.index = lj_prm.index + 1
    lj_prm['sigma/2'] = lj_prm['Rmin/2'] / (2.**(1./6.))
    lj_prm['sigma/2,1-4'] = lj_prm['Rmin/2,1-4'] / (2.**(1./6.))

    bond_str = [x for x in prm_str.split('\nBONDS')[1].split('\nANGLES')[0].split('\n') if (x and not x.startswith('!'))]
    bond_prm_list, bond_prm_comment = list(map(list, zip(*[x.split('!') for x in bond_str])))

    bond_prm = pd.read_csv(io.StringIO('\n'.join(bond_prm_list)),
                        comment='!', sep=r'\s+', usecols=[0, 1, 2, 3],
                        names=['at1', 'at2', 'Kb', 'b0'])

    # V(bond) = Kb(b - b0)**2
    # Kb: kcal/mole/A**2
    # b0: A
    bond_prm['comment'] = bond_prm_comment
    bond_prm['comment'] = '# ' + bond_prm['comment']

    bond_prm1 = bond_prm[bond_prm['at1'].isin(polymer_df['cgenff'])].index
    bond_prm2 = bond_prm[bond_prm['at2'].isin(polymer_df['cgenff'])].index

    bond_index = bond_prm1.intersection(bond_prm2)
    bond_prm = bond_prm.loc[bond_index].reset_index(drop=True)
    bond_prm.index = bond_prm.index + 1

    angle_str = [x for x in prm_str.split('\nANGLES')[1].split('\nDIHEDRALS')[0].split('\n') if (x and not x.startswith('!'))]
    angle_prm_list, angle_prm_comment = list(map(list, zip(*[x.split('!') for x in angle_str])))

    angle_prm = pd.read_csv(io.StringIO('\n'.join(angle_prm_list)),
                            comment='!', sep=r'\s+', usecols=[0, 1, 2, 3, 4, 5, 6],
                            names=['at1', 'at2', 'at3', 'Ktheta', 'Theta0', 'kUB', 'rUB']).fillna(0)

    #V(angle) = Ktheta(Theta - Theta0)**2
    #Ktheta: kcal/mole/rad**2
    #Theta0: degrees
    #V(Urey-Bradley) = Kub(S - S0)**2
    #Kub: kcal/mole/A**2 (Urey-Bradley)
    angle_prm['comment'] = angle_prm_comment
    angle_prm['comment'] = '# ' + angle_prm['comment']

    angle_prm1 = angle_prm[angle_prm['at1'].isin(polymer_df['cgenff'])].index
    angle_prm2 = angle_prm[angle_prm['at2'].isin(polymer_df['cgenff'])].index
    angle_prm3 = angle_prm[angle_prm['at3'].isin(polymer_df['cgenff'])].index
    ang_index = angle_prm1.intersection(angle_prm2).intersection(angle_prm3)
    angle_prm = angle_prm.loc[ang_index].reset_index(drop=True)
    angle_prm.index = angle_prm.index + 1

    dihedral_str = [x for x in prm_str.split('\nDIHEDRALS')[1].split('\nIMPROPERS')[0].split('\n') if (x and not x.startswith('!'))]
    dihedral_prm_list, dihedral_prm_comment = list(map(list, zip(*[x.split('!') for x in dihedral_str])))
    dihedral_prm = pd.read_csv(io.StringIO('\n'.join(dihedral_prm_list)),
                            comment='!', sep=r'\s+', usecols=[0, 1, 2, 3, 4, 5, 6],
                            names=['at1', 'at2', 'at3', 'at4', 'Kchi', 'n', 'delta'])

    # V(dihedral) = Kchi(1 + cos(n(chi) - delta))
    # Kchi: kcal/mole
    # n: multiplicity
    # delta: degrees
    dihedral_prm['comment'] = dihedral_prm_comment
    dihedral_prm['comment'] = '# ' + dihedral_prm['comment']

    dihedral_prm1 = dihedral_prm[dihedral_prm['at1'].isin(polymer_df['cgenff'])].index
    dihedral_prm2 = dihedral_prm[dihedral_prm['at2'].isin(polymer_df['cgenff'])].index
    dihedral_prm3 = dihedral_prm[dihedral_prm['at3'].isin(polymer_df['cgenff'])].index
    dihedral_prm4 = dihedral_prm[dihedral_prm['at4'].isin(polymer_df['cgenff'])].index
    dih_index = dihedral_prm1.intersection(dihedral_prm2).intersection(dihedral_prm3).intersection(dihedral_prm4)
    dihedral_prm = dihedral_prm.loc[dih_index].reset_index(drop=True)
    dihedral_prm.index = dihedral_prm.index + 1

    improper_str = [x for x in prm_str.split('\nIMPROPERS')[1].split('\nNONBONDED')[0].split('\n') if (x and not x.startswith('!'))]
    improper_prm_list, improper_prm_comment = list(map(list, zip(*[x.split('!') for x in improper_str])))
    improper_prm = pd.read_csv(io.StringIO('\n'.join(improper_prm_list)),
                            comment='!', sep=r'\s+', usecols=[0, 1, 2, 3, 4, 5, 6],
                            names=['at1', 'at2', 'at3', 'at4', 'Kpsi', 'ignored', 'psi0'])

    # V(improper) = Kpsi(psi - psi0)**2
    # Kpsi: kcal/mole/rad**2
    # psi0: degrees
    # note that the second column of numbers (0) is ignored
    improper_prm['comment'] = improper_prm_comment
    improper_prm['comment'] = '# ' + improper_prm['comment']

    improper_prm1 = improper_prm[improper_prm['at1'].isin(polymer_df['cgenff'])].index
    improper_prm2 = improper_prm[improper_prm['at2'].isin(polymer_df['cgenff'])].index
    improper_prm3 = improper_prm[improper_prm['at3'].isin(polymer_df['cgenff'])].index
    improper_prm4 = improper_prm[improper_prm['at4'].isin(polymer_df['cgenff'])].index
    imp_index = improper_prm1.intersection(improper_prm2).intersection(improper_prm3).intersection(improper_prm4)
    improper_prm = improper_prm.loc[imp_index].reset_index(drop=True)
    improper_prm.index = improper_prm.index + 1

    self_lj = []
    _polymer_df = polymer_df.drop_duplicates(subset=['type']).reset_index(drop=True)
    _polymer_df.index = _polymer_df.index + 1
    for i in range(1, 1+len(_polymer_df)):
        atom_type = _polymer_df.loc[i, 'cgenff']
        curr_lj_prm = lj_prm[lj_prm['at']==atom_type]
        self_lj.append(curr_lj_prm)
    self_lj_df = pd.concat(self_lj, axis=0).reset_index(drop=True)
    self_lj_df.index = self_lj_df.index + 1
    self_lj_df['id'] = self_lj_df.index

    pair_coeff = ''
    for i in range(1, 1+len(_polymer_df)):
        for j in range(i, 1+len(_polymer_df)):
            mixed_sigma = self_lj_df.at[i, 'sigma/2'] + self_lj_df.at[j, 'sigma/2']
            mixed_sigma14 = self_lj_df.at[i, 'sigma/2,1-4'] + self_lj_df.at[j, 'sigma/2,1-4']
            mixed_epsilon = (self_lj_df.at[i, 'epsilon'] * self_lj_df.at[j, 'epsilon']) ** (1./2.)
            mixed_epsilon14 = (self_lj_df.at[i, 'eps,1-4'] * self_lj_df.at[j, 'eps,1-4']) ** (1./2.)

            pair_coeff = pair_coeff + 'pair_coeff ' + "{:.0f}".format(self_lj_df.at[i, 'id']) + ' ' + \
                                                      "{:.0f}".format(self_lj_df.at[j, 'id']) + ' ' + \
                                                      "{:.6f}".format(mixed_epsilon) + ' ' + \
                                                      "{:.6f}".format(mixed_sigma) + ' ' + \
                                                      "{:.6f}".format(mixed_epsilon14) + ' ' + \
                                                      "{:.6f}".format(mixed_sigma14) + ' ' + \
                                                      '# ' + self_lj_df.at[i, 'at'] + '-' + self_lj_df.at[j, 'at'] + '\n'
    #print(pair_coeff)
    _polymer_bond_df = polymer_bond_df.drop_duplicates(subset=['type']).reset_index(drop=True)
    _polymer_bond_df.index = _polymer_bond_df.index + 1
    bond_coeff = ""
    for i in range(1, 1+len(_polymer_bond_df)):
        all_atoms = _polymer_bond_df.loc[i, 'cgenff'].split('-')
        prm_found = False
        for j in range(1, 1+len(bond_prm)):
            if bond_prm.loc[j, ['at1', 'at2']].to_list() == all_atoms or bond_prm.loc[j, ['at2', 'at1']].to_list() == all_atoms:
                bond_coeff = bond_coeff + 'bond_coeff ' + str(i) + ' ' + \
                                "{:.4f}".format(bond_prm.at[j, 'Kb']) + ' ' + \
                                "{:.4f}".format(bond_prm.at[j, 'b0']) + ' ' + \
                                bond_prm.at[j, 'comment'] + '\n'
                prm_found = True
                break
        if prm_found == False:
            bond_coeff = bond_coeff + 'bond_coeff ' + str(i) + ' 0. 2.0' + '\n'
    #print(bond_coeff)

    angle_coeff = ""
    _polymer_angle_df = polymer_angle_df.drop_duplicates(subset=['type']).reset_index(drop=True)
    _polymer_angle_df.index = _polymer_angle_df.index + 1
    for i in range(1, 1+len(_polymer_angle_df)):
        all_atoms = _polymer_angle_df.loc[i, 'cgenff'].split('-')
        prm_found = False
        for j in range(1, 1+len(angle_prm)):
            if angle_prm.loc[j, ['at1', 'at2', 'at3']].to_list() == all_atoms or angle_prm.loc[j, ['at3', 'at2', 'at1']].to_list() == all_atoms:
                angle_coeff = angle_coeff + 'angle_coeff ' + str(i) + ' ' + \
                                "{:.4f}".format(angle_prm.at[j, 'Ktheta']) + ' ' + \
                                "{:.2f}".format(angle_prm.at[j, 'Theta0']) + ' ' + \
                                "{:.4f}".format(angle_prm.at[j, 'kUB']) + ' ' + \
                                "{:.4f}".format(angle_prm.at[j, 'rUB']) + ' ' + \
                                angle_prm.at[j, 'comment'] + '\n'
                prm_found = True
                break
        if prm_found == False:
            angle_coeff = angle_coeff + 'angle_coeff ' + str(i) + ' 0.  0.  0.  0.' + '\n'
    #print(angle_coeff)

    dihedral_coeff = ""
    _polymer_dihedral_df = polymer_dihedral_df.drop_duplicates(subset=['type']).reset_index(drop=True)
    _polymer_dihedral_df.index = _polymer_dihedral_df.index + 1
    for i in range(1, 1+len(_polymer_dihedral_df)):
        all_atoms = _polymer_dihedral_df.loc[i, 'cgenff'].split('-')
        prm_found = False
        for j in range(1, 1+len(dihedral_prm)):
            if dihedral_prm.loc[j, ['at1', 'at2', 'at3', 'at4']].to_list() == all_atoms or dihedral_prm.loc[j, ['at4', 'at3', 'at2', 'at1']].to_list() == all_atoms:
                weight = 1.0
                if all_atoms[0].startswith('C') and all_atoms[1].startswith('C') and all_atoms[2].startswith('C') and all_atoms[3].startswith('C'):
                    weight = 0.5
                dihedral_coeff = dihedral_coeff + 'dihedral_coeff ' + str(i) + ' ' + \
                                "{:.4f}".format(dihedral_prm.at[j, 'Kchi']) + ' ' + \
                                "{:.0f}".format(dihedral_prm.at[j, 'n']) + ' ' + \
                                "{:.0f}".format(dihedral_prm.at[j, 'delta']) + ' ' + \
                                str(weight) + ' ' + \
                                dihedral_prm.at[j, 'comment'] + '\n'
                prm_found = True
                break
        if prm_found == False:
            dihedral_coeff = dihedral_coeff + 'dihedral_coeff ' + str(i) + ' 0.0  0  0  0.0' + '\n'
    #print(dihedral_coeff)

    improper_coeff = ""
    _polymer_improper_df = polymer_improper_df.drop_duplicates(subset=['type']).reset_index(drop=True)
    _polymer_improper_df.index = _polymer_improper_df.index + 1
    for i in range(1, 1+len(_polymer_improper_df)):
        all_atoms = _polymer_improper_df.loc[i, 'cgenff'].split('-')
        center_atom = all_atoms[0]
        satellite_atoms = sorted(all_atoms[1:4])
        search_df = improper_prm[improper_prm['at1'] == center_atom].reset_index(drop=True)
        if len(search_df) > 0:
            for j in range(0, len(search_df)):
                satellite_atoms_prm = sorted(search_df.loc[j, ['at2', 'at3', 'at4']])
                if satellite_atoms == satellite_atoms_prm:
                    #if [all_atoms[1], all_atoms[2], all_atoms[3]] == search_df.loc[j, ['at2', 'at3', 'at4']].to_list():
                        #print('No swap!')
                    if [all_atoms[1], all_atoms[3], all_atoms[2]] == search_df.loc[j, ['at2', 'at3', 'at4']].to_list():
                        improper_df.loc[i, ['at2','at3','at4']] = improper_df.loc[i, ['at2','at4','at3']]
                    elif [all_atoms[2], all_atoms[1], all_atoms[3]] == search_df.loc[j, ['at2', 'at3', 'at4']].to_list():
                        improper_df.loc[i, ['at2','at3','at4']] = improper_df.loc[i, ['at3','at2','at4']]
                    elif [all_atoms[3], all_atoms[2], all_atoms[1]] == search_df.loc[j, ['at2', 'at3', 'at4']].to_list():
                        improper_df.loc[i, ['at2','at3','at4']] = improper_df.loc[i, ['at4','at3','at2']]
                    elif [all_atoms[2], all_atoms[3], all_atoms[1]] == search_df.loc[j, ['at2', 'at3', 'at4']].to_list():
                        improper_df.loc[i, ['at2','at3','at4']] = improper_df.loc[i, ['at3','at4','at2']]
                    elif [all_atoms[3], all_atoms[1], all_atoms[2]] == search_df.loc[j, ['at2', 'at3', 'at4']].to_list():
                        improper_df.loc[i, ['at2','at3','at4']] = improper_df.loc[i, ['at4','at2','at3']]
                    improper_df.loc[i, 'cgenff'] = id2cgenff[improper_df.loc[i, 'at1']] + '-' + \
                                                id2cgenff[improper_df.loc[i, 'at2']] + '-' + \
                                                id2cgenff[improper_df.loc[i, 'at3']] + '-' + \
                                                id2cgenff[improper_df.loc[i, 'at4']]
                    improper_df.loc[i,'comment'] = '# ' + improper_df.loc[i,'cgenff']
                    improper_coeff = improper_coeff + 'improper_coeff ' + str(i) + ' ' + \
                                    "{:.4f}".format(search_df.at[j, 'Kpsi']) + ' ' + \
                                    "{:.2f}".format(search_df.at[j, 'psi0']) + ' ' + \
                                    search_df.at[j, 'comment'] + '\n'
                    break
        else:
            improper_coeff = improper_coeff + 'improper_coeff ' + str(i) + ' 0.0000 0.00' + '\n'


    cgenff36 = '''pair_style     lj/charmmfsw/coul/long 10.0 12.0
pair_modify    tail yes
kspace_style   pppm 1.0e-5
bond_style     harmonic
angle_style    charmm
dihedral_style charmmfsw
improper_style harmonic
special_bonds  charmm
neighbor       2.0 bin
neigh_modify   every 1 delay 0 check yes
'''

    cgenff36 = cgenff36 + '''
''' + pair_coeff + '''

''' + bond_coeff + '''

''' + angle_coeff + '''

''' + dihedral_coeff + '''

''' + improper_coeff + '''

'''

    with open('./cgenff36.ff', 'w') as ff_file:
        ff_file.write(cgenff36)

    min_coord = min([polymer_df['x'].min() - 1.0, polymer_df['y'].min() - 1.0, polymer_df['z'].min() - 1.0])
    max_coord = max([polymer_df['x'].max() + 1.0, polymer_df['y'].max() + 1.0, polymer_df['z'].max() + 1.0])

    xlo, xhi, ylo, yhi, zlo, zhi = write_dfs_to_lmp_data(data_fname, polymer_mass_df, polymer_df, polymer_bond_df, polymer_angle_df, polymer_dihedral_df, polymer_improper_df)

    return lj_prm, bond_prm, angle_prm, dihedral_prm, improper_prm, xlo, xhi, ylo, yhi, zlo, zhi

def write_dfs_to_lmp_data(data_fname, mass_df, df, bond_df=None, angle_df=None, dihedral_df=None, improper_df=None, padding=1.0, force_cube=False):
    new_sec_names = ['head',
        '\n\nMasses\n\n',
        '\n\nAtoms \n\n']
    min_coord = min([df['x'].min() - 1.0, df['y'].min() - 1.0, df['z'].min() - 1.0])
    max_coord = max([df['x'].max() + 1.0, df['y'].max() + 1.0, df['z'].max() + 1.0])

    xlo = df['x'].min() - padding
    xhi = df['x'].max() + padding
    ylo = df['y'].min() - padding
    yhi = df['y'].max() + padding
    zlo = df['z'].min() - padding
    zhi = df['z'].max() + padding

    mass_df['element'] = mass_df['mass'].round().map({
        16: 'O',
        12: "C",
        1: "H",
        14: 'N', 
    })
    mass_df['comment'] = " # " + mass_df['element']

    df_columns = ['id', 'mol', 'type', 'q', 'x', 'y', 'z']
    df["comment"] = " # "
    for x in df[list(set(df.columns) - set(df_columns))]:
        df["comment"]=df["comment"]+ " "+df[x].astype(str)
    if force_cube:
        deltaXYZ = max(xhi-xlo, yhi-ylo, zhi-zlo)
        xlo = -deltaXYZ/2.
        ylo = -deltaXYZ/2.
        zlo = -deltaXYZ/2.
        xhi = deltaXYZ/2.
        yhi = deltaXYZ/2.
        zhi = deltaXYZ/2.
        df.loc[:, ["x", "y", "z"]] = df.loc[:, ["x", "y", "z"]] - df.loc[:, ["x", "y", "z"]].values.astype(float).mean(axis=0)

    bond_header_string = ""
    bond_str = ""
    new_sec_names.append("")
    if type(bond_df) != type(None):
        if len(bond_df) >= 1:
            bond_df_columns = ['id', 'type', 'at1', 'at2']
            bond_df["comment"] = " # "
            for x in bond_df[list(set(bond_df.columns) - set(bond_df_columns))]:
                bond_df["comment"]=bond_df["comment"]+ " " + bond_df[x].astype(str)
            bond_header_string = str(len(bond_df)) + """ bonds
""" + str(int(bond_df['type'].max())) + """ bond types
"""
            bond_str = bond_df[bond_df_columns + ['comment']].to_string(header=None, index=None) + '\n'
            new_sec_names[-1] = '\n\nBonds \n\n'

    angle_header_string = ""
    angle_str = ""
    new_sec_names.append("")
    if type(angle_df) != type(None):
        if len(angle_df) >= 1:
            angle_df_columns = ['id', 'type', 'at1', 'at2', 'at3']
            angle_df["comment"] = " # "
            for x in angle_df[list(set(angle_df.columns) - set(angle_df_columns))]:
                angle_df["comment"]=angle_df["comment"]+ " " + angle_df[x].astype(str)
            angle_header_string = str(len(angle_df)) + """ angles
""" + str(int(angle_df['type'].max())) + """ angle types
"""
            angle_str = angle_df[angle_df_columns + ['comment']].to_string(header=None, index=None) + '\n'
            new_sec_names[-1] = '\n\nAngles \n\n'

    dihedral_header_string = ""
    dihedral_str = ""
    new_sec_names.append("")
    if type(dihedral_df) != type(None):
        if len(dihedral_df) >= 1:
            dihedral_df_columns = ['id', 'type', 'at1', 'at2', 'at3', 'at4']
            dihedral_df["comment"] = " # "
            for x in dihedral_df[list(set(dihedral_df.columns) - set(dihedral_df_columns))]:
                dihedral_df["comment"]=dihedral_df["comment"]+ " " + dihedral_df[x].astype(str)
            dihedral_header_string = str(len(dihedral_df)) + """ dihedrals
""" + str(int(dihedral_df['type'].max())) + """ dihedral types
"""
            dihedral_str = dihedral_df[dihedral_df_columns + ['comment']].to_string(header=None, index=None) + '\n'
            new_sec_names[-1] = '\n\nDihedrals \n\n'

    improper_header_string = ""
    improper_str = ""
    new_sec_names.append("")
    if type(improper_df) != type(None):
        if len(improper_df) >= 1:
            improper_df_columns = ['id', 'type', 'at1', 'at2', 'at3', 'at4']
            improper_df["comment"] = " # "
            for x in improper_df[list(set(improper_df.columns) - set(improper_df_columns))]:
                improper_df["comment"]=improper_df["comment"]+ " " + improper_df[x].astype(str)
            improper_header_string = str(len(improper_df)) + """ impropers
""" + str(int(improper_df['type'].max())) + """ improper types
"""
            improper_str = improper_df[improper_df_columns + ['comment']].to_string(header=None, index=None) + '\n'
            new_sec_names[-1] = '\n\nImpropers \n\n'


    new_sec_strs = ['LAMMPS data file written by xyan11@uic.edu' + """

""" + str(len(df)) + """ atoms
""" + str(len(mass_df)) + """ atom types
""" + bond_header_string + angle_header_string + dihedral_header_string + improper_header_string + """
""" + "{:.6f}".format(xlo) + """ """ + "{:.6f}".format(xhi) + """ xlo xhi
""" + "{:.6f}".format(ylo) + """ """ + "{:.6f}".format(yhi) + """ ylo yhi
""" + "{:.6f}".format(zlo) + """ """ + "{:.6f}".format(zhi) + """ zlo zhi
""",
    mass_df[['type', 'mass', 'comment']].to_string(header=None, index=None) + '\n',
    df[df_columns + ['comment']].to_string(header=None, index=None) + '\n',
    bond_str,
    angle_str,
    dihedral_str,
    improper_str]

    write_lmp_data(data_fname, new_sec_names, new_sec_strs)
    return xlo, xhi, ylo, yhi, zlo, zhi

def map_discrete_colors(ncolors):
    n_per_channel = int((ncolors - 1) / 3.) + 1
    R = (np.concatenate([np.zeros(n_per_channel), 
                         np.linspace(0, 1, n_per_channel),
                         np.ones(n_per_channel)], axis=0) * 255).astype(int)
    G = (np.concatenate([np.linspace(0, 1, n_per_channel), 
                         np.ones(n_per_channel), 
                         np.linspace(1, 0, n_per_channel)], axis=0) * 255).astype(int)
    B = (np.concatenate([np.ones(n_per_channel), 
                         np.linspace(1, 0, n_per_channel),
                         np.zeros(n_per_channel)], axis=0) * 255).astype(int)
    A = np.ones(n_per_channel * 3).astype(int)
    colors = ["rgba(" + ",".join(x) + ")" for x in (np.array([R, G, B, A]).T).astype(str).tolist()]
    return dict(zip([x+1 for x in range(ncolors)], colors))

def read_lmp_fix_file(fname):
    outlines = []
    with io.open(fname, "r", newline="\n") as rf:
        outlines = rf.readlines()
    line2_args = [x.strip() for x in list(filter(None, outlines[1].replace("#", "").split(" ")))]
    
    args = dict(zip(line2_args, [[] for x in line2_args]))
    time_arg_name = line2_args[0]
    nlines_arg_name = line2_args[1]
    conserve_arg_name = line2_args[2]
    args["dfs"] = []
    
    df_header = [x.strip() for x in list(filter(None, outlines[2].replace("#", "").split(" ")))]

    line_i = 3
    while line_i < len(outlines):
        new_args = [int(np.round(float(x), 0)) for x in list(filter(None, outlines[line_i].replace("#", "").split(" ")))]
        args[time_arg_name].append(new_args[0])
        args[nlines_arg_name].append(new_args[1])
        args[conserve_arg_name].append(new_args[2])
        df = pd.read_csv(io.StringIO("".join(outlines[line_i+1:line_i+1+new_args[1]])), sep=r"\s+", names=df_header)
        args["dfs"].append(df)
        line_i = line_i + new_args[1] + 1
    return args

def viz_3d_scatter(xyzs, markersize=10):
    xyzmin = np.inf
    xyzmax = -np.inf
    for xyz in xyzs:
        if xyz.min() < xyzmin:
            xyzmin = xyz.min()
        if xyz.max() > xyzmax:
            xyzmax = xyz.max()

    fig = go.Figure(data=[go.Scatter3d(x=xyz[:, 0], 
                                       y=xyz[:, 1], 
                                       z=xyz[:, 2],
                                       mode='markers',
                                       marker={"size": markersize}) for xyz in xyzs])
    fig.update_layout(
        scene = dict(
            xaxis = dict(nticks=10, range=[xyzmin-10,xyzmax+10],
                         backgroundcolor="rgba(80, 70, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            yaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 80, 70, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                        ),
            zaxis = dict(nticks=10, range=[xyzmin-10, xyzmax+10],
                         backgroundcolor="rgba(70, 70, 80, 0.5)",
                         gridcolor="white",
                         showbackground=True,
                         zerolinecolor="white",
                         title=dict(font=dict(color="rgba(150,150,150,1)")),
                         ),
        ),
        width=1400,
        height=1400,
        margin=dict(r=10, l=10, b=10, t=10),
        showlegend=False)
    fig.update_layout(scene_aspectmode='cube', paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
        scene_aspectmode='cube', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_layout(
        font_color="rgba(150,150,150,1)",
        title_font_color="rgba(150,150,150,1)",
        legend_title_font_color="rgba(150,150,150,1)",
    )
    fig.show()

def gen_sphere_points(R, dx=5):
    xyz = []
    for theta in np.linspace(0, np.pi, int(np.pi * R / dx) + 1):
        for phi in np.linspace(0, 2 * np.pi, int(2 * np.pi * R * np.sin(theta) / dx) + 1, endpoint=False):
            xyz.append([R * np.sin(theta) * np.cos(phi), 
                        R * np.sin(theta) * np.sin(phi), 
                        R * np.cos(theta)])
    return np.array(xyz)

def align_chain(xyz, inner_anchor, outer_anchor, aligned_startpoint, aligned_direction):
    from scipy.spatial.transform import Rotation as R
    _xyz = xyz - inner_anchor
    _vec_orig = (outer_anchor - inner_anchor) / np.linalg.norm(outer_anchor - inner_anchor)
    _vec_align = aligned_direction
    rot_angle = np.arccos(np.dot(_vec_orig, _vec_align) / (np.linalg.norm(_vec_orig) * np.linalg.norm(_vec_align)))
    rot_axis = np.cross(_vec_orig, _vec_align) / np.linalg.norm(np.cross(_vec_orig, _vec_align))
    mrp = np.tan(rot_angle / 4.) * rot_axis
    return (R.from_mrp(mrp).as_matrix() @ _xyz.T).T + aligned_startpoint


def build_micelle(micelle_xyz, df, bond_df, angle_df, dihedral_df, improper_df, inner_anchor, outer_anchor):
    total_atom_dfs = []
    total_bond_dfs = []
    total_angle_dfs = []
    total_dihedral_dfs = []
    total_improper_dfs = []
    natoms = 0
    nmols = 0
    for micelle_point in micelle_xyz:
        new_xyz = align_chain(df.loc[:, ["x", "y", "z"]].values.astype(float), 
                              inner_anchor, 
                              outer_anchor, 
                              micelle_point, 
                              micelle_point)
        _df = df.copy(deep=True)
        _df.loc[:, ["x", "y", "z"]] = new_xyz
        _df["id"] = _df["id"] + natoms
        _df["mol"] = _df["mol"] + nmols
        total_atom_dfs.append(_df)
        
        _bond_df = bond_df.copy(deep=True)
        _bond_df["at1"] = _bond_df["at1"] + natoms
        _bond_df["at2"] = _bond_df["at2"] + natoms
        total_bond_dfs.append(_bond_df)
        
        _angle_df = angle_df.copy(deep=True)
        _angle_df["at1"] = _angle_df["at1"] + natoms
        _angle_df["at2"] = _angle_df["at2"] + natoms
        _angle_df["at3"] = _angle_df["at3"] + natoms
        total_angle_dfs.append(_angle_df)
        
        _dihedral_df = dihedral_df.copy(deep=True)
        _dihedral_df["at1"] = _dihedral_df["at1"] + natoms
        _dihedral_df["at2"] = _dihedral_df["at2"] + natoms
        _dihedral_df["at3"] = _dihedral_df["at3"] + natoms
        _dihedral_df["at4"] = _dihedral_df["at4"] + natoms
        total_dihedral_dfs.append(_dihedral_df)
        
        _improper_df = improper_df.copy(deep=True)
        _improper_df["at1"] = _improper_df["at1"] + natoms
        _improper_df["at2"] = _improper_df["at2"] + natoms
        _improper_df["at3"] = _improper_df["at3"] + natoms
        _improper_df["at4"] = _improper_df["at4"] + natoms
        total_improper_dfs.append(_improper_df)
        
        natoms = natoms + len(df)
        nmols = nmols + 1
        
    total_atom_df = pd.concat(total_atom_dfs, axis=0).reset_index(drop=True)
    total_atom_df.index = total_atom_df.index + 1
    total_atom_df["id"] = total_atom_df.index
    total_bond_df = pd.concat(total_bond_dfs, axis=0).reset_index(drop=True)
    total_bond_df.index = total_bond_df.index + 1
    total_bond_df["id"] = total_bond_df.index
    total_angle_df = pd.concat(total_angle_dfs, axis=0).reset_index(drop=True)
    total_angle_df.index = total_angle_df.index + 1
    total_angle_df["id"] = total_angle_df.index
    total_dihedral_df = pd.concat(total_dihedral_dfs, axis=0).reset_index(drop=True)
    total_dihedral_df.index = total_dihedral_df.index + 1
    total_dihedral_df["id"] = total_dihedral_df.index
    total_improper_df = pd.concat(total_improper_dfs, axis=0).reset_index(drop=True)
    total_improper_df.index = total_improper_df.index + 1
    total_improper_df["id"] = total_improper_df.index
    return total_atom_df, total_bond_df, total_angle_df, total_dihedral_df, total_improper_df




def attempt_to_pack_cube_box(solute_xyz, Lx, target_density, solute_total_mass, M_solvent, distance_limit=2.1, density_convergence=0.02, max_iter=50, verbose=False):
    N_Avogadro = 6.02214076e23
    Volume = ((Lx * 1e-8) ** 3)
    compensation_coefficient = 0.8
    _upper_bound = 1
    _lower_bound = 0
    _iter = 0
    last_3_upper_bounds = [_upper_bound+1, _upper_bound+2, _upper_bound+3]
    last_3_lower_bounds = [_lower_bound-1, _lower_bound-2, _lower_bound-3]
    last_3_Nx = [-1, -2, -3]
    N_solvent = int(((Volume * target_density * N_Avogadro) - solute_total_mass) / M_solvent)
    Nx = int((N_solvent) ** (1./3.) * (1 + compensation_coefficient))
    solvent_spacing = Lx / Nx

    grid3D = (np.array([np.repeat(np.arange(Nx), Nx*Nx), 
                        np.tile(np.repeat(np.arange(Nx), Nx), Nx), 
                        np.tile(np.arange(Nx), Nx*Nx)]).T) * solvent_spacing
    grid3D = grid3D - grid3D.mean(axis=0)
    
    distmat = distance_matrix(grid3D, solute_xyz)
    idx1, idx2 = (distmat < distance_limit).nonzero()
    good_point_indices = list(set([x for x in range(0, grid3D.shape[0])])-set(idx1))
    N_solvent_guessed = len(good_point_indices)
    curr_density = (solute_total_mass + (N_solvent_guessed * M_solvent)) / Volume / N_Avogadro
    best_case = {"solvent_coordinates": grid3D[good_point_indices, :], 
                 "N_solvent_guessed": N_solvent_guessed, 
                 "density": curr_density}
    while np.abs(target_density - curr_density) > density_convergence:
        _iter = _iter + 1
        Nx = int((N_solvent) ** (1./3.) * (1 + compensation_coefficient))
        last_3_upper_bounds = last_3_upper_bounds[1:] + [_upper_bound]
        last_3_lower_bounds = last_3_lower_bounds[1:] + [_lower_bound]
        last_3_Nx = last_3_Nx[1:] + [Nx]
        if verbose:
            print("#######################", "iteration", _iter, "#######################")
            print("testing coefficient:", compensation_coefficient)
            print("upper bound:", _upper_bound)
            print("lower bound:", _lower_bound)
            print("Nx:", Nx)
        solvent_spacing = Lx / Nx
        grid3D = (np.array([np.repeat(np.arange(Nx), Nx*Nx), 
                            np.tile(np.repeat(np.arange(Nx), Nx), Nx), 
                            np.tile(np.arange(Nx), Nx*Nx)]).T) * solvent_spacing
        grid3D = grid3D - grid3D.mean(axis=0)
        distmat = distance_matrix(grid3D, solute_xyz)
        idx1, idx2 = (distmat < distance_limit).nonzero()
        good_point_indices = list(set([x for x in range(0, grid3D.shape[0])])-set(idx1))
        N_solvent_guessed = len(good_point_indices)
        curr_density = (solute_total_mass + (N_solvent_guessed * M_solvent)) / ((Lx * 1e-8) ** 3) / N_Avogadro
        if np.abs(best_case["density"] - target_density) > np.abs(curr_density - target_density):
            best_case["density"] = curr_density
            best_case["N_solvent_guessed"] = N_solvent_guessed
            best_case["solvent_coordinates"] = grid3D[good_point_indices, :]
        if solvent_spacing < distance_limit:
            _upper_bound = compensation_coefficient
            compensation_coefficient = compensation_coefficient * 0.9
            if verbose:
                print("N_solvent_guessed:", N_solvent_guessed)
                print("solvent number difference:", np.abs(N_solvent_guessed - N_solvent))
                print("current density:", curr_density)
                print("density difference:", np.abs(curr_density - target_density))
                print("#######################", "iteration", _iter, "#######################\n\n")
            continue
        
        if np.abs(curr_density - target_density) <= density_convergence:
            if verbose:
                print("N_solvent_guessed:", N_solvent_guessed)
                print("solvent number difference:", np.abs(N_solvent_guessed - N_solvent))
                print("current density:", curr_density)
                print("density difference:", np.abs(curr_density - target_density))
                print("#######################", "iteration", _iter, "#######################\n\n")
            break
        elif target_density > curr_density + density_convergence:
            _lower_bound = compensation_coefficient
        elif target_density < curr_density - density_convergence:
            _upper_bound = compensation_coefficient
        compensation_coefficient = (_upper_bound + _lower_bound) * 0.5
        if verbose:
            print("N_solvent_guessed:", N_solvent_guessed)
            print("solvent number difference:", np.abs(N_solvent_guessed - N_solvent))
            print("current density:", curr_density)
            print("density difference:", np.abs(curr_density - target_density))
            print("#######################", "iteration", _iter, "#######################\n\n")
        if _iter >= 3:
            if (last_3_upper_bounds[0] == last_3_upper_bounds[2] and last_3_lower_bounds[0] == last_3_lower_bounds[2]) or len(list(set(last_3_Nx)))==1:
                break
        if _iter >= max_iter:
            break
        
    return best_case


def replicate_mols_by_translation(nmols, displacement, df, bond_df=None, angle_df=None, dihedral_df=None, improper_df=None):
    natoms_per_mol = len(df)
    total_atom_df = pd.concat([df] * nmols, axis=0).reset_index(drop=True)
    total_atom_df.index = total_atom_df.index + 1
    total_atom_df["id"] = total_atom_df.index
    total_atom_df["mol"] = np.repeat(np.arange(0, nmols) + 1, len(df))
    total_atom_df.loc[:, ["x", "y", "z"]] = np.repeat(displacement, natoms_per_mol, axis=0) + total_atom_df.loc[:, ["x", "y", "z"]].values.astype(float)

    if type(bond_df) != type(None): 
        nbonds_per_mol = len(bond_df)
        total_bond_df = pd.concat([bond_df] * nmols, axis=0).reset_index(drop=True)
        total_bond_df.index = total_bond_df.index + 1
        total_bond_df["id"] = total_bond_df.index
        total_bond_df.loc[:, ["at1", "at2"]] = total_bond_df.loc[:, ["at1", "at2"]] + \
            np.repeat(np.repeat(np.array([[x] for x in range(0, nmols)]), nbonds_per_mol, axis=0), 2, axis=1) * natoms_per_mol
    else:
        total_bond_df = None

    if type(angle_df) != type(None): 
        nangles_per_mol = len(angle_df)
        total_angle_df = pd.concat([angle_df] * nmols, axis=0).reset_index(drop=True)
        total_angle_df.index = total_angle_df.index + 1
        total_angle_df["id"] = total_angle_df.index
        total_angle_df.loc[:, ["at1", "at2", "at3"]] = total_angle_df.loc[:, ["at1", "at2", "at3"]] + \
            np.repeat(np.repeat(np.array([[x] for x in range(0, nmols)]), nangles_per_mol, axis=0), 3, axis=1) * natoms_per_mol
    else:
        total_angle_df = None
        
    if type(dihedral_df) != type(None): 
        ndihedrals_per_mol = len(dihedral_df)
        total_dihedral_df = pd.concat([dihedral_df] * nmols, axis=0).reset_index(drop=True)
        total_dihedral_df.index = total_dihedral_df.index + 1
        total_dihedral_df["id"] = total_dihedral_df.index
        total_dihedral_df.loc[:, ["at1", "at2", "at3", "at4"]] = total_dihedral_df.loc[:, ["at1", "at2", "at3", "at4"]] + \
            np.repeat(np.repeat(np.array([[x] for x in range(0, nmols)]), ndihedrals_per_mol, axis=0), 4, axis=1) * natoms_per_mol
    else:
        total_dihedral_df = None

    if type(improper_df) != type(None): 
        nimpropers_per_mol = len(improper_df)
        total_improper_df = pd.concat([improper_df] * nmols, axis=0).reset_index(drop=True)
        total_improper_df.index = total_improper_df.index + 1
        total_improper_df["id"] = total_improper_df.index
        total_improper_df.loc[:, ["at1", "at2", "at3", "at4"]] = total_improper_df.loc[:, ["at1", "at2", "at3", "at4"]] + \
            np.repeat(np.repeat(np.array([[x] for x in range(0, nmols)]), nimpropers_per_mol, axis=0), 4, axis=1) * natoms_per_mol
    else:
        total_improper_df = None

    return total_atom_df, total_bond_df, total_angle_df, total_dihedral_df, total_improper_df



def combine_solvent_solute(solute_dfs, solvent_dfs):
    solute_mass_df, total_solute_atom_df, total_solute_bond_df, total_solute_angle_df, total_solute_dihedral_df, total_solute_improper_df = solute_dfs
    solvent_mass_df, total_solvent_atom_df, total_solvent_bond_df, total_solvent_angle_df, total_solvent_dihedral_df, total_solvent_improper_df = solvent_dfs
    
    total_mass_df = pd.concat([solute_mass_df, solvent_mass_df], axis=0).reset_index(drop=True)
    total_mass_df.index = total_mass_df.index + 1
    total_mass_df["type"] = total_mass_df.index

    if type(total_solvent_atom_df) != type(None):
        total_solvent_atom_df.loc[:, ["type"]] = total_solvent_atom_df.loc[:, ["type"]] + total_solute_atom_df["type"].max()
        total_solvent_atom_df.loc[:, ["mol"]] = total_solvent_atom_df.loc[:, ["mol"]] + total_solute_atom_df["mol"].max()
        total_atom_df = pd.concat([total_solute_atom_df, total_solvent_atom_df], axis=0).reset_index(drop=True)
        total_atom_df.index = total_atom_df.index + 1
        total_atom_df["id"] = total_atom_df.index
        total_solute_atom_number = len(total_solute_atom_df)
    else:
        total_atom_df = total_solute_atom_df
    
    if type(total_solvent_bond_df) != type(None):
        total_solvent_bond_df.loc[:, ["at1", "at2"]] = total_solvent_bond_df.loc[:, ["at1", "at2"]] + total_solute_atom_number
        total_solvent_bond_df.loc[:, ["type"]] = total_solvent_bond_df.loc[:, ["type"]] + total_solute_bond_df["type"].max()
        total_bond_df = pd.concat([total_solute_bond_df, total_solvent_bond_df], axis=0).reset_index(drop=True)
        total_bond_df.index = total_bond_df.index + 1
        total_bond_df["id"] = total_bond_df.index
    else:
        total_bond_df = total_solute_bond_df
    
    if type(total_solvent_angle_df) != type(None):
        total_solvent_angle_df.loc[:, ["at1", "at2", "at3"]] = total_solvent_angle_df.loc[:, ["at1", "at2", "at3"]] + total_solute_atom_number
        total_solvent_angle_df.loc[:, ["type"]] = total_solvent_angle_df.loc[:, ["type"]] + total_solute_angle_df["type"].max()
        total_angle_df = pd.concat([total_solute_angle_df, total_solvent_angle_df], axis=0).reset_index(drop=True)
        total_angle_df.index = total_angle_df.index + 1
        total_angle_df["id"] = total_angle_df.index
    else:
        total_angle_df = total_solute_angle_df
        
    if type(total_solvent_dihedral_df) != type(None):
        total_solvent_dihedral_df.loc[:, ["at1", "at2", "at3", "at4"]] = total_solvent_dihedral_df.loc[:, ["at1", "at2", "at3", "at4"]] + total_solute_atom_number
        total_solvent_dihedral_df.loc[:, ["type"]] = total_solvent_dihedral_df.loc[:, ["type"]] + total_solute_dihedral_df["type"].max()
        total_dihedral_df = pd.concat([total_solute_dihedral_df, total_solvent_dihedral_df], axis=0).reset_index(drop=True)
        total_dihedral_df.index = total_dihedral_df.index + 1
        total_dihedral_df["id"] = total_dihedral_df.index
    else:
        total_dihedral_df = total_solute_dihedral_df

    if type(total_solvent_improper_df) != type(None):
        total_solvent_improper_df.loc[:, ["at1", "at2", "at3", "at4"]] = total_solvent_improper_df.loc[:, ["at1", "at2", "at3", "at4"]] + total_solute_atom_number
        total_solvent_improper_df.loc[:, ["type"]] = total_solvent_improper_df.loc[:, ["type"]] + total_solute_improper_df["type"].max()
        total_improper_df = pd.concat([total_solute_improper_df, total_solvent_improper_df], axis=0).reset_index(drop=True)
        total_improper_df.index = total_improper_df.index + 1
        total_improper_df["id"] = total_improper_df.index
    else:
        total_improper_df = total_solute_improper_df

    return total_mass_df, total_atom_df, total_bond_df, total_angle_df, total_dihedral_df, total_improper_df


def read_ff2pandas(fname):
    read_str = None
    with io.open(fname, "r", newline="\n") as rf:
        read_str = rf.read()

    line_list = read_str.split("\n")
    pair_coeffs = []
    bond_coeffs = []
    angle_coeffs = []
    dihedral_coeffs = []
    improper_coeffs = []
    global_settings = []
    for line in line_list:
        if "pair_coeff" in line:
            pair_coeffs.append(line.strip())
        elif "bond_coeff" in line:
            bond_coeffs.append(line.strip())
        elif "angle_coeff" in line:
            angle_coeffs.append(line.strip())
        elif "dihedral_coeff" in line:
            dihedral_coeffs.append(line.strip())
        elif "improper_coeff" in line:
            improper_coeffs.append(line.strip())
        else:
            if line.strip() != "":
                global_settings.append(line.strip().split("#")[0])

    pair_coeff_data_strs = [x.split("#")[0] for x in pair_coeffs]
    pair_coeff_comments = [x.split("#")[1] if "#" in x else "" for x in pair_coeffs]
    pair_coeff_df = pd.read_csv(io.StringIO("\n".join(pair_coeff_data_strs)), sep=r"\s+", header=None, index_col=None, 
                                names=["pair_coeff", "type1", "type2", "epsilon", "sigma", "epsilon14", "sigma14"]).fillna("")
    pair_coeff_df["#"] = "#"
    pair_coeff_df["comment"] = pair_coeff_comments

    if len(bond_coeffs) > 0:
        bond_coeff_data_strs = [x.split("#")[0] for x in bond_coeffs]
        bond_coeff_comments = [x.split("#")[1] if "#" in x else "" for x in bond_coeffs]
        bond_coeff_df = pd.read_csv(io.StringIO("\n".join(bond_coeff_data_strs)), sep=r"\s+", header=None, index_col=None, 
                                    names=["bond_coeff", "type", "Kb", "b0"]).fillna("")
        bond_coeff_df["#"] = "#"
        bond_coeff_df["comment"] = bond_coeff_comments
    else:
        bond_coeff_df = None

    if len(angle_coeffs) > 0:
        angle_coeff_data_strs = [x.split("#")[0] for x in angle_coeffs]
        angle_coeff_comments = [x.split("#")[1] if "#" in x else "" for x in angle_coeffs]
        angle_coeff_df = pd.read_csv(io.StringIO("\n".join(angle_coeff_data_strs)), sep=r"\s+", header=None, index_col=None, 
                                    names=["angle_coeff", "type", "Ktheta", "r", "kUB", "rUB"]).fillna("")
        angle_coeff_df["#"] = "#"
        angle_coeff_df["comment"] = angle_coeff_comments
    else:
        angle_coeff_df = None

    if len(dihedral_coeffs) > 0:
        dihedral_coeff_data_strs = [x.split("#")[0] for x in dihedral_coeffs]
        dihedral_coeff_comments = [x.split("#")[1] if "#" in x else "" for x in dihedral_coeffs]
        dihedral_coeff_df = pd.read_csv(io.StringIO("\n".join(dihedral_coeff_data_strs)), sep=r"\s+", header=None, index_col=None, 
                                    names=["dihedral_coeff", "type", "Kchi", 
                                           "n", "delta", "weight"]).fillna("")
        dihedral_coeff_df["n"] = ["%d" % float(x) if x!="" else x for x in dihedral_coeff_df["n"]]
        dihedral_coeff_df["delta"] = ["%d" % float(x) if x!="" else x for x in dihedral_coeff_df["delta"]]
        dihedral_coeff_df["#"] = "#"
        dihedral_coeff_df["comment"] = dihedral_coeff_comments
    else:
        dihedral_coeff_df = None

    if len(improper_coeffs) > 0:
        improper_coeff_data_strs = [x.split("#")[0] for x in improper_coeffs]
        improper_coeff_comments = [x.split("#")[1] if "#" in x else "" for x in improper_coeffs]
        improper_coeff_df = pd.read_csv(io.StringIO("\n".join(improper_coeff_data_strs)), sep=r"\s+", header=None, index_col=None, 
                                    names=["improper_coeff", "type", "Kpsi", "psi0"]).fillna("")
        improper_coeff_df["#"] = "#"
        improper_coeff_df["comment"] = improper_coeff_comments
    else:
        improper_coeff_df = None

    return list(filter(None, global_settings)), pair_coeff_df, bond_coeff_df, angle_coeff_df, dihedral_coeff_df, improper_coeff_df



def mix_ff_files(solute_ff_fname, solvent_ff_fname, mixed_ff_fname, total_atom_type_label_map):
    solute_settings, solute_pair_coeff, solute_bond_coeff, solute_angle_coeff, solute_dihedral_coeff, solute_improper_coeff = read_ff2pandas(solute_ff_fname)
    solvent_settings, solvent_pair_coeff, solvent_bond_coeff, solvent_angle_coeff, solvent_dihedral_coeff, solvent_improper_coeff = read_ff2pandas(solvent_ff_fname)
    solute_self_lj_coeff = solute_pair_coeff[solute_pair_coeff["type1"]==solute_pair_coeff["type2"]].copy(deep=True).sort_values(by="type1").reset_index(drop=True)
    solute_self_lj_coeff.index = solute_self_lj_coeff.index + 1
    solvent_pair_coeff.loc[:, ["type1", "type2"]] = solvent_pair_coeff.loc[:, ["type1", "type2"]] + solute_pair_coeff["type1"].max()
    solvent_self_lj_coeff = solvent_pair_coeff[solvent_pair_coeff["type1"]==solvent_pair_coeff["type2"]].copy(deep=True).sort_values(by="type1").reset_index(drop=True)
    solvent_self_lj_coeff.index = solvent_self_lj_coeff.index + 1 + solute_self_lj_coeff["type1"].max()
    solvent_self_lj_coeff["cgenff"] = solvent_self_lj_coeff["type1"].map(total_atom_type_label_map)
    solute_self_lj_coeff["cgenff"] = solute_self_lj_coeff["type1"].map(total_atom_type_label_map)

    mixed_lj_coeff = []
    for type_i in solvent_self_lj_coeff["type1"]:
        for type_j in solute_self_lj_coeff["type1"]:
            mixed_sigma = 0.5 * (solvent_self_lj_coeff.at[type_i, "sigma"].astype(float) + solute_self_lj_coeff.at[type_j, "sigma"].astype(float))
            # mixed_sigma14 = 0.5 * (solvent_self_lj_coeff.at[type_i, "sigma14"].astype(float) + solute_self_lj_coeff.at[type_j, "sigma14"].astype(float))
            mixed_sigma14 = ""
            mixed_epsilon = (solvent_self_lj_coeff.at[type_i, "epsilon"].astype(float) * solute_self_lj_coeff.at[type_j, "epsilon"].astype(float)) ** (1./2.)
            # mixed_epsilon14 = (solvent_self_lj_coeff.at[type_i, "epsilon14"].astype(float) * solute_self_lj_coeff.at[type_j, "epsilon14"].astype(float)) ** (1./2.)
            mixed_epsilon14 = ""
            mixed_lj_coeff.append(["pair_coeff", type_j, type_i, mixed_epsilon, mixed_sigma, mixed_epsilon14, mixed_sigma14, '#', 
                                   solute_self_lj_coeff.at[type_j, "cgenff"] + "-" + solvent_self_lj_coeff.at[type_i, "cgenff"]])
    mixed_pair_coeff = pd.DataFrame(mixed_lj_coeff, columns=["pair_coeff", "type1", "type2", "epsilon", "sigma", "epsilon14", "sigma14", "#", "comment"]).fillna("")

    solute_s = [[list(filter(None, x.split(" ")))[0], 
                  list(filter(None, x.split(" ")))[1], 
                  " ".join(list(filter(None, x.split(" ")))[2:])] for x in solute_settings]
    solvent_s = [[list(filter(None, x.split(" ")))[0], 
                list(filter(None, x.split(" ")))[1], 
                " ".join(list(filter(None, x.split(" ")))[2:])] for x in solvent_settings]
    mixed_settings = []
    hybrid_settings = {}
    for si in solute_s:
        matched_setting_name = False
        for sj in solvent_s:
            if si[0] == sj[0]:
                matched_setting_name = True
                if si[1] != sj[1]:
                    mixed_settings.append(list(filter(None, [si[0], "hybrid"] + si[1:] + sj[1:])))
                    hybrid_settings[si[0]] = list(filter(None, [si[1], sj[1]]))
                else:
                    mixed_settings.append(list(filter(None, si)))
        if not matched_setting_name:
            mixed_settings.append(list(filter(None, si)))
    mixed_settings = [x[0].ljust(20, " ") + " ".join(x[1:]) for x in mixed_settings]

    if "pair_style" in hybrid_settings.keys():
        mixed_pair_coeff["style_name"] = hybrid_settings["pair_style"][0]
        solute_pair_coeff["style_name"] = hybrid_settings["pair_style"][0]
        solvent_pair_coeff["style_name"] = hybrid_settings["pair_style"][1]
        total_pair_coeff = pd.concat([solute_pair_coeff, mixed_pair_coeff, solvent_pair_coeff], axis=0)
        total_pair_coeff["type1"] = total_pair_coeff["type1"].astype(int)
        total_pair_coeff["type2"] = total_pair_coeff["type2"].astype(int)
        total_pair_coeff = total_pair_coeff.sort_values(by=["type1", "type2"]).reset_index(drop=True)
        total_pair_coeff.index = total_pair_coeff.index + 1
        total_pair_coeff["comment"] = total_pair_coeff["type1"].map(total_atom_type_label_map) + "-" + total_pair_coeff["type2"].map(total_atom_type_label_map)
        total_pair_coeff = total_pair_coeff[total_pair_coeff.columns[0:3].tolist() + [total_pair_coeff.columns[-1]] + total_pair_coeff.columns[3:-1].tolist()]
    else:
        total_pair_coeff = pd.concat([solute_pair_coeff, mixed_pair_coeff, solvent_pair_coeff], axis=0)
        total_pair_coeff["type1"] = total_pair_coeff["type1"].astype(int)
        total_pair_coeff["type2"] = total_pair_coeff["type2"].astype(int)
        total_pair_coeff = total_pair_coeff.sort_values(by=["type1", "type2"]).reset_index(drop=True)
        total_pair_coeff.index = total_pair_coeff.index + 1
        total_pair_coeff["comment"] = total_pair_coeff["type1"].map(total_atom_type_label_map) + "-" + total_pair_coeff["type2"].map(total_atom_type_label_map)
        # total_pair_coeff = total_pair_coeff[[total_pair_coeff.columns[0], total_pair_coeff.columns[-1]] + total_pair_coeff.columns[1:-1].tolist()]

    if type(solvent_bond_coeff) != type(None):
        solvent_bond_coeff["type"] = solvent_bond_coeff["type"] + solute_bond_coeff["type"].max()
    if "bond_style" in hybrid_settings.keys():
        solute_bond_coeff['style_name'] = hybrid_settings["bond_style"][0]
        solvent_bond_coeff['style_name'] = hybrid_settings["bond_style"][1]
        total_bond_coeff = pd.concat([solute_bond_coeff, solvent_bond_coeff], axis=0).reset_index(drop=True)
        total_bond_coeff.index = total_bond_coeff.index + 1
        total_bond_coeff = total_bond_coeff[total_bond_coeff.columns[0:2].tolist() + [total_bond_coeff.columns[-1]] + total_bond_coeff.columns[2:-1].tolist()]
    else:
        total_bond_coeff = pd.concat([solute_bond_coeff, solvent_bond_coeff], axis=0).reset_index(drop=True)
        total_bond_coeff.index = total_bond_coeff.index + 1

    if type(solvent_angle_coeff) != type(None):
        solvent_angle_coeff["type"] = solvent_angle_coeff["type"] + solute_angle_coeff["type"].max()
    if "angle_style" in hybrid_settings.keys():
        solute_angle_coeff['style_name'] = hybrid_settings["angle_style"][0]
        solvent_angle_coeff['style_name'] = hybrid_settings["angle_style"][1]
        total_angle_coeff = pd.concat([solute_angle_coeff, solvent_angle_coeff], axis=0).reset_index(drop=True)
        total_angle_coeff.index = total_angle_coeff.index + 1
        total_angle_coeff = total_angle_coeff[total_angle_coeff.columns[0:2].tolist() + [total_angle_coeff.columns[-1]] + total_angle_coeff.columns[2:-1].tolist()]
    else:
        total_angle_coeff = pd.concat([solute_angle_coeff, solvent_angle_coeff], axis=0).reset_index(drop=True)
        total_angle_coeff.index = total_angle_coeff.index + 1

    if type(solvent_dihedral_coeff) != type(None):
        solvent_dihedral_coeff["type"] = solvent_dihedral_coeff["type"] + solute_dihedral_coeff["type"].max()
    if "dihedral_style" in hybrid_settings.keys():
        solute_dihedral_coeff['style_name'] = hybrid_settings["dihedral_style"][0]
        solvent_dihedral_coeff['style_name'] = hybrid_settings["dihedral_style"][1]
        total_dihedral_coeff = pd.concat([solute_dihedral_coeff, solvent_dihedral_coeff], axis=0).reset_index(drop=True)
        total_dihedral_coeff.index = total_dihedral_coeff.index + 1
        total_dihedral_coeff = total_dihedral_coeff[total_dihedral_coeff.columns[0:2].tolist() + [total_dihedral_coeff.columns[-1]] + total_dihedral_coeff.columns[2:-1].tolist()]
    else:
        total_dihedral_coeff = pd.concat([solute_dihedral_coeff, solvent_dihedral_coeff], axis=0).reset_index(drop=True)
        total_dihedral_coeff.index = total_dihedral_coeff.index + 1

    if type(solvent_improper_coeff) != type(None):
        solvent_improper_coeff["type"] = solvent_improper_coeff["type"] + solute_improper_coeff["type"].max()
    if "improper_style" in hybrid_settings.keys():
        solute_improper_coeff['style_name'] = hybrid_settings["improper_style"][0]
        solvent_improper_coeff['style_name'] = hybrid_settings["improper_style"][1]
        total_improper_coeff = pd.concat([solute_improper_coeff, solvent_improper_coeff], axis=0).reset_index(drop=True)
        total_improper_coeff.index = total_improper_coeff.index + 1
        total_improper_coeff = total_improper_coeff[total_improper_coeff.columns[0:2].tolist() + [total_improper_coeff.columns[-1]] + total_improper_coeff.columns[2:-1].tolist()]
    else:
        total_improper_coeff = pd.concat([solute_improper_coeff, solvent_improper_coeff], axis=0).reset_index(drop=True)
        total_improper_coeff.index = total_improper_coeff.index + 1

    with io.open(mixed_ff_fname, "w", newline="\n") as wf:
        wf.write("\n".join(mixed_settings) + """

""" + total_pair_coeff.to_string(header=None, index=None) + """

""" + total_bond_coeff.to_string(header=None, index=None) + """

""" + total_angle_coeff.to_string(header=None, index=None) + """

""" + total_dihedral_coeff.to_string(header=None, index=None) + """

""" + total_improper_coeff.to_string(header=None, index=None) + """

""")
    return solute_bond_coeff, solvent_bond_coeff, solvent_angle_coeff


def replicate_lmp_data_by_N(N, df, bond_df=None, angle_df=None, dihedral_df=None, improper_df=None): 
    df_col = ["id", "mol", "type", "q", "x", "y", "z"]
    ret_df = pd.DataFrame(np.tile(df.loc[:, df_col].values, (N, 1)), columns=df_col).astype({"id": int, 
                                                                                             "mol": int, 
                                                                                             "type": int, 
                                                                                             "q": float, 
                                                                                             "x": float, 
                                                                                             "y": float, 
                                                                                             "z": float})
    ret_df["id"] = ret_df["id"] + np.repeat(np.arange(0, N) * df["id"].max(), df["id"].max())
    ret_df["mol"] = ret_df["mol"] + np.repeat(np.arange(0, N), len(df))

    ret_bond_df = None
    if type(bond_df) != type(None):
        if len(bond_df) >= 1:
            bond_df_col = ["id", "type", "at1", "at2"]
            ret_bond_df = pd.DataFrame(np.tile(bond_df.loc[:, bond_df_col].values, (N, 1)), columns=bond_df_col).astype({"id": int, 
                                                                                                                         "type": int, 
                                                                                                                         "at1": int, 
                                                                                                                         "at2": int})
            ret_bond_df["id"] = ret_bond_df["id"] + np.repeat(np.arange(0, N) * bond_df["id"].max(), bond_df["id"].max())
            ret_bond_df["at1"] = ret_bond_df["at1"] + np.repeat(np.arange(0, N) * df["id"].max(), len(bond_df))
            ret_bond_df["at2"] = ret_bond_df["at2"] + np.repeat(np.arange(0, N) * df["id"].max(), len(bond_df))
        

    ret_angle_df = None
    if type(angle_df) != type(None):
        if len(angle_df) >= 1:
            angle_df_col = ["id", "type", "at1", "at2", "at3"]
            ret_angle_df = pd.DataFrame(np.tile(angle_df.loc[:, angle_df_col].values, (N, 1)), columns=angle_df_col).astype({"id": int, 
                                                                                                                             "type": int, 
                                                                                                                             "at1": int, 
                                                                                                                             "at2": int, 
                                                                                                                             "at3": int})
            ret_angle_df["id"] = ret_angle_df["id"] + np.repeat(np.arange(0, N) * angle_df["id"].max(), angle_df["id"].max())
            ret_angle_df["at1"] = ret_angle_df["at1"] + np.repeat(np.arange(0, N) * df["id"].max(), len(angle_df))
            ret_angle_df["at2"] = ret_angle_df["at2"] + np.repeat(np.arange(0, N) * df["id"].max(), len(angle_df))
            ret_angle_df["at3"] = ret_angle_df["at3"] + np.repeat(np.arange(0, N) * df["id"].max(), len(angle_df))


    ret_dihedral_df = None
    if type(dihedral_df) != type(None):
        if len(dihedral_df) >= 1:
            dihedral_df_col = ["id", "type", "at1", "at2", "at3", "at4"]
            ret_dihedral_df = pd.DataFrame(np.tile(dihedral_df.loc[:, dihedral_df_col].values, (N, 1)), columns=dihedral_df_col).astype({"id": int, 
                                                                                                                                         "type": int, 
                                                                                                                                         "at1": int, 
                                                                                                                                         "at2": int, 
                                                                                                                                         "at3": int, 
                                                                                                                                         "at4": int})
            ret_dihedral_df["id"] = ret_dihedral_df["id"] + np.repeat(np.arange(0, N) * dihedral_df["id"].max(), dihedral_df["id"].max())
            ret_dihedral_df["at1"] = ret_dihedral_df["at1"] + np.repeat(np.arange(0, N) * df["id"].max(), len(dihedral_df))
            ret_dihedral_df["at2"] = ret_dihedral_df["at2"] + np.repeat(np.arange(0, N) * df["id"].max(), len(dihedral_df))
            ret_dihedral_df["at3"] = ret_dihedral_df["at3"] + np.repeat(np.arange(0, N) * df["id"].max(), len(dihedral_df))
            ret_dihedral_df["at4"] = ret_dihedral_df["at4"] + np.repeat(np.arange(0, N) * df["id"].max(), len(dihedral_df))



    ret_improper_df = None
    if type(improper_df) != type(None):
        if len(improper_df) >= 1:
            improper_df_col = ["id", "type", "at1", "at2", "at3", "at4"]
            ret_improper_df = pd.DataFrame(np.tile(improper_df.loc[:, improper_df_col].values, (N, 1)), columns=improper_df_col).astype({"id": int, 
                                                                                                                                         "type": int, 
                                                                                                                                         "at1": int, 
                                                                                                                                         "at2": int, 
                                                                                                                                         "at3": int, 
                                                                                                                                         "at4": int})
            ret_improper_df["id"] = ret_improper_df["id"] + np.repeat(np.arange(0, N) * improper_df["id"].max(), improper_df["id"].max())
            ret_improper_df["at1"] = ret_improper_df["at1"] + np.repeat(np.arange(0, N) * df["id"].max(), len(improper_df))
            ret_improper_df["at2"] = ret_improper_df["at2"] + np.repeat(np.arange(0, N) * df["id"].max(), len(improper_df))
            ret_improper_df["at3"] = ret_improper_df["at3"] + np.repeat(np.arange(0, N) * df["id"].max(), len(improper_df))
            ret_improper_df["at4"] = ret_improper_df["at4"] + np.repeat(np.arange(0, N) * df["id"].max(), len(improper_df))

        
    return ret_df, ret_bond_df, ret_angle_df, ret_dihedral_df, ret_improper_df


def gen_grid3D(Nx, spacing=1.):
    grid3D = (np.array([np.repeat(np.arange(Nx), Nx*Nx), 
                        np.tile(np.repeat(np.arange(Nx), Nx), Nx), 
                        np.tile(np.arange(Nx), Nx*Nx)]).T) * spacing
    grid3D = grid3D - grid3D.mean(axis=0)
    return grid3D