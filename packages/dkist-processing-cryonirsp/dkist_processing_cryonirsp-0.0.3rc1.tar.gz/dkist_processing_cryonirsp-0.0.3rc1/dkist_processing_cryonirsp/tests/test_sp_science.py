import json
import random
from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pytest
from astropy.io import fits
from astropy.time import Time
from astropy.time import TimeDelta
from dkist_header_validator import spec122_validator
from dkist_processing_common._util.scratch import WorkflowFileSystem
from dkist_processing_common.tests.conftest import FakeGQLClient

from dkist_processing_cryonirsp.models.tags import CryonirspStemName
from dkist_processing_cryonirsp.models.tags import CryonirspTag
from dkist_processing_cryonirsp.tasks.sp_science import CalibrationCollection
from dkist_processing_cryonirsp.tasks.sp_science import SPScienceCalibration
from dkist_processing_cryonirsp.tests.conftest import cryonirsp_testing_parameters_factory
from dkist_processing_cryonirsp.tests.conftest import CryonirspConstantsDb
from dkist_processing_cryonirsp.tests.conftest import CryonirspHeadersValidObserveFrames
from dkist_processing_cryonirsp.tests.conftest import generate_fits_frame

# from dkist_processing_common.models.tags import Tag


@pytest.fixture(scope="function", params=["Full Stokes", "Stokes-I"])
def sp_science_calibration_task(
    tmp_path,
    recipe_run_id,
    assign_input_dataset_doc_to_task,
    init_cryonirsp_constants_db,
    request,
):
    num_map_scans = 2
    num_beams = 2
    num_scan_steps = 2
    exposure_time = 0.02  # From CryonirspHeadersValidObserveFrames fixture
    if request.param == "Full Stokes":
        num_modstates = 2
    else:
        num_modstates = 1
    array_shape = (1, 30, 60)
    intermediate_shape = (30, 30)
    dataset_shape = (num_beams * num_map_scans * num_scan_steps * num_modstates,) + array_shape[1:]

    constants_db = CryonirspConstantsDb(
        NUM_MODSTATES=num_modstates,
        NUM_MAP_SCANS=num_map_scans,
        NUM_SCAN_STEPS=num_scan_steps,
        NUM_BEAMS=num_beams,
        OBSERVE_EXPOSURE_TIMES=(exposure_time,),
        MODULATOR_SPIN_MODE="Continuous" if request.param == "Full Stokes" else "Off",
    )
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with SPScienceCalibration(
        recipe_run_id=recipe_run_id, workflow_name="sp_science_calibration", workflow_version="VX.Y"
    ) as task:
        try:  # This try... block is here to make sure the dbs get cleaned up if there's a failure in the fixture
            all_zeros = np.zeros(intermediate_shape)
            all_ones = np.ones(intermediate_shape)
            task.scratch = WorkflowFileSystem(
                scratch_base_path=tmp_path, recipe_run_id=recipe_run_id
            )
            param_class = cryonirsp_testing_parameters_factory(param_path=tmp_path)
            assign_input_dataset_doc_to_task(task, param_class())
            # Create fake bad pixel map
            task.intermediate_frame_write_arrays(
                arrays=np.zeros((1, 1)),
                task_tag=CryonirspTag.task_bad_pixel_map(),
            )
            # Create fake demodulation matrices
            demod_matrices = np.zeros((1, 1, 4, num_modstates))
            for modstate in range(num_modstates):
                demod_matrices[0, 0, :, modstate] = [1, 2, 3, 4]
            for beam in range(num_beams):
                demod_hdul = fits.HDUList([fits.PrimaryHDU(data=demod_matrices)])
                task.fits_data_write(
                    hdu_list=demod_hdul,
                    tags=[
                        CryonirspTag.intermediate(),
                        CryonirspTag.frame(),
                        CryonirspTag.task_demodulation_matrices(),
                        CryonirspTag.beam(beam + 1),
                    ],
                )

            # Create fake geometric objects
            angle = np.array([0.0])
            offset = np.array([-10.2, 5.1])
            spec_shift = np.zeros(intermediate_shape[0])
            for beam in range(1, num_beams + 1):
                task.intermediate_frame_write_arrays(
                    arrays=angle, beam=beam, task_tag=CryonirspTag.task_geometric_angle()
                )
                task.intermediate_frame_write_arrays(
                    arrays=spec_shift,
                    beam=beam,
                    task_tag=CryonirspTag.task_geometric_sepectral_shifts(),
                )
                for modstate in range(1, num_modstates + 1):
                    task.intermediate_frame_write_arrays(
                        arrays=offset
                        * (beam - 1),  # Because we need the fiducial array to have (0, 0) offset
                        beam=beam,
                        modstate=modstate,
                        task_tag=CryonirspTag.task_geometric_offset(),
                    )

            # Create fake dark intermediate arrays
            for beam in range(1, num_beams + 1):
                task.intermediate_frame_write_arrays(
                    all_zeros,
                    beam=beam,
                    task_tag=CryonirspTag.task_dark(),
                    exposure_time=exposure_time,
                )

            # And a beam border intermediate array
            for beam in range(1, num_beams + 1):
                task.intermediate_frame_write_arrays(
                    arrays=np.array([0, 30, ((beam - 1) * 30), (30 + (beam - 1) * 30)]),
                    task_tag=CryonirspTag.task_beam_boundaries(),
                    beam=beam,
                )

            # Create fake lamp and solar gain intermediate arrays
            for beam in range(1, num_beams + 1):
                for modstate in range(1, num_modstates + 1):
                    gain_hdul = fits.HDUList([fits.PrimaryHDU(data=all_ones)])
                    task.fits_data_write(
                        hdu_list=gain_hdul,
                        tags=[
                            CryonirspTag.intermediate(),
                            CryonirspTag.frame(),
                            CryonirspTag.task_lamp_gain(),
                            CryonirspTag.beam(beam),
                            CryonirspTag.modstate(modstate),
                        ],
                    )

                    task.fits_data_write(
                        hdu_list=gain_hdul,
                        tags=[
                            CryonirspTag.intermediate(),
                            CryonirspTag.frame(),
                            CryonirspTag.task_solar_gain(),
                            CryonirspTag.beam(beam),
                            CryonirspTag.modstate(modstate),
                        ],
                    )

            # Create fake observe arrays
            start_time = datetime.now()
            for map_scan in range(1, num_map_scans + 1):
                for scan_step in range(1, num_scan_steps + 1):
                    for modstate in range(1, num_modstates + 1):
                        ds = CryonirspHeadersValidObserveFrames(
                            dataset_shape=dataset_shape,
                            array_shape=array_shape,
                            time_delta=10,
                            scan_step=scan_step,
                            num_scan_steps=num_scan_steps,
                            num_map_scans=num_map_scans,
                            map_scan=map_scan,
                            num_modstates=num_modstates,
                            modstate=modstate,
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
                            header_generator=header_generator, shape=array_shape
                        )
                        header = hdul[0].header
                        task.fits_data_write(
                            hdu_list=hdul,
                            tags=[
                                CryonirspTag.task_observe(),
                                CryonirspTag.meas_num(1),
                                CryonirspTag.scan_step(scan_step),
                                CryonirspTag.map_scan(map_scan),
                                CryonirspTag.modstate(modstate),
                                CryonirspTag.linearized(),
                                CryonirspTag.frame(),
                                CryonirspTag.exposure_time(exposure_time),
                            ],
                        )

            yield task, request.param, offset, header, intermediate_shape
        finally:
            task.scratch.purge()
            task.constants._purge()


@pytest.fixture(scope="session")
def sp_headers_with_dates() -> tuple[list[fits.Header], str, int, int]:
    num_headers = 5
    start_time = "1969-12-06T18:00:00"
    exp_time = 12
    time_delta = 10
    ds = CryonirspHeadersValidObserveFrames(
        dataset_shape=(num_headers, 4, 4),
        array_shape=(1, 4, 4),
        time_delta=time_delta,
        num_map_scans=1,
        map_scan=1,
        num_scan_steps=1,
        scan_step=1,
        num_modstates=num_headers,
        modstate=1,
        start_time=datetime.fromisoformat(start_time),
        num_meas=1,
        meas_num=1,
        arm_id="SP",
    )
    headers = [
        spec122_validator.validate_and_translate_to_214_l0(d.header(), return_type=fits.HDUList)[
            0
        ].header
        for d in ds
    ]
    random.shuffle(headers)  # Shuffle to make sure they're not already in time order
    for h in headers:
        h["XPOSURE"] = exp_time  # Exposure time, in ms

    return headers, start_time, exp_time, time_delta


@pytest.fixture(scope="session")
def sp_compressed_headers_with_dates(
    sp_headers_with_dates,
) -> tuple[list[fits.Header], str, int, int]:
    headers, start_time, exp_time, time_delta = sp_headers_with_dates
    comp_headers = [fits.hdu.compressed.CompImageHeader(h, h) for h in headers]
    return comp_headers, start_time, exp_time, time_delta


@pytest.fixture(scope="function")
def sp_calibration_collection_with_geo_shifts(shifts) -> CalibrationCollection:
    num_beams, num_mod, _ = shifts.shape
    geo_shifts = {
        str(b + 1): {f"m{m + 1}": shifts[b, m, :] for m in range(num_mod)} for b in range(num_beams)
    }
    return CalibrationCollection(
        dark=dict(),
        angle=dict(),
        state_offset=geo_shifts,
        spec_shift=dict(),
        demod_matrices=None,
    )


def test_sp_science_calibration_task(sp_science_calibration_task, mocker):
    """
    Given: A SPScienceCalibration task
    When: Calling the task instance
    Then: There are the expected number of science frames with the correct tags applied and the headers have been correctly updated
    """

    mocker.patch(
        "dkist_processing_common.tasks.mixin.metadata_store.GraphQLClient", new=FakeGQLClient
    )

    # When
    task, polarization_mode, offset, og_header, og_single_beam_shape = sp_science_calibration_task
    task()

    # 1 from re-dummification
    expected_final_shape = (
        1,
        og_single_beam_shape[0],
        og_single_beam_shape[1],
    )

    # Then
    tags = [
        CryonirspTag.calibrated(),
        CryonirspTag.frame(),
    ]
    files = list(task.read(tags=tags))
    if polarization_mode == "Full Stokes":
        # 2 raster steps * 2 map scans * 4 stokes params = 16 frames
        assert len(files) == 16
    elif polarization_mode == "Stokes-I":
        # 2 raster steps * 2 map scans * 1 stokes param = 4 frames
        assert len(files) == 4
    for file in files:
        hdul = fits.open(file)
        assert len(hdul) == 1
        hdu = hdul[0]
        assert type(hdul[0]) is fits.PrimaryHDU
        assert hdu.data.shape == expected_final_shape
        assert "DATE-BEG" in hdu.header.keys()
        assert "DATE-END" in hdu.header.keys()

        # Check that scan step keys were updated
        scan_step = [
            int(t.split("_")[-1]) for t in task.tags(file) if CryonirspStemName.scan_step.value in t
        ][0]

        assert hdu.header["CNNUMSCN"] == 2
        assert hdu.header["CNCURSCN"] == scan_step

        # Check that WCS keys were updated
        if offset[0] > 0:
            assert hdu.header["CRPIX2"] == og_header["CRPIX2"]
        if offset[1] > 0:
            assert hdu.header["CRPIX1"] == og_header["CRPIX1"]

    quality_files = task.read(tags=[CryonirspTag.quality("TASK_TYPES")])
    for file in quality_files:
        with file.open() as f:
            data = json.load(f)
            assert isinstance(data, dict)
            assert data["total_frames"] == task.scratch.count_all(
                tags=[CryonirspTag.linearized(), CryonirspTag.frame(), CryonirspTag.task_observe()]
            )


def test_compute_sp_date_keys(sp_headers_with_dates, recipe_run_id, init_cryonirsp_constants_db):
    """
    Given: A set of SP headers with different DATE-OBS values
    When: Computing the time over which the headers were taken
    Then: A header with correct DATE-BEG, DATE-END, and DATE-AVG keys is returned
    """
    headers, start_time, exp_time, time_delta = sp_headers_with_dates
    constants_db = CryonirspConstantsDb()
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with SPScienceCalibration(
        recipe_run_id=recipe_run_id, workflow_name="science_calibration", workflow_version="VX.Y"
    ) as task:
        final_header = task._compute_date_keys(headers)
        final_header_from_single = task._compute_date_keys(headers[0])

    date_end = (
        Time(start_time)
        + (len(headers) - 1) * TimeDelta(time_delta, format="sec")
        + TimeDelta(exp_time / 1000.0, format="sec")
    ).isot

    assert final_header["DATE-BEG"] == start_time
    assert final_header["DATE-END"] == date_end

    date_end_from_single = (
        Time(headers[0]["DATE-BEG"])
        # + TimeDelta(time_delta, format="sec")
        + TimeDelta(exp_time / 1000.0, format="sec")
    ).isot

    assert final_header_from_single["DATE-BEG"] == headers[0]["DATE-BEG"]
    assert final_header_from_single["DATE-END"] == date_end_from_single


def test_compute_sp_date_keys_compressed_headers(
    sp_compressed_headers_with_dates, recipe_run_id, init_cryonirsp_constants_db
):
    """
    Given: A set of SP compressed headers with different DATE-OBS values
    When: Computing the time over which the headers were taken
    Then: A header with correct DATE-BEG, DATE-END, and DATE-AVG keys is returned
    """
    headers, start_time, exp_time, time_delta = sp_compressed_headers_with_dates
    constants_db = CryonirspConstantsDb()
    init_cryonirsp_constants_db(recipe_run_id, constants_db)
    with SPScienceCalibration(
        recipe_run_id=recipe_run_id, workflow_name="science_calibration", workflow_version="VX.Y"
    ) as task:
        final_header = task._compute_date_keys(headers)
        final_header_from_single = task._compute_date_keys(headers[0])

    date_end = (
        Time(start_time)
        + (len(headers) - 1) * TimeDelta(time_delta, format="sec")
        + TimeDelta(exp_time / 1000.0, format="sec")
    ).isot

    assert final_header["DATE-BEG"] == start_time
    assert final_header["DATE-END"] == date_end

    date_end_from_single = (
        Time(headers[0]["DATE-BEG"]) + TimeDelta(exp_time / 1000.0, format="sec")
    ).isot

    assert final_header_from_single["DATE-BEG"] == headers[0]["DATE-BEG"]
    assert final_header_from_single["DATE-END"] == date_end_from_single
