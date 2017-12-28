package com.freedomandy.service

import java.util.Calendar

import akka.actor.ActorSystem
import akka.http.scaladsl.Http
import akka.http.scaladsl.model.{HttpRequest, HttpResponse, ResponseEntity, StatusCodes}
import akka.stream.ActorMaterializer
import akka.util.ByteString
import com.freedomandy.data.Stock

import scala.concurrent.Future

/**
  * Created by andy on 19/12/2017.
  */

case class StockService(implicit system: ActorSystem, implicit val materializer: ActorMaterializer) {
  implicit val ec = system.dispatcher
  private val GOOGLE_FINANCE_URI = "https://finance.google.com/finance"
  private val http = Http(system)
  import spray.json._

  def getStock(exchange: String, ticker: String): Future[Option[Stock]] = {
    def unmarshalJSON(entity: ResponseEntity): Future[Stock] = {
      entity.dataBytes.runFold(ByteString(""))(_ ++ _).map(body => {
        def getValue(jValue: String) = jValue.substring(1, jValue.length -1)

        val bodyString = body.utf8String
        val bodyJsObject = body.utf8String.substring(5, bodyString.length - 2).parseJson.asJsObject

        Stock( getValue(bodyJsObject.getFields("exchange").head.prettyPrint),
          getValue(bodyJsObject.getFields("t").head.prettyPrint),
          getValue(bodyJsObject.getFields("l").head.prettyPrint).toDouble,
          getValue(bodyJsObject.getFields("c").head.prettyPrint).toDouble,
          getValue(bodyJsObject.getFields("cp").head.prettyPrint).toDouble,
          Calendar.getInstance().getTime().getTime)

      })
    }

    val pollRequest = HttpRequest(uri = GOOGLE_FINANCE_URI + s"?q=$exchange:$ticker&output=json")

    http.singleRequest(pollRequest).flatMap {
      case HttpResponse(StatusCodes.OK, headers, entity, _) =>
        unmarshalJSON(entity).map(Some(_))
      case _ =>
        Future.successful(None)
    }
  }
}
