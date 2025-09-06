/**
 * @fileoverview Tag API service for fetching and managing tags
 * @module api/tags
 */
import api from './index';
import type { Tag } from '../types';

/**
 * Fetch all available tags from the API
 * 
 * @returns Promise resolving to array of tags
 * @throws Error if the API request fails
 * 
 * @example
 * ```tsx
 * const tags = await getTags();
 * console.log(tags); // [{ id: 1, name: 'online' }, ...]
 * ```
 */
export async function getTags(): Promise<Tag[]> {
  try {
    const response = await api.get<Tag[]>('/v1/tags/');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch tags:', error);
    throw error;
  }
}

/**
 * Create a new tag
 * 
 * @param name - The name of the tag to create
 * @returns Promise resolving to the created tag
 * @throws Error if the API request fails or tag already exists
 * 
 * @example
 * ```tsx
 * const newTag = await createTag('electronics');
 * console.log(newTag.id); // Newly created tag ID
 * ```
 */
export async function createTag(name: string): Promise<Tag> {
  try {
    const response = await api.post<Tag>('/v1/tags/', { name });
    return response.data;
  } catch (error) {
    console.error('Failed to create tag:', error);
    throw error;
  }
}