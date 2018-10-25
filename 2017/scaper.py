# -*- coding: utf-8 -*-

### URL format:
# https://dl.acm.org/tab_about.cfm?id=3173574&type=proceeding&parent_id=3173574&parent_type=proceeding&title=Proceedings%20of%20the%202017%20CHI%20Conference%20on%20Human%20Factors%20in%20Computing%20Systems&toctitle=CHI%20Conference%20on%20Human%20Factors%20in%20Computing%20Systems&tocissue_date=&notoc=0&usebody=tabbody&tocnext_id=&tocnext_str=&tocprev_id=&tocprev_str=&toctype=conference

from BeautifulSoup import BeautifulSoup
import re

f = open("2017-04-01-chi2017papers.md.txt","r")
lines = f.readlines()
f.close()

toc = open("tab_about.cfm.html","r").read()
soup = BeautifulSoup(toc)

out = ""
tflag = 0

for line in lines:
    if line == "- authors:\n" and tflag == 1:
        out += "  doiurl: %s\n"%url
        out += line
        tflag = 0
    else:
        try:
            out += line.decode('utf-8')
        except:
            print line
    if line[:7] == "  title":
        t=line[9:].strip("\n").strip("'")
        st = t.replace("''","'").replace("&","&#38;")
        st = st.decode('utf-8').replace("é".decode('utf-8'),'&#233;').encode('utf-8')
        res = soup.findAll(text=re.compile('^'+st+'.*',re.IGNORECASE))
        if len(res) == 0:
            ### This will print the ones that fail to match. In most cases it is:
            ###     1) The title has changed between the sheridan data and the confer data
            ###     2) The title has some special character
            ###     3) A TOCHI or other paper
            print st
        else:
            ## okay, there's a match
            tflag = 1
            tr = res[0].parent.parent.parent.parent
            nexttr = tr.findNext("tr").findNext("tr").findNext("tr")
            a = nexttr.find("a")
            url = a['href']
            
f = open("newpost.txt","w")
f.write(out.encode('utf-8'))
f.close()