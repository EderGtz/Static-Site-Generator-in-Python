description: An analytical project comparing recursive forecasting models implemented in both Python and R, using exponential smoothing across 10 economic indicators.

---

# RecursiveForecast — Python vs. R Comparative Study

[< Back Home](/)

[< Projects](/projects)

An analytical project comparing recursive forecasting models implemented in both Python and R. Developed as part of a homework at UVEG, it implements the Exponential Smoothing algorithm to predict 2020 values from historical 2015-2019 data across 10 economic indicators.

## Overview

RecursiveForecast implements exponential smoothing for time-series forecasting in two languages (Python and R) and compares the results. The core challenge is applying the smoothing formula recursively over every value in a column to produce a truly accumulated forecast, rather than using only the last value as a pivot point.

The project covers 10 indicators (HC, HI, HT, HTP, U6E, UI6E, UCHE, UITI, UIFH, UTC6E) and produces comparative plots showing the forecast trends.

## The Algorithm

Exponential smoothing smooths time-series data using an exponential window function. The formula applied is:

` St = alpha * Xt-1 + (1 - alpha) * St-1 `

Where:

- **St:** Forecast for the current period
- **alpha:** Smoothing factor (set to 0.5 in this project)
- **Xt-1:** Actual value of the previous period
- **St-1:** Forecast of the previous period

The recursion is the key part: each forecast depends on the previous forecast, creating a chain that accumulates the smoothing effect across the entire series.

## Sample Data

Original data (first 5 rows of 2015-2019):

```
      HC      HI     HT    HTP    U6E   UI6E   UCHE   UITI   UIFH   UTC6E
1  44.900  39.200  93.50  43.70  51.30  57.40  51.30  12.80  29.10  71.50
2  45.600  47.000  93.10  52.10  47.00  59.50  52.20  14.70  20.50  73.60
3  45.400  50.900  93.20  49.50  45.30  63.90  46.80  20.40  16.70  72.20
4  44.900  52.900  92.90  47.30  45.00  65.80  46.70  23.70  13.40  73.50
5  44.300  56.400  92.50  45.90  43.00  70.10  44.60  27.20  10.70  75.10
```

Forecasted values for 2020 (6th row):

```
      HC      HI     HT    HTP    U6E   UI6E   UCHE   UITI   UIFH   UTC6E
6  44.706  53.175  92.79  46.95  44.56  66.79  46.29  23.79  13.89  74.02
```

## Comparative Implementation

### Python Implementation

- **Paradigm:** Imperative and procedural
- **Key libraries:** numpy for data handling, matplotlib for visualization
- **Approach:** Explicit state management with granular control over the iteration process. Each step of the recursion is handled explicitly, making the logic easy to trace and debug.

The Python version produces modern, customizable graphical output and is more versatile for extending the analysis to additional indicators or smoothing variants.

### R Implementation

- **Paradigm:** Functional programming
- **Key libraries:** purrr (tidyverse) for functional operations, base graphics for plotting
- **Approach:** Uses `reduce` to synthesize the forecasting logic into a compact and expressive syntax. The functional style maps naturally onto the recursive formula.

The R implementation offers a concise statistical approach that is well-suited to the academic context of the project.

## Visualization

The project generates comparative plots for all 10 indicators showing both the historical data (2015-2019) and the forecasted 2020 values. While the R implementation provides a concise statistical view, the Python version produces more customizable and visually refined output.

## Technology Stack

**Languages:** Python, R

**Python libraries:** numpy, matplotlib

**R libraries:** purrr (tidyverse), base graphics

**Techniques:** Exponential Smoothing, Time-Series Forecasting, Recursive Computation

**Context:** UVEG Reto 4 -- academic data analysis project

## Repository

[github.com/EderGtz/RecursiveForecast---Python-vs.-R](https://github.com/EderGtz/RecursiveForecast---Python-vs.-R)