
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class TerminalHelper:
        
    def print_to_terminal(self, column_values, column_spaces, color=bcolors.ENDC):
        line = ''
        for i in range(len(column_spaces)):
            line += column_values[i].ljust(column_spaces[i])
        line += column_values[-1]
        print(color+line+bcolors.ENDC)

    def print_list_of_dicts_as_graph(self, keys, data, color_rules=None, col_space=5):
        spacing = self._calculate_spacing(keys, data, col_space)
        self.print_to_terminal([key.upper() for key in keys], spacing)
        for item in data:
            values = [item[key] for key in keys]
            color = color_rules(item) if color_rules else bcolors.ENDC
            self.print_to_terminal(values, spacing, color)

    def _calculate_spacing(self, keys, data, col_space):
        widths = []
        for key in keys[:-1]:
            widths.append(max([len(x[key]) for x in data])+col_space)
        return widths



