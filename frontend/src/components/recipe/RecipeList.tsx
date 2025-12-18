/**
 * Recipe List Component - Displays all recipes
 */
import { useQuery } from '@tanstack/react-query';
import recipeService from '../../services/recipeService';
import type { Recipe } from '../../types/recipe';

interface RecipeListProps {
  onSelectRecipe: (recipeId: string) => void;
}

export default function RecipeList({ onSelectRecipe }: RecipeListProps) {
  const { data: recipes, isLoading, error } = useQuery({
    queryKey: ['recipes'],
    queryFn: () => recipeService.listRecipes(),
  });

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p className="text-red-700">Failed to load recipes</p>
        <p className="text-red-600 text-sm mt-2">
          {error instanceof Error ? error.message : 'Unknown error'}
        </p>
      </div>
    );
  }

  if (!recipes || recipes.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          className="w-16 h-16 mx-auto text-gray-400 mb-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
          />
        </svg>
        <h2 className="text-xl font-semibold text-gray-700 mb-2">
          No Recipes Yet
        </h2>
        <p className="text-gray-600">
          Create your first recipe to get started
        </p>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">All Recipes</h2>
        <p className="text-gray-600 mt-1">
          {recipes.length} {recipes.length === 1 ? 'recipe' : 'recipes'} found
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {recipes.map((recipe: Recipe) => (
          <RecipeCard
            key={recipe.id}
            recipe={recipe}
            onClick={() => onSelectRecipe(recipe.id)}
          />
        ))}
      </div>
    </div>
  );
}

interface RecipeCardProps {
  recipe: Recipe;
  onClick: () => void;
}

function RecipeCard({ recipe, onClick }: RecipeCardProps) {
  // Get unique cooking actions from all steps
  const allActions = recipe.steps.flatMap((step) =>
    step.extracted_actions.map((action) => action.canonical_name)
  );
  const uniqueActions = Array.from(new Set(allActions));

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer border border-gray-200 overflow-hidden"
    >
      {/* Recipe Header */}
      <div className="p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
          {recipe.title}
        </h3>
        {recipe.description && (
          <p className="text-gray-600 text-sm mb-4 line-clamp-3">
            {recipe.description}
          </p>
        )}

        {/* Recipe Metadata */}
        <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
          <div className="flex items-center gap-1">
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
            <span>{recipe.steps.length} steps</span>
          </div>
          {recipe.recipe_metadata?.servings && (
            <div className="flex items-center gap-1">
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
              <span>{recipe.recipe_metadata.servings} servings</span>
            </div>
          )}
        </div>

        {/* Cooking Actions Tags */}
        {uniqueActions.length > 0 && (
          <div className="pt-4 border-t border-gray-100">
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">
              Techniques ({uniqueActions.length})
            </p>
            <div className="flex flex-wrap gap-2">
              {uniqueActions.slice(0, 6).map((action) => (
                <span
                  key={action}
                  className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-50 text-blue-700"
                >
                  {action}
                </span>
              ))}
              {uniqueActions.length > 6 && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                  +{uniqueActions.length - 6} more
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Click to view indicator */}
      <div className="bg-gray-50 px-6 py-3 border-t border-gray-100">
        <div className="flex items-center justify-between text-sm text-primary font-medium">
          <span>View Recipe</span>
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </div>
      </div>
    </div>
  );
}
