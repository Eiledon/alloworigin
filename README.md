# [alloworigin.com](http://alloworigin.com)
Django implementation of anyorigin.com    
Uses Django, [requests lib](http://docs.python-requests.org/en/latest/) and [tor](https://www.torproject.org/)

**what is the difference between anyorigin.com and alloworigin.com?**  
Well, while alloworigin.com is open source and free to use,  
anyorigin.com is closed source and not free.

**whateverorigin.org is open source and free, why use alloworigin.com?**  
whateverorigin.org is a good alternative to anyorigin.com, but  
it has not been maintained well, thus some basic functions remain [broken](https://github.com/ripper234/Whatever-Origin/issues/10)  
alloworigin.com is an attempt to fix this.  
alloworigin.com is written in Django,  
so all of the Django community can participate in alloworigin.com

**features**  
1. anonymous get request using tor   
2. reduce change of getting banned from a site using tor  
3. compress content using zlib [coming soon]  
4. write tests [coming soon]

**usage**  
basic usage  
http://alloworigin.com/get?url=http://example.com
  
with callback  
http://alloworigin.com/get?url=http://example.com&callback=foo

anonymous request using tor, with callback   
http://alloworigin.com/get?url=http://example.com&callback=foo&tor=1

***alloworigin.com may be unstable at the moment as it is on a test server***
