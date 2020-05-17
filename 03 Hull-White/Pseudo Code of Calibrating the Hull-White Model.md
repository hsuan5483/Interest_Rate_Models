# Pseudo Code of Calibrating the Hull-White Model

<font size=3>Author: 許沛萱 Pei-Hsuan Hsu
Email: 07350003@gm.scu.edu.tw</font>
---

:::success
**定義**
marketR: 市場spot rate
modelR: Hull-White 算出的 spot rate
YC_DF: Yield Curve data
:::

## Part 1: 處理資料

### *Calculating log price of zero-coupon bond*
><font color='orange'>**Function**</font>
**INPUT**: Maturity $T$, Spot Rate at time t
**OUTPUT**: $lnP(t,T)$
<font color='orange'>**EndFunction**</font>


### *Calculating instantaneous forward rate*
><font color='orange'>**Function**</font>
**INPUT**: Maturity $T$, Spot Rate at time $t$
**OUTPUT**: $f(t,T)$
<font color='orange'>**EndFunction**</font>


### *Calculating the derivative of instantaneous forward rate*
><font color='orange'>**Function**</font>
**INPUT**: Maturity $T$, Spot Rate at time $t$
**OUTPUT**: $f_t(t,T)$
<font color='orange'>**EndFunction**</font>


### *Generating information needed in Hull-White model*
><font color='orange'>**Function**</font>
**INPUT**: Yield Curve, tenors
**OUTPUT**: Dataframe <font color='green'>YC_DF</font> with $[Tenors, marketR, P(t,T), F(0;t,T), f(t,T), f_t(t,T)]$
<font color='orange'>**EndFunction**</font>

## Part 2: The Hull-White Model

![](https://i.imgur.com/Ld3m5iG.png)


### *Calculating <font color='#2874A6'>theta</font> in Hull-White model*
><font color='orange'>**Function**</font>
**INPUT**: a, sigma, t, <font color='green'>YC_DF</font>
**OUTPUT**: $\theta(t)$
<font color='orange'>**EndFunction**</font>

### *Calculating <font size=3>$B(t,T)$</font>*
><font color='orange'>**Function**</font>
**INPUT**: a, sigma, t, T
**OUTPUT**: <font size=3>$B(t,T)$</font>
<font color='orange'>**EndFunction**</font>

### *Calculating <font size=3>$lnA(t,T)$</font>*
><font color='orange'>**Function**</font>
**INPUT**: a, sigma, t, T, <font color='green'>YC_DF</font>
**OUTPUT**: <font size=3>$lnA(t,T)$</font>
<font color='orange'>**EndFunction**</font>

### *Zero-coupon bond prices under Hull-White model*
><font color='orange'>**Function**</font>
**INPUT**: a, sigma, t, <font color='green'>YC_DF</font>
**OUTPUT**: $P_{Hull-White} (t, T)$, $R_{Hull-White} (t, T)$, <font color='#F1C40F'>DF_HullWhite</font>
<font color='orange'>**EndFunction**</font>

:::info
註：<font color='#F1C40F'>DF_HullWhite</font>為包含Hull-White資訊的dataframe
:::

### *Objective function for calibrating Hull-White parameters*
><font color='orange'>**Function**</font>
**INPUT**: a, sigma, t, <font color='green'>YC_DF</font>
**OUTPUT**: <font color='red'>sum of squared error</font> between marketR and $R_{Hull-White} (t, T)$
<font color='orange'>**EndFunction**</font>

### *Finding optimal parameters by minimize the sum of squared error*
><font color='orange'>**Function**</font>
**INPUT**: initial guess of $a$
**OUTPUT**: Optimal Results
<font color='orange'>**EndFunction**</font>




