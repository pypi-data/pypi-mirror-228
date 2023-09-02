# About fuzzaprox package

This package allows to approximate input data from above and from bellow.

- from above by a inverse upper approximation and
- from bellow by a inverse bottom approximation

Fuzzy transformations used in this package are based on operations of Lukasiewicz algebra.


## Zdroje


## Code of Conduct


## License

Open-sourced software licensed under the [MIT license](LICENSE.md).


## Installation

You can install the package via pip:

```bash
pip install fuzzaprox
```

## Usage

### Initialization

```python
from fuzzaprox.Fuzzaprox import Fuzzaprox
fa = Fuzzaprox()
```


### Set input data
Some data to approximate.
```python
import numpy as np

length_data = 200
data_x_idx = np.linspace(0, 4 * np.pi, length_data)  # in radians for a full sine wave
sin_val_y = np.sin(data_x_idx)
noise_level = 0.4
noise = noise_level * np.random.normal(size=length_data)
full_data_y = sin_val_y + noise
y_vals = full_data_y.tolist()
fa.set_input_data(y_vals)  # Sets Input data
```

### Define fuzzy set shape

Now we need to define fuzzy sets.
The definition is done by definition of 4 values - 
 - Start of fuzzy set base - usually 0
 - Start of kernel 
 - End of kernel
 - End of fuzzy set base 

```python
fa.define_fuzzy_set(0, 12, 14, 26)
```

### Run approximation

```python
fa.run()
```

### Results:

Received Inverse transformation values can be obtained by following:

### Inverse approximation values
```python
# get inverse approximation
approx_inv_upper = fa.get_inv_approx_upper()  # get upper approximation
approx_inv_bottom = fa.get_inv_approx_bottom()  # get bottom approximation
```

### Forward approximation values

(This would be usefully mainly for compression reasons)

```python
# get forward approximation
approx_fw_upper = fa.get_fw_approx_upper()
approx_fw_bottom = fa.get_fw_approx_bottom()
```

### Plotting results

We can plot the obtained approximations ufor example 
using matplot pyplot library like this:

```python
# get normalised input values of y
normalised_y = fa.get_normalised_y_vals()
# get x axis values
x_axis_values = fa.get_x_axes()


# and plot it results
import matplotlib.pyplot as plt

fig, axs = plt.subplots(3)

axs[0].plot(x_axis_values, full_data_y)
axs[1].plot(x_axis_values, approx_inv_upper)
axs[2].plot(x_axis_values, approx_inv_bottom)

plt.show()
```

# Credits
RNDr. Martina Daňková, Ph.D.