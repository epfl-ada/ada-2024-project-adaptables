from dataclasses import dataclass
# The following Color Palette is color-blind friendly, as has been carefully curated from Tol and IBM's specialized palettes (https://davidmathlogic.com/colorblind/)
# You can play with it/visualize it here : https://coolors.co/88ccee-e69f00-cc79a7-f0e442-009e73-d55e00-882255-332288-4465ab-999999
COLOR_PALETTE = ["#88CCEE","#E69F00","#CC79A7","#F0E442","#009E73","#D55E00","#882255","#332288","#4465AB","#999999"]

@dataclass
class RunConfig:
    USE_MATPLOTLIB: bool

NOTEBOOK_RUNCONFIG = RunConfig(False)