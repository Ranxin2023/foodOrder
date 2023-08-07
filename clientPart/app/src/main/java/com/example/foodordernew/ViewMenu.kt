package com.example.foodordernew

import android.os.Bundle
import android.widget.ImageView
import android.widget.LinearLayout
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
//import androidx.core.view.marginTop
class ViewMenu:AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.view_menu)
        val imageContainer = findViewById<LinearLayout>(R.id.foodMenuScrollView)
        val imageResourceIds = arrayOf(
            R.drawable.bigmac,
            R.drawable.french_fries,
            R.drawable.doublecheeseburger,
            // Add more image resource IDs here...
        )

        // Loop through the image resource IDs and add ImageView for each image
        for (imageResId in imageResourceIds) {
            val imageView = ImageView(this)
            imageView.setImageDrawable(ContextCompat.getDrawable(this, imageResId))
            imageView.layoutParams = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
            ).apply {
                setMargins(0, resources.getDimensionPixelSize(R.dimen.image_margin_top), 0, 0)
            }

            imageContainer.addView(imageView)
        }
    }
}