/**
 * RecipeView - Main container component for displaying a recipe
 */
import { useQuery } from '@tanstack/react-query';
import recipeService from '../../services/recipeService';
import RecipeStep from './RecipeStep';

interface RecipeViewProps {
  recipeId: string;
}

export default function RecipeView({ recipeId }: RecipeViewProps) {
  const { data: recipe, isLoading, error } = useQuery({
    queryKey: ['recipe', recipeId],
    queryFn: () => recipeService.getRecipe(recipeId),
  });

  if (isLoading) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-8 bg-gray-200 rounded w-3/4"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        {[1, 2, 3].map(i => (
          <div key={i} className="recipe-step-card h-32"></div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <h2 className="text-red-800 font-semibold">Error loading recipe</h2>
        <p className="text-red-600">
          {error instanceof Error ? error.message : 'Unknown error occurred'}
        </p>
      </div>
    );
  }

  if (!recipe) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <p className="text-yellow-800">Recipe not found</p>
      </div>
    );
  }

  return (
    <article className="max-w-4xl mx-auto p-6">
      {/* Recipe Header */}
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          {recipe.title}
        </h1>
        {recipe.description && (
          <p className="text-lg text-gray-600">{recipe.description}</p>
        )}
        <div className="mt-4 text-sm text-gray-500">
          Created: {new Date(recipe.created_at).toLocaleDateString()}
        </div>
      </header>

      {/* Recipe Steps */}
      <div className="space-y-6">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">
          Instructions
        </h2>
        {recipe.steps.map((step) => (
          <RecipeStep key={step.id} step={step} />
        ))}
      </div>
    </article>
  );
}
