========================
StoNED with Z variables
========================

A firm’s ability to operate efficiently often depends on operational conditions and practices, 
such as the production environment and the firm specific characteristics for example  
technology  selection  or  managerial  practices.  Banker  and  Natarajan (2008) refer to both variables that 
characterize operational conditions and practices as `contextual variables`.

* Contextual variables are often (but not always) **external factors** that are beyond the control of firms

    - Examples: competition, regulation, weather, location

    - Need to adjust efficiency estimates for operating environment

    - Policy makers may influence the operating environment

* Contextual variables can also be **internal factors**

    - Examples: management practices, ownership
    
    - Better understanding of the impacts of internal factors can help the firm to improve performance


Taking the multiplicative model as our starting point, 
we introduce the contextual variables, represented by `r`-dimensional vectors :math:`z_i` that 
represent the measured values of operational conditions and practices, to obtain 
the following semi-nonparametric, partial log-linear equation

.. math::
    :nowrap:

    \begin{align*}
        \text{ln} y_i = \text{ln} f(\bf x_i) + \delta^{'}Z_i + v_i - u_i.
    \end{align*}

In this equation, parameter vector :math:`\delta=(\delta_1...\delta_r)` represents the 
marginal effects ofcontextual variables on output. All other variables maintain their 
previous definitions.

Following Johnson and Kuosmanen (2011), we incorporate the contextual variables in step 1 of 
the StoNED estimation routine and refine the multiplicative CNLS problem as follows:

.. math::
    :nowrap:
    
    \begin{align*}
        & \underset{\alpha, \beta, \varepsilon} {min} \sum_{i=1}^n\varepsilon_i^2 \\
        & \text{s.t.} \\
        &  \text{ln} y_i = \text{ln}(\phi_i+1) + \delta^{'}z_i + \varepsilon_i  \quad \forall i\\
        &   \phi_i  = \alpha_i + \beta_i^{'}X_i -1 \quad \forall i \\
        &  \alpha_i + \beta_i^{'}X_i \le \alpha_j + \beta_j^{'}X_i  \quad  \forall i, j\\
        &  \beta_i \ge 0 \quad  \forall i \\
    \end{align*}

Denote by :math:`\delta^{StoNEZD}` the coefficients  of  the contextual variables 
obtained as theoptimal solution to above nonlinear problem. Johnson and Kuosmanen (2011) examine the statisticalproperties of this estimator in 
detail, showing its unbiasedness, consistency, and asymptotic efficiency.


Example `[.ipynb] <https://colab.research.google.com/github/ds2010/pyStoNED/blob/master/notebooks/StoNEZD.ipynb>`_
------------------------------------------------------------------------------------------------------------------------------

In the following code, we estimatie a log-transformed cost function model with z-variable and 
show how to obtain the firm-specific inefficiency.

.. code:: python

    # import packages
    from pystoned import CNLS, StoNED
    from pystoned.constant import CET_MULT, FUN_COST, RTS_CRS, RED_MOM
    from pystoned.dataset import load_Finnish_electricity_firm
    
    # import all data (including the contextual varibale)
    data = load_Finnish_electricity_firm(x_select=['Energy', 'Length', 'Customers'],   
                                         y_select=['TOTEX'],
                                         z_select=['PerUndGr'])

    # define and solve the StoNED model using MoM approach
    model = CNLS.CNLS(y=data.y, x=data.x, z=data.x, cet = CET_MULT, fun = FUN_COST, rts = RTS_CRS) 
    model.optimize('email@address')

    # Residual decomposition
    rd = StoNED.StoNED(model)
    print(rd.get_technical_inefficiency(RED_MOM))
