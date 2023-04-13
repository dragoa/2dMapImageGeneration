### First Meeting Notes

Date: 23/03/2023

Participants: Marco Menapace (Senior Engineer **M**), Cristiano Nattero (Senior Software Developer **C**)

Notes:

**So, what is WASDI?**
- **C,M**: WASDI is an online platform that offers services to develop and deploy online applications that use satellite data. WASDI is a horizontal technology that provides services for vertical applications that enable researchers to collect satellite data, visualize it online, run algorithms, and evaluate results.


**So, what is the problem that you are facing?** 
- **C,M**: So one of the things we'd like to do now is to better improve the user interface of the WASDI platform. The goal of WASDI is to help the expert users (the ones that are really good working with images) better serve the needs of the end-users that aren't familiar with raw data. Since you are new to the application, we would like your feedback on what needs to be changed or improved.

**Have you considered any new features that could be included?**
- **C**: A possible new feature could be the ability to export a gif file showing the time evolution of a particular phenomenon. One problem to consider is that the images are stored in a WASDI database and need to be downloaded. These images may also be very large, so resizing may be necessary.
We would also like to have the ability to export the report, when finished, to a pdf file, for example. We are also open to any suggestions related to improving the user interface.

**How does wasdi work with data? And how are they read?**
- **C**: WASDI takes images from different providers, these are then preprocessed before being displayed and then saved in a database. When wasdi is first launched, these images must be downloaded and a function in the WASDI library returns the path to them. There is also an heuristic algorithm that shows the best images from different providers.

**So what we should do at first? And what are the programming languages that you are using?**
- **C**: Lets warm up the things with trying the WASDI platform and look out for any suggestion. It can be accessed via browser or directly from your machine using one of the supported WASDI libraries. WASDI in fact supports several programming languages, but to get started it may be useful to use Python. WASDI also provides [some documentation](https://wasdi.readthedocs.io/en/latest/index.html#) and some tutorials that you can check out.

**Do we need any particular requirement to use WASDI on our PC?**
- **C**: No special requirements are necessary, but you will note that when working with large images, they will need to be downloaded and this may take some time.