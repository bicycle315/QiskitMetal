#!/usr/bin/env python
# coding: utf-8

# In[1]:
''' This NfingerCapacitor can be tapered by controlling the taper_height. 
    after the finger, the capacitor plate is as flat as the 'flat'.
          
        __|__|___  north
        |      |   cap_distant
        --------
        |||||||    finger_length 
        |||||||    finger_count
        --------   
       |        |  flat
        \      /   taper_height
         \    /
           ||      south  
                 '''


from qiskit_metal.qlibrary.core import QComponent
import numpy as np
from qiskit_metal import draw, Dict
class FingerCapacitor(QComponent):
    component_metadata = Dict(short_name='cpw',
                              _qgeometry_table_poly='True',
                              _qgeometry_table_path='True')
    default_options = Dict(north_width='10um', north_gap='6um',
                           south_width='10um', south_gap='6um',
                           cap_width='10um', cap_gap='6um', cap_gap_ground='6um',
                           finger_length='20um', finger_count='5',
                           cap_distance='300um',
                           taper_height='100um',flat='50um')

    def make(self):
        """Build the component."""
        p = self.p               
        N = int(p.finger_count)
        taper_height=p.taper_height
        flat=p.flat
        
                



        #Finger Capacitor
        cap_box = draw.rectangle(N * p.cap_width + (N - 1) * p.cap_gap,
                                 p.cap_gap + 2 * p.cap_width + p.finger_length,
                                 0, 0)
        make_cut_list = []
        make_cut_list.append([0, (p.finger_length) / 2])
        make_cut_list.append([(p.cap_width) + (p.cap_gap / 2),
                              (p.finger_length) / 2])
        flip = -1

        for i in range(1, N):
            make_cut_list.append([
                i * (p.cap_width) + (2 * i - 1) * (p.cap_gap / 2),
                flip * (p.finger_length) / 2
            ])
            make_cut_list.append([
                (i + 1) * (p.cap_width) + (2 * i + 1) * (p.cap_gap / 2),
                flip * (p.finger_length) / 2
            ])
            flip = flip * -1

        cap_cut = draw.LineString(make_cut_list).buffer(p.cap_gap / 2,
                                                        cap_style=2,
                                                        join_style=2)
        cap_cut = draw.translate(cap_cut,
                                 -(N * p.cap_width + (N - 1) * p.cap_gap) / 2,
                                 0)

        cap_body = draw.subtract(cap_box, cap_cut)
        cap_body = draw.translate(
            cap_body, 0, -p.cap_distance -
            (p.cap_gap + 2 * p.cap_width + p.finger_length) / 2)

        cap_etch = draw.rectangle(
            N * p.cap_width + (N - 1) * p.cap_gap + 2 * p.cap_gap_ground,
            p.cap_gap + 2 * p.cap_width + p.finger_length +p.cap_gap_ground, 
            0, -p.cap_distance -
            (p.cap_gap + 2 * p.cap_width + p.finger_length) / 2)

        


        #CPW
        north_cpw = draw.LineString([[0, 0], [0, -p.cap_distance]])

        south_cpw = draw.Polygon(((-(N * p.cap_width + (N - 1) * p.cap_gap)/2,-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length)),
        (-(N * p.cap_width + (N - 1) * p.cap_gap)/2,-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length)-flat),
        (-p.south_width/2,-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length)-taper_height-flat),
        (p.south_width/2,-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length)-taper_height-flat),        
        ((N * p.cap_width + (N - 1) * p.cap_gap)/2,-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length)-flat),
        ((N * p.cap_width + (N - 1) * p.cap_gap)/2,-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length))))

        taper_etch= draw.Polygon(((-(N * p.cap_width + (N - 1) * p.cap_gap + 2 * p.cap_gap_ground)/2,-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length)),
        (-(N * p.cap_width + (N - 1) * p.cap_gap + 2 * p.cap_gap_ground)/2,-p.cap_distance-flat-(p.cap_gap + 2 * p.cap_width + p.finger_length)),
        (-(p.south_width/2 + p.south_gap),-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length)-flat-taper_height),
        (p.south_width/2 + p.south_gap,-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length)-flat-taper_height),
        ((N * p.cap_width + (N - 1) * p.cap_gap + 2 * p.cap_gap_ground)/2,-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length)-flat),
        ((N * p.cap_width + (N - 1) * p.cap_gap + 2 * p.cap_gap_ground)/2,-p.cap_distance-(p.cap_gap + 2 * p.cap_width + p.finger_length))))

        #Rotate and Translate
        c_items = [north_cpw, south_cpw, taper_etch, cap_body, cap_etch]
        c_items = draw.rotate(c_items, p.orientation, origin=(0, 0))
        c_items = draw.translate(c_items, p.pos_x, p.pos_y)
        [north_cpw, south_cpw,taper_etch, cap_body, cap_etch] = c_items

        #Add to qgeometry tables
        self.add_qgeometry('path', {'north_cpw': north_cpw},
                           width=p.north_width,
                           layer=p.layer)
        self.add_qgeometry('path', {'north_cpw_sub': north_cpw},
                           width=p.north_width + 2 * p.north_gap,
                           layer=p.layer,
                           subtract=True)
        self.add_qgeometry('poly',{'south_cpw': south_cpw}, layer=p.layer)
        self.add_qgeometry('poly',{'taper_etch': taper_etch}, layer=p.layer, subtract=True)
        self.add_qgeometry('poly', {'cap_body': cap_body}, layer=p.layer)
        self.add_qgeometry('poly', {'cap_etch': cap_etch},
                           layer=p.layer,
                           subtract=True)

        #Add pins
        north_pin_list = north_cpw.coords
       #south_pin_list = south_cpw.coords

        self.add_pin('north_end',
                     points=np.array(north_pin_list[::-1]),
                     width=p.north_width,
                     input_as_norm=True)
        '''self.add_pin('south_end',
                     points=np.array(south_pin_list),
                     width=p.south_width,
                     input_as_norm=True)'''


# In[ ]:




