---
name: recipe-create-edit-ui
description: Implementation of recipe create and edit UI for Fold It In project
category: web-development
state: complete
---

# Recipe Create and Edit UI Implementation

This skill documents the implementation of the recipe create and edit UI for the Fold It In community recipe site, covering both the API endpoint updates and the frontend forms.

## Overview

Implemented the recipe creation and editing functionality for the Fold It In community recipe site with:

1. Extended PATCH API route to support full recipe updates
2. Create page (app/recipes/new/page.tsx) 
3. Edit page (app/recipes/[id]/edit/page.tsx)
4. Reusable RecipeForm client component 
5. Styling for the form

## Key Features

- Complete CRUD support for recipes (POST and PATCH endpoints)
- Drag-and-drop reordering for ingredients, steps, and images
- Client-side Zod validation before submission  
- Auto-save to localStorage with draft restoration
- Authentication and authorization checks
- Proper error handling and user feedback
- Clean, editorial styling consistent with project design tokens

## Technical Implementation Details

### API Extension (app/api/v1/recipes/[id]/route.ts)

Extended the PATCH endpoint to accept updates for all recipe fields including:
- Tags with upsert and replace semantics
- Ingredients with full replacement using transactional updates
- Steps with full replacement using transactional updates  
- Images with full replacement using transactional updates

Used proper Prisma model names from schema:
- `recipeIngredient` for ingredients 
- `recipeStep` for steps
- `recipeImage` for images

### Frontend Implementation (app/recipes/new/RecipeForm.tsx)

Created a comprehensive client-side form component with:

- Form state management using useState
- Drag-and-drop functionality using @dnd-kit
- Image upload handling with presigned URLs  
- Auto-save to localStorage every 30 seconds
- Draft restoration for create mode
- Validation (Zod) before submission
- Confirmation dialog for unsaved changes

### File Structure Created

1. `app/api/v1/recipes/[id]/route.ts` - Extended PATCH API 
2. `app/recipes/new/page.tsx` - New recipe creation page
3. `app/recipes/[id]/edit/page.tsx` - Edit recipe page  
4. `app/recipes/new/RecipeForm.tsx` - Reusable form component
5. `app/recipes/new/RecipeForm.module.css` - Form styling

## Design Integration

- Used project's color palette (--cream, --warm-white, --ink, --brown, --terracotta, --sage, --gold)
- Applied typography from design tokens (Fraunces for headings, Cormorant Garamond for body)
- Followed existing UI component patterns (Button, Input, Textarea, Badge, Modal)  
- Responsive layout with appropriate spacing and visual hierarchy

## Validation and Testing

The implementation includes:
- Client-side validation using Zod
- Proper handling of edge cases (empty arrays, null values, etc.)
- Error feedback for users on failed submissions
- Authenticated access controls ensuring only recipe owners can edit