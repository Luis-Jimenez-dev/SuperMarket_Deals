import { Link, useLocation } from 'react-router-dom'

function MealPlanPage() {
  const location = useLocation()

  const mealPlan = location.state?.mealPlan
  const store = location.state?.store

  // User reached this page without generating a meal plan first
  if (!mealPlan) {
    return (
      <div className="app">
        <Link to="/">← Back</Link>

        <h1>No Meal Plan Yet</h1>
        <p>Build a meal plan from the home page first.</p>

        <Link to="/">Go to Home</Link>
      </div>
    )
  }

  const recipes = mealPlan.recipes ?? []
  const shoppingList = mealPlan.shopping_list ?? {}

  return (
    <div className="app">
      <Link to="/">← Back</Link>

      <div className="meal-plan-header">
        <h1>Your Meal Plan</h1>

        {store && (
          <p>
            Based on this week's deals at {store.name}
            {store.city && ` · ${store.city}, ${store.state}`}
          </p>
        )}
      </div>

      <section className="recommended-meals">
        <h2>Recommended Meals</h2>

        {recipes.length > 0 ? (
          recipes.map((recipe, index) => (
            <div className="meal-card" key={index}>

              <div className="meal-card-header">
                <h3>{recipe.recipe}</h3>

                <span className="match-badge">
                  {recipe.match_percentage?.toFixed(0)}% match
                </span>
              </div>

              <p>
                Matched Deal Cost: ${recipe.total_cost?.toFixed(2)}
              </p>

              <div className="missing-ingredients">
                <p>Still Needed</p>

                <div className="ingredient-tags">
                  {recipe.missing?.length > 0 ? (
                    recipe.missing.map((ingredient, ingredientIndex) => (
                      <span key={ingredientIndex}>
                        {ingredient}
                      </span>
                    ))
                  ) : (
                    <span>No additional ingredients needed</span>
                  )}
                </div>
              </div>

            </div>
          ))
        ) : (
          <p>No matching meals were found for this week's deals.</p>
        )}
      </section>

      <section className="shopping-list">
        <h2>Shopping List</h2>

        {Object.keys(shoppingList).length > 0 ? (
          Object.entries(shoppingList).map(([name, item]) => (
            <div className="shopping-list-item" key={name}>
              <span>{name}</span>

              <span>
                {item.quantity} {item.unit}
              </span>
            </div>
          ))
        ) : (
          <p>No items have been added to your shopping list.</p>
        )}
      </section>

    </div>
  )
}

export default MealPlanPage