import numpy as np 
import matplotlib.pylab as plt 
from time import time
from sompy.sompy import SOMFactory
from sklearn import metrics
import sklearn.cluster as clust
from sompy.visualization.hitmap import HitMapView


class Mysm:
    def __init__(self, data, names,initialization='random', train_rough_len=2, train_finetune_len=5, view2D='view2D', n_clusters=4, hitmap='hitmap', outfile='out'):
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
        self.build()
        self.train()
        self.get_view2D()
        self.cluster()
        self.get_hitmap()
        self.get_result()
        
    def set_train_len(self, train_rough_len=2,train_finetune_len=5):
        self.train_rough_len = train_rough_len
        self.train_finetune_len = train_finetune_len
    
    def set_view2D_name(self, view2D='view2D'):
        self.view2D = view2D
    
    def set_n_clusters(self, n_clusters=4):
        self.n_clusters = n_clusters
    
    def set_hitmap_name(self, hitmap='hitmap'):
        self.hitmap = hitmap
    
    def set_outfile_name(self, outfile='out'):
        self.outfile = outfile
    

    def build(self):
        self.sm = SOMFactory().build(data=self.data, normalization='var', initialization=self.initialization, component_names=self.names)
    
    def train(self):
        self.sm.train(n_job=1, verbose=False, train_rough_len=self.train_rough_len, train_finetune_len=self.train_finetune_len)
    
    def get_error(self):
        topographic_error = self.sm.calculate_topographic_error()
        quantization_error = np.mean(self.sm._bmu[1])
        return topographic_error, quantization_error
    
    def get_view2D(self):
        from sompy.visualization.mapview import View2D
        view2D  = View2D(10,10,"rand data",text_size=10)
        view2D.build_save(self.sm, col_sz=4, which_dim="all", desnormalize=True, filename=self.view2D)

    def cluster(self):
        self.sl = clust.KMeans(self.n_clusters).fit_predict(self.data)
        return self.sl

    def Clu_assessment(self):
        return metrics.calinski_harabaz_score(self.data,self.sl)
    
    def get_result(self):
        np.savetxt(self.outfile+'.txt',self.sl)

    def get_hitmap(self):
        self.sm.cluster(self.n_clusters)
        hits  = HitMapView(20,20,"Clustering",text_size=12)
        #a=hits.show(sm)
        hits.build_save(self.sm,filename=self.hitmap)