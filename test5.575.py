pic = pg.screenshot(region=(icon1-111, icon2-38, 1, 8))
img_frame = np.array(pic)
img_frame = cv.cvtColor(img_frame, cv.COLOR_BGR2RGB)

image = img_frame.reshape((img_frame.shape[0] * img_frame.shape[1], 3))

k = 1
clt = KMeans(n_clusters=k)
clt.fit(image)

self.kk = 1

for center in clt.cluster_centers_:
    break

if center[2] < 57 or 70 < center[2] < 90:
    minsec = secs_to_minsec(self.time_left_int - 100)
    self.minsec1 = self.time_left_int - 100
    self.lcd1.display(minsec)
    self.label1.setText('<b>3페이즈 패턴<b>')
