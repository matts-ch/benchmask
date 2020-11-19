# benchmask
Simple Setup to Benchmark Facemasks


 * [Table of contents](#table-of-contents)
 * [Goal](#Goal)
 * [Findings](#Findings)
 * [Features](#Features)
 * [Setup](#Setup)
 * [Procedure](#Procedure)
 * [Next Steps](#next-steps)



## Goal

- Cheap, easy setup to benchmark masks in terms of filtration efficiency and differential pressure
- Sealing to (dummy) head is tested as well


Fineprint, what it is not, and disclaimer

- Replacement for lab testing, mainly since measuring particulate matter is hard, lab devices cost 15k and still have limitations. 
- No policitcal, medical claims

And yes, I think a bad mask is still better than no mask, mainly for the big droplet transmission vector. For aerosols, I assume only a good mask with good sealing can make a difference. 

Disclaimer: 
This is intentionally a very early publication. I will add more details and code, if someone is interested (agile publishing ;-))
Filtration efficiency needs rescaling, but the relative values among the masks are OK. 
I am an employee from Sensirion, therefore It was obvious to choose these sensors


## Findings




![alt text](https://github.com/matts-ch/benchmask/blob/main/overview.png "Example Measurement Set")
- Sealing is important, see e.g. the mask with the "bad nosepiece" with tape, this mask performs excellent
![alt text](https://github.com/matts-ch/benchmask/blob/main/bad_nose_piece.jpg "Bad Nosepiece")
![alt text](https://github.com/matts-ch/benchmask/blob/main/overview_badnp.png "Bad Nosepiece")

- Cotton and other regular community masks perform rather poorly
![alt text](https://github.com/matts-ch/benchmask/blob/main/cilander.jpg "Regular Community")
![alt text](https://github.com/matts-ch/benchmask/blob/main/overview_community.png "Bad Nosepiece")

- "Flat masks" perform very poorly, especially if there is no nose piece
![alt text](https://github.com/matts-ch/benchmask/blob/main/flatmask.jpg "Flat Mask")
![alt text](https://github.com/matts-ch/benchmask/blob/main/overview_flat.png "Flat mask, bad filtration, hard to breath if taped")


![alt text](https://github.com/matts-ch/benchmask/blob/main/overview.png "Example Measurement Set")

## Features

- Benchmark filtration efficiency
- Benchmark differential pressure (how hard to breath through mask)
- More realistic test, dummy head instead of the usual fabric only lab tests
- Huge range of volume flows possible
- Both directions possible (in-/exhale)
- Very simple setup, off the shelf and cheap parts

and some limitations
- I used only one artificial head, the findings are only valid with for that exact head. 
- Particulate matter measurements are hard, I used a very affordable sensor, not lab equipment
- The Efficiency scaling is off, I need to adjust it, but the relative comparison is valid

## Setup

![alt text](https://github.com/matts-ch/benchmask/blob/main/system.JPG "Overview Setup")


![alt text](https://github.com/matts-ch/benchmask/blob/main/system_photo1.png "Overview Setup")


![alt text](https://github.com/matts-ch/benchmask/blob/main/head.png "Head")


![alt text](https://github.com/matts-ch/benchmask/blob/main/Box.jpg "Box")


The main idea is to use the fan with the mask as a air purifier inside a closed space. The better the mask, the faster the decrease in particle concentration. Given everything else (mainly the volume flow) ist constant. 

The setup is rather simple and with off the shelf parts, bill of material ca. 200USD. 

- Fan, e.g. remote control plane electric ducted fan (EDF), search for EDF (e.g. Banggood, Hobbyking etc.)
- Speed controller for the fan, also RC stuff, search for brushless esc. The requirements in terms of voltage/amps are minimal (8V,5A should already do it)
- Flow sensor is usded to measure the volume flow, I used a SFM3019
- Differential pressure sensor, I used a SDP3x evaluation board, but also SDP6xx, SDP8xx work perfect for that job. If you choose the sensor, keep in mind, that the differential pressure is rather small (ca. 20Pa), this is very small for the usual membrane based sensors
- Particulate matter sensor, I recommend a SPS30. 
- Humidity/Temperature sensor, not absolutely necessary, but a very low relative humidity might lead to static charges and therefore an additional 'cleaning effect', SHT31 is a very robust choice and readily available on breakout boards
- Head: I used a hairpiece stand, but obviously 3D printing is always an option




## Procedure

- Wear mask
![alt text](https://github.com/matts-ch/benchmask/blob/main/ffp2.jpg "ffp2 mask")
- Generate particles inside the box (extinguish small candle)
- Close box
- Set fan speed such that the flow is in the desired range (I used 20litres/minute)
- wait 1min (homogenous particle distribution)
- start measurement, measure until concentration dropped significantly, 3minutes or 30% of the concentration is a good starting point
- fit the exponential curve to the data
![alt text](https://github.com/matts-ch/benchmask/blob/main/semilog_fit_out_ffp2_shen_huan_taped1.png "Overview Setup")


- normalize filtration efficiency and pressure drop with volume flow (sometimes it is not possible to perfectly match the desired volume flow)


## Next Steps

- Improve Documentation
- Simulate a beard
- Use a second head
- Closed loop controller for volumen flow
- Automate whole measurement

