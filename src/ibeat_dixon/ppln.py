from miblab import pipe

import ibeat_dixon as ppln


PIPELINE = 'dixon'

def run(build):
    
    ppln.stage_1_download.run(build)
    ppln.stage_2_data_harmonization.run(build)


if __name__=='__main__':

    BUILD = r"C:\Users\md1spsx\Documents\Data\iBEAt_Build"
    pipe.run_script(run, BUILD, PIPELINE)