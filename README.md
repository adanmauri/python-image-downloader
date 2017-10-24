# What is Python Image Downloader?
Python Image Downloader is a library to download images from Google Images (other sites also)

```python
from image_downloader import *

id = ImageDownlaoder()
id.get_images('query', dump=True, q=10)

# Also:
id.get_jpeg('query', dump=True, q=10)
id.get_png('query', dump=True, q=10)
id.get_gif('query', dump=True, q=10)
```

TODO
====

* Documentation
* Refactoring
* Python 3 fixes
