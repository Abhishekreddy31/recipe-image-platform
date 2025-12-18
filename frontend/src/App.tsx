/**
 * Main App Component
 */
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
import RecipeView from './components/recipe/RecipeView';
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
                Welcome to Recipe Platform
              </h2>
              <p className="text-gray-600 mb-6">
                Create a recipe to see automatic cooking technique image detection
              </p>
              <button
                onClick={() => setShowCreateForm(true)}
                className="btn-primary"
              >
                Create Your First Recipe
              </button>
            </div>
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
