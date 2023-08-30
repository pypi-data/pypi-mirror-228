"""CryoNIRSP tags."""
from enum import Enum

from dkist_processing_common.models.tags import StemName
from dkist_processing_common.models.tags import Tag

from dkist_processing_cryonirsp.models.task_name import CryonirspTaskName
from dkist_processing_cryonirsp.models.task_name import TaskName


class CryonirspStemName(str, Enum):
    """Controlled list of Tag Stems."""

    linearized = "LINEARIZED"
    beam = "BEAM"
    scan_step = "SCAN_STEP"
    curr_frame_in_ramp = "CURR_FRAME_IN_RAMP"
    time_obs = "TIME_OBS"
    meas_num = "MEAS_NUM"
    modstate = "MODSTATE"
    map_scan = "MAP_SCAN"


class CryonirspTag(Tag):
    """CryoNIRSP specific tag formatting."""

    @classmethod
    def beam(cls, beam_num: int) -> str:
        """
        Tags by beam number.

        Parameters
        ----------
        beam_num
            The beam number

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(CryonirspStemName.beam, beam_num)

    @classmethod
    def scan_step(cls, scan_step: int) -> str:
        """
        Tags by the current scan step number.

        Parameters
        ----------
        scan_step
            The current scan step number

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(CryonirspStemName.scan_step, scan_step)

    @classmethod
    def map_scan(cls, map_scan: int) -> str:
        """
        Tags by the current scan step number.

        Parameters
        ----------
        map_scan
            The current map_scan number

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(CryonirspStemName.map_scan, map_scan)

    @classmethod
    def modstate(cls, modstate: int) -> str:
        """
        Tags by the current modstate number.

        Parameters
        ----------
        modstate
            The current scan step number

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(CryonirspStemName.modstate, modstate)

    @classmethod
    def linearized(cls) -> str:
        """
        Tags for linearized frames.

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(CryonirspStemName.linearized)

    @classmethod
    def curr_frame_in_ramp(cls, curr_frame_in_ramp: int) -> str:
        """
        Tags based on the current frame number in the ramp.

        Parameters
        ----------
        curr_frame_in_ramp
            The current frame number for this ramp

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(CryonirspStemName.curr_frame_in_ramp, curr_frame_in_ramp)

    @classmethod
    def time_obs(cls, time_obs: str) -> str:
        """
        Tags by the observe date.

        Parameters
        ----------
        time_obs
            The observe time

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(CryonirspStemName.time_obs, time_obs)

    @classmethod
    def meas_num(cls, meas_num: int) -> str:
        """
        Tags by the measurement number.

        Parameters
        ----------
        meas_num
            The current measurement number

        Returns
        -------
        The formatted tag string
        """
        return cls.format_tag(CryonirspStemName.meas_num, meas_num)

    # TODO: These should all go into `*-common` at some point
    #######
    @classmethod
    def task_observe(cls) -> str:
        """Tags input observe objects."""
        return cls.format_tag(StemName.task, TaskName.observe.value)

    @classmethod
    def task_polcal(cls) -> str:
        """Tags input polcal objects."""
        return cls.format_tag(StemName.task, TaskName.polcal.value)

    @classmethod
    def task_dark(cls) -> str:
        """Tags intermediate dark calibration objects."""
        return cls.format_tag(StemName.task, TaskName.dark.value)

    @classmethod
    def task_lamp_gain(cls) -> str:
        """Tags intermediate lamp gain calibration objects."""
        return cls.format_tag(StemName.task, TaskName.lamp_gain.value)

    @classmethod
    def task_solar_gain(cls) -> str:
        """Tags intermediate solar gain calibration objects."""
        return cls.format_tag(StemName.task, TaskName.solar_gain.value)

    @classmethod
    def task_demodulation_matrices(cls) -> str:
        """Tags intermediate demodulation matric calibration objects."""
        return cls.format_tag(StemName.task, TaskName.demodulation_matrices.value)

    @classmethod
    def task_geometric_angle(cls) -> str:
        """Tags intermediate geometric angle calibration objects."""
        return cls.format_tag(StemName.task, TaskName.geometric_angle.value)

    @classmethod
    def task_geometric_offset(cls) -> str:
        """Tags intermediate geometric offset calibration objects."""
        return cls.format_tag(StemName.task, TaskName.geometric_offsets.value)

    @classmethod
    def task_geometric_sepectral_shifts(cls) -> str:
        """Tags intermediate geometric spectral shift calibration objects."""
        return cls.format_tag(StemName.task, TaskName.geometric_spectral_shifts.value)

    ########

    @classmethod
    def task_beam_boundaries(cls) -> str:
        """Tags intermediate beam boundary calibration objects."""
        return cls.format_tag(StemName.task, CryonirspTaskName.beam_boundaries.value)

    @classmethod
    def task_bad_pixel_map(cls) -> str:
        """Tags intermediate bad pixel map objects."""
        return cls.format_tag(StemName.task, CryonirspTaskName.bad_pixel_map.value)

    @classmethod
    def task_polcal_dark(cls) -> str:
        """Tags intermediate polcal dark calibration objects."""
        return cls.format_tag(StemName.task, CryonirspTaskName.polcal_dark.value)

    @classmethod
    def task_polcal_gain(cls) -> str:
        """Tags intermediate polcal gain calibration objects."""
        return cls.format_tag(StemName.task, CryonirspTaskName.polcal_gain.value)
