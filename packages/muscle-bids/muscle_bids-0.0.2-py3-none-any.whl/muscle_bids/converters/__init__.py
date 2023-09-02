from .mese_siemens import MeSeConverterSiemensMagnitude
from .megre_ge import MeGreConverterGEMagnitude, MeGreConverterGEPhase, MeGreConverterGEReal, \
    MeGreConverterGEImaginary, MeGreConverterGEReconstructedMap
from .mese_philips import MeSeConverterPhilipsMagnitude, MeSeConverterPhilipsPhase, MeSeConverterPhilipsReconstructedMap
from .quantitative_maps import T1Converter, T2Converter, FFConverter, B0Converter, B1Converter

converter_list = [
    MeSeConverterSiemensMagnitude,
    MeGreConverterGEMagnitude,
    MeGreConverterGEPhase,
    MeGreConverterGEReal,
    MeGreConverterGEImaginary,
    MeGreConverterGEReconstructedMap,
    MeSeConverterPhilipsMagnitude,
    MeSeConverterPhilipsPhase,
    MeSeConverterPhilipsReconstructedMap
]