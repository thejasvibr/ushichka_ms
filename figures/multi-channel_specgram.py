# -*- coding: utf-8 -*-
"""
Code to create the multi-channel, 2-panel figure in the Ushichka
preprint showing the single and multi-bat call situations. 

@author: Thejasvi Beleyur
License: MIT License
"""

import glob
import numpy as np 
import soundfile as sf
import matplotlib.pyplot as plt 
from matplotlib import gridspec
plt.rcParams['agg.path.chunksize'] = 10000

#%% 
# Import clear good single and multi-bat recording files
audio_files = glob.glob('MULTIWAV*')

fs = 192000
multibat_audio, _ = sf.read(audio_files[0], start=int(6*fs), stop=int(fs*6.2))
singlebat_audio, _ = sf.read(audio_files[1], start=int(0.4*fs), stop=int(0.6*fs))

#%%
# find the 'loudest part' of the audio by looking at the moving abs values
#multibat_rms = np.convolve(np.abs(multibat_audio[:,0]), np.ones(192*20),'same')
# singlebat_rms = np.convolve(np.abs(singlebat_audio[:,0]), np.ones(192*20),'same')

#%%
# plt.figure()
# plt.plot(np.linspace(0, multibat_rms.size/fs, multibat_rms.size), multibat_rms)
# plt.plot(np.linspace(0, singlebat_rms.size/fs, singlebat_rms.size), singlebat_rms)


#%%
# Function to make all spectrograms look the same

def get_vminmax(audio_data):
    '''

    Parameters
    ----------
    audio_data : list with np.arrays

    Returns
    -------
    vmin, vmax : float
        The global lowest and highest values amongst all channels  and all files. 
    '''
    all_vmin = []
    all_vmax = []
    for each_audio in audio_data:
        for channel in range(each_audio.shape[1]):
            spec, _, _,_ = plt.specgram(each_audio[:,channel], Fs=192000, NFFT=192,
                                      noverlap=190, mode='magnitude'); plt.close()
            all_vmin.append(spec.min())
            all_vmax.append(spec.max())
    vmin = np.min(all_vmin)
    vmax = np.max(all_vmax)
    return vmin, vmax
    
dB = lambda X: 20*np.log10(X)

def remove_all_spines():
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

def make_specgram(audio_channel, **kwargs):
    plt.specgram(audio_channel, Fs=192000, NFFT=192, noverlap=190,mode='magnitude', **kwargs);
    plt.yticks([]);plt.ylabel('');plt.xticks([]);
    plt.ylim(-10000,98000);plt.xlim(0,0.2)
    remove_all_spines()

#%%
#
vmin_val, vmax_val = get_vminmax([singlebat_audio, multibat_audio])
#%%
def put_yticks(silent=False):
    
    if not silent:
        plt.yticks([0,48000,96000],[0,'',96], fontsize=6)
    else:
        plt.yticks([0,48000,96000],['','',''], fontsize=6)
    plt.gca().tick_params(axis='y', pad=0.25)
        
def put_xticks():
    plt.xticks([0,0.1,0.2],[0,100,200], fontsize=6)
    plt.gca().tick_params(axis='x', pad=1)

#%% 
db_vmin = dB(vmin_val) -3
db_vmax = dB(vmax_val) + 3

label_x, label_y = 0.0, 1.1

kwargs = {'vmin':db_vmin, 'vmax':db_vmax}

fig0 = plt.figure(figsize=(7,3.5))


gs0 = gridspec.GridSpec(18, 41, figure=fig0)

col1_inds = list(range(1,22))
col2_inds = list(range(22,42))

gs_00 = fig0.add_subplot(gs0[1:5,col1_inds[0]:col1_inds[-1]])
gs_01 = fig0.add_subplot(gs0[1:5,col2_inds[0]:col2_inds[-1]])
gs_10 = fig0.add_subplot(gs0[5:9,col1_inds[0]:col1_inds[-1]])
gs_11 = fig0.add_subplot(gs0[5:9,col2_inds[0]:col2_inds[-1]])
gs_20 = fig0.add_subplot(gs0[9:13,col1_inds[0]:col1_inds[-1]])
gs_21 = fig0.add_subplot(gs0[9:13,col2_inds[0]:col2_inds[-1]])
gs_30 = fig0.add_subplot(gs0[13:17,col1_inds[0]:col1_inds[-1]])
gs_31 = fig0.add_subplot(gs0[13:17,col2_inds[0]:col2_inds[-1]])


# row 1
plt.sca(gs_00)
make_specgram(singlebat_audio[:,0], **kwargs)
plt.text(label_x, label_y, 'A', transform=plt.gca().transAxes, fontsize=8)
put_yticks()
plt.sca(gs_01)
make_specgram(multibat_audio[:,0], **kwargs)
put_yticks(True)
plt.text(label_x, label_y, 'B', transform=plt.gca().transAxes, fontsize=8)

# row 2

plt.sca(gs_10)
make_specgram(singlebat_audio[:,1], **kwargs)
put_yticks()
plt.sca(gs_11)
make_specgram(multibat_audio[:,1], **kwargs)
put_yticks(True)
#row 3
plt.sca(gs_20)
make_specgram(singlebat_audio[:,2], **kwargs)
put_yticks()
plt.sca(gs_21)
make_specgram(multibat_audio[:,2], **kwargs)
put_yticks(True)
#row 4
plt.sca(gs_30)
make_specgram(singlebat_audio[:,3], **kwargs)
put_yticks()
put_xticks()
plt.sca(gs_31)
make_specgram(multibat_audio[:,3], **kwargs)
put_xticks()
put_yticks(True)

# put global X and Y labels
plt.figtext(0.485,0.08, 'Time (ms)', fontsize=8)
plt.figtext(0.1,0.375, 'Frequency (kHz)', rotation=90, fontsize=8)

plt.savefig('single_multibat_specgram.png', bbox_inches='tight', dpi=600)

