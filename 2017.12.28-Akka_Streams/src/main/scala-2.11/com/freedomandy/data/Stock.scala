package com.freedomandy.data

/**
  * Created by andy on 25/12/2017.
  */
case class Stock(exchange: String, ticker: String, lastPrice: Double, change: Double, changePercentage: Double,
                 lastTime: Long)
