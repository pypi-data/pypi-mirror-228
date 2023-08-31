import pandas as pd
import numpy as np
from vnpt import round_half_even
from decimal import Decimal

#region 声级数据计算
def calc_Leq(spl_series:pd.Series) -> float:
    '''
    功能：
        计算一组声级数据的等效声压级（Leq）
    参数：
        spl_series: pd.Series，声级数据
    返回值：
        Leq：float，计算得到的等效声压级（Leq）
    '''
    spl_arr = np.array(spl_series).astype(Decimal)
    Leq = 10 * np.log10(
                        np.mean(
                            np.power(10, 0.1 * spl_arr)))
    # print("保留小数前：",Leq)
    Leq = round_half_even(Leq, 1)
    # print("保留1位小数后：",Leq)
    return Leq

def calc_PSL(spl_series: pd.Series, percent_arr: list=[10, 50, 90]) -> dict:
    '''
    功能：
        计算一组数据的累积百分声级（percentile sound level, PSL）
    参数：
        spl_series: pd.Series，声级数据
        percent_arr: list，需要计算的百分位数列表，默认为 [10, 50, 90]
    返回值：
        result: dict，各百分位数所对应的累积百分声级（PSL）
    '''
    if len(spl_series):
        result = {}
        for idx, percent in enumerate(percent_arr):
            assert percent > 0 and percent < 100, f"百分位数需要在0到100之间: percent_arr[{idx}]={percent}"
            result[f'L{percent}'] = round_half_even(spl_series.quantile(1 - percent / 100), 1)
        return result
    else:
        print("spl_series长度为0")

def calc_LA(spl_series: pd.Series) -> dict:
    '''
    功能：
        计算监测声强时所需的各类声级数据，包括：L10、L50、L90、Leq、Lmax、Lmin、标准差(std)
    参数：
        spl_series: pd.Series，声级数据
    返回值：
        result: dict，记录了计算出的各类声级数据，{"L10": float, "L50": float, "L90": float,
                                                            "Leq": float, "Lmax": float, "Lmin": float, "std": float}
    '''
    if len(spl_series):
        # 调用函数 calc_PSL() 计算 L10、L50、L90
        result = calc_PSL(spl_series)
        # 调用函数 calc_Leq() 计算等效声压级（Leq）
        result['Leq'] = calc_Leq(spl_series)
        # 计算最大值、最小值、标准差
        result['Lmax'] = spl_series.max()
        result['Lmin'] = spl_series.min()
        result['std'] = round_half_even(spl_series.std(), 1)
        return result
#endregion

#region 噪声水平等级划分
def evalRoadLeq(Leq, is_day=True):
    '''
    道路交通噪声强度等级划分
    '''
    Day_Standard =[68, 70, 72, 74]
    Night_Standard =[58, 60, 62, 64]
    if is_day:
        std = Day_Standard
    else:
        std = Night_Standard    
    Levels = ['一级','二级','三级','四级','五级']
    Evaluations = ['好','较好','一般','较差','差']
    
    eval = f'{Levels[-1]}/{Evaluations[-1]}'
    
    for idx,s in enumerate(std):
        if Leq <= s:
            eval = f'{Levels[idx]}/{Evaluations[idx]}'
            break
    return eval, idx+1

def evalRegionLeq(Leq, is_day=True):
    '''
    区域噪声强度等级划分
    '''
    Day_Standard =[50, 55, 50, 65]
    Night_Standard =[40, 45, 50, 55]
    if is_day:
        std = Day_Standard
    else:
        std = Night_Standard    
    Levels = ['一级','二级','三级','四级','五级']
    Evaluations = ['好','较好','一般','较差','差']
    
    eval = f'{Levels[-1]}/{Evaluations[-1]}'
    
    for idx,s in enumerate(std):
        if Leq <= s:
            eval = f'{Levels[idx]}/{Evaluations[idx]}'
            break
    return eval, idx+1
#endregion