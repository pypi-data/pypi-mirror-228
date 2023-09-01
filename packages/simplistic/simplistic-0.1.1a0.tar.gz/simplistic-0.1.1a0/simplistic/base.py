import numpy as np

class Trait():
    """
    Description for class.

    :ivar _params_list: List of arguments for mapping
    :ivar _params_dict: Dictionary for mapping arguements
    :ivar _command_seq: Sequence of commands to return
    """

    PREF_LONG_FLAG = False

    def __init__(self, params_list, params_dict):
        """ Assign parameter list and parameter dictionary """

        self._params_list = params_list
        self._params_dict = params_dict
        self._params_set_list = []
        self._command_seq = []

    def _map_params(self):
        """ Maps user defined text to literal cli arguements 

        Parameters
        ----------
        params_dict : dict-like mapping
            Mapping of user-defined terms to cli arguements
        params_list : list-like of arguments
            List of user-defined terms to pass

        Process
        -----------
        1. Match (nlp) term to either (long) or (short) argument
        2. Check (arg_format) for make sure they are present & correct data type.
        3. Check that non-(optional) arguemnts are present 

        4. Check (ordering) or arguements
        5. Check (positional) to make sure arguemnts are properly ordered

        """
        
        self._format_params()

        sub_sequence = []

        if self._check_valid_params():

            for param_set in self._params_set_list:

                param_key, param_type = param_set

                FLAG_VALUE = None

                LONG_FLAG = self._params_dict.get(param_key).get("long", None)
                SHRT_FLAG = self._params_dict.get(param_key).get("short", None)

                if (self.PREF_LONG_FLAG is True):

                    if (isinstance(LONG_FLAG, str)):
                        FLAG_VALUE = LONG_FLAG
                    else:
                        FLAG_VALUE = SHRT_FLAG
                else:
                    pass

                if (self.PREF_LONG_FLAG is False):
                    if (isinstance(SHRT_FLAG, str)):
                        FLAG_VALUE = SHRT_FLAG
                    else:
                        FLAG_VALUE = LONG_FLAG
                else:
                    pass

                if param_type == None:
                    sub_sequence.append(FLAG_VALUE)
                else:
                    sub_sequence.extend([FLAG_VALUE, param_type])

        return sub_sequence

    def _check_valid_params(self):
        """ Check if the nlp terms exist in the mapping dictionary """

        VALID_PARAMS = True

        for param_set in self._params_set_list:

            param_flag, param_arg = param_set

            FLAG_EXIST = self._params_dict.get(param_flag, False)

            if FLAG_EXIST:
                LONG_FLAG = self._params_dict.get(param_flag).get("long", None)
                SHRT_FLAG = self._params_dict.get(
                    param_flag).get("short", None)
                ARGS_LIST = self._params_dict.get(
                    param_flag).get("arg_format", None)
            else:
                LONG_FLAG = None
                SHRT_FLAG = None
                ARGS_LIST = None

            # Display error messages / inconsitancies and invalidate process
            if FLAG_EXIST in [None, np.nan]:
                print(f"    {param_flag}: Param not found.")
                VALID_PARAMS = False

            if (LONG_FLAG in [None, np.nan]) and (SHRT_FLAG in [None, np.nan]):
                print(f"    {param_flag}: Flag not found.")
                VALID_PARAMS = False

            if (param_arg == None) & isinstance(ARGS_LIST, list):
                print(f"    {param_flag}: Arg required but not found.")
                VALID_PARAMS = False

            if (param_arg != None) & ~isinstance(ARGS_LIST, list):
                print(
                    f"    {param_flag}: Arg ({param_arg}) passed but does ({param_flag}) does not accept an arg.")
                VALID_PARAMS = False

        return VALID_PARAMS

    def _format_params(self):
        """ Gather the initial parameters for this call """

        """
        Partition the parameter list into expected format
            Expected format: [[param1, arg_type],[param2, arg_type]]
        """

        params_set_list = []

        for param in self._params_list:

            if isinstance(param, list):
                self._params_set_list.append(param)
            else:
                self._params_set_list.append([param, None])



    def get_result(self):
        """ Gather the proper argument string for this call """

        sub_sequence = self._map_params()
        self._command_seq = " ".join(sub_sequence)

        return self._command_seq
