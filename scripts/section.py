import re
import typing

from group import Group
from exceptions import *
from problem_tracker import ProblemTracker


class Section:
    _RAW_VALUE_TYPE       = bool | int | str
    _RAW_VALUE_LIST_TYPE  = list[_RAW_VALUE_TYPE]
    
    _RAW_OPTION_TYPE      = tuple[str, _RAW_VALUE_TYPE|_RAW_VALUE_LIST_TYPE]
    _RAW_OPTION_LIST_TYPE = list[_RAW_OPTION_TYPE]
    
    _RAW_SECTION_TYPE     = tuple[str, _RAW_OPTION_LIST_TYPE]
    RAW_SECTION_LIST_TYPE = list[_RAW_SECTION_TYPE]
    
    
    def __ini__(self, raw_section: _RAW_SECTION_TYPE) -> None:
        self.full_name, self._raw_options = raw_section
        # self.name, *self.subnames = self.full_name.split(':')
        # doesn't seem to work with type hinting -
        # self.subnames is list[str] but marked Unknown
        name, *subnames = self.full_name.split(':')
        self.name, self.subnames = name, subnames
        
        self._options_are_set = False
        self._options: dict[str, set[str]] = dict()
        
    @property
    def first_subname_parameters(self) -> set[str]:
        if not self.subnames:
            return set()
    
        first_subname = self.subnames[0]
        parameter_names = Group(first_subname.split('-'))
        
        for repeated_parameter in parameter_names.repeated:
            ProblemTracker.print_warning(
                f"Duplicate parameters '{repeated_parameter}' "
                f"in the first subname '{first_subname}' "
                f"of the [{self.full_name}] section are ambiguous! It will be ignored."
            )
            
        return parameter_names.distinct
    
    def is_potential_ts(self, ts_names: set[str]) -> bool:
        return self.name in ts_names and len(self.subnames) == 1
    
    def get_option(self, option_name: str) -> set[str]|None:
        if not self._options_are_set:
            self._set_options()
        
        return self._options.get(option_name)
    
    def _set_options(self) -> None:
        problem_tracker = ProblemTracker(IniDuplicateOptions)
        
        for raw_option in self._raw_options:
            self._set_option(raw_option, problem_tracker)
            
        problem_tracker.raise_error_if_found(
            "{errors_found} errors found during options parsing!"
        )
        
        self._options_are_set = True
        
    def _set_option(
        self,
        raw_option: _RAW_OPTION_TYPE,
        problem_tracker: ProblemTracker
    ) -> None:
        option_name, option_value = raw_option
        
        if option_name in self._options:
            problem_tracker.print_error(
                f"Duplicate '{option_name}' options "
                f"in the [{self.full_name}] section are ambiguous!"
            )
        
        if isinstance(option_value, str):
            values = option_value.strip('\n')
            
            SEPARATORS = ['\n', ',']
            RE_PATTERN = '[{}]'.format(''.join(SEPARATORS))
            
            values = re.split(RE_PATTERN, values)
            values = typing.cast(list[str], values)
        elif isinstance(option_value, list):
            values = list(map(str, option_value))
        else:
            values = [str(option_value)]
            
        formatted_values = Group(map(str.strip, values))
        
        for repeated_value in formatted_values.repeated:
            ProblemTracker.print_warning(
                f"Duplicate '{repeated_value}' values in the '{option_name}' option "
                f"of the [{self.full_name}] section are ambiguous! It will be ignored."
            )
            
        self._options[option_name] = formatted_values.distinct