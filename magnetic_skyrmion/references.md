In this file, list any sources you used to assist you with this coursework, including generative AI tools, such as ChatGPT.


Source 1:
https://stackoverflow.com/questions/66146156/can-i-avoid-a-looping-through-a-vector-for-the-same-operation-python

I used this forum after looking for a way to avoid looping through 2D arrays. I was trying to optimize the code for the zeeman and anisotropy methods of the systems module. I didn't use any information, but the first answer on this forum led me to source 2 after further research.

Source 2:
https://stackoverflow.com/questions/37142135/sum-numpy-ndarray-with-3d-array-along-a-given-axis-1

I used the information given in the last part of the first answer to help me implement the optimized versions of my zeeman and anisotropy methods. However, I did not copy anything verbatim and came up with most of the code myself.

```python
#Let A be the array, then in your example when the axis is 1, #[i,:,k] is added. Likewise, for axis 0, [:,j,k] are added #and when axis is 2, [i,j,:] are added.

A = np.array([
   [[ 1,  2,  3],[ 4,  5,  6], [12, 34, 90]],
   [[ 4,  5,  6],[ 2,  5,  6], [ 7,  3,  4]]
])

np.sum(A,axis = 2)
    array([[ 6, 15,136],
           [15, 13, 14]])
```


Source 3:
https://stackoverflow.com/questions/28010860/slicing-3d-numpy-arrays
I used this stackoverflow forum to learn how to efficiently implement the mean method of the spins module. My thinking was that you can extract the x,y and z components of the (nx,ny,3) array directly and do not need to loop. I used the information given in the first part of the first answer. Note: I also used this knowledge afterwards for my plotting fucntion.
```python

In [233]: B = np.arange(2*3*4).reshape((2,3,4))
array([[[ 0,  1,  2,  3],
        [ 4,  5,  6,  7],       <-- first (3,4) array
        [ 8,  9, 10, 11]],

       [[12, 13, 14, 15],
        [16, 17, 18, 19],      <-- second (3,4) array
        [20, 21, 22, 23]]])
for i in range(4):
  print(B[:,:,i])

        # [[ 0  4  8]
        #  [12 16 20]]
        # [[ 1  5  9]
        #  [13 17 21]]
        # [[ 2  6 10]
        #  [14 18 22]]
        # [[ 3  7 11]
        #  [15 19 23]]
```

Source 4:
https://krajit.github.io/sympy/vectorFields/vectorFields.html

I used these code snippets for my plotting. However, I modified the first line of code to make it work for my case and did not copy it exactly.

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

x,y = np.meshgrid(np.linspace(-5,5,10),np.linspace(-5,5,10))

u = 1
v = -1

plt.quiver(x,y,u,v)
plt.show()
```


Source 5:
https://matplotlib.org/stable/gallery/images_contours_and_fields/quiver_demo.html#sphx-glr-gallery-images-contours-and-fields-quiver-demo-py
I specifically looked at the last plot, which is colored. I used the code np.hypot() to effectively calculate the magnitude of the spin vectors and to make the spin vectors on my plot colored. I also adapted the plt.quiver in my line accordingly.

```python
Q = ax3.quiver(X, Y, U, V, M, units='x', pivot='tip', width=0.022,
               scale=1 / 0.15)
```
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html
I used this documentation to help me understand what was going on in the code

Source 6:

https://www.geeksforgeeks.org/matplotlib-pyplot-colorbar-function-in-python/

I used the first code example to add the colorbar
```python
plt.colorbar(label="Like/Dislike Ratio", orientation="horizontal")
```


Source 7:
https://realpython.com/copying-python-objects/#:~:text=Making%20a%20shallow%20copy%20of,a%20deep%20copy%20is%20slower.

I used the "Making Shallow Copied" and "Making Deep Copies" section of this to learn the differences between deep copies and shallow copies.

Source 8:
https://www.w3resource.com/numpy/array-creation/copy.php

I used the first source to learn how to make a deep copy using numpy as I tried to avoid importing modules other than numpy.

Source 9:

https://sparkbyexamples.com/numpy/numpy-norm-of-vector/
```python
# Example 2: Get the linalg.norm() with 1-D array
arr = np.array([2, 4, 6, 8, 10, 12, 14])
arr2 = np.linalg.norm(arr)
```

Used this example to calculate the norm more efficiently.
