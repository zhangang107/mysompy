import numpy as np 
import matplotlib.pylab as plt 
from time import time
from sompy.sompy import SOMFactory
from sklearn import metrics
import sklearn.cluster as clust
from sompy.visualization.hitmap import HitMapView


class Mysm:
    def __init__(self, data, names,initialization='random', train_rough_len=2, train_finetune_len=5, view2D='view2D', n_clusters=4, hitmap='hitmap', outfile='out'):
        """
        This somopy init
        :param data: data to be clustered, represented as a matrix of n rows,
            as inputs and m cols as input features
        :param names: features names
        :param initialization: method to be used for initialization of the som
        :param train_rough_len: length of  rough train
        :param train_finetune_len: length of finetune train
        :param view_2D : name of view_2D png
        :param n_clusters : num of clusters
        :param hitmap : name of hitmap png
        :param outfile : name of output txt
        """
        self.data = data
        self.names = names
        self.sm = None
        self.initialization = initialization
        self.train_rough_len = train_rough_len
        self.train_finetune_len = train_finetune_len
        self.view2D = view2D
        self.n_clusters = n_clusters
        self.hitmap = hitmap
        self.outfile =outfile
        self.sl = None
    
    def easytest(self):
        """
        quick test
        """
        self.build()
        self.train()
        self.get_view2D()
        self.cluster()
        self.get_hitmap()
        self.get_result()
        
    def set_train_len(self, train_rough_len=2,train_finetune_len=5):
        """
        set train length
        :param train_rough_len : length of  rough train
        :param train_finetune_len: length of finetune train
        """
        self.train_rough_len = train_rough_len
        self.train_finetune_len = train_finetune_len
    
    def set_view2D_name(self, view2D='view2D'):
        """
        set 2D png name
        :param view_2D : name of view_2D png
        """
        self.view2D = view2D
    
    def set_n_clusters(self, n_clusters=4):
        """
        set num of clusters
        :param n_clusters : num of clusters
        """
        self.n_clusters = n_clusters
    
    def set_hitmap_name(self, hitmap='hitmap'):
        """
        set hitmap png name
        :param hitmap : name of hitmap png
        """
        self.hitmap = hitmap
    
    def set_outfile_name(self, outfile='out'):
        """
        set output txt name
        :param outfile : name of output txt
        """
        self.outfile = outfile
    

    def build(self):
        """
        build SOMFactory
        """
        self.sm = SOMFactory().build(data=self.data, normalization='var', initialization=self.initialization, component_names=self.names)
    
    def train(self):
        """
        train SOM
        """
        self.sm.train(n_job=1, verbose=False, train_rough_len=self.train_rough_len, train_finetune_len=self.train_finetune_len)
    
    def get_error(self):
        """
        get the topographic_error and quantization_error after train
        :Returns : topographic_error and quantization_error tuple
        """
        topographic_error = self.sm.calculate_topographic_error()
        quantization_error = np.mean(self.sm._bmu[1])
        return topographic_error, quantization_error
    
    def get_view2D(self):
        """
        produced 2D png before cluster after train
        """
        from sompy.visualization.mapview import View2D
        view2D  = View2D(10,10,"rand data",text_size=10)
        view2D.build_save(self.sm, col_sz=4, which_dim="all", desnormalize=True, filename=self.view2D)

    def cluster(self):
        """
        cluster
        """
        self.sl = clust.KMeans(self.n_clusters).fit_predict(self.data)
        return self.sl

    def Clu_assessment(self):
        """
        return cluster assessment by metrics
        :return : cluster assessment
        """
        return metrics.calinski_harabaz_score(self.data,self.sl)
    
    def get_result(self):
        """
        produced output txt 
        """
        np.savetxt(self.outfile+'.txt',self.sl)

    def get_hitmap(self):
        """
        produced hitmap png
        """
        self.sm.cluster(self.n_clusters)
        hits  = HitMapView(20,20,"Clustering",text_size=12)
        hits.build_save(self.sm,filename=self.hitmap)