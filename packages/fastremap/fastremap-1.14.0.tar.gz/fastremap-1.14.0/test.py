import fastremap
import numpy as np 
import time

image = np.ones((512,512,512), dtype=np.uint8, order="F")

cs = 128

s = time.time()
res = fastremap.tobytes(image, (cs,cs,cs))
print(time.time() - s)

s = time.time()
for z in range(4):
	for y in range(4):
		for x in range(4):
			cutout = image[x*cs:(x+1)*cs, y*cs:(y+1)*cs, z*cs:(z+1)*cs]
			cutout.tobytes("F")
print(time.time() - s)

s = time.time()
image.tobytes("F")
print(time.time() - s)

s = time.time()
image = fastremap.asfortranarray(image)
print(image.flags)
image.tobytes("F")
print(time.time() - s)


# x = fastremap.asfortranarray(x)
# print(x)
# print(x.flags)
# print(x.strides)

# print(x.dtype)



# # @profile
# # def run():
# #   x = np.ones( (512,512,512), dtype=np.uint32, order='C')
# #   x += 1
# #   print(x.strides, x.flags)
# #   y = np.asfortranarray(x)
# #   print(x.strides, x.flags)

# #   print("done.")

# # run()