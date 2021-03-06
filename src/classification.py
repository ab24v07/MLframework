'''
Created on Feb 20, 2013

@author: Ash Booth

TODO:
- write data files for performances and paramterisations
- add preprocessing functionality
- catch the errors when we can't fit a classifier
'''

import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV

from sklearn import decomposition
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, NuSVC
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.lda import LDA
from sklearn.qda import QDA
#from sklearn.ensemble.weight_boosting import AdaBoostClassifier
from sklearn import cross_validation
from sklearn.metrics import classification_report, confusion_matrix

class Classification(object):
    '''
    classdocs
    '''


    def __init__(self, verbose,
                 inputs_train_val, targets_train_val,
                 inputs_test, targets_test, cv = "loo", num_folds = None,
                 PCA = False,
                 Logit = False, perceptron = False, SGDC = True,
                 SVC = False, NuSVC = False, 
                 KNNC = False, RNNC = False,
                 GaussNB = False, MultiNB = False, BernNB = False,
                 DTC = False,
                 RFC = False, ETC = False, GBC = False, #adac = False,
                 LDA = False, QDA = False):
        '''
        Constructor
        '''
        self.inputs_train_val = inputs_train_val
        self.targets_train_val = targets_train_val
        self.inputs_test = inputs_test
        self.targets_test = targets_test
        self.PCA = PCA
        
        try:
            if cv=="loo" or cv=="kfold":
                pass
        except NameError:
            print "cv must be either loo or kfolds"
        if cv == "loo":
            self.cv = cross_validation.LeaveOneOut(self.inputs_train_val.shape[0])
        elif cv == "kfold":
            try:
                self.cv = cross_validation.KFold(self.inputs_train_val.shape[0],k=num_folds)
            except ValueError:
                print "Must enter valid number of folds"

        self.estimators = []
        if Logit: self.estimators.append(self.__gen_logit_estimator(verbose))
        if SVC: self.estimators.append(self.__gen_svc_estimator(verbose))
        if NuSVC: self.estimators.append(self.__gen_nusvc_estimator(verbose))
        if SGDC: self.estimators.append(self.__gen_sgd_estimator(verbose))
        if KNNC: self.estimators.append(self.__gen_knn_estimator(verbose))
        if RNNC: self.estimators.append(self.__gen_rnn_estimator(verbose))
        if GaussNB: self.estimators.append(self.__gen_gnb_estimator(verbose))
        if MultiNB: self.estimators.append(self.__gen_mnb_estimator(verbose))
        if BernNB: self.estimators.append(self.__gen_bnb_estimator(verbose))
        if DTC: self.estimators.append(self.__gen_dtc_estimator(verbose))
        if RFC: self.estimators.append(self.__gen_rfc_estimator(verbose))
        if ETC: self.estimators.append(self.__gen_etc_estimator(verbose))
        if GBC: self.estimators.append(self.__gen_gbc_estimator(verbose))
#        if adac: self.estimators.append(self.__gen_adac_estimator(verbose))
        if LDA: self.estimators.append(self.__gen_lda_estimator(verbose))
        if QDA: self.estimators.append(self.__gen_qda_estimator(verbose))
        
        self.outdata = []
        
        

    def __gen_logit_estimator(self,verbose):
        logistic = LogisticRegression()
        if self.PCA:
            description = "logitClassifier with PCA"
            if verbose: print "generating logit classifier grid search with PCA..."
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('logistic', logistic)])
            n_components = [20, 40, 64]
            Cs = np.logspace(-4, 4, 7)
            penalty =  ['l1', 'l2']
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,
                                     logistic__penalty=penalty, logistic__C=Cs), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else: 
            description = "logitClassifier"
            if verbose: print "generating logit classifier grid search..."
            pipe = Pipeline(steps=[('logistic', logistic)])
            Cs = np.logspace(-4, 4, 7)
            penalty =  ['l1', 'l2']
            estimator = GridSearchCV(pipe,
                                     dict(logistic__penalty=penalty, logistic__C=Cs), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_svc_estimator(self,verbose):
        svc = SVC()
        if self.PCA:
            description = "SVC with PCA"
            if verbose: print "generating support vector classifier grid search with PCA..."
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('svc', svc)])
            n_components = [20, 40, 64]
            
            kernels = ['linear', 'poly', 'rbf', 'sigmoid']
            Cs = np.logspace(-4, 4, 7)
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,
                                     svc__C=Cs,svc__kernel=kernels), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "SVC"
            if verbose: print "generating support vector classifier grid search..."
            pipe = Pipeline(steps=[('svc', svc)])            
            kernels = ['linear', 'poly', 'rbf', 'sigmoid']
            Cs = np.logspace(-4, 4, 7)
            estimator = GridSearchCV(pipe,
                                     dict(svc__C=Cs, svc__kernel=kernels), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_nusvc_estimator(self,verbose):
        nusvc = NuSVC()
        if self.PCA:
            description= "NuSVC with PCA"
            if verbose: print "generating nu support vector classifier grid search with PCA..."
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('nusvc', nusvc)])
            n_components = [20, 40, 64]
            kernels = ['linear', 'poly', 'rbf', 'sigmoid']
            nu = [0.05,0.1,0.15]
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,
                                     nusvc__nu=nu,nusvc__kernel=kernels), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description= "NuSVC"
            if verbose: print "generating nu support vector classifier grid search..."
            pipe = Pipeline(steps=[('nusvc', nusvc)])            
            kernels = ['linear', 'poly', 'rbf', 'sigmoid']
            nu = [0.05,0.1,0.15]
            estimator = GridSearchCV(pipe, dict(nusvc__nu=nu, nusvc__kernel=kernels), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_sgd_estimator(self,verbose):
        sgd = SGDClassifier()
        if self.PCA:
            description = "SGDClassifier with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('sgd', sgd)])
            n_components = [20, 40, 64]
            loss = ['hinge', 'log', 'modified_huber']
            penalty = ['l2', 'l1', 'elasticnet']
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,
                                     sgd__loss=loss, sgd__penalty=penalty), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "SGDClassifier"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('sgd', sgd)])
            loss = ['hinge', 'log', 'modified_huber']
            penalty = ['l2', 'l1', 'elasticnet']
            estimator = GridSearchCV(pipe,
                                     dict(sgd__loss=loss, sgd__penalty=penalty), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_knn_estimator(self,verbose):
        knn = KNeighborsClassifier()
        if self.PCA:
            description = "KNNClassifier with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('knn', knn)])
            n_components = [20, 40, 64]
            n_neighbors = [3]#5,9]
            algorithm = ['ball_tree', 'kd_tree', 'brute']
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,
                                     knn__n_neighbors=n_neighbors, knn__algorithm=algorithm), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "KNNClassifier"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('knn', knn)])
            n_neighbors = [3]#,5,9]
            algorithm = ['ball_tree', 'kd_tree', 'brute']
            estimator = GridSearchCV(pipe,
                                     dict(knn__n_neighbors=n_neighbors, knn__algorithm=algorithm), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_rnn_estimator(self,verbose):
        rnn = RadiusNeighborsClassifier(outlier_label=-1)
        if self.PCA:
            description = "RNNClassifier with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('rnn', rnn)])
            n_components = [20, 40, 64]
            radius = [1.0]
            algorithm = ['auto'] # ['ball_tree', 'kd_tree', 'brute']
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,
                                     rnn__radius=radius, rnn__algorithm=algorithm), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "RNNClassifier"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('rnn', rnn)])
            radius = [1.6]
            algorithm = ['auto'] #['ball_tree', 'kd_tree', 'brute']
            estimator = GridSearchCV(pipe,
                                     dict(rnn__radius=radius, rnn__algorithm=algorithm), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_gnb_estimator(self,verbose):
        gnb = GaussianNB()
        if self.PCA:
            description = "GaussianNB with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('gnb', gnb)])
            n_components = [20, 40, 64]
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "GaussianNB"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('gnb', gnb)])
            estimator = GridSearchCV(pipe,dict(), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_mnb_estimator(self,verbose):
        mnb = MultinomialNB(fit_prior=True)
        if self.PCA:
            description = "MultinomialNB with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('mnb', mnb)])
            n_components = [20, 40, 64]
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "MultinomialNB"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('mnb', mnb)])
            alpha = [1.0]
            estimator = GridSearchCV(pipe, dict(mnb__alpha=alpha), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_bnb_estimator(self,verbose):
        bnb = BernoulliNB(fit_prior=True)
        if self.PCA:
            description = "BernoulliNB with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('bnb', bnb)])
            n_components = [20, 40, 64]
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "BernoulliNB"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('bnb', bnb)])
            alpha = [1.0]
            estimator = GridSearchCV(pipe, dict(bnb__alpha=alpha), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_dtc_estimator(self,verbose):
        dtc = DecisionTreeClassifier(random_state=0)
        if self.PCA:
            description = "DTClassifier with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('dtc', dtc)])
            n_components = [20, 40, 64]
            criteria = ['entropy', 'gini']
            max_depth = [None, 3, 5, 7]
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,
                                          dtc__criterion=criteria, dtc__max_depth=max_depth), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "DTClassifier"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('dtc', dtc)])
            criteria = ['entropy', 'gini']
            max_depth = [None, 3, 5, 7]
            estimator = GridSearchCV(pipe,
                                     dict(dtc__criterion=criteria, dtc__max_depth=max_depth), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_rfc_estimator(self,verbose):
        rfc = RandomForestClassifier(n_jobs=1)
        if self.PCA:
            description = "RFClassifier with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('rfc', rfc)])
            n_components = [20, 40, 64]
            n_estimators = [5, 10, 15]
            criteria = ['entropy', 'gini']
            max_depth = [None, 3, 5, 7]
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,
                                          rfc__criterion=criteria, rfc__max_depth=max_depth,
                                          rfc__n_estimators=n_estimators), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "RFClassifier"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('rfc', rfc)])
            n_estimators = [5, 10, 15]
            criteria = ['entropy', 'gini']
            max_depth = [None, 3, 5, 7]
            estimator = GridSearchCV(pipe,
                                     dict(rfc__criterion=criteria, rfc__max_depth=max_depth,
                                          rfc__n_estimators=n_estimators), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_etc_estimator(self,verbose):
        etc = ExtraTreesClassifier(n_jobs=1)
        if self.PCA:
            description = "ETClassifier with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('etc', etc)])
            n_components = [20, 40, 64]
            n_estimators = [5, 10, 15]
            criteria = ['entropy', 'gini']
            max_depth = [None, 3, 5, 7]
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,
                                          etc__criterion=criteria, etc__max_depth=max_depth,
                                          etc__n_estimators=n_estimators), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "ETClassifier"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('etc', etc)])
            n_estimators = [5, 10, 15]
            criteria = ['entropy', 'gini']
            max_depth = [None, 3, 5, 7]
            estimator = GridSearchCV(pipe,
                                     dict(etc__criterion=criteria, etc__max_depth=max_depth,
                                          etc__n_estimators=n_estimators), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_gbc_estimator(self,verbose):
        gbc = GradientBoostingClassifier(n_estimators=100)
        if self.PCA:
            description = "GBClassifier with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('gbc', gbc)])
            n_components = [20, 40, 64]
            max_depth = [1, 3, 5]
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,
                                          gbc__max_depth=max_depth), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "GBClassifier"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('gbc', gbc)])
            max_depth = [1, 3, 5]
            estimator = GridSearchCV(pipe,
                                     dict(gbc__max_depth=max_depth), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
#    def __gen_adac_estimator(self,verbose):
#        adac = AdaBoostClassifier()
#        if self.PCA:
#            description = "ADAClassifier with PCA"
#            if verbose: print "generating {}...".format(description)
#            pca = decomposition.PCA()
#            pipe = Pipeline(steps=[('pca', pca), ('adac', adac)])
#            n_components = [20, 40, 64]
#            n_estimators = [15, 50, 100, 200]
#            learning_rate = [0.8,1.0,1.2]
#            estimator = GridSearchCV(pipe,
#                                     dict(pca__n_components=n_components,
#                                          adac__learning_rate = learning_rate, adac__n_estimators=n_estimators), n_jobs=-1, 
#                                     verbose=1, cv=self.cv)
#        else:
#            description = "ADAClassifier"
#            if verbose: print "generating {}...".format(description)
#            pipe = Pipeline(steps=[('adac', adac)])
#            n_estimators = [15, 50, 100, 200]
#            learning_rate = [0.8,1.0,1.2]
#            estimator = GridSearchCV(pipe,
#                                     dict(adac__n_estimators=n_estimators,adac__learning_rate = learning_rate), n_jobs=-1, 
#                                     verbose=1, cv=self.cv)
#        return [estimator, description]
    
    def __gen_lda_estimator(self,verbose):
        lda = LDA()
        if self.PCA:
            description = "LDAClassifier with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('lda', lda)])
            n_components = [20, 40, 64]
            lda_components=[None]
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components,lda__n_components=lda_components), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "LDAClassifier"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('lda', lda)])
            lda_components=[None]
            estimator = GridSearchCV(pipe,dict(lda__n_components=lda_components), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]
    
    def __gen_qda_estimator(self,verbose):
        qda = QDA()
        if self.PCA:
            description = "QDAClassifier with PCA"
            if verbose: print "generating {}...".format(description)
            pca = decomposition.PCA()
            pipe = Pipeline(steps=[('pca', pca), ('qda', qda)])
            n_components = [20, 40, 64]
            priors = [None]
            estimator = GridSearchCV(pipe,
                                     dict(pca__n_components=n_components, qda__priors=priors), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        else:
            description = "QDAClassifier"
            if verbose: print "generating {}...".format(description)
            pipe = Pipeline(steps=[('qda', qda)])
            priors = [None]
            estimator = GridSearchCV(pipe, dict(qda__priors=priors), n_jobs=-1, 
                                     verbose=1, cv=self.cv)
        return [estimator, description]

    def fit_models(self, verbose):
        print "\nfitting models..."
        for e in self.estimators:
            if verbose: print "fitting {}...".format(e[1])
            try:
                e[0].fit(self.inputs_train_val,self.targets_train_val)
            except:
                print "could not fit {}".format(e[1])
        
        
    def test_models(self):
        print "\ntesting models..."
        for e in self.estimators:
            try:
                cv_score = e[0].score(self.inputs_train_val, self.targets_train_val)
                test_score = e[0].score(self.inputs_test, self.targets_test)
                self.outdata.append([e[1],cv_score,test_score])
            except:
                print "could not test {}".format(e[1])
    
    def write_data(self,verbose):
        print "\nwriting data..."
        import csv
        if self.PCA: filenames = ["scores_pca.csv", "params_pca.txt"]
        else: filenames = ["scores.csv", "params.txt"]
        with open(filenames[0], 'wb') as csvfile:
            scores = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            scores.writerows([["Algorithm", "CrossVal Score", "Test Score"]])
            scores.writerows(self.outdata)
        param_file = open(filenames[1], 'wb')
        for e in self.estimators:
            param_file.write(e[1])
            param_file.write("{}".format(e[0]))
            param_file.write("\n\n")
        param_file.close()
        
    def print_results(self):
        print "\n###########################################"
        print "########### CV AND TEST RESULTS ###########"
        print "###########################################"
        temp_data = self.outdata
        temp_data.insert(0, ["Algorithm", "Validation Score", "Test Score\n"])
        s = [[str(e) for e in row] for row in self.outdata]
        lens = [len(max(col, key=len)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print '\n'
        print '\n'.join(table)
        
    def print_classification_reports(self, conf=True):
        print "\n###########################################"
        print "######### CLASSIFICATION REPORTS ##########"
        print "###########################################"
        for e in self.estimators:
            try:
                preds = e[0].predict(self.inputs_test)
                print e[1] + " classificiation report..."
                print(classification_report(self.targets_test, preds, labels = [1,2,3,4],target_names=['B', 'S', 'T', 'U']))
                cnf = confusion_matrix(self.targets_test, preds, labels=[1,2,3,4])
                np.savetxt("{}_conf_matrix.csv".format(e[1]), cnf, delimiter=',')
            except:
                print "\n"
    
        
        
    
    
            
            
            
            
            