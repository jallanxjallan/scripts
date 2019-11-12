#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  extract_pdf_content.py
#  
#  Copyright 2018 Jeremy Allan <jeremy@Jeremyallan.com>



import os
import re
import attr
from collections import namedtuple


from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator


''' This is what we are trying to do:
1) Transfer information from PDF file to PDF document object. This is done using parser
2) Open the PDF file
3) Parse the file using PDFParser object
4) Assign the parsed content to PDFDocument object
5) Now the information in this PDFDocumet object has to be processed. For this we need
   PDFPageInterpreter, PDFDevice and PDFResourceManager
 6) Finally process the file page by page 
 Fortunately, though, each object also provides a bbox (bounding box) attribute, which is a four-part tuple of the object's page position: (x0,
y0, x1, y1)
x0: the distance from the left of the page to the left edge of the box.
 y0: the distance from the bottom of the page to the lower edge of the box.
 x1: the distance from the left of the page to the right edge of the box.
 y1: the distance from the bottom of the page to the upper edge of the box.

Remember in PDF the page origin is the *bottom left corner*.
So the bottom left is (0,0) and the top right corner is
somewhere like (612,792) in the case of A4 paper.

def __attrs_post_init__(self):
        (minx, miny, maxx, maxy) = self.tbox.bbox
        self.top_left = (minx, maxy)
        self.top_right = (maxx, maxy)
        self.bottom_left = (minx, miny)
        self.bottom_right = (maxx, miny) 

'''

TextBox = namedtuple("TextBox", ('position', 'text'))

def component_name(layout, bounding_box):
    import json
    (minx, miny, maxx, maxy) = bb
    return json.dumps(dict(
        minx=minx,
        miny=miny,
        maxx=maxx,
        maxy=maxy,
        x0=ly.x0,
        x1=ly.x1,
        y0=ly.y0,
        y1=ly.y1,
        height=ly.height,
        width=ly.width
        )
    )
    
    #~ if (maxx - minx) > ly.width/2 and (maxy - miny) > ly.height/2:
        #~ return "main_text"
    #~ elif ly.x1 - maxy < 10:
        #~ return "header"
    #~ elif miny - ly.x0  < 10:
        #~ return "footer"
    #~ else:
        #~ return "unknown"
        
'''
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_objs', 
'add', 'analyze', 'bbox', 'extend', 'get_text', 'get_writing_mode', 'hdistance', 'height', 'hoverlap', 'index', 'is_empty', 'is_hoverlap', 'is_voverlap', 'set_bbox', 'vdistance', 'voverlap', 'width', 'x0', 'x1', 'y0', 'y1']
'''

@attr.s
class TextBox():
    layout = attr.ib()
    tb = attr.ib()
    
    def __attrs_post_init__(self):
        (self.minx, self.miny, self.maxx, self.maxy) = self.tb.bbox
        self.text = self.tb.get_text()


@attr.s
class Page():
    layout = attr.ib()
    
    @property
    def page_no(self):
        return self.layout.pageid
        
    def text_boxes(self):
        for tb in [b for b in self.layout if isinstance(b, LTTextBox)]:
            yield TextBox(self.layout, tb)

def parse_pdf_document(pdf_source):
    with open(pdf_source, "rb") as infile:
        # Create parser object to parse the pdf content
        parser = PDFParser(infile)
        
        password = ""

        # Store the parsed content in PDFDocument object
        document = PDFDocument(parser, password)

        # Check if document is extractable, if not abort
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed
        
        # Create PDFResourceManager object that stores shared resources such as fonts or images
        rsrcmgr = PDFResourceManager()

        # set parameters for analysis
        laparams = LAParams()

        # Create a PDFDevice object which translates interpreted information into desired format
        # Device needs to be connected to resource manager to store shared resources
        device = PDFDevice(rsrcmgr)
        # Extract the decive to page aggregator to get LT object elements
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # Create interpreter object to process page content from PDFDocument
        # Interpreter needs to be connected to resource manager for shared resources and device 
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        
        # Ok now that we have everything to process a pdf document, lets process it page by page
       
        for seq, page in enumerate(PDFPage.create_pages(document)):
            #~ # As the interpreter processes the page stored in PDFDocument object
            interpreter.process_page(page)
            #~ # The device renders the layout from interpreter
            yield Page(device.get_result())
