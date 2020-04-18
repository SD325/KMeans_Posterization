import urllib.request
import io
from PIL import Image
import random


K = 8


def restrict_3(val):
    if val < 255 // 3:
        return 0
    elif val > 255 * 2 // 3:
        return 255
    else:
        return 127


def naive_vector_quant_27(filename):
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            r = restrict_3(r)
            g = restrict_3(g)
            b = restrict_3(b)
            nvq_27.putpixel((x, y), (r, g, b))
    nvq_27.save(filename)


def restrict_2(val):
    return 0 if val < 128 else 255


def naive_vector_quant_8(filename):
    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))
            r = restrict_2(r)
            g = restrict_2(g)
            b = restrict_2(b)
            nvq_8.putpixel((x, y), (r, g, b))
    nvq_8.save(filename)


def squared_error(a, b):
    return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1]) + (a[2] - b[2]) * (a[2] - b[2])


def k_means(filename):
    means = [img.getpixel((random.randrange(width), random.randrange(height))) for _ in range(K)]
    mean_per_pix = {i: 0 for i in range(width * height)}
    sum_per_mean = [(0, 0, 0) for _ in range(K)]
    num_per_mean = [0 for _ in range(K)]
    changed = True
    first = True
    gen_num = 1
    while changed:
        changed = False
        for x in range(width):
            for y in range(height):
                pix_ind = y * width + x
                this_pix = img.getpixel((x, y))
                min_error = float("inf")
                min_ind = 0
                for i, m in enumerate(means):
                    this_error = squared_error(this_pix, m)
                    if this_error < min_error:
                        min_error = this_error
                        min_ind = i
                if mean_per_pix[pix_ind] != min_ind:
                    changed = True
                mean_per_pix[pix_ind] = min_ind
                num_per_mean[min_ind] += 1
                sum_per_mean[min_ind] = (sum_per_mean[min_ind][0] + this_pix[0],
                                         sum_per_mean[min_ind][1] + this_pix[1],
                                         sum_per_mean[min_ind][2] + this_pix[2])
        means = [(sum_per_mean[i][0] // num_per_mean[i],
                  sum_per_mean[i][1] // num_per_mean[i],
                  sum_per_mean[i][2] // num_per_mean[i]) for i in range(K)]
        print("Generation", gen_num, ": ", means)
        gen_num += 1
        if first:
            changed = True
        first = False
    for x in range(width):
        for y in range(height):
            pix_ind = y * width + x
            k_means_img.putpixel((x, y), means[mean_per_pix[pix_ind]])
    k_means_img.save(filename)


# URL = 'https://i.pinimg.com/originals/95/2a/04/952a04ea85a8d1b0134516c52198745e.jpg'
# f = io.BytesIO(urllib.request.urlopen(URL).read())  # Download the picture at the url as a file object
image_name = 'my_image'
image_type = 'png'
img = Image.open('%s.%s' % (image_name, image_type))


width, height = img.size

nvq_27 = Image.new('RGB', img.size, 'white')
naive_vector_quant_27('nvq_27_%s.png' % image_name)

nvq_8 = Image.new('RGB', img.size, 'white')
naive_vector_quant_8('nvq_8_%s.png' % image_name)

k_means_img = Image.new('RGB', img.size, 'white')
k_means('k_means_%s_%s.png' % (image_name, K))
