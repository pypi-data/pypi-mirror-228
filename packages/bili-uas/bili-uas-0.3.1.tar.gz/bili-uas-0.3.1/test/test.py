if __name__ == '__main__':
    import wordcloud
    import numpy as np
    import cv2 as cv

    a = cv.imread("/Users/jhzg/Desktop/program/BiliBili-UP-Auxiliary-System/test/mask1.jpg")
    # print(a.shape)
    # print(a[0][0])
    # print(a[150][150])
    wf = {"111": 0.1
        , "222": 0.2
        , "333": 0.3
        , "444": 0.4
        , "555": 0.5}
    a = a.astype(np.uint8)
    wc = wordcloud.WordCloud(font_path='PingFang.ttc', mask=a, height=675, width=1080, background_color='white')
    wc.generate_from_frequencies(wf)
    image = wc.to_image()
    image.save("test_img.png", quality=100)

    pass
