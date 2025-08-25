import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'

const FeaturedPage = () => {
  const [featuredImage, setFeaturedImage] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showFullscreen, setShowFullscreen] = useState(false)

  // Format date to mm/dd/year hh:mm AM/PM
  const formatExifDate = (dateString) => {
    if (!dateString || dateString === 'Unknown') return 'Unknown';
    
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return dateString; // Return original if invalid
      
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const year = date.getFullYear();
      
      let hours = date.getHours();
      const minutes = String(date.getMinutes()).padStart(2, '0');
      const ampm = hours >= 12 ? 'PM' : 'AM';
      
      hours = hours % 12;
      hours = hours ? hours : 12; // 0 should be 12
      const formattedHours = String(hours).padStart(2, '0');
      
      return `${month}/${day}/${year} ${formattedHours}:${minutes} ${ampm}`;
    } catch (error) {
      return dateString; // Return original if formatting fails
    }
  };

  useEffect(() => {
    const fetchFeaturedImage = async () => {
      try {
        const response = await fetch('https://minds-eye-master-production.up.railway.app/api/featured')
        if (!response.ok) {
          throw new Error('Failed to fetch featured image')
        }
        const data = await response.json()
        
        if (data) {
          setFeaturedImage(data)
        } else {
          setError('No featured image set')
        }
      } catch (err) {
        console.error('Error fetching featured image:', err)
        setError('Failed to load featured image')
      } finally {
        setLoading(false)
      }
    }

    fetchFeaturedImage()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-900 pt-20 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500"></div>
      </div>
    )
  }

  if (error || !featuredImage) {
    return (
      <div className="min-h-screen bg-slate-900 pt-20 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-orange-500 mb-4">No Featured Image</h2>
          <p className="text-slate-300">{error || 'No featured image has been set yet.'}</p>
        </div>
      </div>
    )
  }

  const imageUrl = `https://minds-eye-master-production.up.railway.app/static/assets/${featuredImage.image}`
  const exif = featuredImage.exif_data || {}

  return (
    <div className="min-h-screen bg-slate-900 pt-20">
      {/* Header */}
      <div className="text-center py-12">
        <motion.h1 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl md:text-5xl font-bold text-orange-500 mb-4"
        >
          WEEKLY FEATURED IMAGE
        </motion.h1>
      </div>

      <div className="max-w-7xl mx-auto px-6 pb-12">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Featured Image */}
          <motion.div 
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="lg:col-span-2"
          >
            <div className="relative">
              {/* Main Image */}
              <div className="rounded-lg overflow-hidden shadow-2xl cursor-pointer"
                   onClick={() => setShowFullscreen(true)}>
                <img
                  src={imageUrl}
                  alt={featuredImage.title}
                  className="w-full h-auto hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600"><rect width="800" height="600" fill="%23374151"/><text x="400" y="300" text-anchor="middle" fill="%23fff" font-size="24">Featured Image</text></svg>'
                  }}
                />
              </div>
              
              {/* Click to view fullscreen hint */}
              <div className="absolute bottom-4 right-4 bg-black bg-opacity-50 text-white px-3 py-1 rounded-md text-sm">
                Click to view fullscreen
              </div>
            </div>
          </motion.div>

          {/* Technical Details */}
          <motion.div 
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
            className="space-y-6"
          >
            {/* EXIF Data Card */}
            <div className="bg-slate-800 rounded-lg p-6">
              <h3 className="text-orange-500 text-lg font-semibold mb-4">Image Capture Information</h3>
              
              <div className="space-y-3 text-slate-300">
                {exif && Object.keys(exif).length > 0 ? (
                  <>
                    {exif.camera && (
                      <div className="flex justify-between">
                        <span className="text-slate-400">Camera:</span>
                        <span className="text-right text-sm">{exif.camera}</span>
                      </div>
                    )}
                    
                    {exif.lens && (
                      <div className="flex justify-between">
                        <span className="text-slate-400">Lens:</span>
                        <span className="text-right text-sm">{exif.lens}</span>
                      </div>
                    )}
                    
                    {exif.aperture && exif.aperture !== 'Unknown' && (
                      <div className="flex justify-between">
                        <span className="text-slate-400">Aperture:</span>
                        <span>f/{exif.aperture}</span>
                      </div>
                    )}
                    
                    {exif.shutter_speed && exif.shutter_speed !== 'Unknown' && (
                      <div className="flex justify-between">
                        <span className="text-slate-400">Shutter:</span>
                        <span>{exif.shutter_speed}s</span>
                      </div>
                    )}
                    
                    {exif.iso && exif.iso !== 'Unknown' && (
                      <div className="flex justify-between">
                        <span className="text-slate-400">ISO:</span>
                        <span>{exif.iso}</span>
                      </div>
                    )}
                  </>
                ) : (
                  <div className="text-slate-400 text-sm italic">
                    EXIF data not available for this image
                  </div>
                )}
                
                {exif.date_taken && exif.date_taken !== 'Unknown' && (
                  <div className="flex justify-between">
                    <span className="text-slate-400">Date:</span>
                    <span className="text-right text-sm">{formatExifDate(exif.date_taken)}</span>
                  </div>
                )}
              </div>
              
              <button 
                className="w-full mt-6 bg-orange-500 hover:bg-orange-600 text-white py-2 px-4 rounded-md transition-colors"
                onClick={() => setShowFullscreen(true)}
              >
                View Fullscreen
              </button>
              
              {/* Download Button */}
              <button 
                className="w-full mt-3 bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-md transition-colors flex items-center justify-center gap-2"
                onClick={() => {
                  const link = document.createElement('a')
                  link.href = imageUrl
                  link.download = `${featuredImage.title || 'featured-image'}.jpg`
                  link.target = '_blank'
                  document.body.appendChild(link)
                  link.click()
                  document.body.removeChild(link)
                }}
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Download Image
              </button>
            </div>
            
            {/* Image Information Badges */}
            <div className="bg-slate-800 rounded-lg p-6 mt-6">
              <div className="flex flex-wrap gap-3">
                <div className="bg-orange-500 text-white px-4 py-2 rounded-md text-sm font-bold">
                  {featuredImage.title}
                </div>
                {featuredImage.categories && featuredImage.categories.length > 0 && (
                  <div className="bg-orange-600 text-white px-4 py-2 rounded-md text-sm">
                    {featuredImage.categories[0]}
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        </div>

        {/* Story Behind the Shot */}
        {featuredImage.story && (
          <motion.div 
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="mt-12 bg-slate-800 rounded-lg p-8"
          >
            <h3 className="text-orange-500 text-2xl font-semibold mb-6">The Story Behind the Shot</h3>
            <p className="text-slate-300 text-lg leading-relaxed">
              {featuredImage.story}
            </p>
          </motion.div>
        )}
      </div>

      {/* Fullscreen Modal */}
      {showFullscreen && (
        <div className="fixed inset-0 bg-black bg-opacity-95 z-50 flex items-center justify-center p-4"
             onClick={() => setShowFullscreen(false)}>
          <div className="relative max-w-full max-h-full">
            {/* Close button */}
            <button 
              className="absolute top-4 right-4 text-white text-2xl bg-black bg-opacity-50 rounded-full w-10 h-10 flex items-center justify-center hover:bg-opacity-75 z-10"
              onClick={(e) => {
                e.stopPropagation()
                setShowFullscreen(false)
              }}
            >
              ×
            </button>
            
            {/* Fullscreen image - right-click enabled */}
            <img
              src={imageUrl}
              alt={featuredImage.title}
              className="max-w-full max-h-full object-contain"
              style={{ 
                userSelect: 'auto',
                pointerEvents: 'auto',
                WebkitUserSelect: 'auto',
                MozUserSelect: 'auto',
                msUserSelect: 'auto'
              }}
              onContextMenu={(e) => {
                // Allow right-click context menu for this image only
                e.stopPropagation()
              }}
              onClick={(e) => e.stopPropagation()}
            />
            
            {/* Download hint */}
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black bg-opacity-75 text-white px-4 py-2 rounded-md text-sm">
              Right-click to save image
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default FeaturedPage

