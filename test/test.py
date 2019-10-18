import xml.etree.ElementTree as et
import re
root = et.parse('../res/KB.xml').getroot()

f = open("test.txt","w+", encoding='utf-8')
f2 = open("testSolutions.txt","w+", encoding='utf-8')
i = 1
for type_tag in root.findall('documento/faq_list/faq/perguntas'):
    pergunta = type_tag.find('pergunta')
    temp = pergunta.text
    temp = re.sub("[ ]*\n[ ]*", ' ', temp)
    re.sub(u"\n", ' ', pergunta.text)
    f.write( temp + "\n")
    f2.write(str(i) + "\n")
    i+=1
    type_tag.remove(pergunta)


f.close()
f2.close()
tree = et.ElementTree(root)
tree.write("KBTest.xml", encoding='utf-8')