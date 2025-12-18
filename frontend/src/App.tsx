/**
 * Main App Component
 */
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
import RecipeView from './components/recipe/RecipeView';
import RecipeList from './components/recipe/RecipeList';
import CreateRecipeForm from './components/recipe/CreateRecipeForm';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 2,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  const [selectedRecipeId, setSelectedRecipeId] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-6xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Recipe Platform
                </h1>
                <p className="text-sm text-gray-600">
                  Cooking with visual guidance
                </p>
              </div>
              <button
                onClick={() => setShowCreateForm(!showCreateForm)}
                className="btn-primary"
              >
                {showCreateForm ? 'Cancel' : 'Create Recipe'}
              </button>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-6xl mx-auto px-4 py-8">
          {showCreateForm ? (
            <CreateRecipeForm
              onSuccess={(recipe) => {
                setSelectedRecipeId(recipe.id);
                setShowCreateForm(false);
              }}
            />
          ) : selectedRecipeId ? (
            <div>
              <button
                onClick={() => setSelectedRecipeId(null)}
                className="mb-4 text-primary hover:text-primary-dark"
              >
                ← Back to list
              </button>
              <RecipeView recipeId={selectedRecipeId} />
            </div>
          ) : (
            <RecipeList onSelectRecipe={setSelectedRecipeId} />
          )}
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-gray-200 mt-12">
          <div className="max-w-6xl mx-auto px-4 py-6 text-center text-sm text-gray-600">
            <p>
              100% free and open-source | Images from{' '}
              <a
                href="https://commons.wikimedia.org"
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline"
              >
                Wikimedia Commons
              </a>
            </p>
            <p className="mt-2">
              Built with FastAPI + React + spaCy NLP
            </p>
          </div>
        </footer>
      </div>
    </QueryClientProvider>
  );
}

export default App;
