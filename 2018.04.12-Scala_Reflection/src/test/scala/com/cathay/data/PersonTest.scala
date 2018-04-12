package com.cathay.data

import org.scalatest.{BeforeAndAfterAll, FunSpecLike, Matchers}
import scala.reflect.runtime.universe._
/**
  * @author Andy Huang on 02/04/2018
  */
class PersonTest extends Matchers with FunSpecLike with BeforeAndAfterAll {
  def getTypeTag[T: TypeTag](obj: T) = typeTag[T]

  describe("Scala Reflection Example") {
    it("Inspection") {
      val employee = Employee("Elon Musk", "elon@spacex.com")
      val eType = getTypeTag(employee).tpe

      assert(eType.toString == "com.cathay.data.Employee")
      assert(eType == typeOf[Employee])

      // Inspecting parent class
      def getDirectBase(a: ClassSymbol) = {
        val base = a.baseClasses.toSet - a
        val basebase = base.flatMap {
          case x: ClassSymbol => x.baseClasses.toSet - x
        }
        base -- basebase
      }

      assert(getDirectBase(eType.typeSymbol.asClass).contains(typeOf[Person].typeSymbol))
    }

    it("Instantiation") {
      // Getting the Employee class mirror
      val m = runtimeMirror(getClass.getClassLoader)
      val classSymbol = typeOf[Employee].typeSymbol.asClass
      val classMirror = m.reflectClass(classSymbol)

      // Invoking mirror constructor to get instance
      val constructorSymbol = typeOf[Employee].decl(termNames.CONSTRUCTOR).asMethod
      val constructorMirror = classMirror.reflectConstructor(constructorSymbol)
      val employee = constructorMirror("Elon Musk", "elon@spacex.com")

      assert(employee == Employee("Elon Musk", "elon@spacex.com"))
    }

    it("Invocation") {
      val employee = Employee("Elon Musk", "elon@spacex.com")
      val m = runtimeMirror(getClass.getClassLoader)
      val instanceMirror = m.reflect(employee)

      // Invoking method
      val prettyMethodSymbol = getTypeTag(employee).tpe.decl("toJson": TermName).asMethod
      val prettyMethodMirror = instanceMirror.reflectMethod(prettyMethodSymbol)

      assert(prettyMethodMirror.apply() == employee.toJson())

      // Invoking getter and setter
      val nameFieldSymbol = getTypeTag(employee).tpe.decl("name": TermName).asTerm
      val nameFieldMirror = instanceMirror.reflectField(nameFieldSymbol)

      assert(nameFieldMirror.get == employee.name)

      nameFieldMirror.set("Stephen Hawking")
      assert(nameFieldMirror.get == "Stephen Hawking")
    }

    it("Symbol") {
      assert(typeOf[Employee].member(TermName("name")).toString == "value name")
      assert(typeOf[Employee].member(TermName("toJson")).toString == "method toJson")

      // Casting to Term Symbol to check whether is Getter
      assert(typeOf[Employee].member(TermName("name")).asTerm.isGetter)

      // Casting to Method Symbol to check the parameters
      assert(typeOf[Employee].member(TermName("toJson")).asMethod.paramLists.flatten.isEmpty)

      // Checking whether is constructor
      assert(typeOf[Employee].member(termNames.CONSTRUCTOR).isConstructor)
    }

    it("Types") {
      // Checking the subtyping relationship between two types
      assert(typeOf[Employee] <:< typeOf[Person])

      // Checking for equality between two types
      def getType[T: TypeTag](obj: T) = typeOf[T]
      assert(typeOf[Employee] =:= getType(Employee("Elon Musk", "elon@spacex.com")))
    }

    it("Trees") {
      val employee = Employee("Elon Musk", "elon@spacex.com")

      // Creating tree via method parse on TOOLBOXES, i.e. create tree via string
      import scala.tools.reflect.ToolBox

      val functionalLiteral =
            """ (name: String, email: String) => {
          |   com.cathay.data.Employee(name, email)
          | } """.stripMargin
      val toolbox = runtimeMirror(getClass.getClassLoader).mkToolBox()
      val tree = toolbox.parse(functionalLiteral)

      // Display tree
      println(showRaw(tree))

      // Compiling and executing it at runtime by using ToolBox
      val getEmployee = toolbox.eval(tree).asInstanceOf[(String, String) => Employee]

      assert(getEmployee("Elon Musk", "elon@spacex.com") == employee)
    }
  }

}
