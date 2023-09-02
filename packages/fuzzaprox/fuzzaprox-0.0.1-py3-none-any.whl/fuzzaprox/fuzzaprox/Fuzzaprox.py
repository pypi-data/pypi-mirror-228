import numpy as np

from fuzzaprox.transformation.Transform import Transform
from fuzzaprox.transformation.FuzzySet import FuzzySet
from fuzzaprox.services.DataService import DataService


class Fuzzaprox:

    def __init__(self):
        self.fuzzy_set_instance = None
        self.fuzzy_set_push = None
        self.transformation = None
        self.data_x = None
        self.norm_data_y = None
        self.orig_data_y = None

    def define_fuzzy_set(self, base_start, kernel_start, kernel_end, base_end):
        """ Define fuzzy set by parameters """
        fuzzy_set_instance = FuzzySet({'kernel_start': int(kernel_start - base_start),
                                       'kernel_end': int(kernel_end - base_start),
                                       'fuzzy_set_width': int(base_end - base_start)})
        self.fuzzy_set_instance = fuzzy_set_instance
        self.set_fuzzy_set_push(fuzzy_set_instance.fuzzy_set_width)

    def set_fuzzy_set(self, fuzzy_set_setting):
        """ Sets fuzzy set by Dictionary """
        self.fuzzy_set_instance = FuzzySet(fuzzy_set_setting)

    def set_fuzzy_set_with_instance(self, fuzzy_set_instance):
        """ Sets fuzzy set with by Instance """
        self.set_fuzzy_set({"kernel_start": fuzzy_set_instance.kernel_start,
                            "kernel_end": fuzzy_set_instance.kernel_end,
                            "fuzzy_set_width": fuzzy_set_instance.fuzzy_set_width})
        self.fuzzy_set_instance = fuzzy_set_instance

    def set_fuzzy_set_push(self, fuzzy_set_push):
        """ Sets the distance between fuzzy sets """
        self.fuzzy_set_push = int(fuzzy_set_push/2)

    @staticmethod
    def convert_list_to_array(list_data):
        """ Just converts list to array, if not already in ndarray format """
        if type(list_data) == list:
            np_array = np.array(list_data)
        elif type(list_data) == np.ndarray:
            np_array = list_data
        else:
            raise ValueError("Y data should be in list or np.array format")
        return np_array

    @staticmethod
    def generate_x_axis_from_y_list(y_np_array):
        x_axes = np.linspace(0, len(y_np_array) - 1, len(y_np_array), dtype=int)
        return x_axes

    def set_input_data(self, y_values):
        """ Sets input data, which will be approximated """
        # convert list to array
        data_as_array = self.convert_list_to_array(y_values)
        self.orig_data_y = y_values  # set original data

        # normalise data to interval [0,1]
        normalised_y_np_array = DataService.normalise(data_as_array)
        self.norm_data_y = normalised_y_np_array

        # create x-axis
        self.data_x = self.generate_x_axis_from_y_list(normalised_y_np_array)

    def run(self):
        # set necessary input
        self.transformation = Transform(self.data_x,
                                        self.norm_data_y,
                                        self.fuzzy_set_instance,
                                        self.fuzzy_set_push)

        # run upper and bottom Approximation
        self.transformation.upper_bottom_forward_ft()  # Calculates Forward F-transforms
        self.transformation.calculate_inverse_ft()  # Calculates Inverse F-transforms

    def get_approximations(self):

        # format output
        return_dict = self.transformation.return_input_param_and_approx()
        return return_dict

    def get_inv_approx_upper(self):
        """ Returns upper inv approximation """
        inv_approx_upper = self.transformation.upper_t_inv_data_y
        return inv_approx_upper

    def get_fw_approx_upper(self):
        """ Returns upper fw approximation """
        fw_approx_upper_x = self.transformation.upper_t_fw_data_x
        fw_approx_upper_y = self.transformation.upper_t_fw_data_y
        fw_approx_upper = {"fw_x": fw_approx_upper_x, "fw_y": fw_approx_upper_y}
        return fw_approx_upper

    def get_inv_approx_bottom(self):
        """ Returns bottom inv approximation """
        inv_approx_bottom = self.transformation.bottom_t_inv_data_y
        return inv_approx_bottom

    def get_fw_approx_bottom(self):
        """ Returns upper fw approximation """
        fw_approx_bottom_x = self.transformation.bottom_t_fw_data_x
        fw_approx_bottom_y = self.transformation.bottom_t_fw_data_y
        fw_approx_bottom = {"fw_x": fw_approx_bottom_x, "fw_y": fw_approx_bottom_y}
        return fw_approx_bottom

    def get_normalised_y_vals(self):
        """ Returns normalised-Y values """
        return self.norm_data_y

    def get_x_axes(self):
        """ Return just X-axes range with values of integer numbers """
        return self.data_x
