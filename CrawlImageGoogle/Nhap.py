import urllib.request
from urllib.parse import quote
import os

# link = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Th%C3%A1p_R%C3%B9a_3.jpg/1200px-Th%C3%A1p_R%C3%B9a_3.jpg"
link = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Tháp_Rùa_3.jpg/1200px-Tháp_Rùa_3.jpg"
lst = list(urllib.parse.urlsplit(link))
print(lst)
temp = [quote(elm) for elm in lst]
temp = urllib.parse.urlunsplit(temp)
print("temp = ", temp)
name = link.split("/")[-1]
data = urllib.request.urlopen(temp).read()
print(os.path.abspath(name))
f = open("./Data/" + name, mode="wb")
f.write(data)
f.close()