import cv2 
import click
from PIL import Image

from time import sleep
#RSA

# STEP 1: Generate Two Large Prime Numbers (p,q) randomly
from random import randrange, getrandbits
from tkinter import *
  
# import filedialog module
from tkinter import filedialog
flg=0;

# Function for opening the
# file explorer window
def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Image files",
                                                        "*.jpg*"),
                                                       ("all files",
                                                        "*.*")))
    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)
    global signatureImage
    signatureImage = filename
def browseFiles1():
    filename1 = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Image files",
                                                        "*.jpg*"),
                                                       ("all files",
                                                        "*.*")))
      
       
    label_file_explorer1.configure(text="File Opened: "+filename1)
    global colorImage
    colorImage = filename1



def start():
    from tkinter.ttk import Progressbar
    from tkinter import ttk
    import cv2
    import click
    from PIL import Image

        
    def merge(img1, img2, output):
        merged_image = Steganography.merge(Image.open(img1), Image.open(img2))
        merged_image.save(output)


    #@cli.command()
    #@click.option('--img', required=True, type=str, help='Image that will be hidden')
    #@click.option('--output', required=True, type=str, help='Output image')

    def unmerge(img, output):
        unmerged_image = Steganography.unmerge(Image.open(img))
        unmerged_image.save(output)
    flg=1
    #print("Clicked")
    def power(a,d,n):
      ans=1;
      while d!=0:
        if d%2==1:
          ans=((ans%n)*(a%n))%n
        a=((a%n)*(a%n))%n
        d>>=1
      return ans;


    def MillerRabin(N,d):
      a = randrange(2, N - 1)
      x=power(a,d,N);
      if x==1 or x==N-1:
        return True;
      else:
        while(d!=N-1):
          x=((x%N)*(x%N))%N;
          if x==1:
            return False;
          if x==N-1:
            return True;
          d<<=1;
      return False;


    def is_prime(N,K):
      if N==3 or N==2:
        return True;
      if N<=1 or N%2==0:
        return False;
      
      #Find d such that d*(2^r)=X-1
      d=N-1
      while d%2!=0:
        d/=2;

      for _ in range(K):
        if not MillerRabin(N,d):
          return False;
      return True;  
      



    def generate_prime_candidate(length):
      # generate random bits
      p = getrandbits(length)
      # apply a mask to set MSB and LSB to 1
      # Set MSB to 1 to make sure we have a Number of 1024 bits.
      # Set LSB to 1 to make sure we get a Odd Number.
      p |= (1 << length - 1) | 1
      return p



    def generatePrimeNumber(length):
      A=4
      while not is_prime(A, 128):
            A = generate_prime_candidate(length)
      return A



    #Step 3: Find E such that GCD(E,eulerTotient)=1(i.e., e should be co-prime) such that it satisfies this condition:-  1<E<eulerTotient

    def GCD(a,b):
      if a==0:
        return b;
      return GCD(b%a,a)



    # Step 4: Find D. 
    #For Finding D: It must satisfies this property:-  (D*E)Mod(eulerTotient)=1;
    #Now we have two Choices
    # 1. That we randomly choose D and check which condition is satisfying above condition.
    # 2. For Finding D we can Use Extended Euclidean Algorithm: ax+by=1 i.e., eulerTotient(x)+E(y)=GCD(eulerTotient,e)
    #Here, Best approach is to go for option 2.( Extended Euclidean Algorithm.)

    def gcdExtended(E,eulerTotient):
      a1,a2,b1,b2,d1,d2=1,0,0,1,eulerTotient,E

      while d2!=1:

        # k
        k=(d1//d2)

        #a
        temp=a2
        a2=a1-(a2*k)
        a1=temp

        #b
        temp=b2
        b2=b1-(b2*k)
        b1=temp

        #d
        temp=d2
        d2=d1-(d2*k)
        d1=temp

        D=b2

      if D>eulerTotient:
        D=D%eulerTotient
      elif D<0:
        D=D+eulerTotient

      return D

    from tensorflow.keras.preprocessing import image
    class Steganography(object):

        @staticmethod
        def __int_to_bin(rgb):
            """Convert an integer tuple to a binary (string) tuple.

            :param rgb: An integer tuple (e.g. (220, 110, 96))
            :return: A string tuple (e.g. ("00101010", "11101011", "00010110"))
            """
            r, g, b = rgb
            return ('{0:08b}'.format(r),
                    '{0:08b}'.format(g),
                    '{0:08b}'.format(b))

        @staticmethod
        def __bin_to_int(rgb):
            """Convert a binary (string) tuple to an integer tuple.

            :param rgb: A string tuple (e.g. ("00101010", "11101011", "00010110"))
            :return: Return an int tuple (e.g. (220, 110, 96))
            """
            r, g, b = rgb
            return (int(r, 2),
                    int(g, 2),
                    int(b, 2))

        @staticmethod
        def __merge_rgb(rgb1, rgb2):
            """Merge two RGB tuples.

            :param rgb1: A string tuple (e.g. ("00101010", "11101011", "00010110"))
            :param rgb2: Another string tuple
            (e.g. ("00101010", "11101011", "00010110"))
            :return: An integer tuple with the two RGB values merged.
            """
            r1, g1, b1 = rgb1
            r2, g2, b2 = rgb2
            rgb = (r1[:4] + r2[:4],
                   g1[:4] + g2[:4],
                   b1[:4] + b2[:4])
            return rgb

        @staticmethod
        def merge(img1, img2):
            """Merge two images. The second one will be merged into the first one.

            :param img1: First image
            :param img2: Second image
            :return: A new merged image.
            """

            # Check the images dimensions
            if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1]:
                raise ValueError('Image 2 should not be larger than Image 1!')

            # Get the pixel map of the two images
            pixel_map1 = img1.load()
            pixel_map2 = img2.load()

            # Create a new image that will be outputted
            new_image = Image.new(img1.mode, img1.size)
            pixels_new = new_image.load()

            for i in range(img1.size[0]):
                for j in range(img1.size[1]):
                    rgb1 = Steganography.__int_to_bin(pixel_map1[i, j])

                    # Use a black pixel as default
                    rgb2 = Steganography.__int_to_bin((0, 0, 0))

                    # Check if the pixel map position is valid for the second image
                    if i < img2.size[0] and j < img2.size[1]:
                        rgb2 = Steganography.__int_to_bin(pixel_map2[i, j])

                    # Merge the two pixels and convert it to a integer tuple
                    rgb = Steganography.__merge_rgb(rgb1, rgb2)

                    pixels_new[i, j] = Steganography.__bin_to_int(rgb)

            return new_image

        @staticmethod
        def unmerge(img):
            """Unmerge an image.

            :param img: The input image.
            :return: The unmerged/extracted image.
            """

            # Load the pixel map
            pixel_map = img.load()

            # Create the new image and load the pixel map
            new_image = Image.new(img.mode, img.size)
            pixels_new = new_image.load()

            # Tuple used to store the image original size
            original_size = img.size

            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    # Get the RGB (as a string tuple) from the current pixel
                    r, g, b = Steganography.__int_to_bin(pixel_map[i, j])

                    # Extract the last 4 bits (corresponding to the hidden image)
                    # Concatenate 4 zero bits because we are working with 8 bit
                    rgb = (r[4:] + '0000',
                           g[4:] + '0000',
                           b[4:] + '0000')

                    # Convert it to an integer tuple
                    pixels_new[i, j] = Steganography.__bin_to_int(rgb)

                    # If this is a 'valid' position, store it
                    # as the last valid position
                    if pixels_new[i, j] != (0, 0, 0):
                        original_size = (i + 1, j + 1)

            # Crop the image based on the 'valid' pixels
            new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

            return new_image


    @click.group()
    def cli():
        pass


    #@cli.command()
    #@click.option('--img1', required=True, type=str, help='Image that will hide another image')
    #@click.option('--img2', required=True, type=str, help='Image that will be hidden')
    #@click.option('--output', required=True, type=str, help='Output image')


    if(flg==1):
        print("Process started")
        length=5
        P=generatePrimeNumber(length)
        Q=generatePrimeNumber(length)

        print("P: " + str(P))
        print("Q: " + str(Q))



        #Step 2: Calculate N=P*Q and Euler Totient Function = (P-1)*(Q-1)
        N=P*Q
        eulerTotient=(P-1)*(Q-1)
        print("N: " + str(N))
        print("eulerTotient: " + str(eulerTotient))


        E=generatePrimeNumber(4)
        while GCD(E,eulerTotient)!=1:
          E=generatePrimeNumber(4)
        print("E: " + str(E))



        D=gcdExtended(E,eulerTotient)
        print("D: " + str(D))


        print("Public key announcement by User A")
        print("Public Key = {"+str(E)+","+str(N)+"}")
        print("User B merging Signature Image and Normal Image")
        print("Signature Image: " + str(signatureImage))
        print("Signature Image: " + str(colorImage))
        img1 = colorImage   
        img2 = signatureImage 
        output1 = "UserB/merged_image.png"
        print("Image received")
        sig = cv2.imread(img2)
        nor = cv2.imread(img1)

        # cv2.imshow("Signature Image", sig)
        # cv2.waitKey(2)
        # cv2.imshow("Normal Image", nor)
        # cv2.waitKey(2)
        print("Merge Started")
       
        merge(img1,img2,output1)
            
        my_img = cv2.imread('UserB/merged_image.png')
        print(my_img.shape)
        row,col=my_img.shape[0],my_img.shape[1]
        enc = [[0 for x in range(3000)] for y in range(3000)]
             
        # cv2.imshow("Signature Image Merged with Normal Image", my_img)
        cv2.waitKey(2)
        
        #Step 5: Encryption
        print("Encryption Started for Merged Image")
        for i in range(10,row):#200,700
          for j in range(10,col):#200,1000
            r,g,b=my_img[i,j]
            C1=power(r,E,N)
            C2=power(g,E,N)
            C3=power(b,E,N)
            enc[i][j]=[C1,C2,C3]
            C1=C1%256
            C2=C2%256
            C3=C3%256
            my_img[i,j]=[C1,C2,C3]

        print("Encryption completed")

        cv2.imwrite('UserB/encrypted_image.png',my_img)
        cv2.imwrite('UserA/encrypted_image_received.png',my_img)
        # cv2.imshow("Encrypted Image Using RSA Algorithm",my_img)
        cv2.waitKey(2)
        
        print("User A received Encrypted Image, and Decryption started by using Private Key")
        print("Secret Private Key = {"+str(D)+","+str(N)+"}")
        #Step 6: Decryption
        for i in range(10,row):
          for j in range(10,col):
            r,g,b=enc[i][j]
            M1=power(r,D,N)
            M2=power(g,D,N)
            M3=power(b,D,N)
            my_img[i,j]=[M1,M2,M3]
        print("decryption completed")
        cv2.imwrite('UserA/decrypted.png',my_img)
        # cv2.imshow("Decrypted Image",my_img)
        cv2.waitKey(2)
        
        img = 'UserA/decrypted.png'
        output2 = 'UserA/unmerged_signature_image.png'
        print("Unmerge Started")
        unmerge(img,output2)
        print("Unmerge completed")
        # sleep(4)
        # my_img2 = cv2.imread('UserA/unmerged_signature_image.png')
        # cv2.imshow("Decrypted Signature Image",my_img2)
        cv2.waitKey(2)
        print("Process Completed Successfully.")
        
if __name__ == '__main__':
    window = Tk()
  
    # Set window title
    window.title('Signature Image Hiding using Stegnography and Cryptography')
      
    # Set window size
    window.geometry("700x400")
      
    #Set window background color
    window.config(background = "white")
      
    # Create a File Explorer label
    label_file_explorer = Label(window,
                                text = "Please upload signature image",
                                width = 100, height = 4,
                                fg = "blue")
    label_file_explorer1 = Label(window,
                                text = "Please upload normal image",
                                width = 100, height = 4,
                                fg = "blue")
    button_explore = Button(window,
                            text = "Browse Signature Image",
                            command = browseFiles)
    button_explore1 = Button(window,
                            text = "Browse Color Image",
                            command = browseFiles1)
    button_start = Button(window,
                         text = "Start Process",
                         command = start)
    # button_exit = Button(window,
    #                    text = "exit",
    #                    command = exit)  
       
    # Grid method is chosen for placing
    # the widgets at respective positions
    # in a table like structure by
    # specifying rows and columns
    label_file_explorer.grid(column = 1, row = 1, padx=5, pady=5)
    button_explore.grid(column = 1, row = 3, padx=5, pady=5)
    label_file_explorer1.grid(column = 1, row = 5, padx=5, pady=5)
    button_explore1.grid(column = 1, row = 7, padx=5, pady=5)
    
    button_start.grid(column = 1,row = 9, padx=5, pady=5)
    # button_exit.grid(column = 1,row = 12, padx=5, pady=5)
      
    # Let the window wait for any events
    
    
    window.mainloop()


    

