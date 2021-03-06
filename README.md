# Kinetic Inductance Detector drawer - KID drawer
(version 0.1.1 - 19/02/2022)

With this package it is possible to generate .dxf design files of Kinetic Inductance Detectors (KIDs) starting from geometrical parameters defined below:

- `index`: int, the id of the pixel
- `vertical_size`: float, edge size of the absorber
- `line_width`: float, width of the conductive path
- `coupling_capacitor_length`: float, length of the coupling capacitor
- `coupling_capacitor_width`: float, width of the coupling capacitor
- `coupling_connector_width`: float, width of the conductive segment that goes
	from the pixel to the coupling capacitor
- `coupling_capacitor_y_offset`: float, vertical separation between the pixel
	and the coupling capacitor
- `capacitor_finger_number`: float, number of fingers of the interdigital capacitor
	with decimal digits meaning an extra finger of variable length
- `capacitor_finger_gap`: float, gap between interdigitated fingers
- `capacitor_finger_width`: float, width of the interdigitated fingers
- `hilbert_order`: int, hilbert order of the absorber (it is reccommended to not
	exceed the 7th order for computational reasons)
- `absorber_separation`: float, horizontal separation of the absorber from the
	capacitor

These parameters are shown in the following image (with `capacitor_finger_number = 3.6` and `hilbert_order = 3`).

![schematic](/images/schematic.png)

The final dxf drawing has many layers:

- PIXEL: the actual layer where the KID is shown
- PIXEL_AREA: a layer where a rectangle encloses the whole pixel
- ABSORBER_AREA: a layer where a square encloses the absorber section of the KID
- CENTER: a layer where the two diagonals of the ABSORBER_AREA square are shown
- INDEX: a layer where the `index` value of the pixel is shown

The output drawing has the absorber centered to the origin

All the distances are expressed in units of microns.
The following image shows an example of a real KID generated with this package.

![example](/images/example.png)

# Installing
Just download the .zip file and copy/paste the `KID_drawer` directory into the library folder of your python version. Soon the `pip install` version will be available.

# Example
The `test.py` script is an example script. Try to run it. You can find the expected output in the `examples` directory.

```python
# test script

# import the package
import KID_drawer as KID

# define a Pixel object
pixel = KID.Pixel(index = 1,
		  vertical_size = 3000.0,
		  line_width = 4.0,
		  coupling_capacitor_length = 2500.0,
		  coupling_capacitor_width = 80.0,
		  coupling_connector_width = 20.0,
		  coupling_capacitor_y_offset = 120.0,
		  capacitor_finger_number = 50.65,
		  capacitor_finger_gap = 4.0,
		  capacitor_finger_width = 4.0,
		  hilbert_order = 4,
		  absorber_separation = 200.0)

# print the pixel parameters
pixel.print_info()

# save the .dxf file
pixel.save_dxf(filename = 'examples/test/pixel.dxf')
```
