class PDFHandler():
    import warnings
    import numpy as np
    import pandas as pd
    import scipy.stats as st
    import statsmodels as sm
    
    def __init__(self):
        print("This is constructor of ConvertTable")
        
    @staticmethod
    def makePDF(dist, params, size=10000):
        """Generate distributions's Probability Distribution Function """
        
        # Separate parts of parameters
        arg   = params[:-2]
        loc   = params[-2]
        scale = params[-1]
        
        # Get sane start and end points of distribution
        start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
        end   = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)
        
        # Build PDF and turn into pandas Series
        x   = np.linspace(start, end, size)
        y   = dist.pdf(x, loc=loc, scale=scale, *arg)
        pdf = pd.Series(y, x)
        return pdf

    @staticmethod
    def getBestFitDistribution(data, bins=200, ax=None):
        """Model data by finding best fit distribution to data"""
        # Get histogram of original data
        y, x = np.histogram(data, bins=bins, density=True)
        x = (x + np.roll(x, -1))[:-1] / 2.0
        
        # Distributions to check
        DISTRIBUTIONS = [        
            st.norm, st.beta, st.lognorm, st.frechet_r, st.frechet_l, st.logistic, st.gumbel_r, st.gumbel_l
            # st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
            # st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
            # st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
            # st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
            # st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
            # st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
            # st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
            # st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
            # st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
            # st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
        ]

        # Best holders
        best_distribution = st.norm
        best_params       = (0.0, 1.0)
        best_sse          = np.inf
        
        # Estimate distribution parameters from data
        for distribution in DISTRIBUTIONS:
            # Try to fit the distribution
            try:
                # fit dist to data
                params = distribution.fit(data)
                
                # Separate parts of parameters
                arg    = params[:-2]
                loc    = params[-2]
                scale  = params[-1]
                
                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))
                
                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    end
                except Exception:
                    pass
                
                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

            except Exception:
                pass

        return (best_distribution.name, best_params)
    
if __name__ == '__main__':
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np
    import scipy.stats as st
    
    import pandas as pd
    data     = pd.DataFrame( np.random.lognormal(0.0, 1.0, size=1000) )
    
    matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
    matplotlib.style.use('ggplot')
    ax       = data.plot(kind='hist', bins=50, density=True, alpha=0.5 )
    
    # Find best fit distribution
    best_fit_name, best_fit_params = PDFHandler.getBestFitDistribution(data, 200, ax=ax)
    best_dist = getattr(st, best_fit_name)
    # Make PDF with best params 
    pdf = PDFHandler.makePDF(best_dist, best_fit_params)
    
    # Update plots
    dataYLim = ax.get_ylim()
    ax.set_ylim(dataYLim)
    ax.set_title(u'All Fitted Distributions')
    ax.set_xlabel(u'Temp')
    ax.set_ylabel('Frequency')
    
    # Display
    plt.figure(figsize=(12,8))
    ax = pdf.plot(lw=2, label='PDF', legend=True)
    data.plot(kind='hist', bins=50, density=True, alpha=0.5, label='Data', legend=True, ax=ax)
    
    param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
    param_str   = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fit_params)])
    dist_str    = '{}({})'.format(best_fit_name, param_str)
    
    ax.set_title(u'with best fit distribution \n' + dist_str)
    ax.set_xlabel(u'Temp)')
    ax.set_ylabel('Frequency')
    plt.show()

