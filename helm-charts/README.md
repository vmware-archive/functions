Helm Charts
============

This directory contains examples which are packaged as Helm charts since 
their functions connects services that are deployed by charts.


ocr:
----
This example implements an OCR (Optical Character Recognition) pipeline for PDF files. It 
install all required services trasnparently and the python function that glues all services together 

Basically, in this example you upload a PDF file to an object storage server (Minio), which fires up
a webhook that makes that the uploaded file is parsed by Apache Tika and the extracted text then is 
stored in MongoDB. 
