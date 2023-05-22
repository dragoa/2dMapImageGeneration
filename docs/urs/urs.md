
### Usr Requirements Specification Document
##### DIBRIS – Università di Genova. Scuola Politecnica, Software Engineering Course 80154e


**VERSION : 1.1**

**Authors**  
Abdullah Al Foysal
Alessandro Drago

**REVISION HISTORY**

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 27/03/2023 | Alessandro Drago | Given a first description of the project. |
| 1.1 | 13/04/2023 | Alessandro Drago, Abdullah Al Foysal | Update of the urs file, added Context and Motivations. |
| 1.2 | 05/07/2023 | Alessandro Drago, Abdullah Al Foysal | Refined the urs file, added non functional requirements. |
| 1.3 | 21/07/2023 | Alessandro Drago, Abdullah Al Foysal | Requirements are now refined. |

# Table of Contents

1. [Introduction](#p1)
	1. [Document Scope](#sp1.1)
	2. [Definitios and Acronym](#sp1.2) 
	3. [References](#sp1.3)
2. [System Description](#p2)
	1. [Context and Motivation](#sp2.1)
	2. [Project Objectives](#sp2.2)
3. [Requirement](#p3)
 	1. [Stakeholders](#sp3.1)
 	2. [Functional Requirements](#sp3.2)
 	3. [Non-Functional Requirements](#sp3.3)
  

<a name="p1"></a>

## 1. Introduction
This document contains what are the functional and non-functional requirements for a Software Engineering project at FadeOut Software. As well as explained the reason for using those functional and non-functional sectors.

<a name="sp1.1"></a>

### 1.1 Document Scope
This paper introduces the Requirements Analysis for the Software Engineering course (SE-80154) of the Master of Science in Computer Engineering degree in Genoa, Italy.

<a name="sp1.2"></a>

### 1.2 Definitios and Acronym


| Acronym				| Definition | 
| ------------------------------------- | ----------- | 
| SE23                                 | Software Engineering course, 2023 at university of Genoa |
| SE-80154							   | Software Engineering course, 2023 at university of Genoa, 80154 is its ID number |
| WASDI								   | Web Advanced Space Developer Interface |
| FadeOut Software					   | Company holder of WASDI |
| EO					   			   | Earth Observation |
| TIFF					   			   | Stands for Tag Image File Format. It is a file format used to store raster graphics and image information. |
| GeoServer					   		   | Open source server for sharing geospatial data |


<a name="sp1.3"></a>

### 1.3 References 
1. [WASDI Docs](https://wasdi.readthedocs.io/en/latest/index.html)
2. [WASDI Youtube Channel]()
3. [Some Reference](https://github.com/mnarizzano/se23-p08/tree/main/docs/ref)
4. [GeoServer Docs](https://docs.geoserver.org/)
5. [Web Map Service](https://www.ogc.org/standard/wms/)


<a name="p2"></a>

## 2. System Description
<a name="sp2.15"></a>
WASDI is an online platform that offers services to develop and deploy online applications that use satellite data. 
The project involves the developement of a platform that helps Earth Observation (EO) experts process satellite imagery on the cloud. The team is working on developing new software tools that can extract images and data from the results of the analytics tools present on the platform, in order to help communicate the results of the analyses to the stakeholders involved. The project aims to ease the communication of the results of the applications so that decision makers can better understand the phenomena they are dealing with and respond quickly to questions such as flood size, building count, and wildfire location.

### 2.1 Context and Motivation

<a name="sp2.2"></a>
WASDI's web interface provides several tools for both experienced and novice users.<br>
In fact, WASDI allows researchers to create workspaces in which gather satellite data, in particular the Sentinel ones, display them on-line, run algorithms, displaying and evaluating the results, and allows to share these projects among different users.<br>
There are also several applications in the Marketplace that are used to process satellite images and study a particular phenomena. In general this is done by the more experienced users.

### 2.2 Project Obectives 
Through workspaces and applications in the marketplace, researchers are able to collect satellite data and run algorithms on them. Once this phase is finished, a required feature is the ability to create a report in PDF containing all the information from the processing. This report will then be given by the researchers to those less experienced users or stakeholders. 
The document shall have a predefined template in which various information such as date, name and logo of the company, images that were processed and explanatory paragraphs of text are present.
The images found in WASDI's workspace are in TIFF format and therefore before they are inserted into the document, they must be processed. 
On the various servers in which these images are stored is an instance of GeoServer is present. 
So the idea is to take the images from the WASDI workspace, process them with GeoServer by, for example, selecting a certain area of that image, or applying a style, and return this image in a desirable format (PNG or GIF). 

<a name="p3"></a>

## 3. Requirements

| Priorità | Significato | 
| --------------- | ----------- | 
| M | **Mandatory:**   |
| D | **Desiderable:** |
| O | **Optional:**    |
| E | **future Enhancement:** |

<a name="sp3.1"></a>
### 3.1 Stakeholders

FadeOut Software<br>
WASDI

<a name="sp3.2"></a>
### 3.2 Functional Requirements 

| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 | The user shall be able to export a full report of the analysis in a PDF format | M |
| 2.0 | The report shall contain the result of the analysis done on wasdi. |M|
| 3.0 | The report shall have a predefined format. |M|
| 4.0 | The report shall display the logo of the company. |M|
| 5.0 | The report shall contain the images processed via WASDI. |M|
| 6.0 | The report shall contain also images with a specific style uploaded by the user. |M|
| 7.0 | Users shall be able to select a specif area on the images generated. |M|
| 8.0 | Users shall be able to generate a GIF file from a set of TIFFs. | D |
| 9.0 | Users shall be able to generate a PDF file as the output and all the details will be contained by that pdf. | M |

<a name="sp3.3"></a>
### 3.2 Non-Functional Requirements 
 
| ID | Descrizione | Priorità |
| 1.0 | reportlab.pdfgen( can customize the content of the PDF file by modifying the create_pdf() function. | M | 



