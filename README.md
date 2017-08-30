# python-image-downloader
Clase para descargar imágenes de Google Images (también de otros sitios)


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
