import sys
sys.path.insert(0, './../lib')

import wordpress_stats
from mysocialids import *

wordpress_stats.wordpress_dump(wordpress_blogid(),"wordpress_stats.xml")




