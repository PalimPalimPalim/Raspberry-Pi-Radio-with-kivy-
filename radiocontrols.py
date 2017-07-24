"""functions for controlling mpd/mpx radio via python"""

import subprocess


def reboot():
    """reboot pi"""
    subprocess.call('mpc stop', shell=True)
    subprocess.call('reboot', shell=True)

def poweroff():
    """shutdown pi"""
    subprocess.call('mpc stop', shell=True)
    subprocess.call('poweroff', shell=True)

def set_volume(val):
    """ change volume to val or increment if "+5" passed in e.g."""
    subprocess.call('mpc volume ' + str(int(val)), shell=True)

def get_volume():
    """returns volume as 'volume: ##%' """
    output = subprocess.check_output('mpc volume', shell=True)
    return output

def get_volume_num():
    """returns volume as ##"""
    volume_str = get_volume()
    return int(''.join(ele for ele in volume_str if ele.isdigit()))

def pause():
    """pause radio playing"""
    subprocess.call('mpc stop', shell=True)


def play():
    """pause radio playing
    returns song or radio station info"""
    output = subprocess.check_output('mpc play', shell=True)
    return output[0:output.find('\n')]

def toggle():
    """pause radio playing
    returns song or radio station info"""
    output = subprocess.check_output('mpc toggle', shell=True)
    return "playing" in output

def play_next():
    """play next station"""
    subprocess.call('mpc next', shell=True)

def play_previous():
    """play next station"""
    subprocess.call('mpc prev', shell=True)

def clear_stations():
    """clear mpc playlist of all stations"""
    subprocess.call('mpc clear', shell=True)

def add_station(weblink):
    """add station based on weblink"""
    subprocess.call('mpc add ' + weblink, shell=True)

def get_playing():
    output = subprocess.check_output('mpc status', shell=True)
    return "playing" in output

