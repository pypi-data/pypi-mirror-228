from datetime import datetime

import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.make_movie_frames import SPMakeCryonirspMovieFrames
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidObserveFrames
from dkist_processing_cryonirsp.tests.conftest import generate_fits_frame


@pytest.fixture(scope="function")
def sp_movie_frames_task(tmp_path, recipe_run_id, init_cryonirsp_constants_db):
    map_scans = 3
    scan_steps = 2
    constants_db = CryonirspConstantsDb(
        NUM_SCAN_STEPS=scan_steps,
        NUM_MAP_SCANS=map_scans,
        TIME_OBS_LIST=(datetime.now().isoformat("T"),),
    )
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with SPMakeCryonirspMovieFrames(
        recipe_run_id=recipe_run_id, workflow_name="make_movie_frames", workflow_version="VX.Y"
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            task.axis_length = 3
            meas_num = 1  # Use only the first measurement if there are multiple measurements.
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            start_time = datetime.now()
            for stokes_state in ["I", "Q", "U", "V"]:
                for map_scan in range(1, map_scans + 1):
                    for scan_step in range(0, scan_steps + 1):
                        ds = CryonirspHeadersValidObserveFrames(
                            dataset_shape=(2, task.axis_length, task.axis_length),
                            array_shape=(1, task.axis_length, task.axis_length),
                            time_delta=10,
                            num_map_scans=map_scans,
                            map_scan=map_scan,
                            num_scan_steps=scan_steps,
                            scan_step=scan_step,
                            num_modstates=1,
                            modstate=1,
                            start_time=start_time,
                            num_meas=1,
                            meas_num=1,
                            arm_id="SP",
                        )
                        header_generator = (
                            spec122_validator.validate_and_translate_to_214_l0(
                                d.header(), return_type=fits.HDUList
                            )[0].header
                            for d in ds
                        )
                        hdul = generate_fits_frame(
                            header_generator=header_generator, shape=(1, 3, 3)
                        )
                        task.fits_data_write(
                            hdu_list=hdul,
                            tags=[
                                CryonirspTag.output(),
                                CryonirspTag.frame(),
                                CryonirspTag.map_scan(map_scan),
                                CryonirspTag.scan_step(scan_step),
                                CryonirspTag.stokes(stokes_state),
                                CryonirspTag.meas_num(meas_num),
                            ],
                        )
            yield task, map_scans, scan_steps
        finally:
            task.scratch.purge()
            task.constants._purge()


def test_sp_make_movie_frames(sp_movie_frames_task, mocker):
    """
    Given: A SPMakeCryonirspMovieFrames task
    When: Calling the task instance
    Then: a fits file is made for each scan containing the movie frame for that scan
    """
    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )
    task, map_scans, scan_steps = sp_movie_frames_task
    task()
    assert len(list(task.read(tags=[CryonirspTag.movie_frame()]))) == map_scans
    for filepath in task.read(tags=[CryonirspTag.movie_frame()]):
        assert filepath.exists()
        hdul = fits.open(filepath)
        assert hdul[0].header["INSTRUME"] == "CRYO-NIRSP"
        # Multiply by 2 because a single map is (axis_length, steps) but there are 4 stokes in a 2x2 array
        assert hdul[0].data.shape == (
            scan_steps * 2,
            task.axis_length * 2,
        )
