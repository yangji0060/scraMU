# -*- Coding:UTF-8 -*-


import os
import requests
from pyquery import PyQuery as pq

from ConfigParser import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MUscrapy():

    def __init__(self):

        conf = ConfigParser()
        conf.read('conf.ini')
        self.url = 'http://www.mace.manchester.ac.uk'
        self.login_data = dict(conf.items('account'))
        self.headers = dict(conf.items('header'))
        self.ses = requests.session()

    def getPage(self):
        try:
            res = self.ses.get(url = self.url+'/people/staff/academic-staff/', headers = self.headers)
            return res.text.decode('utf-8')
        except requests.exceptions.RequestException:
            print 'open '+self.url+' error'

    def getGeneInfo(self,html):

        doc = pq(html)
        staff = []

        for data in doc('tr'):
            person = []
            for i in range(len(pq(data).find('td'))):
                person.append(pq(data).find('td').eq(i).text())
            person.append(pq(data).find('td').eq(0).find('a').attr('href'))
            person.append(pq(data).find('td').eq(4).find('a').attr('href'))

            if(len(person)!=0 and person[0]):
                staff.append(person)

        return staff

    def mkDir(self,path):
        path = path.strip()

        isPathexits = os.path.exists(path)

        if (not isPathexits):
            os.makedirs(path)
            return True
        else:
            print 'path'+'dir exists'
            return False

    def getPersonBio(self,url,name):
        try:
            res = self.ses.get(self.url+url+'&pg=1', headers = self.headers)
#           with open('personresearch.html','w') as f:
#               f.write(res.text)
            info = []
            doc = pq(res.text)
            for item in doc('div.researchstaffprofile-section').eq(1).find('p'):
                info.append(pq(item).text())
            return info
        except requests.exceptions.RequestException:
            print 'open '+name+' detail page error'



    def getPersonResearch(self,url,name):
        try:
            res = self.ses.get(self.url+url+'&pg=2', headers = self.headers)
#           with open('personresearch.html','w') as f:
#               f.write(res.text)
            info = []
            doc = pq(res.text)
            for item in doc('div.researchstaffprofile-section').eq(0).find('li'):
                info.append(pq(item).text())
            return info
        except requests.exceptions.RequestException:
            print 'open research '+name+' page error'

    def getPersonPub(self,url,name):
        try:
            res = self.ses.get(self.url + url + '&pg=4', headers=self.headers)
            #           with open('personresearch.html','w') as f:
            #               f.write(res.text)
            doc = pq(res.text)
            info = []
            for item in doc('div.researchstaffprofile-section').eq(0).find('li'):
                info.append(pq(item).text())

            return info
        except requests.exceptions.RequestException:
            print 'open '+name+'publication page error'


MU = MUscrapy()

mess = MU.getGeneInfo(MU.getPage())
with open('general.txt','w') as f:
    f.write('name'+'  role'+'  phone'+'  location'+'  email'+'\n')
    for item in mess:
        for i in range(len(item)-2):
            string = str(item[i])
            f.write(string+r'  ')
        f.write('\n')

savePath = 'professor info'
MU.mkDir(savePath)

# save information for all professors in MU engineering college
i = 0
print len(mess)
for item in mess:
    i += 1
    biography = MU.getPersonBio(item[5],item[0])
    research = MU.getPersonResearch(item[5],item[0])
    publication = MU.getPersonPub(item[5],item[0])

    filename = savePath+'/'+str(item[0])+'.txt'
    print 'saving ' +item[0]+' information'+ str(i)
    with open(filename,'w') as f:
        f.write('name' + '  role' + '  phone' + '  location' + '  email' + '\n')
        for i in range(len(item)-2):
            string = str(item[i])
            f.write(string+r'  ')

        f.write('\n')
        f.write('\n')

        f.write('BIOGRAPHY: \n')
        for part in biography:
            f.write(str(part)+'\n')
        f.write('\n')

        f.write('RESEARCH: \n')
        for part in research:
            f.write(str(part)+'\n')
        f.write('\n')

        f.write('PUBLICATION: \n')
        for part in publication:
            f.write(str(part)+'\n')
        f.write('\n')