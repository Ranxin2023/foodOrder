package com.example.foodordernew

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.Response
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException

class OrderFood : AppCompatActivity(){
    override fun onCreate(savedInstanceState: Bundle?){
        super.onCreate(savedInstanceState)
        setContentView(R.layout.order_food)
        val addFrenchFries=findViewById<Button>(R.id.addFrenchFries)
        val subtractFrenchFries=findViewById<Button>(R.id.subtractFrenchFries)
        val numFrenchFries=findViewById<TextView>(R.id.frenchFriesAmount)
        addFrenchFries.setOnClickListener{
            val currentValue: Int = numFrenchFries.text.toString().toInt()
            // Increment the counter by 1
            val newValue = currentValue + 1
            // Update the text view with the new value
            numFrenchFries.text=newValue.toString()
        }
        subtractFrenchFries.setOnClickListener{
            val currentValue: Int = numFrenchFries.text.toString().toInt()
            if(currentValue>0){
                val newValue=currentValue-1
                numFrenchFries.text=newValue.toString()
            }
        }
        val addBigMac=findViewById<Button>(R.id.addBigMac)
        val subtractBigMac=findViewById<Button>(R.id.subtractBigMac)
        val numBigMac=findViewById<TextView>(R.id.bigMacAmount)
        addBigMac.setOnClickListener{
            val currentValue: Int = numBigMac.text.toString().toInt()
            // Increment the counter by 1
            val newValue = currentValue + 1
            // Update the text view with the new value
            numBigMac.text=newValue.toString()
        }
        subtractBigMac.setOnClickListener{
            val currentValue: Int = numBigMac.text.toString().toInt()
            if(currentValue>0){
                val newValue=currentValue-1
                numBigMac.text=newValue.toString()
            }
        }
        val orderFood=findViewById<Button>(R.id.orderButton)
        val priceView=findViewById<TextView>(R.id.costView)
        orderFood.setOnClickListener{

            val urlLocalHost = "http://192.168.56.1//:80"  // Server-side endpoint
            val jsonArr=JSONArray(arrayOf(numFrenchFries.text.toString().toInt(), numBigMac.text.toString().toInt()))
//            val jsonData = "\"method\": \"order\",  \"data\": {$jsonArr}"
            val jsonObject = JSONObject()
            jsonObject.put("method", "ordering")
            jsonObject.put("args", jsonArr)
//            val mediaType: MediaType? = MediaType.parse("application/json; charset=utf-8")
            val mediaType = "application/json; charset=utf-8"?.toMediaTypeOrNull()

            Thread{
                val requestBody = jsonObject.toString().toRequestBody(mediaType)
//                val postBody: RequestBody = FormBody.Builder()
//                    .add("French Fries", numOneText.text.toString())
//                    .add("Big Mac", numTwoText.text.toString())
//                    .build()
                val request = Request.Builder()
                    .url(urlLocalHost)
                    .post(requestBody)
                    .build()
                val response: Response
                val client:OkHttpClient= OkHttpClient()
                val call=client.newCall(request)
                try{
                    response = call.execute()
                    if (response.isSuccessful) {
                        val serverResponse: String? = response.body?.string()
                        val jsonObject = JSONObject(serverResponse)
                        val storeSuccess=jsonObject.getString("commit").toBoolean()
                        val totalPrice = jsonObject.getString("total price")

                        // Update the UI with the total price
                        if(storeSuccess){
                            runOnUiThread {
                                priceView.text = totalPrice
                            }
                        }
                        else{
                            println("Did not store into database")
                        }
                    } else {
                        println("Request failed. Status code: ${response.code}")
                    }
                } catch (e: IOException){
                    e.printStackTrace()
                }
            }.start()
        }
        val viewOrder=findViewById<Button>(R.id.viewOrderButton)
        viewOrder.setOnClickListener{
            val intent = Intent(this, ViewRecipe::class.java)
            startActivity(intent)
        }
    }
}