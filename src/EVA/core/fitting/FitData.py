import lmfit.model
import numpy as np
from functools import partial
from lmfit import Model
from lmfit.models import GaussianModel, QuadraticModel

def gaussian(x: np.ndarray, mu: float, sigma: float, a: float, c: float=0) -> np.ndarray:
    return a / sigma / np.sqrt(2 * np.pi) * np.exp(-(x - mu) ** 2 / 2 / sigma ** 2) + c

def fit_gaussian_lmfit(x_data: np.ndarray, y_data: np.ndarray, peak_params: dict,
                       bg_params: dict) -> lmfit.model.ModelResult:
    model = QuadraticModel(prefix="background_", nan_policy="omit")
    model.set_param_hint("a", **bg_params["background"]["a"])
    model.set_param_hint("b", **bg_params["background"]["b"])
    model.set_param_hint("c", **bg_params["background"]["c"])

    for name, params in peak_params.items():
        peak_model = GaussianModel(prefix=f"{name}_", nan_policy="omit")
        peak_model.set_param_hint("center", **params["center"])
        peak_model.set_param_hint("sigma", **params["sigma"])
        peak_model.set_param_hint("amplitude", **params["amplitude"])

        model += peak_model

    if len(model.param_names) > len(x_data):
        raise TypeError("Not enough points")

    fit_res = model.fit(y_data, x=x_data, weights=1/np.sqrt(y_data))
    return fit_res


def scaled_shifted_gaussians(x: np.ndarray, scale: float, x0: float, params: dict) -> np.ndarray:
    """
    Returns a spectrum of multiple Gaussians, one for each set of peak parameters in 'params', with a vertical shift
    parameter x0 and an overall scale factor 'scale'
    """
    return scale * np.sum([gaussian(x-x0, param["center"]["value"], param["sigma"]["value"],
                     param["amplitude"]["value"], c=0) for param in params.values()], axis=0)

def fit_model_lmfit(x_data: np.ndarray, y_data:np.ndarray, peak_params: dict, bg_params: dict, model_params: dict,
                    constrain_scale: bool=True) -> lmfit.model.ModelResult:
    # First set up the background model
    model = QuadraticModel(prefix="background_", nan_policy="omit")
    model.set_param_hint("a", **bg_params["background"]["a"])
    model.set_param_hint("b", **bg_params["background"]["b"])
    model.set_param_hint("c", **bg_params["background"]["c"])

    # Check how many models will be fitted
    n_models = len(model_params)

    scale_param_names = [] # to store the names of the scale parameters
    for i, (model_id, params) in enumerate(model_params.items()):
        """
        'partial' creates a new fitting function for each model by feeding peak parameters into scaled_shifted_gaussian()
        This way, the fitting function can be generated automatically for each model.

        It's essentially like using a lambda, except the functions will still exist outside this scope. When using a
        lambda expression for this, I found that when plotting result.best_fit, lmfit only plotted the last model,
        instead of all..
        """
        func = partial(scaled_shifted_gaussians, params=peak_params[model_id])

        # partial functions do not have a __name__ attribute, but in order for lmfit to work it needs to have a name
        func.__name__ = f"scaled_shifted_gaussians{i}"

        spectrum_model = Model(func, prefix=f"{model_id}_")
        spectrum_model.set_param_hint("x0", **params["x0"], vary=True)

        # if user wants scale parameters to be constrained as scale1 + scale2 + scale3 = 1
        if constrain_scale:
            if n_models == 1: # if there is only one model, force scale=1
                spectrum_model.set_param_hint("scale", value=1, vary=False, min=0, max=1)

            elif i < n_models - 1: # set all but the last scale parameters to be between 0 and 1
                spectrum_model.set_param_hint("scale", **params["scale"], min=0, max=1)
                scale_param_names.append(f"{model_id}_scale")
            else:
                # Constrain the last scale parameter to be equal to 1 - A - B... etc. to satisfy A + B + C = 1
                # Only one of the scale parameters should have this constraint, otherwise we get recursion errors
                constraint = "1 - " + " - ".join(scale_param_names)
                spectrum_model.set_param_hint("scale", **params["scale"], min=0, max=1, expr=constraint)

        # if no scale constraints are wanted
        else:
            spectrum_model.set_param_hint("scale", **params["scale"])

        # finally, add this model to the total model
        model += spectrum_model

    return model.fit(y_data, x=x_data, weights=1/np.sqrt(y_data))

