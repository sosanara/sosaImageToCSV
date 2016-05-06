from ImageConverter import ImageToCSV

itc = ImageToCSV(200, "img1/")
itc.set_training_data()
itc.save_reduce_image_to_csv('data')
