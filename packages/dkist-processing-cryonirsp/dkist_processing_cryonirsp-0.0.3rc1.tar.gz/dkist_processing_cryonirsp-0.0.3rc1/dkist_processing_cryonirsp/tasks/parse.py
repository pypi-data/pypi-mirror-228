"""Parse CryoNIRSP data."""
from typing import TypeVar

from dkist_processing_common.models.flower_pot import Stem
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.parsers.cs_step import CSStepFlower
from dkist_processing_common.parsers.cs_step import NumCSStepBud
from dkist_processing_common.parsers.single_value_single_key_flower import (
    SingleValueSingleKeyFlower,
)
from dkist_processing_common.parsers.time import ExposureTimeFlower
from dkist_processing_common.parsers.unique_bud import UniqueBud
from dkist_processing_common.tasks import default_constant_bud_factory
from dkist_processing_common.tasks import default_tag_flower_factory
from dkist_processing_common.tasks import ParseDataBase
from dkist_processing_common.tasks.mixin.input_dataset import InputDatasetMixin

from dkist_processing_cryonirsp.models.constants import CryonirspBudName
from dkist_processing_cryonirsp.models.parameters import CryonirspParameters
from dkist_processing_cryonirsp.models.tags import CryonirspStemName
from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.models.task_name import TaskName
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspL0FitsAccess
from dkist_processing_cryonirsp.parsers.cryonirsp_l0_fits_access import CryonirspRampFitsAccess
from dkist_processing_cryonirsp.parsers.map_repeats import MapScanFlower
from dkist_processing_cryonirsp.parsers.map_repeats import NumMapScansBud
from dkist_processing_cryonirsp.parsers.measurements import MeasurementNumberFlower
from dkist_processing_cryonirsp.parsers.measurements import NumberOfMeasurementsBud
from dkist_processing_cryonirsp.parsers.modstates import ModstateNumberFlower
from dkist_processing_cryonirsp.parsers.modstates import NumberOfModstatesBud
from dkist_processing_cryonirsp.parsers.polarimeter_mode import ModulatorSpinModeBud
from dkist_processing_cryonirsp.parsers.polcal_task import PolcalTaskFlower
from dkist_processing_cryonirsp.parsers.scan_step import NumberOfScanStepsBud
from dkist_processing_cryonirsp.parsers.scan_step import ScanStepNumberFlower
from dkist_processing_cryonirsp.parsers.task import CryonirspTaskTypeFlower
from dkist_processing_cryonirsp.parsers.time import CryonirspTaskExposureTimesBud
from dkist_processing_cryonirsp.parsers.time import CryonirspTimeObsBud
from dkist_processing_cryonirsp.parsers.wavelength import ObserveWavelengthBud

S = TypeVar("S", bound=Stem)


class ParseL0CryonirspRampData(ParseDataBase):
    """
    Parse CryoNIRSP ramp data (raw Cryo data) to prepare for Linearity Correction, after which the rest of the common parsing will occur.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    @property
    def fits_parsing_class(self):
        """FITS access class to be used with this task."""
        return CryonirspRampFitsAccess

    @property
    def constant_buds(self) -> list[S]:
        """Add CryoNIRSP specific constants to common constants."""
        return [
            UniqueBud(
                constant_name=CryonirspBudName.camera_readout_mode.value,
                metadata_key="camera_readout_mode",
            ),
            # Time Obs is the unique identifier for each ramp in the data set
            CryonirspTimeObsBud(),
            # This is used to determine which set of linearity correction tables to use.
            UniqueBud(constant_name=CryonirspBudName.arm_id.value, metadata_key="arm_id"),
            # Get the ROI 1 size and origin
            UniqueBud(
                constant_name=CryonirspBudName.roi_1_origin_x.value, metadata_key="roi_1_origin_x"
            ),
            UniqueBud(
                constant_name=CryonirspBudName.roi_1_origin_y.value, metadata_key="roi_1_origin_y"
            ),
            UniqueBud(
                constant_name=CryonirspBudName.roi_1_size_x.value, metadata_key="roi_1_size_x"
            ),
            UniqueBud(
                constant_name=CryonirspBudName.roi_1_size_y.value, metadata_key="roi_1_size_y"
            ),
        ]

    @property
    def tag_flowers(self) -> list[S]:
        """Add CryoNIRSP specific tags to common tags."""
        return [
            SingleValueSingleKeyFlower(
                tag_stem_name=CryonirspStemName.curr_frame_in_ramp.value,
                metadata_key="curr_frame_in_ramp",
            ),
            # time_obs is a unique identifier for all raw frames in a single ramp
            SingleValueSingleKeyFlower(
                tag_stem_name=CryonirspStemName.time_obs.value,
                metadata_key="time_obs",
            ),
        ]

    @property
    def tags_for_input_frames(self) -> list[Tag]:
        """Tags for the input data to parse."""
        return [Tag.input(), Tag.frame()]


class ParseL0CryonirspLinearizedData(ParseDataBase, InputDatasetMixin):
    """
    Parse linearity corrected CryoNIRSP input data to add common and Cryonirsp specific parameters.

    Parameters
    ----------
    recipe_run_id : int
        id of the recipe run used to identify the workflow run this task is part of
    workflow_name : str
        name of the workflow to which this instance of the task belongs
    workflow_version : str
        version of the workflow to which this instance of the task belongs

    """

    def __init__(
        self,
        recipe_run_id: int,
        workflow_name: str,
        workflow_version: str,
    ):
        super().__init__(
            recipe_run_id=recipe_run_id,
            workflow_name=workflow_name,
            workflow_version=workflow_version,
        )
        self.parameters = CryonirspParameters(self.input_dataset_parameters)

    @property
    def fits_parsing_class(self):
        """FITS access class to be used in this task."""
        return CryonirspL0FitsAccess

    @property
    def tags_for_input_frames(self) -> list[Tag]:
        """Tags for the linearity corrected input frames."""
        return [CryonirspTag.linearized(), CryonirspTag.frame()]

    @property
    def constant_buds(self) -> list[S]:
        """Add CryoNIRSP specific constants to common constants."""
        return default_constant_bud_factory() + [
            NumberOfModstatesBud(),
            ModulatorSpinModeBud(),
            NumMapScansBud(),
            NumberOfScanStepsBud(),
            NumberOfMeasurementsBud(),
            NumCSStepBud(self.parameters.max_cs_step_time_sec),
            ObserveWavelengthBud(),
            CryonirspTaskExposureTimesBud(
                stem_name=CryonirspBudName.lamp_gain_exposure_times.value,
                ip_task_type=TaskName.lamp_gain.value,
            ),
            CryonirspTaskExposureTimesBud(
                stem_name=CryonirspBudName.solar_gain_exposure_times.value,
                ip_task_type=TaskName.solar_gain.value,
            ),
            CryonirspTaskExposureTimesBud(
                stem_name=CryonirspBudName.observe_exposure_times.value,
                ip_task_type=TaskName.observe.value,
            ),
            CryonirspTaskExposureTimesBud(
                stem_name=CryonirspBudName.polcal_exposure_times.value,
                ip_task_type=TaskName.polcal.value,
            ),
            UniqueBud(constant_name=CryonirspBudName.axis_1_type.value, metadata_key="axis_1_type"),
            UniqueBud(constant_name=CryonirspBudName.axis_2_type.value, metadata_key="axis_2_type"),
            UniqueBud(constant_name=CryonirspBudName.axis_3_type.value, metadata_key="axis_3_type"),
        ]

    @property
    def tag_flowers(self) -> list[S]:
        """Add CryoNIRSP specific tags to common tags."""
        return default_tag_flower_factory() + [
            CryonirspTaskTypeFlower(),
            PolcalTaskFlower(),
            MapScanFlower(),
            ModstateNumberFlower(),
            ExposureTimeFlower(),
            CSStepFlower(max_cs_step_time_sec=self.parameters.max_cs_step_time_sec),
            ScanStepNumberFlower(),
            MeasurementNumberFlower(),
        ]
