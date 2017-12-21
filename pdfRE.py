#!/usr/bin/python
#encoding=utf-8

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import *
from pdfminer.converter import PDFPageAggregator
import os
import re

'''
获取path路径下的所有pdf名称
'''
def getFileName():
    path="/home/wxw/py_program/pdfs/"
    fileNames = [] 
    for root, dirs, files in os.walk(path):  
        for filespath in files: 
            fileNames.append(os.path.join(root,filespath)) 
    return fileNames

'''
获取fileName这一pdf文件中的全部文本内容
'''
def getContentFromPDF(fileName):
    content=''
    # 打开pdf文件
    fp = open(fileName, 'rb')
    #创建一个和文件对象相关联的PDFParser文档解析器对象 
    parser = PDFParser(fp)
    # 创建一个PDFDocument文档对象用于保存文档结构，参数中password提供初始化密码，如果没有可以不提供
    document = PDFDocument(parser)
    # 检查文档是否允许文本提取
    if not document.is_extractable:
        #如果不允许则放弃，引发PDFTextExtractionNotAllowed异常
        raise PDFTextExtractionNotAllowed
    #创建PDFResourceManager资源管理器对象用于保存共享资源
    rsrcmgr = PDFResourceManager()
    # 设定参数进行分析
    laparams=LAParams()
    #创建一个PDFDevice设备对象，参数为资源管理器对象
    #device = PDFDevice(rsrcmgr)
    device = PDFPageAggregator(rsrcmgr,laparams=laparams)
    #创建一个PDFInterpreter解析器对象，参数为资源管理器对象和设备对象
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # 处理文档中的每一个页面
    for page in PDFPage.create_pages(document):
        #用解析器进行解析
        interpreter.process_page(page)
        # 接受该页面的LTPage对象
        layout=device.get_result()
        for x in layout:
            if(isinstance(x,LTTextBoxHorizontal)):
                content=content+x.get_text().encode('utf-8')
    return content

'''
利用正则匹配content中的IP，有IP返回True
'''
def lookForIP(content):
    patternIP='(?:(?:25[0-5]|2[0-4]\d|(?:(?:1\d{2})|(?:[1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|(?:(?:1\d{2})|(?:[1-9]?\d)))'
    m = re.findall(patternIP,content)
    print 'IP'
    if m:
        #去重
        IPs=list(set(m))
        #输出匹配结果
        print IPs
        return True
    else:
        return False

'''
利用正则匹配content中的SHA-1，有SHA-1返回True
'''        
def lookForSHA1(content):
    patternSHA1='(?<=[\n^\r\s])[a-zA-Z0-9]{40}(?=[\n$\r\s])'
    m = re.findall(patternSHA1,content)
    print 'SHA-1'
    if m:
        #去重
        SHA1=list(set(m))
        #输出匹配结果
        print SHA1
        return True
    else:
        return False

'''
利用正则匹配content中的MD5，有MD5返回True
'''
def lookForMD5(content):
    patternMD5='(?<=[\n^\r\s])[a-zA-Z0-9]{32}(?=[\n$\r\s])'
    m = re.findall(patternMD5,content)
    print 'md5'
    if m:
        #去重
        MD5=list(set(m))
        #输出匹配结果
        print MD5
        return True
    else:
        return False

'''
没啥用
'''
def inBlackList(URL):
    blackList=['U.S','SystemTime.wDay','ystemtime.wMonth','SystemTime.wYear']
    #旧的黑名单
    #blackList=['U.S','SystemTime.wDay','ystemtime.wMonth','SystemTime.wYear','microsoft.com','yahoo.com', 'google.com','163.com','Mail.ru','126.com','Mail.com','127.0.0.1','1.1.1.1','1.0.0.1']
    if URL in blackList:
        return True
    else:
        return False

'''
利用正则匹配content中的url，有url返回True
'''
def lookForURL(content):
    ''' patternURL=re.compile(r'(?<=[\n^\r\s])(?:(?:(?:ht|f)tp(?:s?))\://)?(?:www\.)?(?:(?:(?:(?:25[0-5]|2[0-4]\d|(?:(?:1\d{2})|(?:[1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|(?:(?:1\d{2})|(?:[1-9]?\d))))|[a-zA-Z0-9\-]+(?:\.(?!exe|tmp|Adobe|log|cvr|CF|AD|CC|AA|AG|microsoft|dat|AH|CL|pdf|sys|gif|bat|dll|shp|hlp|doc|docx|vbs|txt)(?:(?:\d+[a-zA-Z]+[a-zA-Z0-9\-]*)|[a-zA-Z]+[a-zA-Z0-9\-]*)){1,5})(?:\:[0-9]+)*(?:/[a-zA-Z0-9\.\;\?\'\\\+&amp;%\$#\=~_\-]+)*(?=[\n$\r\s])',re.I)
    '''
    #正则，纯url的不会被捕获 #patternURL=re.compile(r'(?<=[\n^\r\s])(?:(?:(?:ht|f)tp(?:s?))\://)?(?:www\.)?(?:(?:(?:(?:(?:25[0-5]|2[0-4]\d|(?:(?:1\d{2})|(?:[1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|(?:(?:1\d{2})|(?:[1-9]?\d))))(?:\:[0-9]+)*(?:/[a-zA-Z0-9\.\;\?\'\\\+&amp;%\$#\=~_\-]+)+)|(?:[a-zA-Z0-9\-]+(?:\.(?!exe|tmp|Adobe|log|cvr|CF|AD|CC|AA|AG|microsoft|dat|AH|CL|pdf|sys|gif|bat|dll|shp|hlp|doc|docx|vbs|txt)(?:(?:\d+[a-zA-Z]+[a-zA-Z0-9\-]*)|[a-zA-Z]+[a-zA-Z0-9\-]*)){1,5}(?:\:[0-9]+)*(?:/[a-zA-Z0-9\.\;\?\'\\\+&amp;%\$#\=~_\-]+)*))(?=[\n$\r\s])',re.I)
    
    #正则，纯url的也会被捕获
    patternURL=re.compile(r'(?<=[\n^\r\s])(?:(?:(?:ht|f)tp(?:s?))\://)?(?:www\.)?(?:(?:(?:(?:(?:25[0-5]|2[0-4]\d|(?:(?:1\d{2})|(?:[1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|(?:(?:1\d{2})|(?:[1-9]?\d))))(?:\:[0-9]+)*(?:/[a-zA-Z0-9\;\?\'\\\+&amp;%\$#\=~_\-]+)*)|(?:[a-zA-Z0-9\-]+(?:\.(?!exe|tmp|Adobe|log|cvr|CF|AD|CC|AA|AG|microsoft|dat|AH|CL|pdf|sys|gif|bat|dll|shp|hlp|doc|docx|vbs|txt)(?:(?:\d+[a-zA-Z]+[a-zA-Z0-9\-]*)|[a-zA-Z]+[a-zA-Z0-9\-]*)){1,5}(?:\:[0-9]+)*(?:/[a-zA-Z0-9\.\;\?\'\\\+&amp;%\$#\=~_\-]+)*))(?=[\n$\r\s])',re.I)
    m=patternURL.findall(content)
    print 'url'
    
    if m== False:
        return False
    #去重
    URLs=list(set(m))
    #利用黑名单再次清洗
    for one in URLs:
        whetherIn=inBlackList(one)
        if whetherIn==True:
            URLs.remove(one)
    print URLs
    return True
            

if __name__ == "__main__":
    #获得指定路径下的全部pdf
    fileNames=getFileName()
    #处理每一个pdf
    for fileName in fileNames:
        print "=============================================================================="
        print fileName
        #获得pdf的文本内容
        content=getContentFromPDF(fileName)
        #查IP
        IPresult=lookForIP(content)
        #查SHA1
        SHA1result=lookForSHA1(content)
        #查MD5
        MD5result=lookForMD5(content)
        #查url
        URLresult=lookForURL(content)
    
    
    
    
    
    
    
    
