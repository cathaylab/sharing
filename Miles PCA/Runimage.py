import luigi
import os
import numpy
from luigi import date_interval as d
from saisyo_raw import SimpleDynamicTask
from sklearn.decomposition import PCA
from pylab import *
from skimage import data, io, color

BASEPATH = "{}/..".format(os.path.dirname(os.path.abspath(__file__)))
BASEPATH_DATA = os.path.join(BASEPATH, "data")
BASEPATH_photo = os.path.join(BASEPATH_DATA, "photo")

def cc_ratio(ratio_over,variance_ratio):
    c_ratio = 0
    for index,ratio in enumerate(variance_ratio):
        c_ratio += ratio
        if c_ratio> ratio_over:
            return index
            break

class ImageAnalysis(luigi.Task):
	task_namespace = 'image'
	photopath = luigi.Parameter()
	ratio = luigi.IntParameter()

	def requires(self):
		imagepath = os.path.join(BASEPATH_photo, "Image_{}.npy".format(self.ratio))
		yield Imageload(photopath = self.photopath, ratio = self.ratio, imagepath = imagepath)

	def run(self):
		var_ratio = int(self.ratio)/100
		for input in self.input():
			Brown_gray = numpy.load(input.fn)
		pca_all = PCA(n_components = len(Brown_gray[0]))
		pca_all.fit(Brown_gray)
		n_comp = cc_ratio(var_ratio,pca_all.explained_variance_ratio_)
		pca = PCA(n_components = n_comp)
		pca.fit(Brown_gray)
		Brown_gray_pca = pca.fit_transform(Brown_gray)
		Brown_gray_restored = pca.inverse_transform(Brown_gray_pca)
		plt.imsave(self.output().fn, Brown_gray_restored, cmap=plt.cm.gray)

	def output(self):
            outfile = os.path.join(BASEPATH_photo, "Brown_{}.png".format(self.ratio))
            return luigi.LocalTarget(outfile)


class Imageload(luigi.Task):
	task_namespace = 'image'
	photopath = luigi.Parameter()
	ratio = luigi.IntParameter()
	imagepath = luigi.Parameter()

	def run(self):
	    link = self.photopath
	    Brown_gray = io.imread(link,as_grey=True)
	    numpy.save(self.output().fn,Brown_gray)

	def output(self):		
		return luigi.LocalTarget(self.imagepath)
