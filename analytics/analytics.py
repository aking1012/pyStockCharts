'''
A file to hold all the analytics functions and classes
'''


'''
Crap I need to replicate in pure python without any dependencies...
so I can beat out ta-lib wrappers and clones that either use pandas
or just wrap ta-lib.

Function     Notation    Progress
DONCH    Donchian Channel    DONE
MASSI    Mass Index  DONE
MFI  Money Flow Index    DONE
MOM  Momentum    DONE
OBV  On Balance Volume   DONE
PPSR     Pivot Points, Supports and Resistances  DONE
ROC  Rate of change : ((price/prevPrice)-1)100   DONE
STOK     Stochastic oscillator %K    DONE
STDDEV   Standard Deviation  DONE
STO  Stochastic oscillator %D    DONE
TRIX     1-day Rate-Of-Change (ROC) of a Triple Smooth EMA   DONE
TSI  True Strength Index     DONE
ULTOSC   Ultimate Oscillator     DONE
VORTEX   Vortex Indicator    DONE
EOM  Ease of Movement    DONE
FORCE    Force Index     DONE

APO  Absolute Price Oscillator  
AVGPRICE     Average Price  
BETA     Beta   
BOP  Balance Of Power   
CMO  Chande Momentum Oscillator 
CORREL   Pearson's Correlation Coefficient (r)  
COPP     Coppock Curve   DONE
DEMA     Double Exponential Moving Average  
DX   Directional Movement Index 
HT_DCPERIOD  Hilbert Transform - Dominant Cycle Period  
HT_DCPHASE   Hilbert Transform - Dominant Cycle Phase   
HT_PHASOR    Hilbert Transform - Phasor Components  
HT_SINE  Hilbert Transform - SineWave   
HT_TRENDLINE     Hilbert Transform - Instantaneous Trendline    
HT_TRENDMODE     Hilbert Transform - Trend vs Cycle Mode    
KAMA     Kaufman Adaptive Moving Average    

LINEARREG    Linear Regression  
LINEARREG_ANGLE  Linear Regression Angle    
LINEARREG_INTERCEPT  Linear Regression Intercept    
LINEARREG_SLOPE  Linear Regression Slope    

find_trending_squares
	find least squares lines for high, low, open, and close in the data set
	returns a list of lists in that order
	[[high, low, open, close],[high, low, open, close],....]

find_trending_squares_reduce_outliers:
	attempt to reduce the effect outliers by examining the queryset
	then check the score
	finally look to see if there are significantly few points that deviate
    	from the determined line and recalculate

MAMA     MESA Adaptive Moving Average   
MAX  Highest value over a specified period  
MAXINDEX     Index of highest value over a specified period 
MEDPRICE     Median Price   
MIDPOINT     MidPoint over period   
MIDPRICE     Midpoint Price over period 
MIN Lowest value over a specified period    
MININDEX     Index of lowest value over a specified period  
MINMAX   Lowest and highest values over a specified period  
MINMAXINDEX  Indexes of lowest and highest values over a specified period   
MINUS_DI     Minus Directional Indicator    
MINUS_DM     Minus Directional Movement 
NATR     Normalized Average True Range  
PLUS_DI  Plus Directional Indicator 
PLUS_DM  Plus Directional Movement  
PPO  Percentage Price Oscillator    
ROCP     Rate of change Percentage: (price-prevPrice)/prevPrice 
ROCR     Rate of change ratio: (price/prevPrice)    
ROCR100  Rate of change ratio 100 scale: (price/prevPrice)100   
SAR  Parabolic SAR  
SAREXT   Parabolic SAR - Extended   
SMA  Simple Moving Average  
STOCH    Stochastic 
STOCHF   Stochastic Fast    
STOCHRSI     Stochastic Relative Strength Index 
SUM  Summation  
T3   Triple Exponential Moving Average (T3) 
TEMA     Triple Exponential Moving Average  
TRANGE   True Range 
TRIMA    Triangular Moving Average  
TSF  Time Series Forecast   
TYPPRICE     Typical Price  
VAR  Variance   
WCLPRICE     Weighted Close Price   
WILLR    Williams' %R   
WMA  Weighted Moving Average

The ones below this in Overlays and Indicators contain scaffolds to beat out stockcharts.com
'''

class NotEnoughValuesError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Overlays:
	'''
	Blanket class to contain all overlays.
	This way you can:
	  Instantiate overlays
	  Calculate or fetch the relevant ones
	  Access them as class attributes
	  Reuse them later if you want or write them to a database
	'''
	def __init__(self, datapoints):
		self.datapoints = datapoints
		self.sma = {}
		self.ema = {}
		self.bollinger = {}

	def SMA(self, length=50):
		'''
		Norms are len 50 and len 200, 
		but you're welcome to do whatever you want...
		'''
		try:
			assert(len(self.datapoints) >= length * 2)
		except:
			err_str = 'Not enough values to compute desired set.'+\
				'Needed' + str(length * 2) +\
				'Got' str(len(datapoints)) +\
				''
			print(err_str)
			raise NotEnoughValuesError(err_str)
		pass

	def EMA(self, length=20, mult=1):
		'''
		Norm is 20, mult 1... again do whatever you want.
		Mult is what you increase the exponent by for each step.
		'''
		pass

	def Bollinger(self, length=20, mult=2):
		'''
		'''
		pass

	def Keltner(self, length=20, mult=2, something=10):
		'''
		'''
		pass

	def Ichimoku(self, datapoints):
		'''
		'''
		pass

	def SMAEnvelopes(self, something=20, something_else=2.5):
		'''
		'''
		pass

	def EMAEnvelopes(self, something=20, something_else=2.5):
		'''
		'''
		pass

	def ParabolicSAR(self):
		'''
		'''
		pass

	def ChandalierExits(self):
		'''
		'''
		pass

	def PivotPoints(self):
		'''
		'''
		pass

	def PriceChannels(self):
		'''
		'''
		pass

	def MarketTotal(self):
		'''
		'''
		pass

	def VolumeByPrice(self):
		'''
		'''
		pass

	def ZigZag(self, percentage):
		'''
		'''
		pass

	def ZigZagRetrace(self, percentage):
		'''
		'''
		pass

class Indicators:
	'''
	Correlation
	Chaikin Money Flow
	Chaikin Oscillator
	Coppock Curve
	Date/Time Axis
	Detrended Price (DTO)
	Directional Movement w/ADX
	Ease of Movement
	Force Index
	Know Sure Thing (KST)
	'''
	def __init__(self, datapoints):
		self.datapoints = datapoints
		self.macd = {}
		self.rsi = {}

	def AccumulationDistribution(self):
		pass

	def Aroon(self, something=25):
		pass

	def AroonOsc(self,something=25):
		pass

	def ADX(self, something=14):
		'''
		Average Directional Index
		'''
		pass

	def AvgTrueRange(self, something=14):
		'''
		'''
		pass

	def BollingerWidth(self, length=20, mult=2):
		'''
		'''
		pass

	def CCI(self, something=20):
		'''
		'''
		pass

	def MACD(self, something=12, somethingelse=26, somethingfurther=9):
		pass

	def RSI(self, something=14):
		pass

class CandlePattern:
	def __init__(self, width=5):
		self.width = width

class TwoCrows(CandlePattern):
	def __init__(self, parent):
		CandlePattern.__init__(self, 4)

	def finder(self, dataset):
		pass

class CandlePatterns:
	'''
	All candle patterns within ta-lib
	TwoCrows
	ThreeBlackCrows
	ThreeInside
	ThreeLineStrike
	ThreeOutside
	CDL3STARSINSOUTH     Three Stars In The South   
	CDL3WHITESOLDIERS    Three Advancing White Soldiers 
	CDLABANDONEDBABY     Abandoned Baby 
	CDLADVANCEBLOCK  Advance Block  
	CDLBELTHOLD  Belt-hold  
	CDLBREAKAWAY     Breakaway  
	CDLCLOSINGMARUBOZU   Closing Marubozu   
	CDLCONCEALBABYSWALL  Concealing Baby Swallow    
	CDLCOUNTERATTACK     Counterattack  
	CDLDARKCLOUDCOVER    Dark Cloud Cover   
	CDLDOJI  Doji   
	CDLDOJISTAR  Doji Star  
	CDLDRAGONFLYDOJI     Dragonfly Doji 
	CDLENGULFING     Engulfing Pattern  
	CDLEVENINGDOJISTAR   Evening Doji Star  
	CDLEVENINGSTAR   Evening Star   
	CDLGAPSIDESIDEWHITE  Up/Down-gap side-by-side white lines   
	CDLGRAVESTONEDOJI    Gravestone Doji    
	CDLHAMMER    Hammer 
	CDLHANGINGMAN    Hanging Man    
	CDLHARAMI    Harami Pattern 
	CDLHARAMICROSS   Harami Cross Pattern   
	CDLHIGHWAVE  High-Wave Candle   
	CDLHIKKAKE   Hikkake Pattern    
	CDLHIKKAKEMOD    Modified Hikkake Pattern   
	CDLHOMINGPIGEON  Homing Pigeon  
	CDLIDENTICAL3CROWS   Identical Three Crows  
	CDLINNECK    In-Neck Pattern    
	CDLINVERTEDHAMMER    Inverted Hammer    
	CDLKICKING   Kicking    
	CDLKICKINGBYLENGTH   Kicking - bull/bear determined by the longer marubozu  
	CDLLADDERBOTTOM  Ladder Bottom  
	CDLLONGLEGGEDDOJI    Long Legged Doji   
	CDLLONGLINE  Long Line Candle   
	CDLMARUBOZU  Marubozu   
	CDLMATCHINGLOW   Matching Low   
	CDLMATHOLD   Mat Hold   
	CDLMORNINGDOJISTAR   Morning Doji Star  
	CDLMORNINGSTAR   Morning Star   
	CDLONNECK    On-Neck Pattern    
	CDLPIERCING  Piercing Pattern   
	CDLRICKSHAWMAN   Rickshaw Man   
	CDLRISEFALL3METHODS  Rising/Falling Three Methods   
	CDLSEPARATINGLINES   Separating Lines   
	CDLSHOOTINGSTAR  Shooting Star  
	CDLSHORTLINE     Short Line Candle  
	CDLSPINNINGTOP   Spinning Top   
	CDLSTALLEDPATTERN    Stalled Pattern    
	CDLSTICKSANDWICH     Stick Sandwich 
	CDLTAKURI    Takuri (Dragonfly Doji with very long lower shadow)    
	CDLTASUKIGAP     Tasuki Gap 
	CDLTHRUSTING     Thrusting Pattern  
	CDLTRISTAR   Tristar Pattern    
	CDLUNIQUE3RIVER  Unique 3 River 
	CDLUPSIDEGAP2CROWS   Upside Gap Two Crows   
	CDLXSIDEGAP3METHODS Upside/Downside Gap Three Methods   

	More candle patterns
	Flag up and down patterns...
	Short term linear regression slope high and low should solve for these.
	'''
	def __init__(self, dataset):
		pass

