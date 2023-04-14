
### Usr Requirements Specification Document
##### DIBRIS – Università di Genova. Scuola Politecnica, Software Engineering Course 80154e


**VERSION : 1.1**

**Authors**  
Abdullah Al Foysal<br>
Alessandro Drago

**REVISION HISTORY**

| Version    | Date        | Authors      | Notes        |
| ----------- | ----------- | ----------- | ----------- |
| 1.0 | 27/03/2023 | Alessandro Drago | Given a first description of the project. |
| 1.1 | 13/04/2023 | Alessandro Drago | Update of the urs file, added Context and Motivations |

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
This document contains what are the functional and non-functional requirements for a Software Engineering project at FadeOut Software.

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


<a name="sp1.3"></a>

### 1.3 References 
1. [WASDI Docs](https://wasdi.readthedocs.io/en/latest/index.html)
2. [WASDI Youtube Channel]()
3. [Some Reference](https://github.com/mnarizzano/se23-p08/tree/main/docs/ref)


<a name="p2"></a>

## 2. System Description
<a name="sp2.15"></a>
WASDI is an online platform that offers services to develop and deploy online applications that use satellite data. 
The project involves the developement of a platform that helps Earth Observation (EO) experts process satellite imagery on the cloud. The team is working on developing new software tools that can extract images and data from the results of the analytics tools present on the platform, in order to help communicate the results of the analyses to the stakeholders involved. The project aims to ease the communication of the results of the applications so that decision makers can better understand the phenomena they are dealing with and respond quickly to questions such as flood size, building count, and wildfire location. The team is open to exploring various programming languages and frameworks to achieve their goals.

### 2.1 Context and Motivation

<a name="sp2.2"></a>
In the WASDI platform the user is able to create workspaces, in which images from different satellite providers can be imported. Then the user is also able to select various application from the store and run them in the workspace to compute some results.<br>
Examples could be the detection of floods, or wildfire location.


### 2.2 Project Obectives 
A required feature would be a processor that works as a print server to create a document in pdf format out of the content described by the users.<br>
The user shall be able to submit a file in some markup language, for example LaTeX, containing a description of what he would like to add in the report.
Another desiderable feature would be the possibility for the user to export an animated GIF file out of a set of TIFF images. As per our previous discussions, we are currently developing a print server that will allow users to create documents out of the content they describe. With LaTeX, our print server will enable users to produce documents with precise and consistent formatting, making it ideal for academic writing and research.

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
| 1.0 | Improve the general user interface of the web application | M |
| 2.0 | The user shall be able to export a report in pdf format | M |
| 3.0 | The user shall be able to generate a gif file from a set of TIFF files | D |
| 4.0 | The pdf shall contain all the information that the GIF will have and also will depend on the user that what information USER wants | M |

<a name="sp3.3"></a>
### 3.2 Non-Functional Requirements 
 
| ID | Descrizione | Priorità |
| --------------- | ----------- | ---------- | 
| 1.0 | XXXXX |M|
