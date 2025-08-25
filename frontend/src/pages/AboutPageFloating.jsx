import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

// NUCLEAR OPTION: Completely new component name to force Railway deployment
// TIMESTAMP: 2025-08-25-04-45-00

const AboutPageFloating = () => {
  const [aboutData, setAboutData] = useState({ content: '', images: [] })
  const [loading, setLoading] = useState(true)

  // Simple Markdown processor for basic formatting
  const processMarkdown = (text) => {
    // Convert **bold** to <strong>bold</strong>
    let processed = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    // Convert *italic* to <em>italic</em>
    processed = processed.replace(/\*(.*?)\*/g, '<em>$1</em>')
    // Convert single line breaks to <br> tags
    processed = processed.replace(/\n/g, '<br>')
    return processed
  }

  useEffect(() => {
    const fetchAboutData = async () => {
      try {
        const response = await fetch('/api/about-content')
        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            setAboutData(data)
          } else {
            // Fallback to Rick's authentic content if API fails
            setAboutData({
              content: `Born and raised right here in Madison, Wisconsin, I'm a creative spirit with a passion for bringing visions to life. My journey has woven through various rewarding paths – as a **musician/songwriter**, a **Teacher**, a **REALTOR**, and a **Small Business Owner**. Each of these roles has fueled my inspired, creative, and driven approach to everything I do, especially when it comes to photography.

At the heart of Mind's Eye Photography: Where Moments Meet Imagination is my dedication to you. While I cherish the fulfillment of capturing moments that spark my own imagination, my true passion lies in doing the same for my clients. Based in Madison, I frequently travel across the state, always on the lookout for that next inspiring scene.

For me, client satisfaction isn't just a goal – it's the foundation of every interaction. I pour my energy into ensuring you not only love your photos but also enjoy the entire experience. It's truly rewarding to see clients transform into lifelong friends, and that's the kind of connection I strive to build with everyone I work with.

**Rick Corey**`,
              images: []
            })
          }
        }
      } catch (error) {
        console.error('Error fetching about data:', error)
        // Fallback to Rick's authentic content
        setAboutData({
          content: `Born and raised right here in Madison, Wisconsin, I'm a creative spirit with a passion for bringing visions to life. My journey has woven through various rewarding paths – as a **musician/songwriter**, a **Teacher**, a **REALTOR**, and a **Small Business Owner**. Each of these roles has fueled my inspired, creative, and driven approach to everything I do, especially when it comes to photography.

At the heart of Mind's Eye Photography: Where Moments Meet Imagination is my dedication to you. While I cherish the fulfillment of capturing moments that spark my own imagination, my true passion lies in doing the same for my clients. Based in Madison, I frequently travel across the state, always on the lookout for that next inspiring scene.

For me, client satisfaction isn't just a goal – it's the foundation of every interaction. I pour my energy into ensuring you not only love your photos but also enjoy the entire experience. It's truly rewarding to see clients transform into lifelong friends, and that's the kind of connection I strive to build with everyone I work with.

**Rick Corey**`,
          images: []
        })
      } finally {
        setLoading(false)
      }
    }

    fetchAboutData()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center">
        <div className="text-orange-500 text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <div className="bg-slate-900 py-20">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <motion.h1 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl md:text-5xl font-light text-orange-500 mb-6"
          >
            About Mind's Eye Photography
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-xl text-slate-300"
          >
            Where Moments Meet Imagination
          </motion.p>
        </div>
      </div>

      {/* FLOATING IMAGE LAYOUT - MAGAZINE STYLE */}
      <div className="max-w-4xl mx-auto px-6 py-16">
        <div className="prose prose-lg prose-invert max-w-none">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="text-slate-300 leading-relaxed text-lg"
          >
            {/* Floating Behind the Lens Image - PLACEHOLDER FOR NOW */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6 }}
              className="float-left mr-8 mb-6 w-80 lg:w-96"
            >
              <div className="bg-slate-800 rounded-lg overflow-hidden shadow-2xl aspect-[3/2]">
                {aboutData.images && aboutData.images.length > 0 ? (
                  <img
                    src={`/assets/about/${aboutData.images[0].filename}`}
                    alt="Behind the Lens"
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full bg-gradient-to-br from-green-600 to-green-800 flex items-center justify-center">
                    <p className="text-white text-center font-semibold">
                      Behind the Lens Image<br/>
                      Will appear here once uploaded
                    </p>
                  </div>
                )}
              </div>
              <p className="text-center text-orange-400 text-sm mt-3 font-light">
                Behind the Lens
              </p>
            </motion.div>
            
            {/* Text content that wraps around the floating image */}
            <div dangerouslySetInnerHTML={{ __html: processMarkdown(aboutData.content) }} />
            
            {/* Clear float */}
            <div className="clear-both"></div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default AboutPageFloating

