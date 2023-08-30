import logging
import pytest
# import rompy

import sys
print(sys.path)

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

def test_catalog():
    import intake
    from intake.catalog import Catalog

    logging.info(intake.cat.rompy_data.discover())

    assert isinstance(intake.cat.rompy_data,Catalog)


def test_intake_local_stack():
    import rompy
    import intake
    import os

    mycat = intake.open_catalog(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','catalog.yaml'))
    ds = mycat.local_stack.to_dask()

    assert ds.time.shape == (2,121)

def test_intake_local_stack_single():
    import rompy
    import intake
    import os

    mycat = intake.open_catalog(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','catalog.yaml'))
    ds = mycat.local_stack_single.to_dask()

    assert ds.time.shape == (121,)

def test_intake_local_stack_single_time():
    import rompy
    import intake
    import os

    mycat = intake.open_catalog(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','catalog.yaml'))
    ds = mycat.local_stack_single_time.to_dask()

    assert ds.time.shape == (109,)

def test_intake_local_hindcast():
    import rompy
    import intake
    import os

    mycat = intake.open_catalog(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','catalog.yaml'))
    ds = mycat.local_hindcast.to_dask()

    assert ds.time.shape == (145,)

def test_intake_local_hindcast_single():
    import rompy
    import intake
    import os

    mycat = intake.open_catalog(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','catalog.yaml'))
    ds = mycat.local_hindcast_single.to_dask()

    assert ds.time.shape == (121,)

def test_intake_local_hindcast_single_time():
    import rompy
    import intake
    import os

    mycat = intake.open_catalog(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','catalog.yaml'))
    ds = mycat.local_hindcast_single_time.to_dask()

    assert ds.time.shape == (109,)

def test_intake_local_hindcast_time():
    import rompy
    import intake
    import os

    mycat = intake.open_catalog(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','catalog.yaml'))
    ds = mycat.local_hindcast_time.to_dask()

    assert ds.time.shape == (25,)

def test_intake_local_stack_time():
    import rompy
    import intake
    import os

    mycat = intake.open_catalog(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data','catalog.yaml'))
    ds = mycat.local_stack_time.to_dask()

    assert ds.time.shape == (2,49)

def test_intake_remote_stack():
    import rompy
    import pandas as pd
    ds=rompy.cat.bom.wavewatch3_nci(hindcast=False,
                                    fmt_fields={'fcdate':list(pd.date_range('2021-01-21','2021-01-22').strftime("%Y%m%d")),
                                                'hr':['0000'],
                                                'grid':['PER'],
                                                'output':['msh']}).to_dask()

    assert ds.time.shape == (2,169)

def test_intake_remote_hindcast():
    import rompy
    import pandas as pd
    ds=rompy.cat.bom.wavewatch3_nci(hindcast=True,
                                    fmt_fields={'fcdate':list(pd.date_range('2021-01-21','2021-01-22').strftime("%Y%m%d")),
                                                'hr':['0000'],
                                                'grid':['PER'],
                                                'output':['msh']}).to_dask()
    assert ds.time.shape == (193,)

def test_intake_aodn_wave_buoys_remote():
    import rompy
    df=rompy.cat.aodn.nrt_wave_buoys(startdt='2021-04-05',
                                     enddt='2021-04-29',
                                     geom='POLYGON ((111.0000000000000000 -33.0000000000000000, 111.0000000000000000 -31.5000000000000000, 115.8000030517578125 -31.5000000000000000, 115.8000030517578125 -33.0000000000000000, 111.0000000000000000 -33.0000000000000000))'
                                     ).read()

    assert len(df) == 94

def test_intake_aodn_altimetry_points_remote():
    import rompy
    df=rompy.cat.aodn.nrt_wave_altimetry_points(startdt='2020-02-03',
                                                enddt='2020-02-04',
                                                geom='POLYGON ((111.0000000000000000 -33.0000000000000000, 111.0000000000000000 -31.5000000000000000, 115.8000030517578125 -31.5000000000000000, 115.8000030517578125 -33.0000000000000000, 111.0000000000000000 -33.0000000000000000))'
                                                ).read()

    assert len(df) == 34

def test_intake_aodn_altimetry_remote_stack():
    import rompy
    ds=rompy.cat.aodn.nrt_wave_altimetry(startdt='2020-02-03',
                                         enddt='2020-02-04',
                                         geom='POLYGON ((111.0000000000000000 -33.0000000000000000, 111.0000000000000000 -31.5000000000000000, 115.8000030517578125 -31.5000000000000000, 115.8000030517578125 -33.0000000000000000, 111.0000000000000000 -33.0000000000000000))',
                                         ds_filters={'subset':{'data_vars':['SWH_C']}}).to_dask()

    assert ds.TIME.shape == (49,)

def test_intake_aodn_sar_points_remote():
    import rompy
    df=rompy.cat.aodn.nrt_wave_sar_points(startdt='2021-02-01',
                                          enddt='2021-04-29',
                                          geom='POLYGON ((111.0000000000000000 -33.0000000000000000, 111.0000000000000000 -31.5000000000000000, 115.8000030517578125 -31.5000000000000000, 115.8000030517578125 -33.0000000000000000, 111.0000000000000000 -33.0000000000000000))'
                                         ).read()

    assert len(df) == 28

def test_intake_aodn_sar_remote_stack():
    import rompy
    ds=rompy.cat.aodn.nrt_wave_sar(startdt='2021-03-01',
                                         enddt='2021-04-29',
                                         geom='POLYGON ((111.0000000000000000 -33.0000000000000000, 111.0000000000000000 -31.5000000000000000, 115.8000030517578125 -31.5000000000000000, 115.8000030517578125 -33.0000000000000000, 111.0000000000000000 -33.0000000000000000))',
                                         ds_filters={'subset':{'data_vars':['HS_PART']}}).to_dask()

    assert ds.TIME.shape == (10,)

if __name__ == '__main__':
    # test_intake_remote_stack()
    # test_intake_remote_hindcast()
    # test_intake_local()
    test_intake_local_hindcast_time()
    # test_intake_local_stack_single_time()

