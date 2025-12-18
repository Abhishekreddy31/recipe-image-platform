/**
 * RecipeStep - Individual recipe step with technique images
 */
import type { RecipeStep as RecipeStepType } from '../../types/recipe';
import TechniqueImage from '../technique/TechniqueImage';

interface RecipeStepProps {
  step: RecipeStepType;
}

export default function RecipeStep({ step }: RecipeStepProps) {
  const hasActions = step.extracted_actions && step.extracted_actions.length > 0;

  return (
    <div className="recipe-step-card">
      <div className="flex gap-6">
        {/* Step Content */}
        <div className="flex-1">
          <div className="flex items-start gap-3 mb-3">
            <span className="flex-shrink-0 w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center font-semibold">
              {step.step_number}
            </span>
            <p className="text-lg text-gray-800 leading-relaxed pt-1">
              {step.instruction_text}
            </p>
          </div>

          {/* Mobile: Show technique count */}
          {hasActions && (
            <div className="md:hidden mt-3 pt-3 border-t border-gray-200">
              <p className="text-sm text-gray-600">
                {step.extracted_actions.length} technique{step.extracted_actions.length > 1 ? 's' : ''} detected
              </p>
            </div>
          )}
        </div>

        {/* Desktop: Technique Images (side-by-side) */}
        {hasActions && (
          <div className="hidden md:flex flex-wrap gap-3 w-64">
            {step.extracted_actions.map((action) => (
              <TechniqueImage key={action.id} action={action} />
            ))}
          </div>
        )}
      </div>

      {/* Mobile: Technique Images (stacked below) */}
      {hasActions && (
        <div className="md:hidden mt-4 pt-4 border-t border-gray-200">
          <details className="group">
            <summary className="cursor-pointer text-primary font-medium hover:text-primary-dark transition-colors">
              View {step.extracted_actions.length} technique{step.extracted_actions.length > 1 ? 's' : ''}
            </summary>
            <div className="mt-4 space-y-3">
              {step.extracted_actions.map((action) => (
                <TechniqueImage key={action.id} action={action} />
              ))}
            </div>
          </details>
        </div>
      )}
    </div>
  );
}
