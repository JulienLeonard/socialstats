from distimport import *
faa_stats = distimport("../lib",'faa_stats')
from mysocialids import *

faa_stats.faa_dump(faa_username(),faa_password(),faa_profile(),"faa_stats.xml")



