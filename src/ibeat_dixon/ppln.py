from miblab import pipe

import ibeat_dixon as ppln


PIPELINE = 'dixon'

def run(build, client):
    
    ppln.stage_1_download.run(build)


if __name__=='__main__':

    BUILD = r"C:\Users\md1spsx\Documents\Data\iBEAt_Build"
    pipe.run_dask_script(run, BUILD, PIPELINE, min_ram_per_worker = 4.0)