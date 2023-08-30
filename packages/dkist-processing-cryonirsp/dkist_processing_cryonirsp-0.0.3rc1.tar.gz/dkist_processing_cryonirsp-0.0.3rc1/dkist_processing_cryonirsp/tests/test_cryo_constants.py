from dataclasses import asdict
from dataclasses import dataclass

import pytest

from dkist_processing_cryonirsp.tasks.cryonirsp_base import CryonirspTaskBase


@pytest.fixture(scope="function")
def testing_constants(polarimetric):
    @dataclass
    class testing_constants:
        # obs_ip_start_time: str = "1999-12-31T23:59:59"
        num_modstates: int = 10 if polarimetric else 1
        num_beams: int = 2
        num_cs_steps: int = 18
        num_scan_steps: int = 1000
        wavelength: float = 1082.0
        lamp_gain_exposure_times: tuple[float] = (100.0,)
        solar_gain_exposure_times: tuple[float] = (1.0,)
        observe_exposure_times: tuple[float] = (0.01,)
        modulator_spin_mode: str = "Continuous" if polarimetric else "Off"
        # We don't need all the common ones, but let's put one just to check
        instrument: str = "CHECK_OUT_THIS_INSTRUMENT"
        arm_id: str = "SP"

    return testing_constants()


@pytest.fixture(scope="function")
def expected_constant_dict(testing_constants) -> dict:
    lower_dict = asdict(testing_constants)
    return {k.upper(): v for k, v in lower_dict.items()}


@pytest.fixture(scope="function")
def cryo_science_task_with_constants(
    recipe_run_id, expected_constant_dict, init_cryonirsp_constants_db
):
    class Task(CryonirspTaskBase):
        def run(self):
            ...

    init_cryonirsp_constants_db(recipe_run_id, expected_constant_dict)
    task = Task(
        recipe_run_id=recipe_run_id,
        workflow_name="parse_cryo_input_data",
        workflow_version="VX.Y",
    )

    yield task

    task.constants._purge()


@pytest.mark.parametrize(
    "polarimetric",
    [pytest.param(True, id="Polarimetric"), pytest.param(False, id="Spectrographic")],
)
def test_cryo_constants(cryo_science_task_with_constants, expected_constant_dict, polarimetric):
    task = cryo_science_task_with_constants
    for k, v in expected_constant_dict.items():
        if k.lower() == "modulator_spin_mode":
            continue
        if type(v) is tuple:
            v = list(v)
        assert getattr(task.constants, k.lower()) == v
    assert task.constants.correct_for_polarization == polarimetric
