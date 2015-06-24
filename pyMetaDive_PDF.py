import os,sys,argparse,time,re
from stat import *
from PyPDF2 import PdfFileReader

#command line inputs
parser = argparse.ArgumentParser(description='Process some input arguments.')
parser.add_argument('-f', '--file', type=str, help='filename to parse', required=True)
parser.add_argument('-g', '--GrabText', type=bool, help='extract text. Example -g True', default=False, required=False)
args = parser.parse_args()

# check if it's a file and exists
if not os.path.isfile(args.file): sys.exit()
if os.path.isdir(args.file): sys.exit()

fo = open(args.file, "rb")

# read the file header
head = fo.read(8)

# pdf header file type verification
if "%PDF" not in head:
        print "\nNot a supported document format."
        fo.close()
        sys.exit()

# print filename
print "File:\t\t%s" % args.file

# print pdf header
print "Header:\t\t%s" % head

#open the file for reading by PyPDf2		   
input1 = PdfFileReader(fo)

# check if encrypted
if input1.isEncrypted:
        print "Encrypted:\tEncrypted PDF"
        #i, o, e = select.select( [sys.stdin], [], [], 30 )
        #if(i):
        #        print "Provide password to decrypt PDF"
        #        pass = sys.stdin.readline().strip()
        #        input1.decrypt(pass)
        #else:
        #        print "timeout"
                
# get the primary document meta-data
meta = input1.getDocumentInfo()

#print number of pages
print "Pages:\t\t%s\n" % input1.getNumPages()

# iterate DocumentInfo()
print "Document info"
for (key, value) in meta.iteritems():
	if value:
		print re.sub("/","",key) + ":\t" , value.encode('utf-8')

print "\nXMP info"
#get the pdf xmp information if it exists
xmpinfo = input1.getXmpMetadata()

#print input1.getXmpMetadata()

if hasattr(xmpinfo,'dc_contributor'): print 'dc_contributor', xmpinfo.dc_contributor
if hasattr(xmpinfo,'dc_identifier'): print 'dc_identifier', xmpinfo.dc_identifier
if hasattr(xmpinfo,'dc_date'): print 'dc_date', xmpinfo.dc_date
if hasattr(xmpinfo,'dc_source'): print 'dc_source', xmpinfo.dc_source
if hasattr(xmpinfo,'dc_subject'): print 'dc_subject', xmpinfo.dc_subject	
if hasattr(xmpinfo,'xmp_modifyDate'): print 'xmp_modifyDate', xmpinfo.xmp_modifyDate
if hasattr(xmpinfo,'xmp_metadataDate'): print 'xmp_metadataDate', xmpinfo.xmp_metadataDate
if hasattr(xmpinfo,'xmpmm_documentId'): print 'xmpmm_documentId', xmpinfo.xmpmm_documentId
if hasattr(xmpinfo,'xmpmm_instanceId'): print 'xmpmm_instanceId', xmpinfo.xmpmm_instanceId
if hasattr(xmpinfo,'pdf_keywords'): print 'pdf_keywords', xmpinfo.pdf_keywords
if hasattr(xmpinfo,'pdf_pdfversion'): print 'pdf_pdfversion', xmpinfo.pdf_pdfversion

if hasattr(xmpinfo,'dc_publisher'):
	for y in xmpinfo.dc_publisher:
		if y:
			print "Publisher:\t" + y
#dc_title
#dc_relation

#list = xmpinfo.custom_properties
#print list

#filesystem mac times	
print "\nFilesystem mac times"

(mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(args.file)

# time.strftime("%d/%m/%Y %H:%M:%S",time.localtime(st.ST_CTIME))
print "Creation:\t%s" % time.ctime(ctime)
print "Last Mod:\t%s" % time.ctime(mtime)
print "Last Access:\t%s" % time.ctime(atime)
#print "Size:\t" % os.path.getsize(args.file)

if args.GrabText:
        #get the page text contents if we can
        content = ""
        # Iterate pages
        for i in range(0, input1.getNumPages()):
                # Extract text from page and add to content
                content += input1.getPage(i).extractText() + "\n"
        #content = " ".join(content.replace(u"\xa0", " ").strip().split())
        print content.encode("ascii", "ignore")


fo.close()
