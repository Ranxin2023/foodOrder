package com.example.foodordernew

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val orderButton=findViewById<Button>(R.id.ordering)
        orderButton.setOnClickListener{
            val intent = Intent(this, OrderFood::class.java)
            startActivity(intent)
        }
    }
}