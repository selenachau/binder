# Finding LC class data with ISBN: Intro to Python and API

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/selenachau/binder/HEAD)

Description: 
Collection-centered data for ebook use assessment have varied descriptive metadata. COUNTER allows consistency across vendor platforms, but is limited to providing ISBNs. This session introduces a Python script to fill in Library of Congress classification data so that collection assessment by subject matter is possible. This project extends COUNTER usage reports to assess by LC class and was presented at library conferences in 2023.

Contents: 
Two Jupyter Notebooks - one a walkthrough that demonstrates python isbnlib library and OCLC Classify API (isbn-lcc-walkthough.ipynb), and another (isbn-lcc-quick-convert.ipynb) that allows the user to directly use the tool. Two test csv files - one is a test input file for the quick convert notebook and one is a test output file for the quick convert notebook. Users may upload and overwrite the input csv according to instructions in the quick convert notebook to receive their own output file. A python file (\*.py) is included, which is the same code in the code cell of the quick-convert Jupyter Notebook.

How to Install, Run and Use the Project:
- Go to mybinder.org and enter the URL of this github repository: https://github.com/selenachau/binder or use the [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/selenachau/binder/HEAD) link
- Required packages are installed upon launch
- Note: please read and comply with the OCLC Classify API terms and conditions if you intend to develop and/or publish your own code.
- Instructions are described in each of the Jupyter Notebooks. 


Credits: My work is in part a simplification of Melissa Belvadi's great code: https://github.com/mbelvadi/lcc_from_isbn

Thanks to my ALA Library Research Roundtable mentoring cohort Arthur Aguilera, Teresa Chung, Karen Harker, and Francisco Juarez, for thought sessions around technology and trends in collections assessment. 
