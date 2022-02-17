#!/usr/bin/env python
# coding: utf-8

# In[1]:

'''This launchpadwirebond doesnt have gap part at the side of the chip that ends.'''


from qiskit_metal import draw
from qiskit_metal.toolbox_python.attr_dict import Dict
from qiskit_metal.qlibrary.core import QComponent


# In[2]:


class LaunchpadWirebondDriven_ChipEnd(QComponent):
    default_options = Dict(trace_width='cpw_width',
                           trace_gap='cpw_gap',
                           lead_length='25um',
                           pad_width='80um',
                           pad_height='80um',
                           pad_gap='58um',
                           taper_height='122um')
    def make(self):
    
        p = self.p

        pad_width = p.pad_width
        pad_height = p.pad_height
        pad_gap = p.pad_gap
        trace_width = p.trace_width
        trace_width_half = trace_width / 2.
        pad_width_half = pad_width / 2.
        lead_length = p.lead_length
        taper_height = p.taper_height
        trace_gap = p.trace_gap

        pad_gap = p.pad_gap
        
        # When the Laucnchpad end is in contact with the end of the chip!!
        # Geometry of main launch structure
        # The shape is a polygon and we prepare this point as orientation is 0 degree
        launch_pad = draw.Polygon([
            (0, trace_width_half), (-taper_height, pad_width_half),
            (-(pad_height + taper_height), pad_width_half),
            (-(pad_height + taper_height), -pad_width_half),
            (-taper_height, -pad_width_half), (0, -trace_width_half),
            (lead_length, -trace_width_half), (lead_length, trace_width_half),
            (0, trace_width_half)
        ])

        # Geometry pocket (gap)
        # Same way applied for pocket
        pocket = draw.Polygon([(0, trace_width_half + trace_gap),
                               (-taper_height, pad_width_half + pad_gap),
                               (-(pad_height + taper_height),
                                pad_width_half + pad_gap),
                               (-(pad_height + taper_height),
                                -(pad_width_half + pad_gap)),
                               (-taper_height, -(pad_width_half + pad_gap)),
                               (0, -(trace_width_half + trace_gap)),
                               (lead_length, -(trace_width_half + trace_gap)),
                               (lead_length, trace_width_half + trace_gap),
                               (0, trace_width_half + trace_gap)])

        # These variables are used to graphically locate the pin locations
        main_pin_line = draw.LineString([(lead_length, trace_width_half),
                                         (lead_length, -trace_width_half)])
        driven_pin_line = draw.LineString([
            (-(pad_height + taper_height + pad_gap), pad_width_half),
            (-(pad_height + taper_height + pad_gap), -pad_width_half)
        ])

        # Create polygon object list
        polys1 = [main_pin_line, driven_pin_line, launch_pad, pocket]

        # Rotates and translates all the objects as requested. Uses package functions in
        # 'draw_utility' for easy rotation/translation
        polys1 = draw.rotate(polys1, p.orientation, origin=(0, 0))
        polys1 = draw.translate(polys1, xoff=p.pos_x, yoff=p.pos_y)
        [main_pin_line, driven_pin_line, launch_pad, pocket] = polys1

        # Adds the object to the qgeometry table
        self.add_qgeometry('poly', dict(launch_pad=launch_pad), layer=p.layer)

        # Subtracts out ground plane on the layer its on
        self.add_qgeometry('poly',
                           dict(pocket=pocket),
                           subtract=True,
                           layer=p.layer)

        # Generates the pins
        self.add_pin('tie', main_pin_line.coords, trace_width)
        self.add_pin('in', driven_pin_line.coords, pad_width, gap=pad_gap)


# In[ ]:




