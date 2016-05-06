# sosaImageToCSV
image converter (img to csv)


#### Feature
- 확장자png 고정

#### Usage
- example: testImageConverter.py

```python
from ImageConverter import ImageToCSV

itc = ImageToCSV(200, "img1/")
itc.set_training_data()
itc.reduce_image_size('data')
```