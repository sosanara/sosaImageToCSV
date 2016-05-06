from ImageConverter import ImageToCSV

itc = ImageToCSV(886, "img1/")
itc.set_training_data()
itc.save_reduce_image_to_csv('data')

print "type0: " + str(itc.type0)
print "type1: " + str(itc.type1)
print "type2: " + str(itc.type2)
print "type3: " + str(itc.type3)
print "type4: " + str(itc.type4)
