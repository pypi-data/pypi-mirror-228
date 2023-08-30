from benchmark_apis.hpo.hpobench import HPOBench
from benchmark_apis.hpo.hpolib import HPOLib
from benchmark_apis.hpo.jahs import JAHSBench201
from benchmark_apis.hpo.lcbench import LCBench
from benchmark_apis.synthetic.branin import MFBranin
from benchmark_apis.synthetic.hartmann import MFHartmann


__version__ = "2.2.2"
__copyright__ = "Copyright (C) 2023 Shuhei Watanabe"
__licence__ = "Apache-2.0 License"
__author__ = "Shuhei Watanabe"
__author_email__ = "shuhei.watanabe.utokyo@gmail.com"
__url__ = "https://github.com/nabenabe0928/mfhpo-benchmark-api/"


__all__ = ["HPOBench", "HPOLib", "JAHSBench201", "LCBench", "MFBranin", "MFHartmann"]
