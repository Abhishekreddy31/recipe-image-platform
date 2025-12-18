/**
 * Recipe API service
 */
import { apiClient } from './api';
import type { Recipe, RecipeCreateRequest } from '../types/recipe';

const recipeService = {
  async getRecipe(id: string): Promise<Recipe> {
    const { data } = await apiClient.get<Recipe>(`/recipes/${id}/`);
    return data;
  },

  async listRecipes(skip = 0, limit = 100): Promise<Recipe[]> {
    const { data } = await apiClient.get<Recipe[]>('/recipes/', {
      params: { skip, limit },
    });
    return data;
  },

  async createRecipe(recipe: RecipeCreateRequest): Promise<Recipe> {
    const { data } = await apiClient.post<Recipe>('/recipes/', recipe);
    return data;
  },
};

export default recipeService;
