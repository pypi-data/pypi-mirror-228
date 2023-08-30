from scipy.stats import norm
from scipy.optimize import brentq
import numpy as np
import logging
from datetime import datetime
from volstreet.exceptions import OptionModelInputError
from volstreet.constants import iv_models
from collections import namedtuple
import warnings

bs_logger = logging.getLogger("blackscholes")
today = datetime.now().strftime("%Y-%m-%d")
file_handler = logging.FileHandler(f"bs-{today}.log")
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)
bs_logger.setLevel(logging.INFO)
bs_logger.addHandler(file_handler)

N = norm.cdf
binary_flag = {"c": 1, "p": -1}


def pdf(x):
    """the probability density function"""
    one_over_sqrt_two_pi = 0.3989422804014326779399460599343818684758586311649
    return one_over_sqrt_two_pi * np.exp(-0.5 * x * x)


def d1(S, K, t, r, sigma):
    sigma_squared = sigma * sigma
    numerator = np.log(S / float(K)) + (r + sigma_squared / 2.0) * t
    denominator = sigma * np.sqrt(t)

    if not denominator:
        print("")
    return numerator / denominator


def d2(S, K, t, r, sigma):
    return d1(S, K, t, r, sigma) - sigma * np.sqrt(t)


def forward_price(S, t, r):
    return S / np.exp(-r * t)


def call(S, K, t, r, sigma):
    e_to_the_minus_rt = np.exp(-r * t)
    D1 = d1(S, K, t, r, sigma)
    D2 = d2(S, K, t, r, sigma)

    return S * N(D1) - K * e_to_the_minus_rt * N(D2)


def put(S, K, t, r, sigma):
    e_to_the_minus_rt = np.exp(-r * t)
    D1 = d1(S, K, t, r, sigma)
    D2 = d2(S, K, t, r, sigma)

    return -S * N(-D1) + K * e_to_the_minus_rt * N(-D2)


def delta(S, K, t, r, sigma, flag):
    d_1 = d1(S, K, t, r, sigma)

    if flag.upper().startswith("P"):
        return N(d_1) - 1.0
    else:
        return N(d_1)


def gamma(S, K, t, r, sigma):
    d_1 = d1(S, K, t, r, sigma)
    return pdf(d_1) / (S * sigma * np.sqrt(t))


def theta(S, K, t, r, sigma, flag):
    two_sqrt_t = 2 * np.sqrt(t)

    D1 = d1(S, K, t, r, sigma)
    D2 = d2(S, K, t, r, sigma)

    first_term = (-S * pdf(D1) * sigma) / two_sqrt_t

    if flag.upper().startswith("C"):
        second_term = r * K * np.exp(-r * t) * N(D2)
        return (first_term - second_term) / 365.0

    else:
        second_term = r * K * np.exp(-r * t) * N(-D2)
        return (first_term + second_term) / 365.0


def vega(S, K, t, r, sigma):
    d_1 = d1(S, K, t, r, sigma)
    return S * pdf(d_1) * np.sqrt(t) * 0.01


def rho(S, K, t, r, sigma, flag):
    d_2 = d2(S, K, t, r, sigma)
    e_to_the_minus_rt = np.exp(-r * t)
    if flag.upper().startswith("C"):
        return t * K * e_to_the_minus_rt * N(d_2) * 0.01
    else:
        return -t * K * e_to_the_minus_rt * N(-d_2) * 0.01


def implied_volatility(price, S, K, t, r, flag):
    if flag.upper().startswith("P"):
        f = lambda sigma: price - put(S, K, t, r, sigma)
    else:
        f = lambda sigma: price - call(S, K, t, r, sigma)

    try:
        return brentq(
            f, a=1e-12, b=100, xtol=1e-15, rtol=1e-15, maxiter=1000, full_output=False
        )
    except ValueError as e:
        if "f(a) and f(b) must have different signs" in str(e):
            raise e
        else:
            bs_logger.error(
                f"Error in implied_volatility: {e}, price={price}, S={S}, K={K}, t={t}, r={r}, flag={flag}"
            )
            raise e
    except Exception as e:
        bs_logger.error(
            f"Error in implied_volatility: {e}, price={price}, S={S}, K={K}, t={t}, r={r}, flag={flag}"
        )
        raise e


def greeks(S, K, t, r, sigma, flag):
    greeks_tuple = namedtuple("Greeks", ["delta", "gamma", "theta", "vega"])
    return greeks_tuple(
        delta(S, K, t, r, sigma, flag),
        gamma(S, K, t, r, sigma),
        theta(S, K, t, r, sigma, flag),
        vega(S, K, t, r, sigma),
    )


def test_func():
    # Comparing time to calculate implied volatility using two different methods
    import timeit

    # Generate random data
    np.random.seed(42)
    Ss = np.random.uniform(40000, 45000, 100)
    Ks = np.random.uniform(40000, 45000, 100)
    ts = np.random.uniform(0.0027, 0.0191, 100)
    rs = np.array([0.05] * 100)
    flags = np.random.choice(["c", "p"], 100)
    sigmas = np.random.uniform(0.1, 0.5, 100)
    prices = np.array(
        [
            call(s, k, t, r, sigma) if f == "c" else put(s, k, t, r, sigma)
            for s, k, t, r, sigma, f in zip(Ss, Ks, ts, rs, sigmas, flags)
        ]
    )
    deltas = np.array(
        [
            delta(s, k, t, r, sigma, f)
            for s, k, t, r, sigma, f in zip(Ss, Ks, ts, rs, sigmas, flags)
        ]
    )
    gammas = np.array(
        [gamma(s, k, t, r, sigma) for s, k, t, r, sigma in zip(Ss, Ks, ts, rs, sigmas)]
    )
    thetas = np.array(
        [
            theta(s, k, t, r, sigma, f)
            for s, k, t, r, sigma, f in zip(Ss, Ks, ts, rs, sigmas, flags)
        ]
    )
    vegas = np.array(
        [vega(s, k, t, r, sigma) for s, k, t, r, sigma in zip(Ss, Ks, ts, rs, sigmas)]
    )

    # Calculate implied volatility using two different methods
    start = timeit.default_timer()
    ivs = []
    for price, s, k, t, r, f in zip(prices, Ss, Ks, ts, rs, flags):
        iv = implied_volatility(price, s, k, t, r, f)
        ivs.append(iv)

    stop = timeit.default_timer()
    print("Time to calculate implied volatility using brentq: ", stop - start)

    import pandas as pd

    return pd.DataFrame(
        {
            "spot": Ss,
            "strike": Ks,
            "time": ts * 365,
            "rate": rs,
            "flag": flags,
            "sigma": sigmas,
            "price": prices,
            "delta": deltas,
            "gamma": gammas,
            "theta": thetas,
            "vega": vegas,
            "implied_volatility": ivs,
        }
    )


def check_for_intrinsics(flag, spot, strike, price):
    flag = flag.lower()[0]
    intrinsic_value = max(spot - strike, 0) if flag == "c" else max(strike - spot, 0)
    if intrinsic_value > price:
        bs_logger.error(
            f"Current price {price} of {'call' if flag == 'c' else 'put'} is less than the intrinsic value {intrinsic_value}"
        )
        raise OptionModelInputError(
            f"Current price {price} of {'call' if flag == 'c' else 'put'} is less than the intrinsic value {intrinsic_value}"
        )


def get_iv_model_for_time_to_expiry(time_to_expiry):
    # Filtering the models based on the time to expiry
    filtered_model = [*filter(lambda x: x[0] <= time_to_expiry < x[1], iv_models)][0]
    # Returning the model for the segment
    return iv_models[filtered_model]


def iv_multiple_to_atm(time_to_expiry, spot, strike, symbol="NIFTY"):
    iv_model = get_iv_model_for_time_to_expiry(time_to_expiry)
    distance = (strike / spot) - 1
    distance_squared = distance**2
    moneyness = spot / strike
    distance_time_interaction = distance_squared * time_to_expiry
    finnifty = True if symbol.upper() == "FINNIFTY" else False
    nifty = True if symbol.upper() == "NIFTY" else False
    with warnings.catch_warnings():
        warnings.filterwarnings(action="ignore", category=UserWarning)
        return iv_model.predict(
            [
                [
                    distance,
                    distance_squared,
                    moneyness,
                    distance_time_interaction,
                    finnifty,
                    nifty,
                ]
            ]
        )[0]


def adjusted_iv_from_atm_iv(atm_iv, strike, spot, time_to_expiry, symbol="NIFTY"):
    iv_multiple = iv_multiple_to_atm(time_to_expiry, spot, strike, symbol)
    return atm_iv * iv_multiple


def transform_iv(
    original_iv,
    original_strike,
    new_spot,
    new_time_to_expiry,
    symbol=None,
    maximum_increase=0.8,
):
    """
    This function returns the adjusted implied volatility accounting for the curve effect.
    :param original_iv: Original implied volatility
    :param original_strike: Original strike price
    :param new_spot: New spot price
    :param new_time_to_expiry: New time to expiry in years
    :param symbol: Symbol for the random forest model
    :param maximum_increase: By what factor should the vol increase at the end of the day.
    The increase is linear to the time left to expiry. The default value is 0.8
    :return: Adjusted implied volatility for the strike given the new spot and time to expiry
    """

    symbol = "NIFTY" if symbol is None else symbol.upper()

    if (
        new_time_to_expiry < 0.0008
    ):  # On expiry day we need to adjust the vol as iv increases steadily as we approach expiry
        # Assumption: Vol only increases after 2 hours of open
        opening_time_left_to_expiry = 375 / 525600
        increase_total_time = 255 / 525600
        time_delta = opening_time_left_to_expiry - new_time_to_expiry
        incremental_delta = max(time_delta - (120 / 525600), 0)
        vol_multiple = 1 + (
            (incremental_delta / increase_total_time) * maximum_increase
        )
        new_iv = original_iv * vol_multiple
    else:
        new_iv = original_iv

    iv_multiple = iv_multiple_to_atm(
        new_time_to_expiry, new_spot, original_strike, symbol
    )
    return new_iv * iv_multiple


def transform_option_price(
    strike,
    flag,
    original_price=None,
    original_iv=None,
    original_spot=None,
    original_time_to_expiry=None,
    new_spot=None,
    movement=None,
    time_delta_minutes=None,
    time_delta=None,
    symbol=None,
    maximum_increase_on_expiry_day=0.8,
):
    flag = flag.lower()[0]
    symbol = "NIFTY" if symbol is None else symbol.upper()

    # Setting the original iv if not provided
    if original_iv is None:
        if (
            original_price is None
            or original_spot is None
            or original_time_to_expiry is None
        ):
            raise ValueError(
                "Either original_iv or original_price, original_spot and original_time_to_expiry must be provided "
                "to transform the option price"
            )
        check_for_intrinsics(flag, original_spot, strike, original_price)
        original_iv = implied_volatility(
            original_price, original_spot, strike, original_time_to_expiry, 0.06, flag
        )
        print(f"Original IV: {original_iv}.")
    # Set the new spot price if not provided
    if new_spot is None:
        if original_spot is None or movement is None:
            raise ValueError(
                "Either new_spot or original_spot and movement must be provided to transform the option price"
            )
        new_spot = (1 + movement) * original_spot

    # Set the new time to expiry
    if original_time_to_expiry is None or all(
        [time_delta_minutes is None, time_delta is None]
    ):
        raise ValueError(
            "original_time_to_expiry and time_delta in minutes or years must be provided to transform the option price"
        )
    time_delta = time_delta_minutes / 525600 if time_delta_minutes else time_delta
    new_time_to_expiry = original_time_to_expiry - time_delta
    if new_time_to_expiry < 0.0008 and original_time_to_expiry > 0.0020:
        # If we jump to expiry day during simulation
        original_iv = original_iv * (1 + maximum_increase_on_expiry_day)

    # Derive the new IV
    new_iv = transform_iv(
        original_iv,
        strike,
        new_spot,
        new_time_to_expiry,
        symbol=symbol,
        maximum_increase=maximum_increase_on_expiry_day,
    )

    print(f"Transforming option price with new IV: {new_iv}.")

    # Return the new option price
    price_func = call if flag == "c" else put

    new_price = price_func(new_spot, strike, new_time_to_expiry, 0.06, new_iv)
    return max(new_price, 0.05)


def iv_transformer_coeffs_wip(tte):
    # distance squared coefficient
    dfs2 = 3270.27 * np.exp(-384.38 * tte) + 100
    dfs2 = min(dfs2, 20000)

    # distance coefficient
    if tte < 0.26 / 365:
        dfs = 1
    else:
        dfs = 1 / ((tte**0.45) * 5)
        dfs = min(dfs, 5)
        dfs = -6 + dfs

    # intercept
    if tte < 3 / (24 * 365):
        intercept = 1.07
    elif tte < 0.27 / 365:
        intercept = 1
    else:
        intercept = 0.98
    return dfs2, dfs, intercept


def iv_curve_adjustor(
    movement,
    time_to_expiry,
    iv: int | tuple = 1,
    spot=100,
    strike=100,
    symbol="NIFTY",
    time_delta_minutes=None,
    print_details=False,
):
    """
    This function returns the adjusted implied volatility accounting for the curve effect.
    :param movement: movement of the underlying in percentage with sign
    :param time_to_expiry: time to expiry in years
    :param iv: implied volatility of the strike
    :param spot: spot price
    :param strike: strike price
    :param symbol: symbol for rhe random forest model
    :param time_delta_minutes: time delta in minutes
    :param print_details: print details of the adjustment
    :return: adjusted implied volatility for the strike after the movement
    """

    def get_iv_multiple_to_atm(tte, s, k, sym, distance):
        try:
            # Model the IV curve using the random forest models
            return iv_multiple_to_atm(tte, s, k, sym)
        except Exception as e:
            bs_logger.error(
                f"Error in iv_multiple_to_atm: {e}, time_to_expiry={tte}, spot={s}, strike={k}, symbol={sym}"
            )

            # Get the regression coefficients for the IV curve
            coeffs = iv_transformer_coeffs_wip(tte)

            # Apply the IV curve model to the current displacement
            return coeffs[0] * distance**2 + coeffs[1] * distance + coeffs[2]

    # Calculate the current displacement from ATM
    current_displacement = strike / spot - 1

    # Calculate the new spot price after the movement
    new_spot = spot * (1 + movement)

    # Calculate the new displacement from ATM
    total_displacement = strike / new_spot - 1

    # Get the IV multiple for the current displacement
    current_iv_multiple = get_iv_multiple_to_atm(
        time_to_expiry, spot, strike, symbol, current_displacement
    )

    # Normalize the given IV to the ATM level by dividing by the current IV multiple
    atm_iv = iv / current_iv_multiple

    # New time to expiry after the movement
    new_time_to_expiry = (
        time_to_expiry - (time_delta_minutes / 525600)
        if time_delta_minutes
        else time_to_expiry
    )

    if new_time_to_expiry < 0.000001:
        new_time_to_expiry = 0.000001

    # Apply the IV curve model to the new displacement
    premium_to_atm_iv = get_iv_multiple_to_atm(
        new_time_to_expiry, new_spot, strike, symbol, total_displacement
    )

    if (
        new_time_to_expiry < 0.0008
    ):  # On expiry day we need to adjust the vol as iv increases steadily as we approach expiry
        vol_multiple = 1 + (time_delta_minutes / 375)
        new_atm_iv = atm_iv * vol_multiple
    else:
        new_atm_iv = atm_iv

    # Scale the normalized ATM IV by the premium to get the new IV
    new_iv = new_atm_iv * premium_to_atm_iv

    if print_details:
        print(
            f"New IV: {new_iv} for Strike: {strike}\n"
            f"Starting IV: {iv}, ATM IV: {atm_iv}\nMovement {movement}\n"
            f"Spot after move: {new_spot}\n"
            f"Time to expiry: {new_time_to_expiry} from {time_to_expiry}"
        )

    return new_iv


def target_movement(
    flag,
    starting_price,
    target_price,
    starting_spot,
    strike,
    time_left,
    time_delta_minutes=None,
    symbol="NIFTY",
    print_details=False,
):
    """
    :param flag: 'c' or 'p'
    :param starting_price: current price of the option
    :param target_price: target price of the option
    :param starting_spot: current spot price
    :param strike: strike price
    :param time_left: time left to expiry in years
    :param time_delta_minutes: time delta in minutes
    :param print_details: print details of the adjustment
    :param symbol: symbol for the random forest model
    :return:
    """
    flag = flag.lower()[0]

    # Check if the current price is less than the intrinsic value
    check_for_intrinsics(flag, starting_spot, strike, starting_price)

    price_func = call if flag == "c" else put
    vol = implied_volatility(
        starting_price, starting_spot, strike, time_left, 0.06, flag
    )
    new_time_left = (
        time_left - (time_delta_minutes / 525600) if time_delta_minutes else time_left
    )
    delta_ = delta(starting_spot, strike, new_time_left, 0.06, vol, flag)
    estimated_movement_points = (target_price - starting_price) / delta_
    estimated_movement = estimated_movement_points / starting_spot

    modified_vol = iv_curve_adjustor(
        estimated_movement,
        time_left,
        iv=vol,
        spot=starting_spot,
        strike=strike,
        symbol=symbol,
        time_delta_minutes=time_delta_minutes,
        print_details=print_details,
    )

    f = (
        lambda s1: price_func(s1, strike, new_time_left, 0.06, modified_vol)
        - target_price
    )

    # Setting the bounds for the brentq function
    if target_price > starting_price:
        if flag == "c":
            a = starting_spot * 0.1  # Remove hardcoded buffer
            b = 2 * starting_spot
        else:
            a = 0.05
            b = starting_spot * 2  # Remove hardcoded buffer
    else:
        if flag == "c":
            a = 0.05
            b = starting_spot * 2  # Remove hardcoded buffer
        else:
            a = starting_spot * 0.1  # Remove hardcoded buffer
            b = 2 * starting_spot

    target_spot = brentq(
        f, a=a, b=b, xtol=1e-15, rtol=1e-15, maxiter=1000, full_output=False
    )

    assert isinstance(target_spot, float)

    movement = (target_spot / starting_spot) - 1

    return movement
