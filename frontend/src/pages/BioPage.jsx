import React from 'react'

// BRAND NEW BIO PAGE - BUILT FROM SCRATCH
// NO CACHE, NO HISTORY, NO PROBLEMS
// FLOATING IMAGE LAYOUT LIKE REFERENCE

const BioPage = () => {
  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <div className="bg-slate-900 py-20">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <h1 className="text-4xl md:text-5xl font-light text-orange-500 mb-6">
            About Mind's Eye Photography
          </h1>
          <p className="text-xl text-slate-300">
            Where Moments Meet Imagination
          </p>
        </div>
      </div>

      {/* FLOATING IMAGE LAYOUT - EXACTLY LIKE REFERENCE */}
      <div className="max-w-4xl mx-auto px-6 py-16">
        <div className="text-slate-300 leading-relaxed text-lg">
          
          {/* Floating Behind the Lens Image */}
          <div style={{
            float: 'left',
            marginRight: '2rem',
            marginBottom: '1.5rem',
            width: '320px'
          }}>
            <div className="bg-slate-800 rounded-lg overflow-hidden shadow-2xl" style={{aspectRatio: '3/2'}}>
              <div className="w-full h-full bg-gradient-to-br from-green-600 to-green-800 flex items-center justify-center">
                <p className="text-white text-center font-semibold">
                  Behind the Lens Image<br/>
                  Will appear here once uploaded
                </p>
              </div>
            </div>
            <p className="text-center text-orange-400 text-sm mt-3 font-light">
              Behind the Lens
            </p>
          </div>
          
          {/* Text content that wraps around the floating image */}
          <div>
            <p className="mb-6">
              Born and raised right here in Madison, Wisconsin, I'm a creative spirit with a passion for bringing visions to life. My journey has woven through various rewarding paths – as a <strong>musician/songwriter</strong>, a <strong>Teacher</strong>, a <strong>REALTOR</strong>, and a <strong>Small Business Owner</strong>. Each of these roles has fueled my inspired, creative, and driven approach to everything I do, especially when it comes to photography.
            </p>
            
            <p className="mb-6">
              At the heart of Mind's Eye Photography: Where Moments Meet Imagination is my dedication to you. While I cherish the fulfillment of capturing moments that spark my own imagination, my true passion lies in doing the same for my clients. Based in Madison, I frequently travel across the state, always on the lookout for that next inspiring scene.
            </p>
            
            <p className="mb-6">
              For me, client satisfaction isn't just a goal – it's the foundation of every interaction. I pour my energy into ensuring you not only love your photos but also enjoy the entire experience. It's truly rewarding to see clients transform into lifelong friends, and that's the kind of connection I strive to build with everyone I work with.
            </p>
            
            <p className="font-semibold text-lg">
              Rick Corey
            </p>
          </div>
          
          {/* Clear float */}
          <div style={{clear: 'both'}}></div>
        </div>
      </div>
    </div>
  )
}

export default BioPage

