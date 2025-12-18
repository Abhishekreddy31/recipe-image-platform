/**
 * CreateRecipeForm - Form to create a new recipe
 */
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import recipeService from '../../services/recipeService';
import type { Recipe, RecipeStepCreate } from '../../types/recipe';

interface CreateRecipeFormProps {
  onSuccess: (recipe: Recipe) => void;
}

export default function CreateRecipeForm({ onSuccess }: CreateRecipeFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [steps, setSteps] = useState<string[]>(['']);

  const createRecipeMutation = useMutation({
    mutationFn: recipeService.createRecipe,
    onSuccess: (recipe) => {
      onSuccess(recipe);
      // Reset form
      setTitle('');
      setDescription('');
      setSteps(['']);
    },
  });

  const handleAddStep = () => {
    setSteps([...steps, '']);
  };

  const handleRemoveStep = (index: number) => {
    setSteps(steps.filter((_, i) => i !== index));
  };

  const handleStepChange = (index: number, value: string) => {
    const newSteps = [...steps];
    newSteps[index] = value;
    setSteps(newSteps);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const recipeSteps: RecipeStepCreate[] = steps
      .filter((step) => step.trim())
      .map((step, index) => ({
        step_number: index + 1,
        instruction_text: step.trim(),
      }));

    if (recipeSteps.length === 0) {
      alert('Please add at least one step');
      return;
    }

    createRecipeMutation.mutate({
      title: title.trim(),
      description: description.trim() || undefined,
      steps: recipeSteps,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Create New Recipe</h2>

      {/* Title */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Recipe Title *
        </label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
          placeholder="e.g., Simple Tomato Pasta"
        />
      </div>

      {/* Description */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Description
        </label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={2}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
          placeholder="Brief description of the recipe"
        />
      </div>

      {/* Steps */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Instructions *
        </label>
        <div className="space-y-3">
          {steps.map((step, index) => (
            <div key={index} className="flex gap-2">
              <span className="flex-shrink-0 w-8 h-10 bg-gray-100 rounded flex items-center justify-center text-sm font-semibold">
                {index + 1}
              </span>
              <textarea
                value={step}
                onChange={(e) => handleStepChange(index, e.target.value)}
                rows={2}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="e.g., Dice the onions and mince the garlic..."
              />
              {steps.length > 1 && (
                <button
                  type="button"
                  onClick={() => handleRemoveStep(index)}
                  className="flex-shrink-0 text-red-600 hover:text-red-800"
                >
                  Remove
                </button>
              )}
            </div>
          ))}
        </div>
        <button
          type="button"
          onClick={handleAddStep}
          className="mt-3 text-primary hover:text-primary-dark font-medium"
        >
          + Add Step
        </button>
      </div>

      {/* Submit */}
      <div className="flex gap-3">
        <button
          type="submit"
          disabled={createRecipeMutation.isPending}
          className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {createRecipeMutation.isPending ? 'Creating...' : 'Create Recipe'}
        </button>
      </div>

      {/* Error */}
      {createRecipeMutation.isError && (
        <div className="mt-4 bg-red-50 border border-red-200 rounded-md p-3">
          <p className="text-red-800 text-sm">
            Error creating recipe. Please try again.
          </p>
        </div>
      )}

      {/* Success hint */}
      <p className="mt-4 text-sm text-gray-600">
        💡 Tip: Use cooking verbs like "dice", "sauté", "boil", "whisk" to see automatic technique detection!
      </p>
    </form>
  );
}
