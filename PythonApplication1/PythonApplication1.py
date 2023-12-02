# -*- coding: utf-8 -*-


"""
name:Congyi Xia
time:2022.06.15
"""

from iapws import IAPWS97 as ip
import math

N_e = 1000  # 核电厂输出电功率
η_1 = 0.99  # 一回路能量利用系数
x_fh = 0.9975  # 蒸汽发生器出口蒸汽干度
ξd = 0.0105  # 蒸汽发生器排污率
η_hi = 0.8207  # 高压缸内效率
η_li = 0.8359  # 低压缸内效率
η_m = 0.98  # 汽轮机组机械效率
η_ge = 0.98  # 发电机效率
θ_hu = 3  # 高压给水加热器出口端差
θ_lu = 2  # 低压给水加热器出口端差
η_h = 0.99  # 加热器效率
η_fwpp = 0.58  # 给水泵效率
η_fwpti = 0.8  # 给水泵汽轮机内效率
η_fwptm = 0.9  # 给水泵汽轮机机械效率
η_fwptg = 0.98  # 给水泵汽轮机减速器效率
T_swl = 24  # 循环冷却水进口温度
p_c = 15.6  # 反应堆冷却剂系统运行压力
T_cs = ip(P=p_c,x=0).T - 273.15  # 冷却剂压力对应的饱和温度
ΔT_sub = 16  # 反应堆出口冷却剂过冷度
T_co = T_cs - ΔT_sub  # 反应堆出口冷却剂温度
ΔT_c = 35  # 反应堆进出口冷却剂温升
T_ci = T_co - ΔT_c  # 反应堆进口冷却剂温度
p_s = 6.5  # 蒸汽发生器饱和蒸汽压力
T_fh = ip(P=p_s, x=x_fh).T - 273.15  # 蒸汽发生器饱和蒸汽温度
h_fh = ip(P=p_s, x=x_fh).h  # 蒸汽发生器出口比焓
ΔT_m = (T_co - T_ci) / math.log((T_co - T_fh) / (T_ci - T_fh))  # 对数平均温差
ΔT_sw = 6  # 冷凝器中循环冷却水温升
δT = 5  # 冷凝器传热端差
T_cd = T_swl + ΔT_sw + δT  # 冷凝器凝结水饱和温度
p_cd = ip(T=T_cd + 273.15, x=0).P  # 冷凝器运行压力
p_fh = p_s

Δp_fh = 0.05 * p_fh  # 新蒸汽压损
p_hi = p_fh - Δp_fh  # 高压缸进口蒸汽压力
h_hi = h_fh  # 高压缸进口比焓
x_hi = ip(P=p_hi, h=h_hi).x  # 高压缸进口蒸汽干度
s_hi = ip(P=p_hi, h=h_hi).s  # 高压缸进口熵
p_hz = 0.14 * p_hi  # 高压缸排汽压力
h_hzo = ip(P=p_hz, s=s_hi).h  # 高压缸排汽理想比焓
h_hz = h_hi - (h_hi - h_hzo) * η_hi  # 高压缸排汽真实焓值
x_hz = ip(P=p_hz, h=h_hz).x  # 高压缸出口干度

Δp_rh = 0.01 * p_hz  # 汽水分离再热器中每一级再热蒸汽压损
p_spi = p_hz  # 汽水分离器进口压力
x_spi = x_hz  # 汽水分离器进口干度
p_rh1i = p_spi - Δp_rh  # 一级再热器进口压力
h_spz = ip(P=p_rh1i, x=0).h  # 汽水分离器疏水比焓
x_rh1i = 0.995  # 一级再热器进口干度
h_rh1i = ip(P=p_rh1i, x=x_rh1i).h  # 一级再热器进口比焓
p_rh2i = p_rh1i - Δp_rh  # 二级再热器进口压力
p_rh2z = p_rh2i - Δp_rh  # 二级再热器出口压力
p_rh2hs = p_hi  # 二级再热器加热蒸汽进口压力
x_rh2hs = x_hi  # 二级再热器加热蒸汽进口干度
T_rh2hs = ip(P=p_rh2hs, x=x_rh2hs).T - 273.15  # 二级再热器加热蒸汽温度
h_rh2hs = h_hi  # 二级再热器加热蒸汽进口比焓
h_rh2hz = ip(P=p_rh2hs, x=0).h  # 二级再热器加热蒸汽出口比焓
T_rh2z = T_rh2hs - 14  # 二级再热气出口温度
h_rh2z = ip(P=p_rh2z, T=T_rh2z + 273.15).h  # 二级再热器出口比焓
Δh_rh = 0.5 * (h_rh2z - h_rh1i)  # 再热器中焓升
h_rh2i = h_rh2z - Δh_rh  # 二级再热器进口比焓
T_rh2i = ip(P=p_rh2i, h=h_rh2i).T - 273.15  # 二级再热器进口温度

T_rh1z = T_rh2i  # 一级再热器进口温度
T_rh1hz = T_rh1z + 14  # 一级再热器加热蒸汽温度
p_rh1hz = ip(T=T_rh1hz + 273.15, x=0).P  # 一级再热器加热蒸汽压力
h_rh1hz = ip(T=T_rh1hz + 273.15, x=0).h  # 一级再热器加热蒸汽出口焓值
p_rh1 = p_rh1hz / 0.95  # 一级再热器抽汽压力
h_rh1hso = ip(P=p_rh1, s=s_hi).h  # 一级再热器理想抽汽比焓
h_rh1hs = h_hi - (h_hi - h_rh1hso) * η_hi  # 一级再热器真实抽汽比焓
x_rh1hs = ip(P=p_rh1hz, h=h_rh1hs).x  # 一级再热器加热蒸汽进口干度

Δp_cd = 0.05 * p_cd  # 低压缸排汽压损
p_lz = p_cd + Δp_cd  # 低压缸排汽压力
h_li = h_rh2z  # 低压缸进口比焓
p_li = p_rh2z  # 低压缸进口压力
s_li = ip(h=h_li, P=p_li).s  # 低压缸进口熵
T_li = ip(h=h_li, P=p_li).T  # 低压缸进口温度
h_lho = ip(P=p_lz, s=s_li).h  # 低压缸出口理想比焓
h_lo = h_li - (h_li - h_lho) * η_li  # 低压缸出口真实比焓
x_lz = ip(P=p_lz, h=h_lo).x  # 低压缸排汽干度

p_fw = p_s + 0.1  # 给水压力
h_s = ip(P=p_s, x=0).h  # 蒸汽发生器运行压力下饱和水比焓
h_cd = ip(P=p_cd, x=0).h  # 冷凝器出口凝结水比焓
Z_l = 4  # 低压给水加热器级数
Z_h = 2  # 高压给水加热器级数
Z = Z_l + Z_h + 1  # 回热级数（包括除氧器）
Δh_fwop = (h_s - h_cd) / (Z + 1)  # 每一级加热器理论给水焓升
h_fwop = h_cd + Z * Δh_fwop  # 最佳给水比焓
T_fwop = ip(P=p_fw, h=h_fwop).T - 273.15  # 最佳给水温度
T_fw = 0.88 * T_fwop  # 实际给水温度
h_fw = ip(P=p_fw, T=T_fw + 273.15).h  # 给水比焓
Δh_fw = (h_fw - h_cd) / Z  # 每一级给水的实际焓升

p_dea = 0.96 * p_hz  # 除氧器运行压力（假定值）
h_deao = ip(P=p_dea, x=0).h  # 除氧器出口比焓
T_dea = ip(P=p_dea, h=h_deao)  # 除氧器出口给水温度

Δh_fwh = (h_fw - h_deao) / Z_h  # 高压给水加热器每级焓升
Δh_fwl = (h_deao - h_cd) / (Z_l + 1)  # 低压给水加热器每级焓升
p_cwp = 3.1 * p_dea  # 凝水泵出口压力
p_fwp = 1.2 * p_s  # 给水泵出口压力
Δp_fwh = (p_fwp - p_fw) / Z_h  # 高压给水加热器每级压降
Δp_cwl = (p_cwp - p_dea) / (Z_l + 1)  # 低压给水加热器每级压降

# 第一级低压给水加热器
T_lew1 = ip(P=p_cwp - Δp_cwl, h=h_cd + Δh_fwl).T - 273.15 + θ_lu  # 疏水温度
h_lew1 = ip(T=T_lew1 + 273.15, x=0).h  # 疏水比焓
p_lew1 = ip(T=T_lew1 + 273.15, x=0).P  # 疏水压力
p_les1 = p_lew1 / 0.95  # 抽汽压力
h_leso1 = ip(P=p_les1, s=s_li).h  # 抽汽理想比焓
h_les1 = h_li - (h_li - h_leso1) * η_li  # 抽汽真实比焓
x_les1 = ip(P=p_les1, h=h_les1).x  # 抽汽干度

# 第二级低压给水加热器
T_lew2 = ip(P=p_cwp - 2 * Δp_cwl, h=h_cd + 2 * Δh_fwl).T - 273.15 + θ_lu  # 疏水温度
h_lew2 = ip(T=T_lew2 + 273.15, x=0).h  # 疏水比焓
p_lew2 = ip(T=T_lew2 + 273.15, x=0).P  # 疏水压力
p_les2 = p_lew2 / 0.95  # 抽汽压力
h_leso2 = ip(P=p_les2, s=s_li).h  # 抽汽理想比焓
h_les2 = h_li - (h_li - h_leso2) * η_li  # 抽汽真实比焓
x_les2 = ip(P=p_les2, h=h_les2).x  # 抽汽干度

# 第三级低压给水加热器
T_lew3 = ip(P=p_cwp - 3 * Δp_cwl, h=h_cd + 3 * Δh_fwl).T - 273.15 + θ_lu  # 疏水温度
h_lew3 = ip(T=T_lew3 + 273.15, x=0).h  # 疏水比焓
p_lew3 = ip(T=T_lew3 + 273.15, x=0).P  # 疏水压力
p_les3 = p_lew3 / 0.95  # 抽汽压力
h_leso3 = ip(P=p_les3, s=s_li).h  # 抽汽理想比焓
h_les3 = h_li - (h_li - h_leso3) * η_li  # 抽汽真实比焓
x_les3 = ip(P=p_les3, h=h_les3).x  # 抽汽干度

# 第四级低压给水加热器
T_lew4 = ip(P=p_cwp - 4 * Δp_cwl, h=h_cd + 4 * Δh_fwl).T - 273.15 + θ_lu  # 疏水温度
h_lew4 = ip(T=T_lew4 + 273.15, x=0).h  # 疏水比焓
p_lew4 = ip(T=T_lew4 + 273.15, x=0).P  # 疏水压力
p_les4 = p_lew4 / 0.95  # 抽汽压力
h_leso4 = ip(P=p_les4, s=s_li).h  # 抽汽理想比焓
h_les4 = h_li - (h_li - h_leso4) * η_li  # 抽汽真实比焓
x_les4 = ip(P=p_les4, h=h_les4).x  # 抽汽干度

# 第一级高压给水加热器
T_hew1 = ip(P=p_fwp - Δp_fwh, h=h_deao + Δh_fwh).T - 273.15 + θ_hu  # 疏水温度
h_hew1 = ip(T=T_hew1 + 273.15, x=0).h  # 疏水比焓
p_hew1 = ip(T=T_hew1 + 273.15, x=0).P  # 疏水压力
p_hes1 = p_hew1 / 0.95  # 抽汽压力
h_heso1 = ip(P=p_hes1, s=s_hi).h  # 抽汽理想比焓
h_hes1 = h_hi - (h_hi - h_heso1) * η_hi  # 抽汽真实比焓
x_hes1 = ip(P=p_hes1, h=h_hes1).x  # 抽汽干度

# 第二级高压给水加热器
T_hew2 = ip(P=p_fwp - 2 * Δp_fwh, h=h_deao + 2 * Δh_fwh).T - 273.15 + θ_hu  # 疏水温度
h_hew2 = ip(T=T_hew2 + 273.15, x=0).h  # 疏水比焓
p_hew2 = ip(T=T_hew2 + 273.15, x=0).P  # 疏水压力
p_hes2 = p_hew2 / 0.95  # 抽汽压力
h_heso2 = ip(P=p_hes2, s=s_hi).h  # 抽汽理想比焓
h_hes2 = h_hi - (h_hi - h_heso2) * η_hi  # 抽汽真实比焓
x_hes2 = ip(P=p_hes2, h=h_hes2).x  # 抽汽干度

print("T_cs = " + str(T_cs))
print("T_co = " + str(T_co))
print("T_ci = " + str(T_ci))
print("T_fh = " + str(T_fh))
print("ΔT_m = " + str(ΔT_m))
print("p_cd = " + str(p_cd))
print("p_hi = " + str(p_hi))
print("x_hi = " + str(x_hi))
print("p_hz = " + str(p_hz))
print("x_hz = " + str(x_hz))
print("p_spi = " + str(p_spi))
print("x_spi = " + str(x_spi))
print("p_rh1i = " + str(p_rh1i))
print("x_rh1i = " + str(x_rh1i))
print("p_rh1hs = " + str(p_rh1hz))
print("x_rh1hs = " + str(x_rh1hs))
print("p_rh2i = " + str(p_rh2i))
print("T_rh2i = " + str(T_rh2i))
print("p_rh2z = " + str(p_rh2z))
print("T_rh2z = " + str(T_rh2z))
print("p_rh2hs = " + str(p_rh2hs))
print("x_rh2hs = " + str(x_rh2hs))
print("p_li = " + str(p_li))
print("T_li = " + str(T_li))
print("p_lz = " + str(p_lz))
print("x_lz = " + str(x_lz))
print("Δh_fw = " + str(Δh_fw))
print("Δh_fwh = " + str(Δh_fwh))
print("Δh_fwl = " + str(Δh_fwl))
print("\033[0;35m======= 第1级低压给水加热器 =======\033[0m")
print("h_lfwi1 = " + str(h_cd))
print("h_lfwo1 = " + str(h_cd + Δh_fwl))
print("T_lfwi1 = " + str(ip(P=p_cwp, h=h_cd).T - 273.15))
print("T_lfwo1 = " + str(T_lew1 - θ_lu))
print("p_les1 = " + str(p_les1))
print("x_les1 = " + str(x_les1))
print("\033[0;35m======= 第2级低压给水加热器 =======\033[0m")
print("h_lfwi2 = " + str(h_cd + Δh_fwl))
print("h_lfwo2 = " + str(h_cd + 2 * Δh_fwl))
print("T_lfwi2 = " + str(ip(P=p_cwp - Δp_cwl, h=h_cd + Δh_fwl).T - 273.15))
print("T_lfwo2 = " + str(T_lew2 - θ_lu))
print("p_les2 = " + str(p_les2))
print("x_les2 = " + str(x_les2))
print("\033[0;35m======= 第3级低压给水加热器 =======\033[0m")
print("h_lfwi3 = " + str(h_cd + 2 * Δh_fwl))
print("h_lfwo3 = " + str(h_cd + 3 * Δh_fwl))
print("T_lfwi3 = " + str(ip(P=p_cwp - 2 * Δp_cwl, h=h_cd + 2 * Δh_fwl).T - 273.15))
print("T_lfwo3 = " + str(T_lew3 - θ_lu))
print("p_les3 = " + str(p_les3))
print("x_les3 = " + str(x_les3))
print("\033[0;35m======= 第4级低压给水加热器 =======\033[0m")
print("h_lfwi4 = " + str(h_cd + 3 * Δh_fwl))
print("h_lfwo4 = " + str(h_cd + 4 * Δh_fwl))
print("T_lfwi4 = " + str(ip(P=p_cwp - 3 * Δp_cwl, h=h_cd + 3 * Δh_fwl).T - 273.15))
print("T_lfwo4 = " + str(T_lew4 - θ_lu))
print("p_les4 = " + str(p_les4))
print("x_les4 = " + str(x_les4))
print("\033[0;32m============ 除氧器 =============\033[0m")
print("h_deai = " + str(h_cd + 4 * Δh_fwl))
print("h_deao = " + str(h_deao))
print("T_dea = " + str(T_dea))
print("p_dea = " + str(p_dea))
print("\033[0;36m======= 第1级高压给水加热器 =======\033[0m")
print("h_hfwi1 = " + str(h_deao))
print("h_hfwo1 = " + str(h_deao + Δh_fwh))
print("T_hfwi1 = " + str(ip(P=p_fwp, h=h_deao).T - 273.15))
print("T_hfwO1 = " + str(T_hew1 - θ_hu))
print("h_hes1 = " + str(h_hes1))
print("x_hes1 = " + str(x_hes1))
print("\033[0;36m======= 第2级高压给水加热器 =======\033[0m")
print("h_hfwi2 = " + str(h_deao + Δh_fwh))
print("h_hfwo2 = " + str(h_deao + 2 * Δh_fwh))
print("T_hfwi2 = " + str(ip(P=p_fwp - Δp_fwh, h=h_deao + Δh_fwh).T - 273.15))
print("T_hfwO2 = " + str(T_hew2 - θ_hu))
print("h_hes2 = " + str(h_hes2))
print("x_hes2 = " + str(x_hes2))
print("\033[0;31m---------------- 循 环 开 始 -------------------\033[0m")

η_eNPP = 0.3  # 假定核电厂效率初值
G_cd = 1000  # 假定冷凝器出口凝结水流量初值
while True:
    Q_R = N_e / η_eNPP   # 反应堆热功率
    D_s = Q_R * η_1 * 1000 / ((h_fh - h_s) + (1 + ξd) * (h_s - h_fw))  # 总蒸汽产量
    G_fw = (1 + ξd) * D_s  # 蒸汽发生器给水流量
    H_fwp = p_fwp - p_dea  # 给水泵扬程
    ρ_fw = 0.5 * (ip(P=p_fwp, h=h_deao).rho + ip(P=p_dea, x=0).rho)  # 给水泵内密度
    N_fwpp = 1000 * G_fw * H_fwp / ρ_fw  # 给水泵有效功率
    N_fwpt = N_fwpp / (η_fwpp * η_fwpti * η_fwptm * η_fwptg)  # 给水泵汽轮机有效功率
    H_a = h_hi - h_hz  # 给水泵汽轮机内的绝热焓降
    G_sfwp = N_fwpt / H_a  # 给水泵汽轮机耗汽量

    while True:
        # 低压给水加热器抽汽量
        G_les4 = G_cd * Δh_fwl / (η_h * (h_les4 - h_lew4))  # 第四级
        G_les3 = (G_cd * Δh_fwl - η_h * G_les4 * (h_lew4 - h_lew3)) / (η_h * (h_les3 - h_lew3))  # 第三级
        G_les2 = (G_cd * Δh_fwl - η_h * (G_les4 + G_les3) * (h_lew3 - h_lew2)) / (η_h * (h_les2 - h_lew2))  # 第二级
        G_les1 = (G_cd * Δh_fwl - η_h * (G_les4 + G_les3 + G_les2) * (h_lew2 - h_lew1)) / (η_h * (h_les1 - h_lew1))  # 第一级

        G_slp = G_cd - ξd * D_s - G_sfwp  # 低压缸耗汽量
        G_srh1 = G_slp * (h_rh2i - h_rh1i) / (η_h * (h_rh1hs - h_rh1hz))  # 第一级再热器抽汽量
        G_srh2 = G_slp * (h_rh2z - h_rh2i) / (η_h * (h_rh2hs - h_rh2hz))  # 第一级再热器抽汽量

        # 高压给水加热器抽汽量
        G_hes2 = (G_fw * Δh_fwh - η_h * G_srh2 * (h_rh2hz - h_hew2)) / (η_h * (h_hes2 - h_hew2))  # 二级
        G_hes1 = (G_fw * Δh_fwh - η_h * ((G_srh2 + G_hes2) * (h_hew2 - h_hew1) + G_srh1 * (h_rh1hz - h_hew1))) / (η_h * (h_hes1 - h_hew1))  # 一级

        G_fss = G_slp * (x_rh1i - x_spi) / x_spi  # 汽水分离器疏水量
        h_deai = h_cd + 4 * Δh_fwl  # 除氧器入口给水比焓
        G_sdea = (G_fss * (h_spz - h_deao) + (G_srh1 +G_srh2 + G_hes1 + G_hes2) * (h_hew1 - h_deao) + G_cd * (h_deai - h_deao)) / (η_h * (h_deao - h_hz))  # 除氧器抽汽量
        N_tl = (G_slp * (h_li - h_lo) + G_les4 * (h_li - h_les4) + G_les3 * (h_li - h_les3) + G_les2 * (h_li - h_les2) + G_les1 * (h_li - h_les1)) * η_ge * η_li * η_m  # 低压缸发电功率
        N_th = 1000 * N_e - N_tl  # 高压缸发电功率
        G_shp = (N_th / (η_ge * η_hi * η_m) - G_hes1 * (h_hi - h_hes1) - G_hes2 * (h_hi - h_hes2) - G_srh1 * (h_hi - h_rh1hs)) / (h_hi - h_hz)  # 高压缸耗汽量

        D_s_new = G_srh2 + G_shp + G_sfwp  # 蒸汽发生器总蒸汽产量（新）
        G_fw_new = (1 + ξd) * D_s_new  # 蒸汽发生器给水量（新）
        G_cd_new = G_fw_new - G_fss - G_hes2 - G_hes1 - G_srh2 - G_srh1 - G_sdea  # 凝结水流量（新）
        Q_R_new = (D_s_new * (h_fh - h_fw) + ξd * D_s_new * (h_s - h_fw)) / (η_1 * 1000)  # 反应堆热功率（新）
        η_eNPP_new = N_e / Q_R_new  # 核电厂效率

        print("\033[0;34mη_eNPP\033[0m" + " = " + str(η_eNPP))
        print("Q_R = " + str(Q_R))
        print("D_s = " + str(D_s))
        print("G_shp = " + str(G_shp))
        print("G_slp = " + str(G_slp))
        print("G_srh1 = " + str(G_srh1))
        print("G_srh2 = " + str(G_srh2))
        print("G_sdea = " + str(G_sdea))
        print("G_sfwp = " + str(G_sfwp))
        print("G_fw = " + str(G_fw))
        print("H_fwp = " + str(H_fwp))
        print("\033[0;36mG_hes1\033[0m" + " = " + str(G_hes1))
        print("\033[0;36mG_hes2\033[0m" + " = " + str(G_hes2))
        print("\033[0;35mG_les1\033[0m" + " = " + str(G_les1))
        print("\033[0;35mG_les2\033[0m" + " = " + str(G_les2))
        print("\033[0;35mG_les3\033[0m" + " = " + str(G_les3))
        print("\033[0;35mG_les4\033[0m" + " = " + str(G_les4))
        print("------------------ 分 割 线 ---------------------")

        if abs((G_cd_new - G_cd) / G_cd) < 0.01:
            break
        else:
            G_cd = 0.5 * (G_cd_new + G_cd)
    Q_R_new = (D_s_new * (h_fh - h_fw) + ξd * D_s_new * (h_s - h_fw)) / (η_1 * 1000)  # 反应堆热功率（新）
    η_eNPP_new = N_e / Q_R_new  # 核电厂效率
    if abs((η_eNPP_new - η_eNPP) / η_eNPP) < 0.001:
        break
    else:
        η_eNPP = η_eNPP_new

