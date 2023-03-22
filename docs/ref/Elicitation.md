### Elicitation Phase : Gather information about domain and requirement
##### DIBRIS – Università di Genova. Scuola Politecnica, Software Engineering Course 80154

## Table of Contents

1. [Introduction to Earth observation](#p1)
	1. [Definitions](#sp1.1)
2. [Instruments](#p2)
	1. [Passive Instruments](#sp2.1)
	2. [Active Instruments](#sp2.2)
3. [Requirement](#p3)
 	1. [Stakeholders](#sp3.1)
 	2. [Functional Requirements](#sp3.2)
 	3. [Non-Functional Requirements](#sp3.3)
  
  
<a name="p1"></a>

## 1. Introduction to Earth observation
#### What is Earth observation?
> Earth observation is the process of **acquiring observation of the Earth's surface** via different instruments mounted in different platforms.

This instruments can be:
- Active
- Passive

The platforms could be for example:
- Satellites
- Aircraft
- Drones

<a name="sp1.1"></a>

### 1.1 Definitions
#### Remote Sensing 
> The acquisition of information about an object or phenomenon without making physical contact with the object: the term can be applied to acquiring information about the Earth and other planets.

#### Spatial resolution
How can I measure an image resolution? 
> One possibility is the physical dimension that represent a pixel of the image.

#### Spectral resolution
> Spectral resolution describes the amount of spectral detail in a band.

#### Revisit time
> The time elapsed between subsequent observations of the same area of interest.

<a name="sp2"></a>

## 2. Instruments 
Not all the electromagnetic spectrum can be used for Earth observation. We could use:
- The visible spectrum (~0,39 – ~0,70 mm)
- Part of the infrared spectrum (~0,70 – ~14 mm)
- The radio wave range (~1 cm – ~11m)

<picture>
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="https://upload.wikimedia.org/wikipedia/commons/3/34/Atmospheric_electromagnetic_opacity.svg" width="75%" height="30%">
</picture>
<a name="sp2.1"></a>

### 2.1 Passive Instruments 
This type of instruments **detect elettromagnetic emissions** from the components of the Earth's surface and atmosphere.
This method depends on the day/night cycle and can be degraded or blocked by cloud cover.

There are different types of passive imagery.
<a name="sp2.1.1"></a>

#### 2.1.1 **Panchromatic imagery**
> Measure of light intensity over a broad range of the electromagnetic spectrum -> higher spatial resolution

<a name="sp2.1.2"></a>

#### 2.1.2 **Multi-spectral imagery**
> Measure of light intensity in several narrow bands of the electromagnetic spectrum -> lower spatial resolution
<a name="sp2.1.3"></a>

#### 2.1.3 **Pan-sharpened imagery**
> The process of merging multi-spectral images with panchromatic images to provide high resolution coloured images
<a name="sp2.1.4"></a>

#### 2.1.4 **Hyper-spectral imagery**
> Measure of light intensity in a nearly-continuous spectrum. Allows for detection, identification and quantification of surface materials, as well as inferring biological and chemical processes. 

<a name="sp2.2"></a>

### 2.2 Active Instruments 
Instruments are composed of a transmitter that **sends out a specific electromagnetic signal** and of a receiver to **capture the interaction of the signal with the Earth’s surface**.
 -> don't depend on solar illumination

There are different types of active imagery.

<a name="sp2.2.1"></a>

#### 2.2.1 **Synthetic Aperture Radar (SAR)**
Transmits electromagnetic pulses towards the Earth’s surface where they are reflected by the surface features. The instrument’s antenna can detect and record the return pulses. **The intensity of the return pulse and the time** it takes to arrive back at the antenna are used to generate SAR imagery.

It is insensitive to the day/night cycle and most of the time to the meteorological conditions, including clouds.

The wavelength determines how the radar signal interacts with the surface and how far a signal can penetrate into a medium.

<picture>
  <img alt="Shows an illustrated sun in light mode and a moon with stars in dark mode." src="./imgs/wavelength_sar.png">
</picture>

Some of the application of SAR are:
- Flood mapping 
- Deformation mapping: earthquakes, landslides
- DEM creation

<a name="sp2.2.2"></a>

#### 2.2.2 **Light Detection And Ranging (LiDAR)**
So as SAR trasmits electromagnetic pulses towards the Earth’s surface and then the return pulses are recorded, but uses only the **IR, visible or UV wavelengths**.

Lidars are used for **precise measurement of topographic features**, monitoring growth or decline of glaciers, profiling clouds, measuring winds, studying aerosols and quantifying various atmospheric components.

<a name="sp2.2.3"></a>

#### 2.2.3 **Radar altimeter**
Thanks to the ranging capability of radar it measure the surface topography profile along the satellite track. They provide precise measurements of a satellite's height above the ocean by measuring the time interval between the transmission and reception of very short electromagnetic pulses.

<a name="sp2.2.4"></a>

#### 2.2.4 **Radar scatterometer**
A radar scatterometer is a microwave radar sensor used to measure the **reflection** or scattering effect **produced while scanning the surface of the Earth** from an aircraft or a satellite. It provides a measure of wind speed and direction near the sea surface.
