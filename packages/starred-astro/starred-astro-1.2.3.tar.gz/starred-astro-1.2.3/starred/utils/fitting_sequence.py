import warnings

from starred.deconvolution.loss import Loss as deconvLoss
from starred.psf.loss import Loss as psfLoss
from starred.deconvolution.parameters import ParametersDeconv
from starred.utils.noise_utils import propagate_noise
from starred.utils.optimization import Optimizer
from starred.plots import plot_function as pltf
from starred.psf.parameters import ParametersPSF

from copy import deepcopy
import numpy as np


def run_2_steps_PSF_reconstruction(data, model, parameters, sigma_2,
                                   lambda_scales=1., lambda_hf=1., lambda_positivity=0.,
                                   kwargs_optim1=None, kwargs_optim2=None,
                                   method1='l-bfgs-b', method2='adabelief',
                                   method_noise='MC', regularize_full_psf=False,
                                   masks=None, unfix_moffat_final_step=False):
    """
    A high level function for the two-steps (first Moffat fitting, then background + Moffat fitting).

    :param data: array containing the observations
    :param model: Point Spread Function (PSF) class from ``starred.psf.psf``
    :param parameters: parameters class from ``starred.psf.parameters``
    :param sigma_2: array containing the square of the noise maps
    :param lambda_scales: Lagrange parameter that weights intermediate scales in the transformed domain.
    :param lambda_hf: Lagrange parameter weighting the highest frequency scale
    :param lambda_positivity: Lagrange parameter weighting the positivity of the full PSF. 0 means no positivity constraint (recommended).
    :param kwargs_optim1: settings for the non-linear optimizer for step 1 (Moffat fitting)
    :param kwargs_optim2: settings for the non-linear optimizer for step 2 (background fitting)
    :param method1: name of the non-linear optimizer for step 1 (see ``starred.utils.optimization``)
    :param method2: name of the non-linear optimizer for step 2 (see ``starred.utils.optimization``)
    :param method_noise: method for noise propagation. Choose 'MC' for an empirical propagation of the noise or 'SLIT' for analytical propagation.
    :param regularize_full_psf: True if you want to regularize the Moffat and the background (recommended). False regularizes only the background
    :param masks: array containing the masks for the PSF (if given)
    :param unfix_moffat_final_step: if True, also optimizes Moffat parameters (except amplitude) jointly with the background component during step 2 (default is False, meaning that the Moffat component is fixed to model from step 1)
    """
    warnings.warn(
        "DEPRECATION WARNING : This function will be removed soon, please use `run_multi_steps_PSF_reconstruction` instead!")
    if kwargs_optim1 is None:
        kwargs_optim1 = {'maxiter': 1000}
    if kwargs_optim2 is None:
        kwargs_optim2 = {
            'max_iterations': 500, 'min_iterations': None,
            'init_learning_rate': 1e-2, 'schedule_learning_rate': True,
            'restart_from_init': False, 'stop_at_loss_increase': False,
            'progress_bar': True, 'return_param_history': True
        }
    kwargs_init, kwargs_fixed, kwargs_up, kwargs_down = deepcopy(parameters._kwargs_init), deepcopy(
        parameters._kwargs_fixed), \
        deepcopy(parameters._kwargs_up), deepcopy(parameters._kwargs_down)

    # Moffat fit first
    loss = psfLoss(data, model, parameters, sigma_2, model.M, regularization_terms='l1_starlet',
                   regularization_strength_scales=0, regularization_strength_hf=0, masks=masks)
    optim = Optimizer(loss, parameters, method=method1)
    best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(**kwargs_optim1)

    try:
        # this will work only for the Jaxopt optimiser, which have a success argument
        if extra_fields['stat'].success:
            print('Success of the Moffat fit in %i iterations (%2.2f s)' % (extra_fields['stat'].iter_num, runtime))
        else:
            print('Warning: Moffat fit did not converge !')
    except:
        pass

    # Printing partial results
    kwargs_partial = parameters.args2kwargs(best_fit)
    print('Moffat fit :', kwargs_partial)

    # compute noise propagation
    W = propagate_noise(model, np.sqrt(sigma_2), kwargs_partial, wavelet_type_list=['starlet'], method=method_noise,
                        num_samples=500, seed=1, likelihood_type='chi2', verbose=False,
                        upsampling_factor=model.upsampling_factor)[0]

    if not unfix_moffat_final_step:
        # Release background, fix the moffat (default strategy which mitigates potential degeneracies)
        if model.elliptical_moffat:
            kwargs_moffat_fixed = {'fwhm_x': kwargs_partial['kwargs_moffat']['fwhm_x'],
                                   'fwhm_y': kwargs_partial['kwargs_moffat']['fwhm_y'],
                                   'phi': kwargs_partial['kwargs_moffat']['phi'],
                                   'beta': kwargs_partial['kwargs_moffat']['beta'],
                                   'C': kwargs_partial['kwargs_moffat']['C']}
        else:
            kwargs_moffat_fixed = {'fwhm': kwargs_partial['kwargs_moffat']['fwhm'],
                                   'beta': kwargs_partial['kwargs_moffat']['beta'],
                                   'C': kwargs_partial['kwargs_moffat']['C']}
    else:
        # will also optimize the Moffat along with the background
        print('Warning: Moffat parameters (except amplitude) will be optimized jointly with the background.')
        kwargs_moffat_fixed = {'C': kwargs_partial['kwargs_moffat']['C']}

    kwargs_fixed = {
        'kwargs_moffat': kwargs_moffat_fixed,
        'kwargs_gaussian': {},
        'kwargs_background': {},
    }

    # recompile the parameter class as we have changed the number of free parameters
    parameters = ParametersPSF(kwargs_partial, kwargs_fixed, kwargs_up, kwargs_down)
    loss = psfLoss(data, model, parameters, sigma_2, model.M, regularization_terms='l1_starlet',
                   regularization_strength_scales=lambda_scales, regularization_strength_hf=lambda_hf,
                   regularization_strength_positivity=lambda_positivity, W=W, regularize_full_psf=regularize_full_psf)

    optim = Optimizer(loss, parameters, method=method2)
    best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(**kwargs_optim2)
    kwargs_final = parameters.args2kwargs(best_fit)
    print('Final Model :', kwargs_final)

    loss_history = extra_fields['loss_history']

    return model, parameters, loss, kwargs_partial, kwargs_final, loss_history


def run_multi_steps_PSF_reconstruction(data, model, parameters, sigma_2, masks=None,
                                   lambda_scales=1., lambda_hf=1., lambda_positivity=0.,
                                       fitting_sequence=[['background'], ['moffat']],
                                       optim_list=['l-bfgs-b', 'adabelief'],
                                       kwargs_optim_list=None,
                                   method_noise='MC', regularize_full_psf=False,
                                       verbose=True):
    """
    A high level function for the two-steps (first Moffat fitting, then background + Moffat fitting).

    :param data: array containing the observations
    :param model: Point Spread Function (PSF) class from ``starred.psf.psf``
    :param parameters: parameters class from ``starred.psf.parameters``
    :param sigma_2: array containing the square of the noise maps
    :param lambda_scales: Lagrange parameter that weights intermediate scales in the transformed domain.
    :param lambda_hf: Lagrange parameter weighting the highest frequency scale
    :param lambda_positivity: Lagrange parameter weighting the positivity of the full PSF. 0 means no positivity constraint (recommended).
    :param fitting_sequence: list, List of lists, containing the element of the model to keep fixed. Example : [['pts-source-astrometry','pts-source-photometry','background'],['pts-source-astrometry','pts-source-photometry'], ...]
    :param optim_list: List of optimiser. Recommended if background is kept constant : 'l-bfgs-b', 'adabelief' otherwise.
    :param kwargs_optim_list: List of dictionary, containing the setting for the different optimiser.
    :param method_noise: method for noise propagation. Choose 'MC' for an empirical propagation of the noise or 'SLIT' for analytical propagation.
    :param regularize_full_psf: True if you want to regularize the Moffat and the background (recommended). False regularizes only the background
    :param masks: array containing the masks for the PSF (if given)

    :return model, parameters, loss, kwargs_partial_list, LogL_list, loss_history_list
    """

    # Check the sequence
    assert len(fitting_sequence) == len(optim_list), "Fitting sequence and optimiser list have different lenght !"
    if kwargs_optim_list is not None:
        assert len(fitting_sequence) == len(
            kwargs_optim_list), "Fitting sequence and kwargs optimiser list have different lenght !"
    else:
        warnings.warn('No optimiser kwargs provided. Default configuration is used.')
        kwargs_optim_list = [{} for _ in range(len(fitting_sequence))]
    kwargs_init, kwargs_fixed_default, kwargs_up, kwargs_down = deepcopy(parameters._kwargs_init), deepcopy(
        parameters._kwargs_fixed), \
        deepcopy(parameters._kwargs_up), deepcopy(parameters._kwargs_down)

    kwargs_partial_list = [kwargs_init]
    loss_history_list = []
    LogL_list = []
    W = None

    for i, steps in enumerate(fitting_sequence):
        kwargs_fixed = deepcopy(kwargs_fixed_default)
        background_free = True
        print(f'### Step {i + 1}, fixing : {steps} ###')
        for fixed_feature in steps:
            if fixed_feature == 'pts-source-astrometry':
                kwargs_fixed['kwargs_gaussian']['x0'] = kwargs_partial_list[i]['kwargs_gaussian']['x0']
                kwargs_fixed['kwargs_gaussian']['y0'] = kwargs_partial_list[i]['kwargs_gaussian']['y0']
            elif fixed_feature == 'pts-source-photometry':
                kwargs_fixed['kwargs_gaussian']['a'] = kwargs_partial_list[i]['kwargs_gaussian']['a']
                kwargs_fixed['kwargs_moffat']['C'] = kwargs_partial_list[i]['kwargs_moffat']['C']
            elif fixed_feature == 'background':
                # TODO: check if there is a speed up when skipping regularisation in the case of a fixed background
                kwargs_fixed['kwargs_background']['background'] = kwargs_partial_list[i]['kwargs_background'][
                    'background']
                background_free = False
            elif fixed_feature == 'moffat':
                if model.elliptical_moffat:
                    kwargs_fixed['kwargs_moffat']['fwhm_x'] = kwargs_partial_list[i]['kwargs_moffat']['fwhm_x']
                    kwargs_fixed['kwargs_moffat']['fwhm_y'] = kwargs_partial_list[i]['kwargs_moffat']['fwhm_y']
                    kwargs_fixed['kwargs_moffat']['phi'] = kwargs_partial_list[i]['kwargs_moffat']['phi']
                else:
                    kwargs_fixed['kwargs_moffat']['fwhm'] = kwargs_partial_list[i]['kwargs_moffat']['fwhm']
                kwargs_fixed['kwargs_moffat']['beta'] = kwargs_partial_list[i]['kwargs_moffat']['beta']
                kwargs_fixed['kwargs_moffat']['C'] = kwargs_partial_list[i]['kwargs_moffat']['C']
            else:
                raise ValueError(
                    f'Steps {steps} is not defined. Choose between "pts-source-astrometry", "pts-source-photometry", "background" or "moffat"')

        # Lift degeneracy between background and Moffat by fixing Moffat amplitude
        if background_free:
            kwargs_fixed['kwargs_moffat']['C'] = kwargs_partial_list[i]['kwargs_moffat']['C']
            lambda_scales_eff = deepcopy(lambda_scales)
            lambda_hf_eff = deepcopy(lambda_hf)
        else:
            # remove regularisation for speed up
            lambda_scales_eff = 0.
            lambda_hf_eff = 0.

        # recompile the parameter class as we have changed the number of free parameters
        parameters = ParametersPSF(kwargs_partial_list[i], kwargs_fixed, kwargs_up, kwargs_down)
        loss = psfLoss(data, model, parameters, sigma_2, model.M, masks=masks, regularization_terms='l1_starlet',
                       regularization_strength_scales=lambda_scales_eff, regularization_strength_hf=lambda_hf_eff,
                       regularization_strength_positivity=lambda_positivity, W=W,
                       regularize_full_psf=regularize_full_psf)

        optim = Optimizer(loss, parameters, method=optim_list[i])
        best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(**kwargs_optim_list[i])
        if verbose:
            try:
                # this will work only for the Jaxopt optimiser, which have a success argument
                if extra_fields['stat'].success:
                    print(
                        f'Success of the step {i + 1} fit in {extra_fields["stat"].iter_num} iterations ({runtime} s)')
                else:
                    print(f'Warning: step {i + 1} fit did not converge !')
            except:
                pass

        # Saving partial results
        kwargs_partial_steps = deepcopy(parameters.best_fit_values(as_kwargs=True))
        loss_history_list.append(extra_fields['loss_history'])
        LogL_list.append(logL_best_fit)

        # compute noise propagation
        W = propagate_noise(model, np.sqrt(sigma_2), kwargs_partial_steps, wavelet_type_list=['starlet'],
                            method=method_noise,
                            num_samples=400, seed=1, likelihood_type='chi2', verbose=False,
                            upsampling_factor=model.upsampling_factor)[0]

        # update kwargs_partial_list
        kwargs_partial_list.append(deepcopy(kwargs_partial_steps))
        if verbose:
            print('Step %i/%i took %2.f seconds' % (i + 1, len(fitting_sequence), runtime))
            print('Kwargs partial at step %i/%i' % (i + 1, len(fitting_sequence)), kwargs_partial_steps)
            print('LogL : ', logL_best_fit)
            print('Overall Reduced Chi2 : ',
                  -2 * loss._log_likelihood_chi2(kwargs_partial_steps) / (model.image_size ** 2))

    return model, parameters, loss, kwargs_partial_list, LogL_list, loss_history_list

def multi_step_deconvolution(data, model, parameters, sigma_2, s, subsampling_factor,
                              fitting_sequence = [['background'],['pts-source-astrometry'],[]],
                             optim_list=['l-bfgs-b', 'adabelief', 'adabelief'], kwargs_optim_list=None,
                             lambda_scales=1., lambda_hf=1000., lambda_positivity_bkg=100, lambda_positivity_ps=100,
                              prior_list = None, regularize_full_model = False, regularize_pts_source=True,
                              adjust_sky = False, noise_propagation = 'MC', verbose=True):
    """
    A high-level function to run several time the optimisation algorithms and ensure to find the optimal solution.

    :param data: 3D array containing the images, one per epoch. shape (epochs, im_size, im_size)
    :param model: Deconv class, deconvolution model
    :param parameters: ParametersDeconv class
    :param sigma_2: 3D array containing the noisemaps, one per epoch. shape (epochs, im_size, im_size)
    :param s: 3D array containing the narrow PSFs, one per epoch. shape (epochs, im_size_up, im_size_up) where im_size_up needs be a multiple of im_size.
    :param subsampling_factor: integer, ratio of the size of the data pixels to that of the PSF pixels.
    :param fitting_sequence: list, List of lists, containing the element of the model to keep fixed. Example : [['pts-source-astrometry','pts-source-photometry','background'],['pts-source-astrometry','pts-source-photometry'], ...]
    :param optim_list: List of optimiser. Recommended if background is kept constant : 'l-bfgs-b', 'adabelief' otherwise.
    :param kwargs_optim_list: List of dictionary, containing the setting for the different optimiser.
    :param lambda_scales: Lagrange parameter that weights intermediate scales in the transformed domain
    :param lambda_hf: Lagrange parameter weighting the highest frequency scale
    :param lambda_positivity_bkg: Lagrange parameter weighting the positivity of the background. 0 means no positivity constraint.
    :param lambda_positivity_ps: Lagrange parameter weighting the positivity of the point sources. 0 means no positivity constraint.
    :param regularize_full_model: option to regularise just the background (False) or background + point source channel (True)
    :param regularize_pts_source: option to regularise the point source channel
    :param prior_list: list of Prior object, Gaussian prior on parameters to be applied at each step
    :param adjust_sky: bool, True if you want to fit some sky subtraction
    :param noise_propagation: 'MC' or 'SLIT', method to compute the noise propagation in wavelet space. Default: 'MC'.
    :param verbose: bool. Verbosity.

    Return model, parameters, loss, kwargs_partial_list, fig_list, LogL_list, loss_history_list
    """
    #Check the sequence
    assert len(fitting_sequence) == len(optim_list), "Fitting sequence and optimiser list have different lenght !"
    if kwargs_optim_list is not None:
        assert len(fitting_sequence) == len(kwargs_optim_list), "Fitting sequence and kwargs optimiser list have different lenght !"
    else:
        warnings.warn('No optimiser kwargs provided. Default configuration is used.')
        kwargs_optim_list = [{} for _ in range(len(fitting_sequence))]

    if prior_list is None:
        prior_list = [None for _ in range(len(fitting_sequence))]
    else:
        assert len(fitting_sequence) == len(prior_list), "Fitting sequence and prior list have different lenght !"

    #setup the model
    kwargs_init, kwargs_fixed_default, kwargs_up, kwargs_down = deepcopy(parameters._kwargs_init), deepcopy(parameters._kwargs_fixed), \
                                                        deepcopy(parameters._kwargs_up), deepcopy(parameters._kwargs_down)
    if not adjust_sky:
        kwargs_fixed_default['kwargs_background']['mean'] = np.zeros(model.epochs)

    kwargs_partial_list = [kwargs_init]
    fig_list = []
    loss_history_list = []
    LogL_list = []

    W = propagate_noise(model, np.sqrt(sigma_2), kwargs_init, wavelet_type_list=['starlet'],
                        method=noise_propagation,
                        num_samples=500, seed=1, likelihood_type='chi2', verbose=False,
                        upsampling_factor=subsampling_factor)[0]

    for i, steps in enumerate(fitting_sequence):
        kwargs_fixed = deepcopy(kwargs_fixed_default)
        background_free = True
        for fixed_feature in steps:
            if fixed_feature == 'pts-source-astrometry':
                kwargs_fixed['kwargs_analytic']['c_x'] = kwargs_partial_list[i]['kwargs_analytic']['c_x']
                kwargs_fixed['kwargs_analytic']['c_y'] = kwargs_partial_list[i]['kwargs_analytic']['c_y']
            elif fixed_feature == 'pts-source-photometry':
                kwargs_fixed['kwargs_analytic']['a'] = kwargs_partial_list[i]['kwargs_analytic']['a']
            elif fixed_feature == 'background':
                background_free = False
                kwargs_fixed['kwargs_background']['h'] = kwargs_partial_list[i]['kwargs_background']['h']
            else:
                raise ValueError('Steps is not defined. Choose between "pts-source-astrometry", "pts-source-photometry" or "background". ')

        # need to recompile the parameter class, since we have changed the number of free parameters
        parameters = ParametersDeconv(kwargs_partial_list[i], kwargs_fixed, kwargs_up=kwargs_up, kwargs_down=kwargs_down)

        # for speed-up we turn of the regularisation to avoid the starlet decomposition, if the background is fixed
        if background_free:
            lambda_scales_eff, lambda_hf_eff, lambda_positivity_bkg_eff = deepcopy(lambda_scales), deepcopy(
                lambda_hf), deepcopy(lambda_positivity_bkg)
        else:
            lambda_scales_eff, lambda_hf_eff, lambda_positivity_bkg_eff = 0., 0., 0.

        #run the optimisation :
        print('Step %i, fixing :'%(i+1), steps)
        loss = deconvLoss(data, model, parameters, sigma_2, regularization_terms='l1_starlet',
                          regularization_strength_scales=lambda_scales_eff,
                          regularization_strength_hf=lambda_hf_eff,
                          regularization_strength_positivity=lambda_positivity_bkg_eff,
                          regularization_strength_positivity_ps=lambda_positivity_ps,
                          regularize_full_model=regularize_full_model,
                          regularize_pts_source=regularize_pts_source,
                          prior=prior_list[i], W=W,)

        optim = Optimizer(loss, parameters, method=optim_list[i])
        best_fit, logL_best_fit, extra_fields, runtime = optim.minimize(**kwargs_optim_list[i])

        # Saving partial results
        kwargs_partial_steps = deepcopy(parameters.best_fit_values(as_kwargs=True))
        fig_list.append(pltf.plot_deconvolution(model, data, sigma_2, s, kwargs_partial_steps, epoch=0, units='e-', cut_dict=None))
        loss_history_list.append(extra_fields['loss_history'])
        LogL_list.append(logL_best_fit)

        # TODO: if the noise propagation depends on the kwargs in the future, it might be good to recompute W

        kwargs_partial_list.append(deepcopy(kwargs_partial_steps))
        if verbose:
            print('Step %i/%i took %2.f seconds'%(i+1, len(fitting_sequence), runtime))
            print('Kwargs partial at step %i/%i'%(i+1, len(fitting_sequence)), kwargs_partial_steps)
            print('LogL : ', logL_best_fit)
            print('Overall Reduced Chi2 : ',
                  -2 * loss._log_likelihood_chi2(kwargs_partial_steps) / (model.image_size ** 2))

    return model, parameters, loss, kwargs_partial_list, fig_list, LogL_list, loss_history_list