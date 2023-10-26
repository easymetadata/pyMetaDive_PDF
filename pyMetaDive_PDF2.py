import os
import sys
import argparse
import time
import re
from PyPDF2 import PdfReader

#Version 2 - Conversion to Python 3 from Python 2. Update function calls to latest pyPDF2.

# Command line inputs
parser = argparse.ArgumentParser(description='Process some input arguments.')
parser.add_argument('-f', '--file', type=str, help='filename to parse', required=True)
parser.add_argument('-g', '--GrabText', type=bool, help='extract text. Example -g True', default=False, required=False)
args = parser.parse_args()

# Check if it's a file and exists
if not os.path.isfile(args.file):
    sys.exit()
if os.path.isdir(args.file):
    sys.exit()

fo = open(args.file, "rb")

# Read the file header
head = fo.read(8)

# PDF header file type verification
if b"%PDF" not in head:
    print("\nNot a supported document format.")
    fo.close()
    sys.exit()

# Print filename
print("File:\t\t%s" % args.file)

# Print PDF header
print("Header:\t\t%s" % head)

# Open the file for reading by PyPDF2
input1 = PdfReader(fo)

# Check if encrypted
if input1.is_encrypted:
    print("Encrypted:\tEncrypted PDF")

# Get the primary document meta-data
meta = input1.metadata

# Print number of pages
print("Pages:\t\t%s\n" % len(input1.pages))

# Iterate DocumentInfo()
print("Document info")
for key, value in meta.items():
    if value:
        print(re.sub("/", "", key) + ":\t", value.encode('utf-8'))

print("\nXMP info")
# Get the PDF XMP information if it exists
xmpinfo = input1.xmp_metadata

# Print input1.getXmpMetadata()
if hasattr(xmpinfo, 'dc_contributor'):
    print('dc_contributor', xmpinfo.dc_contributor)
if hasattr(xmpinfo, 'dc_identifier'):
    print('dc_identifier', xmpinfo.dc_identifier)
if hasattr(xmpinfo, 'dc_date'):
    print('dc_date', xmpinfo.dc_date)
if hasattr(xmpinfo, 'dc_source'):
    print('dc_source', xmpinfo.dc_source)
if hasattr(xmpinfo, 'dc_subject'):
    print('dc_subject', xmpinfo.dc_subject)
if hasattr(xmpinfo, 'xmp_modifyDate'):
    print('xmp_modifyDate', xmpinfo.xmp_modifyDate)
if hasattr(xmpinfo, 'xmp_metadataDate'):
    print('xmp_metadataDate', xmpinfo.xmp_metadataDate)
if hasattr(xmpinfo, 'xmpmm_documentId'):
    print('xmpmm_documentId', xmpinfo.xmpmm_documentId)
if hasattr(xmpinfo, 'xmpmm_instanceId'):
    print('xmpmm_instanceId', xmpinfo.xmpmm_instanceId)
if hasattr(xmpinfo, 'pdf_keywords'):
    print('pdf_keywords', xmpinfo.pdf_keywords)
if hasattr(xmpinfo, 'pdf_pdfversion'):
    print('pdf_pdfversion', xmpinfo.pdf_pdfversion)

if hasattr(xmpinfo, 'dc_publisher'):
    for y in xmpinfo.dc_publisher:
        if y:
            print("Publisher:\t" + y)

# Filesystem mac times
print("\nFilesystem mac times")

(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(args.file)

# time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(st.ST_CTIME))
print("Creation:\t%s" % time.ctime(ctime))
print("Last Mod:\t%s" % time.ctime(mtime))
print("Last Access:\t%s" % time.ctime(atime))
# print "Size:\t" % os.path.getsize(args.file)

if args.GrabText:
    # Get the page text contents if we can
    content = ""
    # Iterate pages
    for i in range(0, input1.getNumPages()):
        # Extract text from page and add to content
        content += input1.getPage(i).extractText() + "\n"
    # content = " ".join(content.replace(u"\xa0", " ").strip().split())
    print(content.encode("ascii", "ignore"))

fo.close()
