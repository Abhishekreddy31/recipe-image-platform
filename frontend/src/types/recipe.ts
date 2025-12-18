/**
 * Recipe and Recipe Step type definitions
 */

export interface Recipe {
  id: string;
  title: string;
  description?: string;
  created_at: string;
  metadata?: Record<string, any>;
  steps: RecipeStep[];
}

export interface RecipeStep {
  id: string;
  step_number: number;
  instruction_text: string;
  extracted_actions: ExtractedAction[];
}

export interface ExtractedAction {
  id: string;
  canonical_name: string;
  description?: string;
  category: string;
  image_url?: string;
  thumbnail_url?: string;
  attribution?: string;
  license?: string;
  confidence: number;
}

export interface RecipeCreateRequest {
  title: string;
  description?: string;
  steps: RecipeStepCreate[];
  metadata?: Record<string, any>;
}

export interface RecipeStepCreate {
  step_number: number;
  instruction_text: string;
}
