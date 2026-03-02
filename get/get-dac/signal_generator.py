import numpy as np
import time
def get_sin_wave_amplitude(freq, time):
    t = 2*3.14*freq*time
    res = ((np.sin(t)[1])+1)/2
    return (res)

def wait_for_sampling_period(sampling_frequency):
    time.sleep(1/sampling_frequency)