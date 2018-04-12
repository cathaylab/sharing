package com.cathay.data

/**
  * @author Andy Huang on 02/04/2018
  */
class Person(name: String)
case class Employee(name: String, email: String) extends Person(name) {
  def toJson(): String = s"""{ "name": "$name", "email": "$email"}"""
}