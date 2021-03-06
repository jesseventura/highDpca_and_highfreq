# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 20:29:07 2017

@author: Jiacheng Z
"""
#----this correspond to question 4----
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from run import NOW
import pandas as pd

def main():
    N_WeeklyObs = 385

    file_loc = 'https://raw.githubusercontent.com/jiacheng0409/pca/master/HF_Data.csv'
    rwData = pd.read_csv(file_loc)

    SPY = rwData.iloc[:,0].as_matrix()
    AAPL = rwData.iloc[:, 1].as_matrix()
    DeltaSPY = np.diff(SPY, n=1)
    DeltaAAPL = np.diff(AAPL, n=1)
    Sq_DeltaSPY = np.square(DeltaSPY)
    Sq_DeltaAAPL = np.square(DeltaAAPL)
    VolLenWeekly = len(SPY)//N_WeeklyObs +1

    WeeklySpotVol = dict()
    WeeklySpotVol['SPY'] = np.array([0.0] * VolLenWeekly)
    WeeklySpotVol['AAPL'] = np.array([0.0] * VolLenWeekly)

    for idx in range(VolLenWeekly):
        if idx+N_WeeklyObs>len(SPY):
            WeeklyChunkSPY = Sq_DeltaSPY[idx*N_WeeklyObs:]
            WeeklyChunkAAPL = Sq_DeltaAAPL[idx*N_WeeklyObs:]
        else:
            WeeklyChunkSPY = Sq_DeltaSPY[idx*N_WeeklyObs:(idx + 1)*N_WeeklyObs]
            WeeklyChunkAAPL = Sq_DeltaAAPL[idx*N_WeeklyObs:(idx + 1)*N_WeeklyObs]

        WeeklySpotVol['SPY'][idx] = np.sum(WeeklyChunkSPY)
        WeeklySpotVol['AAPL'][idx] = np.sum(WeeklyChunkAAPL)

    plt.figure(figsize=(8, 6))
    plt.plot(WeeklySpotVol['AAPL'],label='AAPL High-frequency Volatility')
    plt.plot(WeeklySpotVol['SPY'], label='SPY High-frequency Volatility')
    plt.title('Fig.7 Weeekly Spot High-Frequency Volatility')
    plt.ylabel('Quadratic Covariance')
    plt.xlabel('No. of Week')
    plt.legend()
    plt.savefig('Fig_7.png')

    print('{0}\n[INFO] Finished calculating high-frequency weekly volatilities.'.
        format('=' * 20 + NOW() + '=' * 20))

    N_DailyObs = N_WeeklyObs/5
    VolLenDaily = len(SPY)//N_DailyObs+1
    DailySpotVol = dict()
    DailySpotVol['AAPL'] = np.array([0.0] * VolLenDaily)
    DailySpotVol['SPY'] = np.array([0.0] * VolLenDaily)
    for idx in range(VolLenDaily):
        if idx+N_DailyObs>len(SPY):
            DailyChunkSPY = Sq_DeltaSPY[idx*N_DailyObs:]
            DailyChunkAAPL = Sq_DeltaAAPL[idx*N_DailyObs:]
        else:
            DailyChunkSPY = Sq_DeltaSPY[idx*N_DailyObs:(idx + 1)*N_DailyObs]
            DailyChunkAAPL = Sq_DeltaAAPL[idx*N_DailyObs:(idx + 1)*N_DailyObs]

        DailySpotVol['SPY'][idx] = np.sum(DailyChunkSPY)
        DailySpotVol['AAPL'][idx] = np.sum(DailyChunkAAPL)

    DailySpotVol['SPY'] /= np.sqrt(N_DailyObs)
    DailySpotVol['AAPL'] /= np.sqrt(N_DailyObs)

    plt.figure(figsize=(8, 6))
    plt.plot(DailySpotVol['AAPL'],label='AAPL High-frequency Volatility')
    plt.plot(DailySpotVol['SPY'], label='SPY High-frequency Volatility')
    plt.title('Fig.8 Daily Spot High-Frequency Volatility')
    plt.ylabel('Quadratic Covariance')
    plt.xlabel('No. of Day')
    plt.legend()
    plt.savefig('Fig_8.png')

    print('{0}\n[INFO] Finished calculating high-frequency daily volatilities.'.
        format('=' * 20 + NOW() + '=' * 20))

    # -----------------------------------------------------------
    # ------------part 2, qeustion 4: jump estimation------------
    # -----------------------------------------------------------
    Delta = 1/float(N_DailyObs)

    Thresholds = dict()
    Thresholds['AAPL'] = np.array([0.0] * len(SPY))
    Thresholds['SPY'] = np.array([0.0] * len(SPY))

    AbsDelta = dict()
    AbsDelta['AAPL'] = np.abs(DeltaAAPL)
    AbsDelta['SPY'] = np.abs(DeltaSPY)

    for idx in range(VolLenDaily):
        if idx + N_DailyObs > len(SPY):
            DailyChunkSPY = AbsDelta['SPY'][idx * N_DailyObs:]
            ThisBiPowerSPY = np.sum(DailyChunkSPY[1:]*DailyChunkSPY[:-1]) * np.sqrt(2/np.pi)
            ThisSigmaSPY = ThisBiPowerSPY/np.sqrt(len(SPY)-idx*N_DailyObs)
            ThisThresholdSPY = 3*ThisSigmaSPY*Delta**0.49

            WeeklyChunkAAPL= AbsDelta['AAPL'][idx * N_DailyObs:]
            ThisBiPowerAAPL= np.sum(WeeklyChunkAAPL[1:] * WeeklyChunkAAPL[:-1]) * np.sqrt(2 / np.pi)
            ThisSigmaAAPL= ThisBiPowerAAPL/ np.sqrt(len(SPY)-idx*N_DailyObs)
            ThisThresholdAAPL= 3 * ThisSigmaAAPL* Delta ** 0.49

            Thresholds['SPY'][idx * N_DailyObs:] = ThisThresholdSPY
            Thresholds['AAPL'][idx * N_DailyObs:] = ThisThresholdAAPL
        else:
            DailyChunkSPY = AbsDelta['SPY'][idx * N_DailyObs:(idx + 1) * N_DailyObs]
            ThisBiPowerSPY = np.sum(DailyChunkSPY[1:] * DailyChunkSPY[:-1]) * np.sqrt(2 / np.pi)
            ThisSigmaSPY = np.sqrt(ThisBiPowerSPY / N_DailyObs)
            ThisThresholdSPY = 3 * ThisSigmaSPY

            DailyChunkAAPL = AbsDelta['AAPL'][idx * N_DailyObs:(idx + 1) * N_DailyObs]
            ThisBiPowerAAPL = np.sum(DailyChunkAAPL[1:] * DailyChunkAAPL[:-1]) * np.sqrt(2 / np.pi)
            ThisSigmaAAPL = np.sqrt(ThisBiPowerAAPL / N_DailyObs)
            ThisThresholdAAPL = 3 * ThisSigmaAAPL

            Thresholds['SPY'][idx * N_DailyObs:(idx + 1) * N_DailyObs] = ThisThresholdSPY
            Thresholds['AAPL'][idx * N_DailyObs:(idx + 1) * N_DailyObs] = ThisThresholdAAPL

    Jumps = dict()
    Jumps['SPY'] = np.array([np.nan]*len(DeltaSPY))
    JumpIndexSPY = AbsDelta['SPY'] > np.abs(Thresholds['SPY'][1:])
    Jumps['SPY'][JumpIndexSPY] = DeltaSPY[JumpIndexSPY]

    Jumps['AAPL'] = np.array([np.nan]*len(DeltaSPY))
    JumpIndexAAPL = AbsDelta['AAPL'] > np.abs(Thresholds['AAPL'][1:])
    Jumps['AAPL'][JumpIndexAAPL] = DeltaAAPL[JumpIndexAAPL]

    DeltaReturns = dict()
    DeltaReturns['SPY'] = DeltaSPY
    DeltaReturns['AAPL'] = DeltaAAPL

    plt.figure(figsize=(8, 6))
    f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
    for idy, axis in enumerate([ax1, ax2]):
        Key = Jumps.keys()[idy]
        thisJumpSerie = Jumps[Key]
        thisDeltaReturnserie = DeltaReturns[Key]
        XAxis = range(len(thisDeltaReturnserie))
        axis.scatter(x=XAxis, y=thisDeltaReturnserie, s=0.1, label='Spot Volitility for {}'.format(Key))
        axis.scatter(x=XAxis, y=thisJumpSerie, s=1.5, label='Estimated Jumps for {}'.format(Key))
        axis.legend()

    ax1.set_title('Fig.9 Daily '+r'$\Delta^NX_i$'+' and Estimated Jumps')
    plt.xlabel('No. of Obeservations')
    plt.savefig('Fig_9.png')

    # -----------------------------------------------------------
    # ---------part 3, qeustion 4: continuous estimation---------
    # -----------------------------------------------------------
    Continuous = dict()
    Continuous['AAPL'] = DeltaAAPL - np.nan_to_num(Jumps['AAPL'])
    Continuous['SPY'] = DeltaSPY- np.nan_to_num(Jumps['SPY'])
    WeeklyContinuousVol = dict()
    WeeklyContinuousVol['SPY'] = np.array([0.0] * VolLenWeekly)
    WeeklyContinuousVol['AAPL'] = np.array([0.0] * VolLenWeekly)

    for idx in range(VolLenWeekly):
        if idx + N_WeeklyObs > len(DeltaSPY):
            WeeklyChunkSPY = np.square(Continuous['SPY'][idx * N_WeeklyObs:])
            WeeklyChunkAAPL = np.square(Continuous['AAPL'][idx * N_WeeklyObs:])
        else:
            WeeklyChunkSPY = np.square(Continuous['SPY'][idx * N_WeeklyObs:(idx + 1) * N_WeeklyObs])
            WeeklyChunkAAPL= np.square(Continuous['AAPL'][idx * N_WeeklyObs:(idx + 1) * N_WeeklyObs])

        WeeklyContinuousVol['SPY'][idx] = np.sum(WeeklyChunkSPY)
        WeeklyContinuousVol['AAPL'][idx] = np.sum(WeeklyChunkAAPL)

    plt.figure(figsize=(8, 6))
    f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
    for idy, axis in enumerate([ax1, ax2]):
        Key = WeeklySpotVol.keys()[idy]
        thisRawVol = WeeklySpotVol[Key]
        thisConVol = WeeklyContinuousVol[Key]
        # XAxis = range(len(thisRawVol))
        axis.plot(thisRawVol, label='Volatility of {}, Mixture'.format(Key))
        axis.plot(thisConVol, label='Volatility of {}, Continuous'.format(Key))
        axis.legend()
    ax1.set_title('Fig.10 Continuous Weekly Volatilities')
    plt.xlabel('No. of Obeservations')
    plt.savefig('Fig_10.png')


if __name__ == '__main__':
    main()