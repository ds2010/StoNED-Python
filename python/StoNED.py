# -*- coding: utf-8 -*-
"""
@Title   : Stochastic nonparametric envelopment of data (StoNED): Residuals decomposition
@Author  : Sheng Dai, Timo Kuosmanen
@Mail    : sheng.dai@aalto.fi (S. Dai); timo.kuosmanen@aalto.fi (T. Kuosmanen)  
@Time    : 2020-04-12 
"""

import qle
import numpy as np
import math
from scipy.stats import norm
import scipy.optimize as opt

def  stoned(eps, func, method, crt):
     # func    = "prod": production frontier;  
     #         = "cost": cost frontier
     # method  = "MOM" : Method of moments
     #         = "QLE" : Quasi-likelihood estimation 
     #         = "NKD" : Nonparametric kernel deconvolution (TBA...)
     # crt     = "addi": Additive composite error term
     #         = "mult": Multiplicative composite error term
    
     if (method == "MoM"):
     
         # Average of residuals (approximately zero)
         mresid = np.mean(eps)
         
         # Calculate the 2nd/3rd central moments for each DMU (sample variance/skewness)
         M2     = (eps -mresid) * (eps -mresid)
         M3     = (eps -mresid) * (eps -mresid) * (eps -mresid) 
         
         # Average of 2nd/ 3rd moments 
         mM2    =  np.mean(M2, axis = 0)
         mM3    =  np.mean(M3, axis = 0)     
     
         if (mM3 < 0):
             mM3 = 0.00001
             
         # standard deviation sigma_u
         sigmau  = (-mM3/((2/math.pi)**(1/2)*(1-4/math.pi)))**(1/3)
     
         # standard deviation sigma_v
         sigmav  = ((mM2-((math.pi-2)/math.pi)*sigmau**2))**(1/2)
     
         # sum of sigma
         sigma2  = sigmau**2 + sigmav**2
     
         # signal to noise ratio (lambda)
         lamda   = sigmau / sigmav

         ## mean (mu) 
         mu      = (sigmau**2*2/math.pi)**(1/2)
     
         # bias adjusted residuals
         epsilon = eps - mu
            
     if (method == "QLE"):
        
         # initial parameter (lambda)
         lamda   = 1.0
 
         # optimatization        
         llres   = opt.minimize(qle.qllf, lamda, eps, method='BFGS')
         
         lamda   = llres.x[0]
         
         # sigmau and sigmav        
         sigma2  = (np.mean(eps**2))/(1-2*lamda**2/(math.pi*(1+lamda**2))) 
        
         # bias adjusted residuals Eq. (3.25)
         ## mean
         mu      =  math.sqrt((2*lamda**2*sigma2)/(math.pi*(1+lamda**2)))
         ## adj. res.
         epsilon =  eps - mu
        
         sigmau  = (math.sqrt(sigma2)*lamda)/(1+lamda)
         sigmav  = math.sqrt(sigma2)/(1+lamda)     
         
     # expected value of the inefficiency term u  Eq. (3.28) in Johnson and Kuosmanen (2015)
     temp   = (1/(1*(2*math.pi)**(1/2)))*np.exp((-((epsilon/(sigmav**2)) - 0)* \
                                                 ((epsilon/(sigmav**2)) - 0))/(2*1**2))

     # Conditional mean
     Eu     = (-epsilon*(sigmau**2)/sigma2) + \
                 (temp / ((1-norm.cdf((epsilon/(sigmav**2))))+0.000001))* \
                                                         (sigmau**2) * (sigmav**2) / sigma2;

     # Technical inefficiency
     if (crt == "addi"):
         if(func == "prod"):
             Etheta = -Eu
         else:
             Etheta = Eu  
     if (crt == "mult"):
         if(func == "prod"):
             Etheta = np.exp(-Eu)
         else:
             Etheta = np.exp(Eu)  
         
     return Etheta
    
     