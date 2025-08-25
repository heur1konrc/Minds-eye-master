import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

const AboutPage = () => {
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
              content: `Born and raised right here in Madison, Wisconsin, I'm a creative spirit with a passion for bringing visions to life. My journey has woven through various rewarding paths – as a musician, a teacher, a REALTOR, and a small business owner. Each of these roles has fueled my inspired, creative, and driven approach to everything I do, especially when it comes to photography.

At the heart of Mind's Eye Photography: Where Moments Meet Imagination is my dedication to you. While I cherish the fulfillment of capturing moments that spark my own imagination, my true passion lies in doing the same for my clients. Based in Madison, I frequently travel across the state, always on the lookout for that next inspiring scene.

For me, client satisfaction isn't just a goal – it's the foundation of every interaction. I pour my energy into ensuring you not only love your photos but also enjoy the entire experience. It's truly rewarding to see clients transform into lifelong friends, and that's the kind of connection I strive to build with everyone I work with.

Rick Corey`,
              images: []
            })
          }
        }
      } catch (error) {
        console.error('Error fetching about data:', error)
        // Fallback to Rick's authentic content
        setAboutData({
          content: `Born and raised right here in Madison, Wisconsin, I'm a creative spirit with a passion for bringing visions to life. My journey has woven through various rewarding paths – as a musician, a teacher, a REALTOR, and a small business owner. Each of these roles has fueled my inspired, creative, and driven approach to everything I do, especially when it comes to photography.

At the heart of Mind's Eye Photography: Where Moments Meet Imagination is my dedication to you. While I cherish the fulfillment of capturing moments that spark my own imagination, my true passion lies in doing the same for my clients. Based in Madison, I frequently travel across the state, always on the lookout for that next inspiring scene.

For me, client satisfaction isn't just a goal – it's the foundation of every interaction. I pour my energy into ensuring you not only love your photos but also enjoy the entire experience. It's truly rewarding to see clients transform into lifelong friends, and that's the kind of connection I strive to build with everyone I work with.

Rick Corey`,
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

      {/* Two-Column Layout */}
      <div className="max-w-7xl mx-auto px-6 py-16">
        <div className="grid lg:grid-cols-3 gap-12">
          
          {/* Left Column - Behind the Lens Images (1/3) */}
          <motion.div 
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="lg:col-span-1"
          >
            <h2 className="text-2xl font-light text-orange-400 mb-8 text-center lg:text-left">
              Behind the Lens
            </h2>
            
            <div className="space-y-6">
              {aboutData.images && aboutData.images.length > 0 ? (
                aboutData.images.map((image, index) => (
                  <motion.div
                    key={image.id}
                    initial={{ opacity: 0, y: 30 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 + index * 0.1 }}
                    className="bg-slate-800 rounded-lg overflow-hidden shadow-lg"
                  >
                    <img
                      src={`/assets/about/${image.filename}`}
                      alt={image.title}
                      className="w-full h-96 object-cover"
                    />
                  </motion.div>
                ))
              ) : (
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.6 }}
                  className="bg-slate-800 rounded-lg p-8 text-center"
                >
                  <p className="text-slate-400">
                    Behind-the-scenes images will appear here once uploaded via the admin panel.
                  </p>
                </motion.div>
              )}
            </div>
          </motion.div>

          {/* Right Column - About Content (2/3) */}
          <motion.div 
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            className="lg:col-span-2"
          >
            <div className="prose prose-lg prose-invert max-w-none">
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.7 }}
                className="text-slate-300 leading-relaxed text-lg"
                dangerouslySetInnerHTML={{ __html: processMarkdown(aboutData.content) }}
              />
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default AboutPage

