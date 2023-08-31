"""
converter provides the class EcostressToSentinelConverter
that can be used for converting the Ecostress spectral library
to Sentinel-2 responses.
"""

import itertools as it
from argparse import ArgumentParser
from pathlib import Path
from spectral import EcostressDatabase

from sentinel_toolkit.colorimetry import (
    sd_to_sentinel_numpy,
    get_well_known_illuminant_names,
    get_well_known_illuminant,
    get_illuminant_from_file
)
from sentinel_toolkit.ecostress import Ecostress
from sentinel_toolkit.srf import S2Srf, S2SrfOptions

_ECOSTRESS_DB_FILENAME = "ecostress.db"
_S2_SRF_FILENAME = "S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.1.xlsx"
_OUTPUT_FILENAME = "ecostress_sentinel_converted.csv"


class EcostressToSentinelConverter:
    """
    EcostressToSentinelConverter provides a way to convert
    all the examples from the Ecostress spectral library,
    which contain values in a given wavelength range,
    to Sentinel-2 responses saved to a CSV file.
    """

    def __init__(self, ecostress, s2_srf):
        self.ecostress = ecostress
        self.s2rf = s2_srf

    def convert_ecostress_to_sentinel_csv(self, s2_srf_options=None, illuminant=None, out=None):
        """
        Converts the ecostress library into Sentinel-2 responses csv.

        The converted values are written to a CSV file
        named sentinel_<A or B>.csv.

        Parameters
        ----------
        s2_srf_options : S2SrfOptions
            The satellite, band names and wavelength range.
            If satellite is missing, satellite 'A' will be used.
            If band ids are missing, all band ids will be used.
            If wavelength range is missing, (360, 830) will be used.
        illuminant : dict
            The illuminant distribution.
            If missing, D65 360-830 nm will be used.
        out : str
            The output filename.
            If missing, "sentinel_<A or B>.csv" will be used.
        """
        if s2_srf_options is None:
            s2_srf_options = S2SrfOptions(satellite='A', wavelength_range=(360, 830))

        satellite, band_ids, wavelength_range = s2_srf_options.unpack()

        band_names = self.s2rf.get_band_names(band_ids)

        output_filename = out if out is not None else f"sentinel_{satellite}.csv"

        spectrum_ids = self.ecostress.get_spectrum_ids(wavelength_range)

        with open(output_filename, 'w', encoding='utf-8') as sentinel_file:
            _write_heading_line(sentinel_file, band_names)
            for spectrum_id in spectrum_ids:
                spectral_data = self.ecostress.get_spectral_distribution_numpy(spectrum_id,
                                                                               wavelength_range)

                local_s2_srf_options = S2SrfOptions(
                    s2_srf_options.satellite,
                    s2_srf_options.band_ids,
                    _get_wavelength_range(spectral_data.wavelengths, wavelength_range)
                )

                sentinel_responses = sd_to_sentinel_numpy(spectral_data,
                                                          self.s2rf,
                                                          local_s2_srf_options,
                                                          illuminant)
                _write_sentinel_responses_line(sentinel_file, spectrum_id, sentinel_responses)


def _write_heading_line(sentinel_file, band_names):
    band_names_line = ','.join(band_names)
    sentinel_file.write(f"SpectrumID,{band_names_line}\n")


def _get_wavelength_range(spectral_data_wavelengths, wavelength_range):
    spectral_data_min_wavelength = spectral_data_wavelengths[0]
    spectral_data_max_wavelength = spectral_data_wavelengths[-1]

    start = max(wavelength_range[0], spectral_data_min_wavelength)
    end = min(wavelength_range[1], spectral_data_max_wavelength)

    return start, end


def _write_sentinel_responses_line(sentinel_file, spectrum_id, sentinel_responses):
    line = ','.join(it.repeat('{}', len(sentinel_responses) + 1)) + '\n'
    line = line.format(spectrum_id, *sentinel_responses)
    sentinel_file.write(line)


def _main():
    args = _parse_args()
    ecostress_db_filename = args.ecostress_db_filename
    s2_srf_filename = args.s2_srf_filename

    ecostress_db_path = Path(ecostress_db_filename)
    if not ecostress_db_path.is_file():
        error_msg = f'The provided ecostress db filename "{ecostress_db_path}" does not exist!'
        raise RuntimeError(error_msg)

    s2_srf_path = Path(s2_srf_filename)
    if not s2_srf_path.is_file():
        error_msg = f'The provided s2a_srf Excel filename "{s2_srf_path}" does not exist!'
        raise RuntimeError(error_msg)

    ecostress_db = EcostressDatabase(ecostress_db_filename)
    converter = EcostressToSentinelConverter(Ecostress(ecostress_db), S2Srf(s2_srf_filename))

    satellite = args.satellite
    band_ids = args.bands
    wavelength_range = (args.wavelength_start, args.wavelength_end)

    s2_srf_options = S2SrfOptions(satellite=satellite,
                                  band_ids=band_ids,
                                  wavelength_range=wavelength_range)

    illuminant = _get_illuminant(args.illuminant, args.illuminant_file, wavelength_range)
    out = args.out
    converter.convert_ecostress_to_sentinel_csv(s2_srf_options, illuminant=illuminant, out=out)


def _parse_args():
    parser = ArgumentParser(description="Ecostress to Sentinel-2 Converter")
    parser.add_argument('-e',
                        '--ecostress_db_filename',
                        required=False,
                        type=str,
                        default=_ECOSTRESS_DB_FILENAME,
                        help="Ecostress SQLite database filename")
    parser.add_argument('-s2',
                        '--s2_srf_filename',
                        required=False,
                        type=str,
                        default=_S2_SRF_FILENAME,
                        help="Sentinel-2 Spectral Response Functions Excel filename")
    parser.add_argument('-s',
                        '--satellite',
                        required=False,
                        type=str,
                        default='A',
                        help="Sentinel-2 Satellite Identifier - A or B."
                             " By default both satellites will be used.")
    parser.add_argument('-b',
                        '--bands',
                        nargs='*',
                        required=False,
                        type=int,
                        default=[1, 2, 3],
                        help="Sentinel-2 Bands Identifiers List - 0 - 12."
                             " By default bands 1, 2, 3 will be used.")
    parser.add_argument('-ws',
                        '--wavelength_start',
                        required=False,
                        type=int,
                        default=360,
                        help="The wavelength range start. Default is 360.")
    parser.add_argument('-we',
                        '--wavelength_end',
                        required=False,
                        type=int,
                        default=830,
                        help="The wavelength range end. Default is 830.")
    illuminant_group = parser.add_mutually_exclusive_group(required=False)
    supported_illuminants = ", ".join(get_well_known_illuminant_names())
    illuminant_group.add_argument('-i',
                                  '--illuminant',
                                  required=False,
                                  type=str,
                                  default='d65',
                                  help=f'The illuminant to use. One of: {supported_illuminants}')
    illuminant_group.add_argument('-if',
                                  '--illuminant_file',
                                  required=False,
                                  type=str,
                                  help='The illuminant file to use. File format: '
                                       '<wavelength> <value> <new_line>... i.e. 360 46.6383')
    parser.add_argument('-o',
                        '--out',
                        required=False,
                        type=str,
                        help="The filename that will be used to store the resulting csv.")
    return parser.parse_args()


def _get_illuminant(illuminant_name, illuminant_filename, wavelength_range):
    if illuminant_name is not None:
        return get_well_known_illuminant(illuminant_name, wavelength_range)
    return get_illuminant_from_file(illuminant_filename, wavelength_range)


if __name__ == "__main__":
    _main()
