# CurrencyConverterBot

## General information

Bot uses foreign exchange rate form official website of Central Bank of the Russian Federation.

Bot updates the course at 03:00 every day

## Commands

This bot has several commands.

**/rate(/get_rate) <reduction>** : gives you the exchange of this currency and compare it with yesterday's exchange

**/convert <reduction1> <amount> <reduction2>** : convert <amount> of currency1 into currency2

**/info** : gives you information about bot

**/ListOfCurrencies** : gives you list of currencies which you can use

**/StartMailing <reduction>** : you will receive messages with rate of entered currency every day

**/EndMailing <reduction>** : you stop receiving everyday messages with entered currency rate

**/MyMailing** : gives you list of currencies rates of which you receive in everyday message

## Examples

**input**: /rate USD

**output**: 1USD = 74.8451(+0.0)RUB

**input**: /convert USD 1.0 BYN

**output**: 1.0USD = 2.5644BYN

**input**: /StartMailing EUR

**output**: Start mailing EUR

**input**: /MyMailing

**output**: EUR

**input**: /EndMailing EUR

**output**: End of mailing EUR


