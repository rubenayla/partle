/**
 * @fileoverview Google Analytics 4 utilities for tracking user interactions
 * @module utils/analytics
 */
// Declare gtag as a global function
declare global {
  interface Window {
    gtag: (...args: any[]) => void;
  }
}

// Your GA4 Measurement ID
export const GA_MEASUREMENT_ID = 'G-E4FDR3NMV7';

/**
 * Initialize Google Analytics 4
 * Call this once when your app starts
 */
export const initGA = (): void => {
  // Only initialize in browser environment
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('config', GA_MEASUREMENT_ID, {
      send_page_view: false, // We'll send page views manually
      anonymize_ip: true, // GDPR compliance
    });
    
    console.log('Google Analytics initialized:', GA_MEASUREMENT_ID);
  }
};

/**
 * Track page views
 * Call this on route changes
 */
export const trackPageView = (path: string, title?: string): void => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('config', GA_MEASUREMENT_ID, {
      page_path: path,
      page_title: title || document.title,
    });
  }
};

/**
 * Track custom events
 * Use this for user interactions
 */
export const trackEvent = (eventName: string, parameters?: Record<string, any>): void => {
  if (typeof window !== 'undefined' && window.gtag) {
    window.gtag('event', eventName, {
      ...parameters,
    });
  }
};

/**
 * Track product view events (e-commerce)
 */
export const trackProductView = (product: {
  id: number;
  name: string;
  price?: number;
  store?: string;
}): void => {
  trackEvent('view_item', {
    currency: 'EUR',
    value: product.price || 0,
    items: [{
      item_id: product.id.toString(),
      item_name: product.name,
      item_category: 'Product',
      item_brand: product.store || 'Unknown',
      price: product.price || 0,
      quantity: 1,
    }]
  });
};

/**
 * Track search events
 */
export const trackSearch = (searchTerm: string, filters?: Record<string, any>): void => {
  trackEvent('search', {
    search_term: searchTerm,
    ...filters,
  });
};

/**
 * Track store visits
 */
export const trackStoreVisit = (store: {
  id: number;
  name: string;
  type?: string;
}): void => {
  trackEvent('view_store', {
    store_id: store.id.toString(),
    store_name: store.name,
    store_type: store.type || 'unknown',
  });
};

/**
 * Track external link clicks (product URLs, store websites)
 */
export const trackExternalLink = (url: string, linkType: 'product' | 'store' | 'other'): void => {
  trackEvent('click_external_link', {
    link_url: url,
    link_type: linkType,
  });
};

/**
 * Track documentation page views
 */
export const trackDocumentationView = (section?: string): void => {
  trackEvent('view_documentation', {
    section: section || 'main',
  });
};