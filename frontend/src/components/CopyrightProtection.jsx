import { useEffect } from 'react';

const CopyrightProtection = () => {
  useEffect(() => {
    // Show copyright dialog on right-click instead of blocking
    const handleContextMenu = (e) => {
      // Only show dialog for images
      if (e.target.tagName === 'IMG') {
        e.preventDefault();
        alert('Copyright Mind\'s Eye Photography 2025\nUse contact form to find purchase options.');
        return false;
      }
    };

    // Disable keyboard shortcuts only for image-related actions
    const handleKeyDown = (e) => {
      // Only block Ctrl+S (Save Page) to prevent saving images
      if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        alert('Copyright Mind\'s Eye Photography 2025\nUse contact form to find purchase options.');
        return false;
      }
      
      // Allow all other keyboard shortcuts for normal browsing
    };

    // Disable drag and drop on images
    const handleDragStart = (e) => {
      if (e.target.tagName === 'IMG') {
        e.preventDefault();
        return false;
      }
    };

    // Disable text selection on images
    const handleSelectStart = (e) => {
      if (e.target.tagName === 'IMG') {
        e.preventDefault();
        return false;
      }
    };

    // Add event listeners
    document.addEventListener('contextmenu', handleContextMenu);
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('dragstart', handleDragStart);
    document.addEventListener('selectstart', handleSelectStart);

    // Add CSS to prevent image selection and dragging
    const style = document.createElement('style');
    style.textContent = `
      img {
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        user-select: none !important;
        -webkit-user-drag: none !important;
        -khtml-user-drag: none !important;
        -moz-user-drag: none !important;
        -o-user-drag: none !important;
        user-drag: none !important;
        pointer-events: auto !important;
      }
      
      /* Disable long-press on mobile */
      img {
        -webkit-touch-callout: none !important;
        -webkit-tap-highlight-color: transparent !important;
      }
      
      /* Prevent image highlighting */
      img::selection {
        background: transparent !important;
      }
      
      img::-moz-selection {
        background: transparent !important;
      }
    `;
    document.head.appendChild(style);

    // Cleanup function
    return () => {
      document.removeEventListener('contextmenu', handleContextMenu);
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('dragstart', handleDragStart);
      document.removeEventListener('selectstart', handleSelectStart);
      if (style.parentNode) {
        style.parentNode.removeChild(style);
      }
    };
  }, []);

  return null; // This component doesn't render anything visible
};

export default CopyrightProtection;

