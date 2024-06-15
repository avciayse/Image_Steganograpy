import os
import tkinter.filedialog
from io import BytesIO
from tkinter import *
from tkinter import messagebox, ttk, scrolledtext

import cv2
import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageTk


class Veri_gomme:
    output_image_size = 0

    def main(self, root):
        root.title('Steganografi')
        root.geometry('960x536')
        root.resizable(width=False, height=False)
        root.configure(bg='grey')

        frame = Frame(root, bg="cyan")
        frame.grid()

        title = Label(frame, text='LSB Steganografisi')
        title.config(font=('Times new roman', 25, 'bold'))
        title.grid(pady=5)
        title.config(bg='#5e5e5e')
        title.grid(row=1)

        encode = ttk.Button(frame, text="Şifrele", command=lambda: self.encode_frame1(frame))
        encode.config(style='Accent.TButton')
        encode.grid(pady=5, row=2)

        decode = ttk.Button(frame, text="Şifre Çöz", command=lambda: self.decode_frame1(frame))
        decode.config(style='Accent.TButton')
        decode.grid(pady=5, row=3)

        analyze = ttk.Button(frame, text="Histogram Analizi", command=self.analyze_images)
        analyze.config(style='Accent.TButton')
        analyze.grid(pady=5, row=4)

        histogram_diff = ttk.Button(frame, text="Histogram Farkı", command=self.histogram_difference)
        histogram_diff.config(style='Accent.TButton')
        histogram_diff.grid(pady=5, row=5)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Accent.TButton', foreground='#111111', background='#5e5e5e', font=('Helvetica', 14))

        root.grid_rowconfigure(1, weight=1)
        root.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Accent.TButton', foreground='#111111', background='#5e5e5e', font=('Helvetica', 14))

    def analyze_images(self):
        image_path1 = tkinter.filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        image_path2 = tkinter.filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        if image_path1 and image_path2:
            self.compare_histograms(image_path1, image_path2)
        else:
            messagebox.showwarning("Uyarı", "Lütfen iki resim seçin.")

    def histogram_difference(self):
        image_path1 = tkinter.filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        image_path2 = tkinter.filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        if image_path1 and image_path2:
            self.plot_histogram_difference(image_path1, image_path2)
        else:
            messagebox.showwarning("Uyarı", "Lütfen iki resim seçin.")

    def plot_histogram_difference(self, image_path1, image_path2):
        """
        İki görüntünün histogram farkını hesaplar ve grafikte gösterir.
        """

        image1 = cv2.imread(image_path1)
        image2 = cv2.imread(image_path2)

        if image1 is None or image2 is None:
            messagebox.showwarning("Hata", f"Görüntü(ler) yüklenirken bir sorun oluştu. Lütfen dosya adında ve dizininde özel karakterler ve boşluk karakteri olmadığından emin olun.\n\nDosya dizininiz:\n\n{image_path1}\n\nve\n\n{image_path2}\n\nÖrnek dizin:C:/Users/kullanıcı/Desktop")
            return

        fig, axes = plt.subplots(3, 1, figsize=(10, 10))

        axes[0].imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
        axes[0].set_title('Görsel 1')
        axes[0].axis('off')

        axes[1].imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
        axes[1].set_title('Görsel 2')
        axes[1].axis('off')

        gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        hist1 = cv2.calcHist([gray_image1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([gray_image2], [0], None, [256], [0, 256])
        hist_diff = hist1 - hist2

        axes[2].plot(hist_diff, color='r')
        axes[2].set_title('Histogram Farkı')
        axes[2].set_xlabel('Piksel Değeri')
        axes[2].set_ylabel('Fark')

        fig.patch.set_facecolor('lightgrey')

        plt.tight_layout()
        plt.show()

    def compare_histograms(self, image_path1, image_path2):
        """
        İki görüntüyü yükler, gri tonlamalı histogramlarını hesaplar, ki-kare uzaklığını hesaplar
        ve görüntüleri ve histogramlarını yan yana gösterir, ayrıca ki-kare uzaklığını da gösterir.
        """

        image1 = cv2.imread(image_path1)
        image2 = cv2.imread(image_path2)

        if image1 is None or image2 is None:
            messagebox.showwarning("Hata", f"Görüntü(ler) yüklenirken bir sorun oluştu. Lütfen dosya adında ve dizininde özel karakterler ve boşluk karakteri olmadığından emin olun.\n\nDosya dizininiz:\n\n{image_path1}\n\nve\n\n{image_path2}\n\nÖrnek dizin:C:/Users/kullanıcı/Desktop")
            return

        image1_rgb = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        image2_rgb = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

        hist1 = cv2.calcHist([image1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0, 256])

        chisq = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CHISQR)
        chisq_text = "Ki-Kare Uzaklığı: {:.2f}".format(chisq)

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))

        fig.patch.set_facecolor('lightgrey')

        axes[0, 0].imshow(image1_rgb)
        axes[0, 0].set_title("Görüntü 1: {}".format(image_path1.split("/")[-1]))
        axes[0, 0].axis("off")

        axes[0, 1].plot(hist1)
        axes[0, 1].set_title("Görüntü 1 Histogramı")
        axes[0, 1].set_xlim([0, 256])

        axes[1, 0].imshow(image2_rgb)
        axes[1, 0].set_title("Görüntü 2: {}".format(image_path2.split("/")[-1]))
        axes[1, 0].axis("off")

        axes[1, 1].plot(hist2)
        axes[1, 1].set_title("Görüntü 2 Histogramı")
        axes[1, 1].set_xlim([0, 256])

        fig.text(0.5, 0.05, chisq_text, ha='center')

        plt.tight_layout()

        plt.show()

    def back(self, frame):
        frame.destroy()
        self.main(root)

    def encode_frame1(self, F):
        F.destroy()
        F2 = Frame(root)
        label1 = Label(F2, text='Veri şifrelemek istediğiniz \ngörüntüyü seçiniz:')
        label1.config(font=('Times new roman', 25, 'bold'), bg='#5e5e5e')
        label1.grid()

        button_bws = Button(F2, text='Dosya Seç', command=lambda: self.encode_frame2(F2))
        button_bws.config(font=('Helvetica', 18), bg='#5e5e5e')
        button_bws.grid()
        button_back = Button(F2, text='İptal', command=lambda: Veri_gomme.back(self, F2))
        button_back.config(font=('Helvetica', 18), bg='#5e5e5e')
        button_back.grid(pady=15)
        button_back.grid()
        F2.grid()

    def decode_frame1(self, F):
        F.destroy()
        d_f2 = Frame(root)
        label1 = Label(d_f2, text='Saklı Metinli Dosyayı Seçiniz:')
        label1.config(font=('Times new roman', 25, 'bold'), bg='#5e5e5e')
        label1.grid()
        label1.config(bg='#5e5e5e')
        button_bws = Button(d_f2, text='Dosya Seç', command=lambda: self.decode_frame2(d_f2))
        button_bws.config(font=('Helvetica', 18), bg='#5e5e5e')
        button_bws.grid()
        button_back = Button(d_f2, text='İptal', command=lambda: Veri_gomme.back(self, d_f2))
        button_back.config(font=('Helvetica', 18), bg='#5e5e5e')
        button_back.grid(pady=15)
        button_back.grid()
        d_f2.grid()

    def encode_frame2(self, e_F2):
        e_pg = Frame(root)
        myfile = tkinter.filedialog.askopenfilename(
            filetypes=([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfile:
            messagebox.showerror("Hata", "Dosya Seçmediniz!")
            return
        else:
            my_img = Image.open(myfile)
            file_name_prefix = os.path.splitext(os.path.basename(myfile))[0]
            if myfile.lower().endswith('.png'):
                output_file = file_name_prefix + "_alfa_kanalı_ve_piksel_bitleri.txt"
                print_pixel_bits_to_file(my_img, "png", output_file)
                print("PNG formatındaki piksel bitleri alfa kanalıyla birlikte '{}' dosyasına yazıldı.".format(
                    output_file))
            elif myfile.lower().endswith('.jpeg') or myfile.lower().endswith('.jpg'):
                output_file = file_name_prefix + "_piksel_bitleri.txt"
                print_pixel_bits_to_file(my_img, "jpg", output_file)
                print("JPG formatındaki piksel bitleri '{}' dosyasına yazıldı.".format(output_file))
            new_image = my_img.resize((300, 200))
            img = ImageTk.PhotoImage(new_image)
            label3 = Label(e_pg, text='Seçilen Dosya :')
            label3.config(font=('Helvetica', 14, 'bold'))
            label3.grid()
            board = Label(e_pg, image=img)
            board.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = my_img.size
            board.grid()
            label2 = Label(e_pg, text='Mesajı girin')
            label2.config(font=('Helvetica', 14, 'bold'))
            label2.grid(pady=15)

            text_a = scrolledtext.ScrolledText(e_pg, width=100, height=10)
            text_a.grid()

            button_frame = Frame(e_pg)
            button_frame.grid(row=4, columnspan=2)

            encode_button = Button(button_frame, text='İptal', command=lambda: Veri_gomme.back(self, e_pg))
            encode_button.config(font=('Helvetica', 14), bg='#e8c1c7')
            encode_button.grid(row=0, column=1, padx=10)

            button_back = Button(button_frame, text='Şifrele',
                                 command=lambda: self.check_and_encode(text_a, my_img, e_pg))
            button_back.config(font=('Helvetica', 14), bg='#e8c1c7')
            button_back.grid(row=0, column=0, padx=10)

        e_pg.grid(row=1)
        e_F2.destroy()

    def check_and_encode(self, text_a, my_img, e_pg):
        data = text_a.get("1.0", "end-1c")
        if len(data) * 8 > (self.o_image_w * self.o_image_h * 3):
            messagebox.showwarning("Uyarı", "Metin, seçilen görüntüye sığmıyor. Daha kısa bir metin kullanın.")
        else:
            self.enc_fun(text_a, my_img)
            Veri_gomme.back(self, e_pg)

    def decode_frame2(self, d_F2):
        d_F3 = Frame(root)
        myfiles = tkinter.filedialog.askopenfilename(
            filetypes=([('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')]))
        if not myfiles:
            messagebox.showerror("Hata", "Dosya Seçmediniz!")
        else:
            my_img = Image.open(myfiles, 'r')
            my_image = my_img.resize((300, 200))
            img = ImageTk.PhotoImage(my_image)
            label4 = Label(d_F3, text='Seçilen Dosya :')
            label4.config(font=('Helvetica', 14, 'bold'))
            label4.grid()
            board = Label(d_F3, image=img)
            board.image = img
            board.grid()
            hidden_data = self.decode(my_img)
            label2 = Label(d_F3, text='Gizli veri :')
            label2.config(font=('Helvetica', 14, 'bold'))
            label2.grid(pady=10)
            text_a = scrolledtext.ScrolledText(d_F3, width=100, height=10)
            text_a.insert(INSERT, hidden_data)
            text_a.configure(state='disabled')
            text_a.grid()
            button_back = Button(d_F3, text='İptal', command=lambda: self.frame_3(d_F3))
            button_back.config(font=('Helvetica', 14), bg='#e8c1c7')
            button_back.grid(pady=15)
            button_back.grid()
            d_F3.grid(row=1)
            d_F2.destroy()

    def decode(self, image):
        image_data = iter(image.getdata())
        data = ''

        while (True):
            pixels = [value for value in image_data.__next__()[:3] +
                      image_data.__next__()[:3] +
                      image_data.__next__()[:3]]
            binary_str = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binary_str += '0'
                else:
                    binary_str += '1'

            data += chr(int(binary_str, 2))
            if pixels[-1] % 2 != 0:
                return data

    def generate_Data(self, data):
        new_data = []

        for i in data:
            new_data.append(format(ord(i), '08b'))
        return new_data

    def modify_Pix(self, pix, data):
        dataList = self.generate_Data(data)
        dataLen = len(dataList)
        imgData = iter(pix)

        for i in range(dataLen):
            # Extracting 3 pixels at a time
            pix = [value for value in imgData.__next__()[:3] +
                   imgData.__next__()[:3] +
                   imgData.__next__()[:3]]

            for j in range(0, 8):
                if (dataList[i][j] == '0') and (pix[j] % 2 != 0):
                    if (pix[j] % 2 != 0):
                        pix[j] -= 1

                elif (dataList[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

            if (i == dataLen - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode_enc(self, newImg, data):
        w = newImg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modify_Pix(newImg.getdata(), data):

            # Putting modified pixels in the new image
            newImg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    def enc_fun(self, text_a, myImg):
        data = text_a.get("1.0", "end-1c")
        if (len(data) == 0):
            messagebox.showinfo("Uyarı", "Lütfen TextBox'a metin girin")
        else:
            newImg = myImg.copy()
            self.encode_enc(newImg, data)
            my_file = BytesIO()
            temp = os.path.splitext(os.path.basename(myImg.filename))[0]
            newImg.save(tkinter.filedialog.asksaveasfilename(initialfile=temp, filetypes=([('png', '*.png')]),
                                                             defaultextension=".png"))
            self.d_image_size = my_file.tell()
            self.d_image_w, self.d_image_h = newImg.size
            messagebox.showinfo("Başarılı", "Başarıyla Kodlandı\nDosya aynı dizinde png olarak kaydedildi")

    def frame_3(self, frame):
        frame.destroy()
        self.main(root)


def print_pixel_bits_to_file(image, format_type, output_file):
    with open(output_file, 'w') as file:
        width, height = image.size

        if format_type == "png":
            file.write("Png Dosyası RGB Bitleri ve (varsa) Alpha Kanalı Bitleri: \n\n")
            for y in range(height):
                for x in range(width):
                    pixel = image.getpixel((x, y))
                    for color in pixel:
                        file.write(format(color, '08b') + " ")
                    file.write("\n")

        elif format_type == "jpg":
            file.write("Jpg Dosyası RGB Bitleri: \n\n")
            for y in range(height):
                for x in range(width):
                    pixel = image.getpixel((x, y))
                    for i in range(3):
                        file.write(format(pixel[i], '08b') + " ")
                    file.write("\n")

root = Tk()
o = Veri_gomme()
o.main(root)
root.mainloop()