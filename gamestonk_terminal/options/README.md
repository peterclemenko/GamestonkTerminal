# OPTIONS

This menu aims to give insight on options. 

This menu aims to give insight on options. Options can cause significant share price movement, and option pricing gives info about market sentiment for a ticker. The usage of the following commands along with an example will be exploited below:

* [exp](#exp)
  * See/set expiry date [Yahoo Finance]
* [voi](#voi)
  * Volume + open interest options trading plot [Yahoo Finance]
* [vcalls](#vcalls)
  * Calls volume + open interest plot [Yahoo Finance]
* [vputs](#vputs)
  * Puts volume + open interest plot [Yahoo Finance]
* [chains](#chains)
  * Display option chains [Source: Tradier]
* [info](#info)
  * _**This requires selenium webdriver installed**_
  * Display option information [Source: Barchart.com]


## exp <a name="exp"></a>

```text
usage: exp [-d {0,1,2,3,4,5,6,7,8,9,10,11}]
```

See/set expiry dates. [Source: Yahoo Finance]

* -d : Expiry date index to set.

<img width="955" alt="exp" src="https://user-images.githubusercontent.com/25267873/115161875-f6706900-a097-11eb-8566-bb7b408856a5.png">


## voi <a name="voi"></a>

```text
usage: voi [-v MIN_VOL] [-m MIN_SP] [-M MAX_SP]
```

Plots Volume + Open Interest of calls vs puts. [Source: Yahoo Finance]

* -v : Minimum volume (considering open interest) threshold of the plot.
* -m : Minimum strike price to consider in the plot.
* -M : Maximum strike price to consider in the plot.

![voinio](https://user-images.githubusercontent.com/25267873/115161878-f7a19600-a097-11eb-889b-e9cc945f174d.png)


## vcalls <a name="vcalls"></a>

```text
usage: vcalls [-m MIN_SP] [-M MAX_SP]
```

Plots Calls Volume + Open Interest. [Source: Yahoo Finance]

* -m : Minimum strike price to consider in the plot.
* -M : Maximum strike price to consider in the plot.

![vcalls](https://user-images.githubusercontent.com/25267873/115161874-f5d7d280-a097-11eb-93e2-3a2b20292f09.png)


## vputs <a name="vputs"></a>

```text
usage: vputs [-m MIN_SP] [-M MAX_SP]
```

Plots Puts Volume + Open Interest. [Source: Yahoo Finance]

* -m : Minimum strike price to consider in the plot.
* -M : Maximum strike price to consider in the plot.

![vputs](https://user-images.githubusercontent.com/25267873/115161873-f40e0f00-a097-11eb-8334-3d4f14b56766.png)


## chains <a name="chains"></a>

````
usage: chains [--calls] [--puts] [-m MIN_SP] [-M MAX_SP]
````

Display options chains. [Source: Tradier]

* --calls : Flag to show calls only
* --puts : Flag to show puts only
* -m : Minimum strike price to consider.
* -M : Maximum strike price to consider.
* -d : Columns to display.  Should be comma separated.  Must be in * -d : Columns to display from the following selection: bid, ask, strike, bidsize, asksize, volume, open_interest, delta, gamma, theta, vega, ask_iv, bid_iv, mid_iv. Default: mid_iv,vega_theta_gamma,delta,volume,open_interest,bid,ask. Note that they are separated by comma.


<img width="948" alt="chains" src="https://user-images.githubusercontent.com/25267873/115161876-f708ff80-a097-11eb-8073-195979862a45.png">


## info <a name="info"></a>
This scrapes the options information from barchart.com/stocks overview.  This includes information such as Historical Volatility and IV Rank.

In order to run, the selenium webdriver must be installed.  
Currently, this runs on either Chrome or Firefox.  The path to the driver should be defined in [config_terminal.py](#config_terminal.py).

Note this may take more time than other commands to process.
````
usage: info [-d DRIVER]
````
* -d/--driver : One of {chrome, firefox}.  This indicates which driver you have installed.

![im](https://user-images.githubusercontent.com/18151143/115454584-efa83a00-a1ee-11eb-9d0f-2558ffa31579.png)