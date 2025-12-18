/**
 * TechniqueImage - Display cooking technique image with attribution
 */
import { useState } from 'react';
import type { ExtractedAction } from '../../types/recipe';

interface TechniqueImageProps {
  action: ExtractedAction;
}

export default function TechniqueImage({ action }: TechniqueImageProps) {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const hasImage = action.image_url || action.thumbnail_url;

  // Build full image URL - images are served from backend root, not /api/v1
  const BACKEND_BASE = import.meta.env.VITE_API_BASE_URL?.replace('/api/v1', '') || 'http://localhost:8000';
  const relativeUrl = action.thumbnail_url || action.image_url;
  const imageUrl = relativeUrl ? `${BACKEND_BASE}${relativeUrl}` : null;

  if (!hasImage || imageError) {
    return (
      <div className="technique-placeholder bg-gray-100 border-2 border-dashed border-gray-300 rounded-md p-4 text-center">
        <div className="text-gray-400 mb-2">
          <svg className="w-8 h-8 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <p className="text-sm text-gray-600 font-medium capitalize">
          {action.canonical_name}
        </p>
        <p className="text-xs text-gray-500 mt-1">Image pending</p>
      </div>
    );
  }

  return (
    <figure className="technique-image relative group">
      {/* Loading skeleton */}
      {!imageLoaded && (
        <div className="absolute inset-0 bg-gray-200 animate-pulse rounded-md" />
      )}

      {/* Image */}
      <img
        src={imageUrl}
        alt={`${action.canonical_name} cooking technique demonstration`}
        className={`w-full h-32 object-cover rounded-md transition-opacity duration-200 ${
          imageLoaded ? 'opacity-100' : 'opacity-0'
        }`}
        onLoad={() => setImageLoaded(true)}
        onError={() => setImageError(true)}
        loading="lazy"
      />

      {/* Overlay with technique name */}
      <figcaption className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-2 text-white text-sm font-medium capitalize">
        {action.canonical_name}
      </figcaption>

      {/* Tooltip on hover */}
      {action.description && (
        <div className="hidden group-hover:block absolute -top-2 left-1/2 transform -translate-x-1/2 -translate-y-full z-10 bg-gray-900 text-white text-xs rounded py-1 px-2 whitespace-nowrap">
          {action.description}
          <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
        </div>
      )}

      {/* Attribution (small text) */}
      {action.attribution && (
        <div className="mt-1 text-xs text-gray-500 truncate">
          {action.license}
        </div>
      )}
    </figure>
  );
}
