"""Cryo instrument polarization task."""
from abc import ABC
from abc import abstractmethod
from collections import defaultdict

import numpy as np
from astropy.io import fits
from dkist_processing_math.arithmetic import divide_arrays_by_array
from dkist_processing_math.arithmetic import subtract_array_from_arrays
from dkist_processing_math.statistics import average_numpy_arrays
from dkist_processing_math.transform.binning import resize_arrays
from dkist_processing_pac.fitter.polcal_fitter import PolcalFitter
from dkist_processing_pac.input_data.drawer import Drawer
from dkist_processing_pac.input_data.dresser import Dresser
from logging42 import logger

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess
from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


class InstrumentPolarizationCalibrationBase(CryonirspTaskBase, ABC):
    """
    Base task class for instrument polarization for a CryoNIRSP calibration run.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    record_provenance = True

    @abstractmethod
    def record_polcal_quality_metrics(self, beam: int, polcal_fitter: PolcalFitter):
        """Abstract method to be implemented in subclass."""
        pass

    def run(self) -> None:
        """
        For each beam.

            - Reduce calibration sequence steps
            - Fit reduced data to PAC parameters
            - Compute and save demodulation matrices

        Returns
        -------
        None

        """
        if not self.constants.correct_for_polarization:
            return

        target_exp_times = self.constants.polcal_exposure_times
        logger.info(f"{target_exp_times = }")

        self.generate_polcal_dark_calibration(target_exp_times)
        self.generate_polcal_gain_calibration(target_exp_times)

        logger.info(
            f"Demodulation matrices will span FOV with shape {(self.parameters.polcal_num_spatial_bins, self.parameters.polcal_num_spatial_bins)}"
        )
        for beam in range(1, self.constants.num_beams + 1):
            with self.apm_processing_step(f"Reducing CS steps for {beam = }"):
                logger.info(f"Reducing CS steps for {beam = }")
                local_reduced_arrays, global_reduced_arrays = self.reduce_cs_steps(beam)

            with self.apm_processing_step(f"Fit CU parameters for {beam = }"):
                logger.info(f"Fit CU parameters for {beam = }")
                local_dresser = Dresser()
                local_dresser.add_drawer(Drawer(local_reduced_arrays))
                global_dresser = Dresser()
                global_dresser.add_drawer(Drawer(global_reduced_arrays))
                pac_fitter = PolcalFitter(
                    local_dresser=local_dresser,
                    global_dresser=global_dresser,
                    fit_mode=self.parameters.polcal_pac_fit_mode,
                    init_set=self.parameters.polcal_pac_init_set,
                    fit_TM=False,
                )

            with self.apm_processing_step(f"Resampling demodulation matrices for {beam = }"):
                demod_matrices = pac_fitter.demodulation_matrices
                # Reshaping the demodulation matrix to get rid of unit length dimensions
                logger.info(f"Resampling demodulation matrices for {beam = }")
                demod_matrices = self.reshape_demod_matrices(demod_matrices)
                logger.info(
                    f"Shape of resampled demodulation matrices for {beam = }: {demod_matrices.shape}"
                )

            with self.apm_writing_step(f"Writing demodulation matrices for {beam = }"):
                self.intermediate_frame_write_arrays(
                    demod_matrices,
                    beam=beam,
                    task_tag=CryonirspTag.task_demodulation_matrices(),
                )

            with self.apm_processing_step("Computing and recording polcal quality metrics"):
                self.record_polcal_quality_metrics(beam, polcal_fitter=pac_fitter)

        with self.apm_processing_step("Computing and logging quality metrics"):
            no_of_raw_polcal_frames: int = self.scratch.count_all(
                tags=[
                    CryonirspTag.linearized(),
                    CryonirspTag.frame(),
                    CryonirspTag.task_polcal(),
                ],
            )

            self.quality_store_task_type_counts(
                task_type=TaskName.polcal.value, total_frames=no_of_raw_polcal_frames
            )

    def reduce_cs_steps(
        self, beam: int
    ) -> tuple[dict[int, list[CryonirspL0FitsAccess]], dict[int, list[CryonirspL0FitsAccess]]]:
        """
        Reduce all of the data for the cal sequence steps for this beam.

        Parameters
        ----------
        beam
            The current beam being processed

        Returns
        -------
        Dict
            A Dict of calibrated and binned arrays for all the cs steps for this beam
        """
        local_reduced_array_dict = defaultdict(list)
        global_reduced_array_dict = defaultdict(list)

        for modstate in range(1, self.constants.num_modstates + 1):
            for exp_time in self.constants.polcal_exposure_times:
                logger.info(f"Loading dark array for {exp_time = } and {beam = }")
                try:
                    dark_array = self.intermediate_frame_load_polcal_dark_array(
                        exposure_time=exp_time,
                        beam=beam,
                    )
                except StopIteration as e:
                    raise ValueError(f"No matching dark array found for {exp_time = } s") from e

                logger.info(f"Loading gain array for {exp_time = } and {beam = }")
                try:
                    gain_array = self.intermediate_frame_load_polcal_gain_array(
                        exposure_time=exp_time, beam=beam
                    )
                except StopIteration as e:
                    raise ValueError(f"No matching gain array found for {exp_time = } s") from e

                for cs_step in range(self.constants.num_cs_steps):
                    local_obj, global_obj = self.reduce_single_step(
                        beam,
                        dark_array,
                        gain_array,
                        modstate,
                        cs_step,
                        exp_time,
                    )
                    local_reduced_array_dict[cs_step].append(local_obj)
                    global_reduced_array_dict[cs_step].append(global_obj)

        return local_reduced_array_dict, global_reduced_array_dict

    def reduce_single_step(
        self,
        beam: int,
        dark_array: np.ndarray,
        gain_array: np.ndarray,
        modstate: int,
        cs_step: int,
        exp_time: float,
    ) -> tuple[CryonirspL0FitsAccess, CryonirspL0FitsAccess]:
        """
        Reduce a single calibration step for this beam, cs step and modulator state.

        Parameters
        ----------
        beam : int
            The current beam being processed
        dark_array : np.ndarray
            The dark array for the current beam
        gain_array : np.ndarray
            The gain array for the current beam
        modstate : int
            The current modulator state
        cs_step : int
            The current cal sequence step
        exp_time : float
            The exposure time

        Returns
        -------
        The final reduced result for this single step
        """
        apm_str = f"{beam = }, {modstate = }, {cs_step = }, and {exp_time = }"
        logger.info(f"Reducing {apm_str}")

        pol_cal_headers = (
            obj.header
            for obj in self.linearized_frame_polcal_fits_access_generator(
                modstate=modstate, cs_step=cs_step, exposure_time=exp_time, beam=beam
            )
        )
        pol_cal_arrays = (
            obj.data
            for obj in self.linearized_frame_polcal_fits_access_generator(
                modstate=modstate, cs_step=cs_step, exposure_time=exp_time, beam=beam
            )
        )

        avg_inst_pol_cal_header = next(pol_cal_headers)
        avg_inst_pol_cal_array = average_numpy_arrays(pol_cal_arrays)

        with self.apm_processing_step(f"Apply basic corrections for {apm_str}"):
            dark_corrected_array = subtract_array_from_arrays(avg_inst_pol_cal_array, dark_array)
            gain_corrected_array = next(divide_arrays_by_array(dark_corrected_array, gain_array))

        with self.apm_processing_step(f"Extract macro pixels from {apm_str}"):
            self._set_original_beam_size(gain_corrected_array)
            output_shape = (
                self.parameters.polcal_num_spatial_bins,
                self.parameters.polcal_num_spectral_bins,
            )
            local_binned_array = next(resize_arrays(gain_corrected_array, output_shape))
            global_binned_array = next(resize_arrays(gain_corrected_array, (1, 1)))

        with self.apm_processing_step(f"Create reduced CryonirspL0FitsAccess for {apm_str}"):
            local_result = CryonirspL0FitsAccess(
                fits.ImageHDU(local_binned_array[:, :], avg_inst_pol_cal_header),
                auto_squeeze=False,
            )

            global_result = CryonirspL0FitsAccess(
                fits.ImageHDU(global_binned_array[None, :, :], avg_inst_pol_cal_header),
                auto_squeeze=False,
            )

        return local_result, global_result

    def reshape_demod_matrices(self, demod_matrices: np.ndarray) -> np.ndarray:
        """Upsample demodulation matrices to match the full beam size.

        Given an input set of demodulation matrices with shape (X', Y', 4, M) resample the output to shape
        (X, Y, 4, M), where X' and Y' are the binned size of the beam FOV, X and Y are the full beam shape, M is the
        number of modulator states.

        If only a single demodulation matrix was made then it is returned as a single array with shape (4, M).

        Parameters
        ----------
        demod_matrices
            A set of demodulation matrices with shape (X', Y', 4, M)

        Returns
        -------
        If X' and Y' > 1 then upsampled matrices that are the full beam size (X, Y, 4, M).
        If X' == Y' == 1 then a single matric for the whole FOV with shape (4, M)
        """
        expected_dims = 4
        if len(demod_matrices.shape) != expected_dims:
            raise ValueError(
                f"Expected demodulation matrices to have {expected_dims} dimensions. Got shape {demod_matrices.shape}"
            )

        data_shape = demod_matrices.shape[
            :2
        ]  # The non-demodulation matrix part of the larger array
        demod_shape = demod_matrices.shape[-2:]  # The shape of a single demodulation matrix
        logger.info(f"Demodulation FOV sampling shape: {data_shape}")
        logger.info(f"Demodulation matrix shape: {demod_shape}")
        if data_shape == (1, 1):
            # A single modulation matrix can be used directly, so just return it after removing extraneous dimensions
            logger.info(f"Single demodulation matrix detected")
            return demod_matrices[0, 0, :, :]

        target_shape = self.single_beam_shape + demod_shape
        logger.info(f"Target full-frame demodulation shape: {target_shape}")
        return self._resize_polcal_array(demod_matrices, target_shape)

    def _set_original_beam_size(self, array: np.ndarray) -> None:
        """Record the shape of a single beam as a class property."""
        self.single_beam_shape = array.shape

    @staticmethod
    def _resize_polcal_array(array: np.ndarray, output_shape: tuple[int, ...]) -> np.ndarray:
        return next(resize_arrays(array, output_shape))

    def generate_polcal_dark_calibration(self, target_exp_times):
        """Compute the polcal dark calibration."""
        with self.apm_task_step(f"Calculating dark frames for {len(target_exp_times)} exp times"):
            for exp_time in target_exp_times:
                for beam in range(1, self.constants.num_beams + 1):
                    logger.info(
                        f"Gathering linearity corrected polcal dark frames for {exp_time = } and {beam = }"
                    )
                    with self.apm_processing_step(
                        f"Calculating polcal dark array(s) for {exp_time = } and {beam = }"
                    ):
                        logger.info(
                            f"Calculating polcal dark array(s) for {exp_time = } and {beam = }"
                        )
                        linearized_dark_arrays = self.linearized_frame_polcal_dark_array_generator(
                            exposure_time=exp_time,
                            beam=beam,
                        )
                        averaged_dark_array = average_numpy_arrays(linearized_dark_arrays)
                        with self.apm_writing_step(f"Writing dark for {exp_time = } and {beam = }"):
                            logger.info(f"Writing dark for {exp_time = } and {beam = }")
                            self.intermediate_frame_write_arrays(
                                averaged_dark_array,
                                task_tag=CryonirspTag.task_polcal_dark(),
                                exposure_time=exp_time,
                                beam=beam,
                            )

    def generate_polcal_gain_calibration(self, exp_times):
        """Compute the polcal gain calibration."""
        with self.apm_task_step(f"Generate gains for {len(exp_times)} exposure times"):
            for exp_time in exp_times:
                for beam in range(1, self.constants.num_beams + 1):
                    logger.info(f"Load polcal dark array for {exp_time = } and {beam = }")
                    try:
                        dark_array = self.intermediate_frame_load_polcal_dark_array(
                            exposure_time=exp_time,
                            beam=beam,
                        )
                    except StopIteration as e:
                        raise ValueError(
                            f"No matching polcal dark found for {exp_time = } s and {beam = }"
                        ) from e

                    logger.info(
                        f"Gathering linearity corrected polcal gain frames for {exp_time = } and {beam = }"
                    )
                    with self.apm_processing_step(
                        f"Calculating polcal gain array(s) for {exp_time = } and {beam = }"
                    ):
                        logger.info(
                            f"Calculating polcal gain array(s) for {exp_time = } and {beam = }"
                        )
                        linearized_gain_arrays = self.linearized_frame_polcal_gain_array_generator(
                            exposure_time=exp_time,
                            beam=beam,
                        )
                        averaged_gain_array = average_numpy_arrays(linearized_gain_arrays)
                        dark_corrected_gain_array = next(
                            subtract_array_from_arrays(averaged_gain_array, dark_array)
                        )

                        bad_pixel_map = self.intermediate_frame_load_bad_pixel_map(beam=beam)
                        bad_pixel_corrected_array = self.corrections_correct_bad_pixels(
                            dark_corrected_gain_array, bad_pixel_map
                        )

                        normalized_gain_array = bad_pixel_corrected_array / np.mean(
                            bad_pixel_corrected_array
                        )

                    with self.apm_writing_step(
                        f"Writing gain array for exposure time {exp_time} and {beam = }"
                    ):
                        logger.info(f"Writing gain for {exp_time = }")
                        self.intermediate_frame_write_arrays(
                            normalized_gain_array,
                            task_tag=CryonirspTag.task_polcal_gain(),
                            exposure_time=exp_time,
                            beam=beam,
                        )


class CIInstrumentPolarizationCalibration(InstrumentPolarizationCalibrationBase):
    """
    Task class for instrument polarization for a CI CryoNIRSP calibration run.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    def record_polcal_quality_metrics(self, beam: int, polcal_fitter: PolcalFitter):
        """Record various quality metrics from PolCal fits."""
        self.quality_store_polcal_results(
            polcal_fitter=polcal_fitter,
            label=f"CryoNIRSP CI beam {beam}",
            bins_1=self.parameters.polcal_num_spatial_bins,
            bins_2=self.parameters.polcal_num_spatial_bins,
            bin_1_type="spatial",
            bin_2_type="spatial",
        )


class SPInstrumentPolarizationCalibration(InstrumentPolarizationCalibrationBase):
    """Task class for instrument polarization for an SP CryoNIRSP calibration run."""

    def record_polcal_quality_metrics(
        self,
        beam: int,
        polcal_fitter: PolcalFitter,
    ) -> None:
        """Record various quality metrics from PolCal fits."""
        self.quality_store_polcal_results(
            polcal_fitter=polcal_fitter,
            label=f"CryoNIRSP SP beam {beam}",
            bins_1=self.parameters.polcal_num_spatial_bins,
            bins_2=self.parameters.polcal_num_spectral_bins,
            bin_1_type="spatial",
            bin_2_type="spectral",
        )
